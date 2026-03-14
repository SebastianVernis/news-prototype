// src/routes/ticker.js — Ticker financiero y titulares en vivo

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';

const ticker = new Hono();

// ── GET /ticker/financials — Datos financieros ───────────────
ticker.get('/financials', async (c) => {
  try {
    // Crear tabla si no existe (primera vez)
    try {
      await c.env.DB.prepare(`
        CREATE TABLE IF NOT EXISTS TICKER_FINANCIALS (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          SIMBOLO TEXT NOT NULL UNIQUE,
          NOMBRE TEXT NOT NULL,
          VALOR TEXT NOT NULL,
          CAMBIO TEXT DEFAULT '0.00%',
          TENDENCIA TEXT DEFAULT 'up',
          UNIDAD TEXT DEFAULT 'MXN',
          FECHA_ACTUALIZACION TEXT DEFAULT (datetime('now'))
        )
      `).run();
    } catch (_) {}

    const res = await c.env.DB.prepare(
      'SELECT SIMBOLO, NOMBRE, VALOR, CAMBIO, TENDENCIA, UNIDAD, FECHA_ACTUALIZACION FROM TICKER_FINANCIALS ORDER BY ID'
    ).all();

    return c.json(res.results || []);
  } catch (e) {
    return c.json([], 200); // Fallback a estáticos
  }
});

// ── GET /ticker/headlines — Titulares para breaking news ─────
ticker.get('/headlines', async (c) => {
  const limit = Math.min(parseInt(c.req.query('limit') || '10'), 30);
  try {
    // Crear tabla si no existe (primera vez)
    try {
      await c.env.DB.prepare(`
        CREATE TABLE IF NOT EXISTS TICKER_HEADLINES (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          TITULO TEXT NOT NULL,
          URL TEXT,
          FUENTE TEXT,
          FECHA_CREACION TEXT DEFAULT (datetime('now'))
        )
      `).run();
    } catch (_) {}

    const res = await c.env.DB.prepare(
      'SELECT TITULO, URL, FUENTE, FECHA_CREACION FROM TICKER_HEADLINES ORDER BY FECHA_CREACION DESC LIMIT ?'
    ).bind(limit).all();

    c.header('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    c.header('Pragma', 'no-cache');
    c.header('Expires', '0');

    return c.json(res.results || []);
  } catch (e) {
    return c.json([], 200); // Fallback a estáticos
  }
});

// ── POST /ticker/financials — Upsert datos financieros (admin/cron) ──
ticker.post('/financials', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const items = await c.req.json();
    if (!Array.isArray(items)) return c.json({ error: 'Se requiere array' }, 400);

    const now = new Date().toISOString();
    for (const item of items) {
      await c.env.DB.prepare(`
        INSERT INTO TICKER_FINANCIALS (SIMBOLO, NOMBRE, VALOR, CAMBIO, TENDENCIA, UNIDAD, FECHA_ACTUALIZACION)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(SIMBOLO) DO UPDATE SET
          NOMBRE = excluded.NOMBRE,
          VALOR = excluded.VALOR,
          CAMBIO = excluded.CAMBIO,
          TENDENCIA = excluded.TENDENCIA,
          UNIDAD = excluded.UNIDAD,
          FECHA_ACTUALIZACION = excluded.FECHA_ACTUALIZACION
      `).bind(
        item.simbolo, item.nombre, item.valor,
        item.cambio || '0.00%', item.tendencia || 'up',
        item.unidad || 'MXN', now
      ).run();
    }

    return c.json({ success: true, updated: items.length });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /ticker/headlines — Insertar titulares (admin/cron) ─
ticker.post('/headlines', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const items = await c.req.json();
    if (!Array.isArray(items)) return c.json({ error: 'Se requiere array' }, 400);

    const now = new Date().toISOString();
    for (const item of items) {
      if (!item.titulo) continue;
      await c.env.DB.prepare(
        'INSERT INTO TICKER_HEADLINES (TITULO, URL, FUENTE, FECHA_CREACION) VALUES (?, ?, ?, ?)'
      ).bind(item.titulo, item.url || null, item.fuente || null, now).run();
    }

    // Mantener solo los últimos 50 titulares
    await c.env.DB.prepare(`
      DELETE FROM TICKER_HEADLINES WHERE ID NOT IN (
        SELECT ID FROM TICKER_HEADLINES ORDER BY FECHA_CREACION DESC LIMIT 50
      )
    `).run();

    return c.json({ success: true, inserted: items.length });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

export default ticker;
