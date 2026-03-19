// src/routes/categories.js — Gestión de categorías

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { slugify } from '../utils/helpers.js';

const categories = new Hono();

// ── GET /categories — Listar categorías activas ──────────────
categories.get('/', async (c) => {
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM CATEGORIAS WHERE ACTIVA = 1 ORDER BY NOMBRE'
    ).all();
    return c.json(res.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /categories — Crear categoría ──────────────────────
categories.post('/', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const { nombre } = await c.req.json();
    if (!nombre) return c.json({ error: 'Nombre requerido' }, 400);

    const slug = slugify(nombre);
    await c.env.DB.prepare(
      'INSERT INTO CATEGORIAS (NOMBRE, SLUG, ACTIVA) VALUES (?, ?, 1)'
    ).bind(nombre.toUpperCase(), slug).run();

    return c.json({ success: true, slug });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

export default categories;
