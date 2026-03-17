// src/cron/facebook.js — Publicación automática a Facebook con timer de 3 horas

import { SITIOS_LIST, SITE_DOMAIN_MAP } from '../config.js';

const THREE_HOURS_MS = 3 * 60 * 60 * 1000;

// ============================================================
// publishToFBIndividual — Publica un artículo a Facebook
// ============================================================
export async function publishToFBIndividual(env, article, siteSlug) {
  try {
    // Get site configuration from DB
    const site = await env.DB.prepare(
      'SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1'
    ).bind(siteSlug).first();

    if (!site) {
      return { success: false, error: `Site ${siteSlug} not found or Facebook inactive` };
    }

    const token = env[site.FACEBOOK_TOKEN_SECRET];
    if (!token) {
      return { success: false, error: `Missing Facebook token for ${siteSlug}` };
    }

    if (!site.FACEBOOK_PAGE_ID) {
      return { success: false, error: `Missing Facebook page ID for ${siteSlug}` };
    }

    // Check article has required fields
    if (!article.TITULO) {
      return { success: false, error: 'Article missing title' };
    }

    // Get domain for the site
    const domain = SITE_DOMAIN_MAP[siteSlug] || `https://${siteSlug}.pages.dev`;
    const url = `${domain}/articulo/?slug=${article.SLUG}`;

    console.log(`[FB] Publishing to ${siteSlug}: ${article.TITULO?.substring(0, 50)}...`);
    console.log(`[FB] URL: ${url}`);

    // Prepare Facebook post
    const formData = new FormData();
    formData.append('message', article.TITULO);
    formData.append('link', url);
    formData.append('access_token', token);

    // Call Facebook Graph API
    const fbResponse = await fetch(
      `https://graph.facebook.com/v19.0/${site.FACEBOOK_PAGE_ID}/feed`,
      {
        method: 'POST',
        body: formData
      }
    );

    const fbResult = await fbResponse.json();

    if (fbResponse.ok && fbResult.id) {
      console.log(`[FB] ✓ Published to ${siteSlug}: ${fbResult.id}`);
      return { success: true, post_id: fbResult.id };
    } else {
      const errorMsg = fbResult.error?.message || 'Unknown Facebook API error';
      console.error(`[FB] ✗ Failed to publish to ${siteSlug}: ${errorMsg}`);
      return { success: false, error: errorMsg };
    }
  } catch (e) {
    console.error(`[FB] Exception publishing to ${siteSlug}:`, e.message);
    return { success: false, error: e.message };
  }
}

// ============================================================
// processFBTimer — Procesa publicaciones a Facebook para todos los sitios
// Publica máximo 1 artículo por sitio cada 3 horas
// ============================================================
export async function processFBTimer(env) {
  console.log('[FB TIMER] Starting Facebook timer processing...');

  const stats = {
    processed: 0,
    success: 0,
    failed: 0,
    skipped: 0
  };

  for (const siteSlug of SITIOS_LIST) {
    const kvKey = `last_fb_post_${siteSlug}`;
    const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

    try {
      // Check timer from KV
      const lastPostRaw = await env.ARTICLES_KV.get(kvKey);
      const lastPostTime = lastPostRaw ? parseInt(lastPostRaw, 10) : 0;
      const now = Date.now();
      const elapsed = now - lastPostTime;

      // Skip if less than 3 hours passed
      if (elapsed < THREE_HOURS_MS && lastPostTime !== 0) {
        const remainingMin = Math.ceil((THREE_HOURS_MS - elapsed) / 60000);
        console.log(`[FB TIMER] ${siteSlug}: skipped (timer active, ${remainingMin} min remaining)`);
        stats.skipped++;
        continue;
      }

      // Get pending article with valid image
      const article = await env.DB.prepare(`
        SELECT
          s.ID as SITIO_ID,
          s.ID_PARAFRASEADO,
          p.TITULO_PARAFRASEADO as TITULO,
          p.SLUG,
          p.URL_IMAGEN
        FROM ${tableName} s
        JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
        WHERE s.FB_PUBLICADO = 0
          AND p.URL_IMAGEN IS NOT NULL
          AND p.URL_IMAGEN != ''
          AND p.URL_IMAGEN NOT LIKE '%logo.png'
          AND p.URL_IMAGEN NOT LIKE '%fallback%'
        ORDER BY s.FECHA_ASIGNACION ASC
        LIMIT 1
      `).first();

      if (!article) {
        console.log(`[FB TIMER] ${siteSlug}: skipped (no pending articles)`);
        stats.skipped++;
        continue;
      }

      stats.processed++;

      // Publish to Facebook
      const fbResult = await publishToFBIndividual(env, article, siteSlug);

      if (fbResult.success) {
        // Update database
        await env.DB.prepare(`
          UPDATE ${tableName}
          SET FB_PUBLICADO = 1, FB_FECHA = datetime('now'), FB_POST_ID = ?
          WHERE ID = ?
        `).bind(fbResult.post_id, article.SITIO_ID).run();

        // Update timer in KV
        await env.ARTICLES_KV.put(kvKey, now.toString());

        console.log(`[FB TIMER] ${siteSlug}: published successfully (${fbResult.post_id})`);
        stats.success++;
      } else {
        console.error(`[FB TIMER] ${siteSlug}: publish failed - ${fbResult.error}`);
        stats.failed++;
      }

      // Small delay between sites to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 500));

    } catch (e) {
      console.error(`[FB TIMER] ${siteSlug}: error - ${e.message}`);
      stats.failed++;
    }
  }

  console.log(`[FB TIMER] Complete: processed=${stats.processed}, success=${stats.success}, failed=${stats.failed}, skipped=${stats.skipped}`);
  return stats;
}
