// src/routes/cms.js — Gestión de artículos CMS (borradores y publicación)

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { articleSlugify } from '../utils/helpers.js';
import { publishToFBIndividual } from '../cron/facebook.js';

const cms = new Hono();

// ── GET /cms/articles — Listar borradores ────────────────────
cms.get('/articles', async (c) => {
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM ARTICULOS_CMS ORDER BY FECHA_CREACION DESC LIMIT 50'
    ).all();
    return c.json(res.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /cms/articles — Crear o actualizar borrador ─────────
cms.post('/articles', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const body = await c.req.json();

    // Soporte de nombres en español e inglés
    const id         = body.id;
    const titulo     = body.titulo     || body.title;
    const contenido  = body.contenido  || body.content;
    const descripcion = body.descripcion || body.excerpt;
    const categoria  = body.categoria  || body.category;
    const url_imagen = body.url_imagen || body.imageUrl;
    const destacado  = body.destacado !== undefined ? body.destacado : (body.featured ? 1 : 0);
    const estado     = body.estado     || body.status;

    if (!titulo) return c.json({ error: 'Título requerido' }, 400);

    const now       = new Date().toISOString();
    const articleId = id || crypto.randomUUID();
    let slug        = articleSlugify(titulo);
    let retryCount  = 0;
    const maxRetries = 3;

    while (retryCount < maxRetries) {
      try {
        if (!id) {
          const existingSlug = await c.env.DB.prepare(
            'SELECT ID, TITULO FROM ARTICULOS_CMS WHERE SLUG = ? LIMIT 1'
          ).bind(slug).first();

          if (existingSlug) {
            slug = `${articleSlugify(titulo)}-${Date.now()}`;
            console.log(`[CMS] SLUG "${articleSlugify(titulo)}" ya existe. Usando: ${slug}`);
          }
        }

        if (id) {
          await c.env.DB.prepare(`
            UPDATE ARTICULOS_CMS SET
              TITULO = ?, SLUG = ?, CONTENIDO = ?, DESCRIPCION = ?,
              CATEGORIA = ?, URL_IMAGEN = ?, DESTACADO = ?, ESTADO = ?,
              LEGACY_SLUG = CASE WHEN SLUG IS NOT NULL AND SLUG != ? THEN SLUG ELSE LEGACY_SLUG END
            WHERE ID = ?
          `).bind(
            titulo, slug, contenido || '', descripcion || '',
            (categoria || 'NACIONAL').toUpperCase(), url_imagen || '',
            destacado || 0, estado || 'BORRADOR', slug, id
          ).run();
        } else {
          await c.env.DB.prepare(`
            INSERT INTO ARTICULOS_CMS (ID, TITULO, SLUG, CONTENIDO, DESCRIPCION, CATEGORIA, URL_IMAGEN, DESTACADO, ESTADO, FECHA_CREACION)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          `).bind(
            articleId, titulo, slug, contenido || '', descripcion || '',
            (categoria || 'NACIONAL').toUpperCase(), url_imagen || '',
            destacado || 0, estado || 'BORRADOR', now
          ).run();
        }

        break; // Éxito — salir del loop

      } catch (dbErr) {
        if (dbErr.message.includes('UNIQUE constraint failed') && retryCount < maxRetries - 1) {
          retryCount++;
          slug = `${articleSlugify(titulo)}-${Date.now()}-${retryCount}`;
          console.log(`[CMS] UNIQUE constraint error. Retry ${retryCount}/${maxRetries} con SLUG: ${slug}`);
        } else {
          throw dbErr;
        }
      }
    }

    return c.json({ success: true, id: articleId, slug });
  } catch (e) {
    console.error('[CMS/articles] Error:', e.message);
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /cms/generate-variations — Generar variaciones → Mesa de Revisión ──
cms.post('/generate-variations', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const { id, sitios } = await c.req.json();
    if (!id || !Array.isArray(sitios) || sitios.length === 0) {
      return c.json({ error: 'ID y sitios requeridos' }, 400);
    }

    const article = await c.env.DB.prepare(
      'SELECT * FROM ARTICULOS_CMS WHERE ID = ?'
    ).bind(id).first();
    if (!article) return c.json({ error: 'Artículo no encontrado' }, 404);

    const now = new Date().toISOString();
    for (const sitio of sitios) {
      await c.env.DB.prepare(`
        INSERT INTO REVISION_CONTENIDO
          (ID_ORIGEN, TIPO_ORIGEN, TITULO_PROPUESTO, CONTENIDO_PROPUESTO,
           DESCRIPCION_PROPUESTA, SITIO_DESTINO, CATEGORIA, ESTADO, FECHA_CREACION)
        VALUES (?, 'CMS', ?, ?, ?, ?, ?, 'PENDIENTE', ?)
      `).bind(
        id, article.TITULO, article.CONTENIDO || '',
        article.DESCRIPCION || '', sitio,
        article.CATEGORIA || 'NACIONAL', now
      ).run();
    }

    return c.json({ success: true, variations: sitios.length });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /cms/publish — Publicar directamente desde CMS ──────
cms.post('/publish', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const { id, sitios, fb_requerido } = await c.req.json();
    if (!id || !Array.isArray(sitios) || sitios.length === 0) {
      return c.json({ error: 'ID y sitios requeridos' }, 400);
    }

    const article = await c.env.DB.prepare(
      'SELECT * FROM ARTICULOS_CMS WHERE ID = ?'
    ).bind(id).first();
    if (!article) return c.json({ error: 'Artículo no encontrado' }, 404);

    const baseSlug = article.SLUG || articleSlugify(article.TITULO);

    // Verificar si ya existe un registro publicado con este SLUG (evita duplicados)
    const existingPara = await c.env.DB.prepare(
      'SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? AND ESTADO = "PUBLICADO" LIMIT 1'
    ).bind(baseSlug).first();

    if (existingPara) {
      const now       = new Date().toISOString();
      const sitiosStr = sitios.join(',');
      const isFeatured = (article.DESTACADO || 0) === 1 &&
        (article.URL_IMAGEN && article.URL_IMAGEN.trim() !== '');

      await c.env.DB.prepare(`
        UPDATE ARTICULOS_PARAFRASEADOS SET
          TITULO_PARAFRASEADO = ?, CONTENIDO = ?, DESCRIPCION_PARAFRASEADA = ?,
          CATEGORIA = ?, FECHA_PUBLICACION = ?, URL_IMAGEN = ?,
          SITIO_DESTINO = ?, DESTACADO = ?
        WHERE ID = ?
      `).bind(
        article.TITULO, article.CONTENIDO || '', article.DESCRIPCION || '',
        (article.CATEGORIA || 'NACIONAL').toUpperCase(), now,
        article.URL_IMAGEN || '', sitiosStr, isFeatured ? 1 : 0, existingPara.ID
      ).run();

      await c.env.DB.prepare(
        "UPDATE ARTICULOS_CMS SET ESTADO = 'PUBLICADO', SITIOS_DESTINO = ?, FECHA_PUBLICACION = ?, DESTACADO = ? WHERE ID = ?"
      ).bind(sitiosStr, now, isFeatured ? 1 : 0, id).run();

      return c.json({ success: true, published: 0, updated: 1, siteCount: sitios.length, message: 'Artículo actualizado (ya existía)' });
    }

    const now       = new Date().toISOString();
    const sitiosStr = sitios.join(',');
    const isFeatured = (article.DESTACADO || 0) === 1 &&
      (article.URL_IMAGEN && article.URL_IMAGEN.trim() !== '');

    // Marcar CMS como publicado
    await c.env.DB.prepare(
      "UPDATE ARTICULOS_CMS SET ESTADO = 'PUBLICADO', SITIOS_DESTINO = ?, FECHA_PUBLICACION = ?, DESTACADO = ? WHERE ID = ?"
    ).bind(sitiosStr, now, isFeatured ? 1 : 0, id).run();

    // Insertar en ARTICULOS_PARAFRASEADOS
    const paraId = crypto.randomUUID();
    await c.env.DB.prepare(`
      INSERT INTO ARTICULOS_PARAFRASEADOS
        (ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA,
         CATEGORIA, AUTOR, FECHA_PUBLICACION, URL_IMAGEN, SITIO_DESTINO,
         DESTACADO, VISTAS, ESTADO)
      VALUES (?, ?, ?, ?, ?, ?, 'Redacción CMS', ?, ?, ?, ?, 0, 'PUBLICADO')
    `).bind(
      paraId, article.TITULO, baseSlug,
      article.CONTENIDO || '', article.DESCRIPCION || '',
      (article.CATEGORIA || 'NACIONAL').toUpperCase(), now,
      article.URL_IMAGEN || '', sitiosStr, isFeatured ? 1 : 0
    ).run();

    // DISTRIBUCIÓN: Insertar en cada tabla ARTICULOS_SITIO_{SLUG}
    for (const siteSlug of sitios) {
      const siteId     = crypto.randomUUID();
      const tableName  = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

      try {
        await c.env.DB.prepare(`
          INSERT INTO ${tableName} (
            ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
            FB_PUBLICADO, FB_FECHA, FB_POST_ID
          ) VALUES (?, ?, datetime('now'), 0, NULL, NULL)
        `).bind(siteId, paraId).run();

        // PUBLICACIÓN INMEDIATA EN FACEBOOK para artículos CMS
        console.log(`[FB] Publishing CMS article ${paraId} to ${siteSlug} immediately...`);
        
        try {
          const fbResult = await publishToFBIndividual(c.env, {
            SITIO_ID: siteId,
            ID_PARAFRASEADO: paraId,
            TITULO: article.TITULO,
            SLUG: baseSlug,
            URL_IMAGEN: article.URL_IMAGEN || ''
          }, siteSlug);
          
          if (fbResult.success) {
            // Actualizar con FB_POST_ID real
            await c.env.DB.prepare(`
              UPDATE ${tableName}
              SET FB_PUBLICADO = 1, FB_FECHA = datetime('now'), FB_POST_ID = ?
              WHERE ID = ?
            `).bind(fbResult.post_id, siteId).run();
            console.log(`[FB] ${siteSlug} SUCCESS: ${fbResult.post_id}`);
          } else {
            console.error(`[FB] ${siteSlug} FAILED: ${JSON.stringify(fbResult.error)}`);
          }
        } catch (fbErr) {
          console.error(`[FB] ${siteSlug} EXCEPTION: ${fbErr.message}`);
        }

        console.log(`[DISTRIBUTION] Article ${paraId} assigned to ${siteSlug}`);
      } catch (e) {
        console.error(`[DISTRIBUTION] Error inserting into ${tableName}:`, e.message);
      }
    }

    return c.json({ success: true, published: 1, siteCount: sitios.length });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

export default cms;
