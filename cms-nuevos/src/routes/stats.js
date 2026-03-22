// src/routes/stats.js — Estadísticas del dashboard

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { SITIOS_LIST } from '../config.js';

const stats = new Hono();

// ── GET /stats/dashboard — Estadísticas reales para el admin ─
stats.get('/dashboard', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    // Total de artículos parafraseados
    const totalPub = await c.env.DB.prepare(
      'SELECT COUNT(*) as count FROM ARTICULOS_PARAFRASEADOS WHERE ESTADO = "PUBLICADO"'
    ).first();

    // Borradores CMS
    const totalCMS = await c.env.DB.prepare(
      "SELECT COUNT(*) as count FROM ARTICULOS_CMS WHERE ESTADO = 'BORRADOR'"
    ).first();

    // Pendientes de revisión
    const totalRev = await c.env.DB.prepare(
      "SELECT COUNT(*) as count FROM REVISION_CONTENIDO WHERE ESTADO = 'PENDIENTE'"
    ).first();

    // Facebook: Contar publicados en todas las tablas de sitio
    let fbPublished = 0;
    for (const siteSlug of SITIOS_LIST) {
      const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
      const result = await c.env.DB.prepare(`
        SELECT COUNT(*) as count FROM ${tableName} WHERE FB_PUBLICADO = 1
      `).first();
      fbPublished += result?.count || 0;
    }

    // Sitios activos
    const totalSites = await c.env.DB.prepare(
      'SELECT COUNT(*) as count FROM SITIOS WHERE ACTIVO = 1'
    ).first();

    // Facebook pendiente: artículos sin publicar en todas las tablas
    let fbPending = 0;
    for (const siteSlug of SITIOS_LIST) {
      const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
      const result = await c.env.DB.prepare(`
        SELECT COUNT(*) as count FROM ${tableName} WHERE FB_PUBLICADO = 0
      `).first();
      fbPending += result?.count || 0;
    }

    // Artículos web publicados hoy (usando FECHA_PUBLICACION de ARTICULOS_PARAFRASEADOS)
    const firstSiteTable = `ARTICULOS_SITIO_${SITIOS_LIST[0].toUpperCase()}`;
    const webToday = await c.env.DB.prepare(`
      SELECT COUNT(*) as count FROM ARTICULOS_PARAFRASEADOS ap
      JOIN ${firstSiteTable} s ON s.ID_PARAFRASEADO = ap.ID
      WHERE ap.ESTADO = 'PUBLICADO' AND DATE(ap.FECHA_PUBLICACION) = DATE('now')
    `).first();

    return c.json({
      articles: totalPub ? totalPub.count : 0,
      drafts: totalCMS ? totalCMS.count : 0,
      pending: totalRev ? totalRev.count : 0,
      facebook: fbPublished,
      facebookPending: fbPending,
      sites: totalSites ? totalSites.count : 0,
      webToday: webToday ? webToday.count : 0,
    });
  } catch (e) {
    console.error('Stats error:', e.message);
    return c.json({ error: e.message }, 500);
  }
});

export default stats;
