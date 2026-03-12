// src/cron/facebook.js — Publicación en Facebook: individual, cola y procesamiento masivo

import { sleep } from '../utils/helpers.js';
import { SITIOS_LIST, log, error, LOG_PREFIXES } from '../config.js';

const FB_LOG = (...args) => log('[FB]', ...args);
const FB_ERR = (...args) => error('[FB]', ...args);

// ============================================================
// publishToFBIndividual — Publica un artículo en la página FB de un sitio
// NO envía parámetro 'picture' para imágenes R2 — Facebook scrapea OG tags
// ============================================================
export async function publishToFBIndividual(env, article, siteSlug) {
  try {
    // Obtener configuración del sitio
    const site = await env.DB.prepare(
      'SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1'
    ).bind(siteSlug).first();

    if (!site) {
      return { success: false, error: 'Site not found or inactive' };
    }

    if (!site.FACEBOOK_PAGE_ID || !site.FACEBOOK_TOKEN_SECRET) {
      return { success: false, error: 'Missing Facebook config' };
    }

    // Obtener token desde secrets
    const token = env[site.FACEBOOK_TOKEN_SECRET];
    if (!token) {
      return { success: false, error: 'Missing secret token' };
    }

    // Construir URL del artículo - USAR .pages.dev para que OG tags funcionen
    // Los dominios personalizados no ejecutan el middleware de OG tags
    const pagesDomain = `${siteSlug}.pages.dev`;
    const url = `https://main.${pagesDomain}/articulo/?slug=${article.SLUG}`;

    // Decodificar título (importado inline para evitar dependencia circular)
    const title = article.TITULO || '';

    FB_LOG(`Publicando en ${siteSlug}: ${title.substring(0, 40)}...`);
    FB_LOG(`URL: ${url} (usando main.${pagesDomain} para OG tags)`);
    FB_LOG(`Imagen: ${article.URL_IMAGEN ? 'R2 (OG scrape)' : 'N/A'}`);

    // NO enviar parámetro 'picture' — Facebook usa OG tags para evitar Error #100 con R2
    const formData = new FormData();
    formData.append('message', title);
    formData.append('link', url);
    formData.append('access_token', token);

    const response = await fetch(
      `https://graph.facebook.com/v19.0/${site.FACEBOOK_PAGE_ID}/feed`,
      { method: 'POST', body: formData }
    );

    const result = await response.json();

    if (response.ok && result.id) {
      return { success: true, post_id: result.id };
    } else {
      FB_ERR('API Error:', result);
      return { success: false, error: result };
    }
  } catch (e) {
    FB_ERR('Exception:', e.message);
    return { success: false, error: e.message };
  }
}

// ============================================================
// processFB — Publica artículos pendientes de FB en todas las tablas de sitio
// ============================================================
export async function processFB(env) {
  try {
    for (const siteSlug of SITIOS_LIST) {
      const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

      const countResult = await env.DB.prepare(`
        SELECT COUNT(*) as c FROM ${tableName}
        WHERE FB_PUBLICADO = 0
      `).first();

      const count = countResult?.c || 0;
      FB_LOG(`${siteSlug}: ${count} artículos pendientes de Facebook`);

      if (count > 0) {
        // Limit 3 para evitar rate limiting
        const articles = await env.DB.prepare(`
          SELECT s.ID as SITIO_ID, s.ID_PARAFRASEADO,
                 p.TITULO_PARAFRASEADO as TITULO, p.SLUG, p.URL_IMAGEN
          FROM ${tableName} s
          JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
          WHERE s.FB_PUBLICADO = 0
          ORDER BY s.FECHA_ASIGNACION ASC
          LIMIT 3
        `).all();

        for (const article of (articles.results || [])) {
          FB_LOG(`${siteSlug} publishing article ${article.SITIO_ID}...`);

          try {
            const result = await publishToFBIndividual(env, article, siteSlug);

            if (result.success) {
              await env.DB.prepare(`
                UPDATE ${tableName}
                SET FB_PUBLICADO = 1, FB_FECHA = datetime('now'), FB_POST_ID = ?
                WHERE ID = ?
              `).bind(result.post_id, article.SITIO_ID).run();

              FB_LOG(`${siteSlug} SUCCESS: ${result.post_id}`);
            } else {
              FB_ERR(`${siteSlug} FAILED: ${result.error}`);
            }
          } catch (fbError) {
            FB_ERR(`${siteSlug} EXCEPTION: ${fbError.message}`);
          }

          // Delay entre publicaciones (2-5 segundos para evitar rate limiting)
          await sleep(2000 + Math.random() * 3000);
        }
      }
    }
  } catch (e) {
    FB_ERR('processFB Error:', e.message);
  }
}

// ============================================================
// processFBTimer — Publica 1 artículo aleatorio con imagen R2
// cuando el timer de 3 horas se cumple para cada sitio
// ============================================================
export async function processFBTimer(env) {
  FB_LOG('Starting Facebook Timer processing...');
  const stats = { processed: 0, success: 0, failed: 0, skipped: 0 };
  const THREE_HOURS_MS = 3 * 60 * 60 * 1000;

  for (const siteSlug of SITIOS_LIST) {
    const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
    const kvKey = `last_fb_post_${siteSlug}`;

    // Obtener última publicación desde KV
    const lastPostRaw = await env.ARTICLES_KV.get(kvKey);
    const lastPostTime = lastPostRaw ? parseInt(lastPostRaw, 10) : 0;
    const now = Date.now();
    const elapsed = now - lastPostTime;

    FB_LOG(`${siteSlug}: Last post ${Math.floor(elapsed / 60000)} min ago`);

    // Solo procesar si pasaron 3 horas
    if (elapsed < THREE_HOURS_MS) {
      FB_LOG(`${siteSlug}: Skipping (timer not reached)`);
      stats.skipped++;
      continue;
    }

    // Seleccionar 1 artículo aleatorio con imagen R2 (no fallback)
    // Filtra imágenes que sean logo.png o vacías
    const randomArticle = await env.DB.prepare(`
      SELECT s.ID as SITIO_ID, s.ID_PARAFRASEADO,
             p.TITULO_PARAFRASEADO as TITULO, p.SLUG, p.URL_IMAGEN
      FROM ${tableName} s
      JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
      WHERE s.FB_PUBLICADO = 0
        AND p.URL_IMAGEN IS NOT NULL
        AND p.URL_IMAGEN != ''
        AND p.URL_IMAGEN NOT LIKE '%logo.png'
        AND p.URL_IMAGEN NOT LIKE '%fallback%'
      ORDER BY RANDOM()
      LIMIT 1
    `).first();

    if (!randomArticle) {
      FB_LOG(`${siteSlug}: No articles with valid R2 image`);
      stats.skipped++;
      // Reset timer para evitar loop infinito
      await env.ARTICLES_KV.put(kvKey, now.toString());
      continue;
    }

    stats.processed++;
    FB_LOG(`${siteSlug}: Publishing "${randomArticle.TITULO?.substring(0, 40)}..."`);

    try {
      const result = await publishToFBIndividual(env, randomArticle, siteSlug);

      if (result.success) {
        // Actualizar tabla del sitio
        await env.DB.prepare(`
          UPDATE ${tableName}
          SET FB_PUBLICADO = 1, FB_FECHA = datetime('now'), FB_POST_ID = ?
          WHERE ID = ?
        `).bind(result.post_id, randomArticle.SITIO_ID).run();

        // Actualizar timer en KV
        await env.ARTICLES_KV.put(kvKey, Date.now().toString());

        stats.success++;
        FB_LOG(`${siteSlug} SUCCESS: ${result.post_id}`);
      } else {
        stats.failed++;
        FB_ERR(`${siteSlug} FAILED: ${JSON.stringify(result.error)}`);
      }
    } catch (e) {
      stats.failed++;
      FB_ERR(`${siteSlug} EXCEPTION: ${e.message}`);
    }

    // Delay entre publicaciones (2-5 segundos)
    await sleep(2000 + Math.random() * 3000);
  }

  FB_LOG(
    `[FB TIMER] Complete: ${stats.processed} processed, ` +
    `${stats.success} success, ${stats.failed} failed, ${stats.skipped} skipped`
  );
  return stats;
}
