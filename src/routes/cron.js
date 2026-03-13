// src/routes/cron.js — Rutas de control y monitoreo del cron job

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { runMasterCron } from '../cron/master.js';

const cron = new Hono();

// ── GET /cron/status — Estado del último cron ejecutado ──────
cron.get('/status', async (c) => {
  const s    = await c.env.ARTICLES_KV.get('cron_status');
  const data = s ? JSON.parse(s) : { lastRun: 'Never' };

  if (data.lastRun !== 'Never') {
    const lastTs = new Date(data.lastRun).getTime();
    const nextTs = lastTs + 30 * 60 * 1000;
    const diff   = Math.max(0, nextTs - Date.now());
    data.nextRunInMinutes = Math.floor(diff / 60000);
    data.nextRunInSeconds = Math.floor((diff % 60000) / 1000);
  }

  // Interpretar estados de tareas para evitar falsos errores
  if (data.tasks) {
    const taskStatus = {};
    for (const [key, value] of Object.entries(data.tasks)) {
      if (key.startsWith('fb_') && value && value.includes('pending')) {
        taskStatus[key] = { status: 'pending',  message: value, isError: false };
      } else if (key.startsWith('fb_') && value && value.startsWith('OK')) {
        taskStatus[key] = { status: 'success',  message: value, isError: false };
      } else if (key.startsWith('fb_') && value && (value.startsWith('Error') || value.startsWith('No published'))) {
        taskStatus[key] = { status: 'issue',    message: value, isError: false };
      } else if (key.startsWith('fb_') && value && value.includes('No eligible')) {
        taskStatus[key] = { status: 'idle',     message: value, isError: false };
      } else {
        const isError = value && value.startsWith('Error');
        taskStatus[key] = { status: isError ? 'error' : 'ok', message: value, isError };
      }
    }
    data.taskDetails = taskStatus;
  }

  return c.json(data);
});

// ── GET /cron/manual — Ejecutar cron manualmente ─────────────
cron.get('/manual', async (c) => {
  try {
    await runMasterCron(c.env);
  } catch (e) {
    console.error('Cron manual error:', e.message);
    return c.json({ error: e.message }, 500);
  }
  const s = await c.env.ARTICLES_KV.get('cron_status');
  return c.json(s ? JSON.parse(s) : { message: 'Cron executed' });
});

// ── POST /cron/ingest — Información sobre ingesta RSS ────────
cron.post('/ingest', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  try {
    return c.json({
      success: true,
      message: 'RSS ingestion runs automatically every 30 minutes via scheduled trigger',
      note:    'Manual ingestion is not required - articles are ingested automatically',
    });
  } catch (e) {
    return c.json({ success: false, error: e.message }, 500);
  }
});

// ── GET /cron/diagnostic — Diagnóstico detallado del cron ─────
cron.get('/diagnostic', async (c) => {
  try {
    const { SITIOS_LIST } = await import('../config.js');
    const now = Date.now();
    const THREE_HOURS_MS = 3 * 60 * 60 * 1000;
    
    const diagnostics = [];
    
    for (const siteSlug of SITIOS_LIST) {
      const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
      const kvKey = `last_fb_post_${siteSlug}`;
      
      // Obtener timer del KV
      const lastPostRaw = await c.env.ARTICLES_KV.get(kvKey);
      const lastPostTime = lastPostRaw ? parseInt(lastPostRaw, 10) : 0;
      const elapsed = now - lastPostTime;
      const elapsedMin = Math.floor(elapsed / 60000);
      const shouldPublish = elapsed >= THREE_HOURS_MS || lastPostTime === 0;
      
      // Contar artículos pendientes
      const pendingCount = await c.env.DB.prepare(`
        SELECT COUNT(*) as c FROM ${tableName} WHERE FB_PUBLICADO = 0
      `).first();
      
      // Contar artículos con imagen válida
      const validImageCount = await c.env.DB.prepare(`
        SELECT COUNT(*) as c FROM ${tableName} s
        JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
        WHERE s.FB_PUBLICADO = 0
          AND p.URL_IMAGEN IS NOT NULL
          AND p.URL_IMAGEN != ''
          AND p.URL_IMAGEN NOT LIKE '%logo.png'
          AND p.URL_IMAGEN NOT LIKE '%fallback%'
      `).first();
      
      diagnostics.push({
        site: siteSlug,
        timer: {
          lastPostTime,
          elapsedMin,
          expires: Math.max(0, 180 - elapsedMin),
          ready: shouldPublish || lastPostTime === 0
        },
        articles: {
          pending: pendingCount?.c || 0,
          withValidImage: validImageCount?.c || 0
        },
        canPublish: shouldPublish && (validImageCount?.c || 0) > 0
      });
    }
    
    const summary = {
      totalSites: diagnostics.length,
      readyToPublish: diagnostics.filter(d => d.timer.ready).length,
      hasPendingArticles: diagnostics.filter(d => d.articles.pending > 0).length,
      canPublishNow: diagnostics.filter(d => d.canPublish).length
    };
    
    return c.json({ summary, diagnostics });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /cron/test-fb — Test de publicación FB para un sitio ─────
cron.get('/test-fb/:siteSlug', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  
  const siteSlug = c.req.param('siteSlug');
  const results = { site: siteSlug, steps: [], error: null };
  
  try {
    const { publishToFBIndividual } = await import('../cron/facebook.js');
    const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
    
    // Step 1: Check site config
    results.steps.push({ step: '1_check_site', status: 'pending' });
    const site = await c.env.DB.prepare(
      'SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1'
    ).bind(siteSlug).first();
    
    if (!site) {
      results.steps[0].status = 'failed';
      results.steps[0].error = 'Site not found or inactive';
      return c.json(results);
    }
    results.steps[0].status = 'ok';
    results.steps[0].data = { page_id: site.FACEBOOK_PAGE_ID, has_token_secret: !!site.FACEBOOK_TOKEN_SECRET };
    
    // Step 2: Check token
    results.steps.push({ step: '2_check_token', status: 'pending' });
    const token = c.env[site.FACEBOOK_TOKEN_SECRET];
    if (!token) {
      results.steps[1].status = 'failed';
      results.steps[1].error = 'Token secret not found in env';
      return c.json(results);
    }
    results.steps[1].status = 'ok';
    results.steps[1].data = { token_length: token.length };
    
    // Step 3: Get pending article
    results.steps.push({ step: '3_get_article', status: 'pending' });
    const article = await c.env.DB.prepare(`
      SELECT s.ID as SITIO_ID, s.ID_PARAFRASEADO,
             p.TITULO_PARAFRASEADO as TITULO, p.SLUG, p.URL_IMAGEN
      FROM ${tableName} s
      JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
      WHERE s.FB_PUBLICADO = 0
        AND p.URL_IMAGEN IS NOT NULL
        AND p.URL_IMAGEN != ''
        AND p.URL_IMAGEN NOT LIKE '%logo.png'
      ORDER BY s.FECHA_ASIGNACION ASC
      LIMIT 1
    `).first();
    
    if (!article) {
      results.steps[2].status = 'failed';
      results.steps[2].error = 'No pending articles with valid image';
      return c.json(results);
    }
    results.steps[2].status = 'ok';
    results.steps[2].data = { id: article.SITIO_ID, title: article.TITULO?.substring(0, 50) };
    
    // Step 4: Publish to FB
    results.steps.push({ step: '4_publish_fb', status: 'pending' });
    const fbResult = await publishToFBIndividual(c.env, article, siteSlug);
    
    if (fbResult.success) {
      results.steps[3].status = 'ok';
      results.steps[3].data = { post_id: fbResult.post_id };
      
      // Update DB
      await c.env.DB.prepare(`
        UPDATE ${tableName}
        SET FB_PUBLICADO = 1, FB_FECHA = datetime('now'), FB_POST_ID = ?
        WHERE ID = ?
      `).bind(fbResult.post_id, article.SITIO_ID).run();
      
      results.success = true;
      results.message = `Published successfully: ${fbResult.post_id}`;
    } else {
      results.steps[3].status = 'failed';
      results.steps[3].error = fbResult.error;
      results.error = fbResult.error;
    }
    
  } catch (e) {
    results.error = e.message;
    results.steps.push({ step: 'error', status: 'failed', error: e.message });
  }
  
  return c.json(results);
});

// ── GET /cron/debug-fb-timer — Debug del Facebook Timer ─────
cron.get('/debug-fb-timer/:siteSlug', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  
  const siteSlug = c.req.param('siteSlug');
  const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
  const kvKey = `last_fb_post_${siteSlug}`;
  const THREE_HOURS_MS = 3 * 60 * 60 * 1000;
  const now = Date.now();
  
  // Get timer
  const lastPostRaw = await c.env.ARTICLES_KV.get(kvKey);
  const lastPostTime = lastPostRaw ? parseInt(lastPostRaw, 10) : 0;
  const elapsed = now - lastPostTime;
  const elapsedMin = Math.floor(elapsed / 60000);
  const shouldPublish = elapsed >= THREE_HOURS_MS || lastPostTime === 0;
  
  // Get pending count
  const pendingCount = await c.env.DB.prepare(`
    SELECT COUNT(*) as c FROM ${tableName} WHERE FB_PUBLICADO = 0
  `).first();
  
  // Get valid image count
  const validImageCount = await c.env.DB.prepare(`
    SELECT COUNT(*) as c FROM ${tableName} s
    JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
    WHERE s.FB_PUBLICADO = 0
      AND p.URL_IMAGEN IS NOT NULL
      AND p.URL_IMAGEN != ''
      AND p.URL_IMAGEN NOT LIKE '%logo.png'
  `).first();
  
  // Get one sample article
  const sampleArticle = await c.env.DB.prepare(`
    SELECT s.ID as SITIO_ID, p.TITULO_PARAFRASEADO as TITULO, p.URL_IMAGEN
    FROM ${tableName} s
    JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
    WHERE s.FB_PUBLICADO = 0
      AND p.URL_IMAGEN IS NOT NULL
      AND p.URL_IMAGEN != ''
    LIMIT 1
  `).first();
  
  return c.json({
    site: siteSlug,
    timer: {
      kvKey,
      lastPostRaw,
      lastPostTime,
      elapsedMin,
      shouldPublish,
      threshold: 180
    },
    articles: {
      pending: pendingCount?.c || 0,
      withValidImage: validImageCount?.c || 0,
      sample: sampleArticle
    },
    willPublish: shouldPublish && (validImageCount?.c || 0) > 0
  });
});

export default cron;
