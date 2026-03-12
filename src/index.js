// src/index.js — Entry point del Worker (NexoPress API)
// Archivo mínimo: solo setup de app, CORS, montaje de rutas y export.

import { Hono } from 'hono';
import { cors } from 'hono/cors';

// ── Config ────────────────────────────────────────────────────
import { ALLOWED_ORIGINS } from './config.js';

// ── Utils ─────────────────────────────────────────────────────
import { injectMetaTags } from './utils/html.js';

// ── Cron ──────────────────────────────────────────────────────
import { runMasterCron } from './cron/master.js';

// ── Rutas ─────────────────────────────────────────────────────
import authRoutes       from './routes/auth.js';
import articleRoutes    from './routes/articles.js';
import statsRoutes      from './routes/stats.js';
import cmsRoutes        from './routes/cms.js';
import revisionRoutes   from './routes/revision.js';
import siteRoutes       from './routes/sites.js';
import categoryRoutes   from './routes/categories.js';
import tickerRoutes     from './routes/ticker.js';
import weatherRoutes    from './routes/weather.js';
import imageRoutes      from './routes/images.js';
import rssRoutes        from './routes/rss.js';
import facebookRoutes   from './routes/facebook.js';
import cronRoutes       from './routes/cron.js';

// ── App ───────────────────────────────────────────────────────
const app = new Hono().basePath('/api');

// ── CORS ──────────────────────────────────────────────────────
app.use('*', cors({
  origin: (origin) => {
    if (!origin) return '*'; // peticiones server-side / curl
    if (ALLOWED_ORIGINS.includes(origin)) return origin;
    if (origin.endsWith('.workers.dev')) return origin;
    if (origin.endsWith('.pages.dev')) return origin;
    if (origin.includes('localhost') || origin.includes('127.0.0.1')) return origin;
    return null;
  },
  allowMethods:  ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders:  ['Content-Type', 'Authorization', 'X-Admin-Token'],
  exposeHeaders: ['Content-Length'],
  maxAge:        86400,
  credentials:   true,
}));

// ── Rutas montadas ────────────────────────────────────────────
app.route('/auth',       authRoutes);
app.route('/articles',   articleRoutes);
app.route('/stats',      statsRoutes);
app.route('/cms',        cmsRoutes);
app.route('/revision',   revisionRoutes);
app.route('/sites',      siteRoutes);
app.route('/categories', categoryRoutes);
app.route('/ticker',     tickerRoutes);
app.route('/weather',    weatherRoutes);
app.route('/images',     imageRoutes);
app.route('/rss',        rssRoutes);
app.route('/facebook',   facebookRoutes);
app.route('/cron',       cronRoutes);

// ── Rutas standalone ──────────────────────────────────────────

// Health check
app.get('/health', (c) => c.json({
  status:    'ok',
  timestamp: new Date().toISOString(),
  version:   '2.0.0',
}));

// Upload de archivos a R2
app.post('/upload', async (c) => {
  try {
    const formData = await c.req.formData();
    const file     = formData.get('file');
    if (!file) return c.json({ error: 'No file provided' }, 400);

    const ext      = file.name?.split('.').pop()?.toLowerCase() || 'jpg';
    const key      = `auto/${crypto.randomUUID()}.${ext}`;
    const buffer   = await file.arrayBuffer();

    await c.env.UPLOADS.put(key, buffer, {
      httpMetadata: { contentType: file.type || 'image/jpeg' },
    });

    const url = `https://uploads.sebastianvernis.space/${key}`;
    return c.json({ success: true, url, key });
  } catch (e) {
    console.error('Upload error:', e.message);
    return c.json({ error: e.message }, 500);
  }
});

// ── Export ────────────────────────────────────────────────────
export default {
  // Maneja peticiones HTTP
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Rutas de la API
    if (url.pathname.startsWith('/api')) {
      return app.fetch(request, env, ctx);
    }

    // Resto: inyectar meta tags OG para SEO en páginas de sitios
    const originalRes = await fetch(request);
    return injectMetaTags(request, env, originalRes);
  },

  // Cron job programado (cada 30 min via wrangler.toml)
  async scheduled(event, env, ctx) {
    ctx.waitUntil(runMasterCron(env));
  },
};
