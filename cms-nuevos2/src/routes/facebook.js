// src/routes/facebook.js — Rutas de gestión y monitoreo de Facebook

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { publishToFBIndividual } from '../cron/facebook.js';
import { SITIOS_LIST } from '../config.js';

const facebook = new Hono();

// ── GET /facebook/debug-tokens — Validar tokens FB por sitio ─
facebook.get('/debug-tokens', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  try {
    const sites = await c.env.DB.prepare(
      'SELECT SLUG, FACEBOOK_TOKEN_SECRET, FACEBOOK_PAGE_ID FROM SITIOS'
    ).all();

    const results = await Promise.all(
      (sites.results || []).map(async (s) => {
        const token     = c.env[s.FACEBOOK_TOKEN_SECRET];
        const has_token = !!token;
        let is_valid    = false;
        let fb_error    = null;

        if (has_token && s.FACEBOOK_PAGE_ID) {
          try {
            const fbRes  = await fetch(
              `https://graph.facebook.com/v19.0/${s.FACEBOOK_PAGE_ID}?fields=name&access_token=${token}`
            );
            const fbData = await fbRes.json();
            if (fbRes.ok) {
              is_valid = true;
            } else {
              fb_error = fbData.error?.message || 'Invalid Token';
            }
          } catch (e) {
            fb_error = e.message;
          }
        }

        return {
          slug:        s.SLUG,
          token_key:   s.FACEBOOK_TOKEN_SECRET,
          has_token,
          is_valid,
          fb_error,
          has_page_id: !!s.FACEBOOK_PAGE_ID,
        };
      })
    );

    return c.json(results);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /facebook/monitor — Estado de publicación FB por sitio ──
facebook.get('/monitor', async (c) => {
  try {
    const results = [];

    for (const siteSlug of SITIOS_LIST) {
      const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

      const siteArticles = await c.env.DB.prepare(`
        SELECT
          s.ID as SITIO_ID,
          s.ID_PARAFRASEADO,
          p.TITULO_PARAFRASEADO as TITULO,
          p.URL_IMAGEN,
          p.FECHA_PUBLICACION,
          s.FB_PUBLICADO,
          s.FB_FECHA,
          s.FB_POST_ID,
          '${siteSlug}' as SITIO,
          'PARA' as TIPO
        FROM ${tableName} s
        JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
        WHERE s.FB_PUBLICADO = 0
        ORDER BY s.FECHA_ASIGNACION DESC
        LIMIT 20
      `).all();

      results.push(...(siteArticles.results || []));
    }

    // Ordenar por fecha de publicación del artículo y limitar a 100
    const sorted = results
      .sort((a, b) => new Date(b.FECHA_PUBLICACION || 0) - new Date(a.FECHA_PUBLICACION || 0))
      .slice(0, 100);

    return c.json(sorted);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /facebook/queue — Artículos pendientes de Facebook ──────
facebook.get('/queue', async (c) => {
  try {
    const results = [];

    for (const siteSlug of SITIOS_LIST) {
      const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

      const pending = await c.env.DB.prepare(`
        SELECT
          s.ID as SITIO_ID,
          s.ID_PARAFRASEADO,
          p.TITULO_PARAFRASEADO as TITULO,
          p.URL_IMAGEN,
          p.FECHA_PUBLICACION,
          s.FB_PUBLICADO,
          s.FB_FECHA,
          '${siteSlug}' as SITIO
        FROM ${tableName} s
        JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
        WHERE s.FB_PUBLICADO = 0
          AND p.URL_IMAGEN IS NOT NULL
          AND p.URL_IMAGEN != ''
        ORDER BY s.FECHA_ASIGNACION DESC
        LIMIT 10
      `).all();

      results.push(...(pending.results || []));
    }

    // Contar totales
    const totalPending = results.length;

    return c.json({
      queue: results.slice(0, 50),
      totalPending,
      message: 'Facebook Queue removed - articles now published immediately by timer',
    });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /facebook/reset-timer/:siteSlug — Resetear timer FB ─
facebook.post('/reset-timer/:siteSlug', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  const siteSlug = c.req.param('siteSlug');
  const kvKey    = `last_fb_post_${siteSlug}`;
  await c.env.ARTICLES_KV.put(kvKey, '0');
  return c.json({ success: true, message: `Timer reset for ${siteSlug}` });
});

// ── POST /facebook/force-publish/:siteSlug — Forzar publicación FB ──
facebook.post('/force-publish/:siteSlug', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  const siteSlug  = c.req.param('siteSlug');
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

  try {
    const article = await c.env.DB.prepare(`
      SELECT
        s.ID as SITIO_ID,
        s.ID_PARAFRASEADO,
        p.TITULO_PARAFRASEADO as TITULO,
        p.SLUG,
        p.URL_IMAGEN
      FROM ${tableName} s
      JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
      WHERE s.FB_PUBLICADO = 0
      ORDER BY s.FECHA_ASIGNACION DESC
      LIMIT 1
    `).first();

    if (!article) {
      return c.json({ error: 'No articles pending for Facebook', success: false });
    }

    const result = await publishToFBIndividual(c.env, article, siteSlug);

    if (result.success) {
      await c.env.DB.prepare(`
        UPDATE ${tableName}
        SET FB_PUBLICADO = 1, FB_FECHA = datetime('now'), FB_POST_ID = ?
        WHERE ID = ?
      `).bind(result.post_id, article.SITIO_ID).run();

      return c.json({ success: true, article: article.SITIO_ID, fb_post_id: result.post_id });
    } else {
      return c.json({ success: false, error: result.error });
    }
  } catch (e) {
    return c.json({ error: e.message, success: false });
  }
});

// ── GET /facebook/recent-posts/:siteSlug — Obtener posts publicados (últimas N horas) ──
facebook.get('/recent-posts/:siteSlug', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  
  const siteSlug = c.req.param('siteSlug');
  const hours = c.req.query('hours') || '24';
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

  try {
    const posts = await c.env.DB.prepare(`
      SELECT
        s.ID as SITIO_ID,
        s.ID_PARAFRASEADO,
        p.TITULO_PARAFRASEADO as TITULO,
        p.SLUG,
        p.URL_IMAGEN,
        s.FB_PUBLICADO,
        s.FB_FECHA,
        s.FB_POST_ID,
        s.FECHA_ASIGNACION
      FROM ${tableName} s
      JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
      WHERE s.FB_PUBLICADO = 1
        AND s.FB_FECHA >= datetime('now', '-${hours} hours')
      ORDER BY s.FB_FECHA DESC
      LIMIT 50
    `).all();

    return c.json(posts.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /facebook/update-post/:siteSlug/:postId — Actualizar post existente ──
facebook.post('/update-post/:siteSlug/:postId', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  
  const siteSlug = c.req.param('siteSlug');
  const postId = c.req.param('postId');
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

  try {
    // Obtener datos del artículo
    const article = await c.env.DB.prepare(`
      SELECT
        s.ID as SITIO_ID,
        p.TITULO_PARAFRASEADO as TITULO,
        p.SLUG,
        p.URL_IMAGEN
      FROM ${tableName} s
      JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
      WHERE s.FB_POST_ID = ?
    `).bind(postId).first();

    if (!article) {
      return c.json({ error: 'Article not found for this post', success: false });
    }

    // Obtener config del sitio
    const site = await c.env.DB.prepare(
      'SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1'
    ).bind(siteSlug).first();

    if (!site) {
      return c.json({ error: 'Site not found or inactive', success: false });
    }

    const token = c.env[site.FACEBOOK_TOKEN_SECRET];
    if (!token) {
      return c.json({ error: 'Missing Facebook token', success: false });
    }

    // Construir URL del artículo (usar .pages.dev para OG tags - producción)
    const pagesDomain = `${siteSlug}.pages.dev`;
    const url = `https://${pagesDomain}/articulo/?slug=${article.SLUG}`;

    console.log(`[FB UPDATE] Updating post ${postId} for ${siteSlug}`);
    console.log(`[FB UPDATE] URL: ${url}`);
    console.log(`[FB UPDATE] Title: ${article.TITULO}`);

    // Actualizar post en Facebook (re-scrapea OG tags)
    const formData = new FormData();
    formData.append('message', article.TITULO || '');
    formData.append('link', url);
    formData.append('access_token', token);

    const response = await fetch(
      `https://graph.facebook.com/v19.0/${postId}`,
      { method: 'POST', body: formData }
    );

    const result = await response.json();

    if (response.ok) {
      console.log(`[FB UPDATE] SUCCESS: Post ${postId} updated`);
      return c.json({ success: true, post_id: postId, message: 'Post updated, OG tags re-scraped' });
    } else {
      console.error(`[FB UPDATE] API Error:`, result);
      return c.json({ success: false, error: result.error?.message || 'Facebook API error' });
    }
  } catch (e) {
    console.error(`[FB UPDATE] Exception:`, e.message);
    return c.json({ error: e.message, success: false });
  }
});

// ── POST /facebook/update-recent/:siteSlug — Actualizar todos los posts recientes ──
facebook.post('/update-recent/:siteSlug', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  
  const siteSlug = c.req.param('siteSlug');
  const hours = c.req.query('hours') || '24';
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

  try {
    // Obtener posts recientes
    const posts = await c.env.DB.prepare(`
      SELECT
        s.ID as SITIO_ID,
        s.FB_POST_ID,
        p.TITULO_PARAFRASEADO as TITULO,
        p.SLUG
      FROM ${tableName} s
      JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
      WHERE s.FB_PUBLICADO = 1
        AND s.FB_FECHA >= datetime('now', '-${hours} hours')
      ORDER BY s.FB_FECHA DESC
      LIMIT 50
    `).all();

    const results = { updated: 0, failed: 0, errors: [] };

    // Obtener config del sitio
    const site = await c.env.DB.prepare(
      'SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1'
    ).bind(siteSlug).first();

    if (!site) {
      return c.json({ error: 'Site not found or inactive', success: false });
    }

    const token = c.env[site.FACEBOOK_TOKEN_SECRET];
    if (!token) {
      return c.json({ error: 'Missing Facebook token', success: false });
    }

    const pagesDomain = `${siteSlug}.pages.dev`;

    for (const post of (posts.results || [])) {
      if (!post.FB_POST_ID) continue;

      const url = `https://${pagesDomain}/articulo/?slug=${post.SLUG}`;

      try {
        const formData = new FormData();
        formData.append('message', post.TITULO || '');
        formData.append('link', url);
        formData.append('access_token', token);

        const response = await fetch(
          `https://graph.facebook.com/v19.0/${post.FB_POST_ID}`,
          { method: 'POST', body: formData }
        );

        const result = await response.json();

        if (response.ok) {
          results.updated++;
          console.log(`[FB UPDATE] ${siteSlug}: Post ${post.FB_POST_ID} updated`);
        } else {
          results.failed++;
          results.errors.push({
            post_id: post.FB_POST_ID,
            error: result.error?.message || 'Unknown error'
          });
          console.error(`[FB UPDATE] ${siteSlug}: Post ${post.FB_POST_ID} failed: ${result.error?.message}`);
        }

        // Delay para evitar rate limiting
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (e) {
        results.failed++;
        results.errors.push({
          post_id: post.FB_POST_ID,
          error: e.message
        });
      }
    }

    return c.json({
      success: true,
      site: siteSlug,
      results,
      message: `Updated ${results.updated} posts, ${results.failed} failed`
    });
  } catch (e) {
    return c.json({ error: e.message, success: false });
  }
});

export default facebook;
