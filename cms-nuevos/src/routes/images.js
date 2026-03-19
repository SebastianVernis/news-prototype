// src/routes/images.js — Servir imágenes desde R2 y subida de archivos

import { Hono } from 'hono';

const images = new Hono();

// ── GET /images/* — Sirve imágenes almacenadas en R2 ─────────
images.get('/*', async (c) => {
  const key = c.req.param('*');
  if (!key) return c.text('Not Found', 404);

  try {
    const object = await c.env.UPLOADS.get(key);
    if (!object) return c.text('Not Found', 404);

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    headers.set('X-Content-Type-Options', 'nosniff');

    return new Response(object.body, { status: 200, headers });
  } catch (e) {
    console.log('Image serve error:', e.message);
    return c.text('Not Found', 404);
  }
});

export default images;
