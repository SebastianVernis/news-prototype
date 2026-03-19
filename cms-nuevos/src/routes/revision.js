// src/routes/revision.js — Mesa de Revisión de contenido

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { articleSlugify } from '../utils/helpers.js';

const revision = new Hono();

// ── GET /revision/pending — Artículos pendientes de revisión ─
revision.get('/pending', async (c) => {
  try {
    const res = await c.env.DB.prepare(
      "SELECT * FROM REVISION_CONTENIDO WHERE ESTADO IN ('PENDIENTE','CORREGIDO') ORDER BY FECHA_CREACION DESC LIMIT 50"
    ).all();
    return c.json(res.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── PUT /revision/:id — Editar contenido en revisión ─────────
revision.put('/:id', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const id = c.req.param('id');
    const { titulo, descripcion, contenido, url_imagen } = await c.req.json();

    try {
      await c.env.DB.prepare(`
        UPDATE REVISION_CONTENIDO SET
          TITULO_PROPUESTO = ?, DESCRIPCION_PROPUESTA = ?,
          CONTENIDO_PROPUESTO = ?, URL_IMAGEN = ?, ESTADO = 'CORREGIDO'
        WHERE ID = ?
      `).bind(titulo, descripcion || '', contenido, url_imagen || '', id).run();
    } catch (_) {
      // Fallback si la columna URL_IMAGEN no existe aún
      await c.env.DB.prepare(`
        UPDATE REVISION_CONTENIDO SET
          TITULO_PROPUESTO = ?, DESCRIPCION_PROPUESTA = ?,
          CONTENIDO_PROPUESTO = ?, ESTADO = 'CORREGIDO'
        WHERE ID = ?
      `).bind(titulo, descripcion || '', contenido, id).run();
    }

    return c.json({ success: true });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /revision/approve/:id — Aprobar y publicar ──────────
revision.post('/approve/:id', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const id = c.req.param('id');

    const rev = await c.env.DB.prepare(
      'SELECT * FROM REVISION_CONTENIDO WHERE ID = ?'
    ).bind(id).first();
    if (!rev) return c.json({ error: 'Revisión no encontrada' }, 404);

    const now    = new Date().toISOString();
    const slug   = articleSlugify(rev.TITULO_PROPUESTO || 'articulo');
    const paraId = crypto.randomUUID();

    const isFeatured = (rev.DESTACADO || 0) === 1 &&
      (rev.URL_IMAGEN && rev.URL_IMAGEN.trim() !== '');

    // Normalizar sitios (asegurar formato coma-separado)
    let sitiosStr = rev.SITIO_DESTINO || '';
    if (sitiosStr.startsWith('[')) {
      try { 
        sitiosStr = JSON.parse(sitiosStr).join(','); 
      } catch (e) {
        // Usar valor original si el parse falla
      }
    }

    // Publicar en ARTICULOS_PARAFRASEADOS
    await c.env.DB.prepare(`
      INSERT INTO ARTICULOS_PARAFRASEADOS
        (ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA,
         CATEGORIA, AUTOR, FECHA_PUBLICACION, SITIO_DESTINO, DESTACADO,
         VISTAS, ESTADO, URL_IMAGEN, FB_REQUERIDO, ES_BREVE)
      VALUES (?, ?, ?, ?, ?, ?, 'Mesa de Revisión', ?, ?, ?, 0, 'PUBLICADO', ?, ?, ?)
    `).bind(
      paraId, rev.TITULO_PROPUESTO, slug,
      rev.CONTENIDO_PROPUESTO || '', rev.DESCRIPCION_PROPUESTA || '',
      (rev.CATEGORIA || 'NACIONAL').toUpperCase(), now, sitiosStr,
      isFeatured ? 1 : 0, rev.URL_IMAGEN || '',
      rev.FB_REQUERIDO || 0, rev.ES_BREVE || 0
    ).run();

    // DISTRIBUCIÓN: Insertar en cada tabla ARTICULOS_SITIO_{SLUG}
    const sitiosArray = sitiosStr.split(',').map((s) => s.trim()).filter((s) => s);
    for (const siteSlug of sitiosArray) {
      const siteId     = crypto.randomUUID();
      const tableName  = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

      try {
        await c.env.DB.prepare(`
          INSERT INTO ${tableName} (
            ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
            FB_PUBLICADO, FB_FECHA, FB_POST_ID
          ) VALUES (?, ?, datetime('now'), 0, NULL, NULL)
        `).bind(siteId, paraId).run();
        console.log(`[DISTRIBUTION] Revision article ${paraId} assigned to ${siteSlug}`);
      } catch (e) {
        console.error(`[DISTRIBUTION] Error inserting into ${tableName}:`, e.message);
      }
    }

    // Marcar revisión como aprobada
    await c.env.DB.prepare(
      "UPDATE REVISION_CONTENIDO SET ESTADO = 'APROBADO' WHERE ID = ?"
    ).bind(id).run();

    return c.json({ success: true, articleId: paraId });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

export default revision;
