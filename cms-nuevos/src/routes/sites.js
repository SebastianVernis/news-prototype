// src/routes/sites.js — Gestión de la red de sitios

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { slugify } from '../utils/helpers.js';
import { SITIOS_LIST } from '../config.js';

const sites = new Hono();

// ── GET /sites — Listar sitios del CMS (filtrado por SITIOS_LIST) ──
sites.get('/', async (c) => {
  try {
    const placeholders = SITIOS_LIST.map(() => '?').join(',');
    const res = await c.env.DB.prepare(
      `SELECT * FROM SITIOS WHERE SLUG IN (${placeholders}) ORDER BY NOMBRE`
    ).bind(...SITIOS_LIST).all();
    return c.json(res.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /sites — Crear o actualizar sitio ───────────────────
sites.post('/', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const body = await c.req.json();
    const { id, nombre, dominio, tagline, activo } = body;
    if (!nombre || !dominio) return c.json({ error: 'Nombre y dominio requeridos' }, 400);

    const siteId = id || crypto.randomUUID();
    const slug   = slugify(nombre);

    await c.env.DB.prepare(`
      INSERT INTO SITIOS (ID, SLUG, NOMBRE, DOMINIO, TAGLINE, ACTIVO)
      VALUES (?, ?, ?, ?, ?, ?)
      ON CONFLICT(ID) DO UPDATE SET
        NOMBRE = excluded.NOMBRE, DOMINIO = excluded.DOMINIO,
        TAGLINE = excluded.TAGLINE, ACTIVO = excluded.ACTIVO
    `).bind(siteId, slug, nombre, dominio, tagline || '', activo ? 1 : 0).run();

    return c.json({ success: true, id: siteId });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /sites/legals/:id — Textos legales del sitio ─────────
sites.get('/legals/:id', async (c) => {
  const id = c.req.param('id');
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM LEGALES WHERE ID_SITIO = ?'
    ).bind(id).first();
    return c.json(res || {});
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /sites/channels/:id — Canales externos del sitio ─────
sites.get('/channels/:id', async (c) => {
  const id = c.req.param('id');
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM CANALES_EXTERNOS WHERE ID_SITIO = ? AND ACTIVO = 1 ORDER BY ORDEN'
    ).bind(id).all();
    return c.json(res.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /sites/menus/:id — Menús de navegación del sitio ─────
sites.get('/menus/:id', async (c) => {
  const id = c.req.param('id');
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM MENUS_NAVEGACION WHERE ID_SITIO = ? AND ACTIVO = 1 ORDER BY ORDEN'
    ).bind(id).all();
    return c.json(res.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /sites/stats — Estadísticas por sitio del CMS (filtrado) ──
sites.get('/stats', async (c) => {
  try {
    const placeholders = SITIOS_LIST.map(() => '?').join(',');
    const sitesRes = await c.env.DB.prepare(
      `SELECT SLUG, NOMBRE FROM SITIOS WHERE SLUG IN (${placeholders}) AND ACTIVO = 1 ORDER BY NOMBRE`
    ).bind(...SITIOS_LIST).all();

    const statsArr = [];
    for (const site of (sitesRes.results || [])) {
      try {
        const tableName = `ARTICULOS_SITIO_${site.SLUG.toUpperCase()}`;
        const counts    = await c.env.DB.prepare(`
          SELECT
            COUNT(*) as total,
            SUM(CASE WHEN FB_PUBLICADO  = 1 THEN 1 ELSE 0 END) as fb
          FROM ${tableName}
        `).first();

        statsArr.push({
          slug:  site.SLUG,
          name:  site.NOMBRE,
          total: counts?.total || 0,
          fb:    counts?.fb    || 0,
        });
      } catch (e) {
        console.error(`Error getting stats for ${site.SLUG}:`, e.message);
        statsArr.push({ slug: site.SLUG, name: site.NOMBRE, total: 0, web: 0, fb: 0 });
      }
    }

    return c.json(statsArr);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

export default sites;
