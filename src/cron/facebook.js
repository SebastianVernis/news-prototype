// src/cron/facebook.js — Publicación en Facebook: individual, cola y procesamiento masivo

import { sleep } from '../utils/helpers.js';
import { SITIOS_LIST, log, error, LOG_PREFIXES } from '../config.js';

// Usar console.log directamente para que los logs se vean siempre en production
const FB_LOG = (...args) => console.log('[FB]', ...args);
const FB_ERR = (...args) => console.error('[FB]', ...args);

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
    // El middleware de OG tags está en el deployment de producción (sin main.)
    const pagesDomain = `${siteSlug}.pages.dev`;
    const url = `https://${pagesDomain}/articulo/?slug=${article.SLUG}`;

    // Decodificar título (importado inline para evitar dependencia circular)
    const title = article.TITULO || '';

    FB_LOG(`Publicando en ${siteSlug}: ${title.substring(0, 40)}...`);
    FB_LOG(`URL: ${url} (usando ${pagesDomain} para OG tags)`);
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
// PUBLICA SI O SI cada 3 horas en TODOS los sitios con artículos pendientes
// USA DB en lugar de KV para evitar problemas de escritura/lectura
// ============================================================
export async function processFBTimer(env) {
  FB_LOG('Starting Facebook Timer processing...');
  const stats = { processed: 0, success: 0, failed: 0, skipped: 0, skipped_timer: 0, skipped_no_articles: 0, skipped_no_image: 0 };
  const THREE_HOURS_MS = 3 * 60 * 60 * 1000;
  const now = Date.now();

  //确保表存在
  try {
    await env.DB.prepare(`
      CREATE TABLE IF NOT EXISTS FB_TIMERS (
        SITE_SLUG TEXT PRIMARY KEY,
        LAST_POST TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `).run();
  } catch (e) {
    FB_LOG('Table check error (may already exist):', e.message);
  }

  for (const siteSlug of SITIOS_LIST) {
    const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

    // Obtener última publicación desde DB
    const lastPostRow = await env.DB.prepare(
      'SELECT LAST_POST FROM FB_TIMERS WHERE SITE_SLUG = ?'
    ).bind(siteSlug).first();

    const lastPostTime = lastPostRow?.LAST_POST ? new Date(lastPostRow.LAST_POST).getTime() : 0;
    const elapsed = now - lastPostTime;
    const elapsedMin = Math.floor(elapsed / 60000);

    FB_LOG(`${siteSlug}: Last post ${lastPostTime === 0 ? 'NEVER' : elapsedMin + ' min ago'}`);

    // Verificar si hay artículos pendientes
    const pendingCount = await env.DB.prepare(`
      SELECT COUNT(*) as c FROM ${tableName}
      WHERE FB_PUBLICADO = 0
    `).first();

    const pending = pendingCount?.c || 0;
    FB_LOG(`${siteSlug}: ${pending} artículos pendientes`);

    // Si no hay artículos pendientes, NO resetear timer - dejar que expire naturalmente
    // Resetear timer aquí crea un loop infinito de espera
    if (pending === 0) {
      FB_LOG(`${siteSlug}: SKIP - No pending articles (timer preserved)`);
      stats.skipped_no_articles++;
      continue;
    }

    // Verificar si hay artículos con imagen válida (para logging)
    const validImageCount = await env.DB.prepare(`
      SELECT COUNT(*) as c FROM ${tableName} s
      JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
      WHERE s.FB_PUBLICADO = 0
        AND p.URL_IMAGEN IS NOT NULL
        AND p.URL_IMAGEN != ''
        AND p.URL_IMAGEN NOT LIKE '%logo.png'
        AND p.URL_IMAGEN NOT LIKE '%fallback%'
    `).first();
    const validImages = validImageCount?.c || 0;

    // PUBLICAR SI O SI si pasaron 3 horas O si nunca ha publicado (lastPostTime = 0)
    const shouldPublish = elapsed >= THREE_HOURS_MS || lastPostTime === 0;

    if (!shouldPublish) {
      FB_LOG(`${siteSlug}: SKIP - Timer not expired (${elapsedMin} min / 180 min), ${validImages} articles with valid image`);
      stats.skipped_timer++;
      continue;
    }

    FB_LOG(`${siteSlug}: PUBLISHING (timer expired: ${elapsedMin} min or never published)`);

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
      FB_LOG(`${siteSlug}: SKIP - No articles with valid R2 image (${pending} total pending, ${validImages} with image)`);
      stats.skipped_no_image++;
      // NO reset timer - allow retry on next cron run
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

        // Actualizar timer en DB
        await env.DB.prepare(`
          INSERT OR REPLACE INTO FB_TIMERS (SITE_SLUG, LAST_POST) VALUES (?, datetime('now'))
        `).bind(siteSlug).run();

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
    `${stats.success} success, ${stats.failed} failed, ` +
    `${stats.skipped_timer} skipped_timer, ${stats.skipped_no_articles} skipped_no_articles, ${stats.skipped_no_image} skipped_no_image`
  );
  return stats;
}
