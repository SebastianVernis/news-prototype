// src/routes/articles.js — CRUD de artículos publicados

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { slugify, parseArticleRow } from '../utils/helpers.js';

const articles = new Hono();

// ── GET /articles — Listado con filtros ──────────────────────
articles.get('/', async (c) => {
  const { site, limit = 20, offset = 0, category } = c.req.query();
  const l = parseInt(limit);
  const o = parseInt(offset);
  const MIN_ARTICLES = 8;

  try {
    const fetchArticles = async (siteFilter, applyOffset = true) => {
      // Si hay sitio específico, consultar ARTICULOS_SITIO_{SLUG}
      if (siteFilter) {
        const tableName = `ARTICULOS_SITIO_${siteFilter.toUpperCase()}`;
        let query = `
          SELECT p.*, s.FB_PUBLICADO, s.FB_FECHA, s.FB_POST_ID
          FROM ${tableName} s
          JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
          WHERE p.ESTADO = 'PUBLICADO'
        `;
        const params = [];

        if (category) {
          query += ' AND LOWER(p.CATEGORIA) = LOWER(?)';
          params.push(category);
        }

        // Excluir artículos sin imagen
        query += " AND p.URL_IMAGEN IS NOT NULL AND p.URL_IMAGEN != '' AND p.URL_IMAGEN NOT LIKE '%logo.png%'";

        query += ' ORDER BY p.FECHA_PUBLICACION DESC LIMIT ? OFFSET ?';
        params.push(l, applyOffset ? o : 0);

        const res = await c.env.DB.prepare(query).bind(...params).all();
        return (res.results || []).map(parseArticleRow).filter(Boolean);
      }

      // Sin filtro de sitio: consultar PARAFRASEADOS y CMS
      let queryPara  = "SELECT *, 'PARAFRASEADO' as SOURCE_TABLE FROM ARTICULOS_PARAFRASEADOS WHERE ESTADO = 'PUBLICADO'";
      let paramsPara = [];
      let queryCMS   = "SELECT *, 'CMS' as SOURCE_TABLE FROM ARTICULOS_CMS WHERE ESTADO = 'PUBLICADO'";
      let paramsCMS  = [];

      if (category) {
        queryPara += ' AND LOWER(CATEGORIA) = LOWER(?)';
        paramsPara.push(category);
        queryCMS += ' AND LOWER(CATEGORIA) = LOWER(?)';
        paramsCMS.push(category);
      }

      queryPara += ' ORDER BY FECHA_PUBLICACION DESC LIMIT ? OFFSET ?';
      paramsPara.push(l, applyOffset ? o : 0);
      queryCMS += ' ORDER BY FECHA_PUBLICACION DESC LIMIT ? OFFSET ?';
      paramsCMS.push(l, applyOffset ? o : 0);

      const [resPara, resCMS] = await Promise.all([
        c.env.DB.prepare(queryPara).bind(...paramsPara).all(),
        c.env.DB.prepare(queryCMS).bind(...paramsCMS).all(),
      ]);

      return [...(resPara.results || []), ...(resCMS.results || [])]
        .map(parseArticleRow)
        .filter(Boolean)
        .sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt))
        .slice(0, l);
    };

    let arts = await fetchArticles(site);

    // Complementar si hay menos del mínimo y estamos en un sitio específico
    if (site && arts.length < MIN_ARTICLES && o === 0) {
      const allArticles = await fetchArticles(null, false);
      const existingIds = new Set(arts.map((a) => a.id));
      const extras = allArticles.filter((a) => !existingIds.has(a.id));
      arts = [...arts, ...extras].slice(0, l);
    }

    return c.json({ articles: arts });
  } catch (e) {
    console.error('Error fetching articles:', e.message);
    return c.json({ articles: [] });
  }
});

// ── GET /articles/timeline — Noticias breves ─────────────────
articles.get('/timeline', async (c) => {
  const { site, limit = 20 } = c.req.query();
  try {
    const s   = site ? `%${site}%` : '%';
    const res = await c.env.DB.prepare(
      'SELECT * FROM ARTICULOS_PARAFRASEADOS WHERE ES_BREVE = 1 AND SITIO_DESTINO LIKE ? ORDER BY FECHA_PUBLICACION DESC LIMIT ?'
    ).bind(s, parseInt(limit)).all();
    return c.json({ articles: (res.results || []).map(parseArticleRow) });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /articles/id/:id — Artículo por ID ───────────────────
articles.get('/id/:id', async (c) => {
  const id = c.req.param('id');
  try {
    const rowPara = await c.env.DB.prepare(
      "SELECT *, 'PARAFRASEADO' as SOURCE_TABLE FROM ARTICULOS_PARAFRASEADOS WHERE ID = ? LIMIT 1"
    ).bind(id).first();
    if (rowPara) return c.json({ article: parseArticleRow(rowPara) });

    const rowCMS = await c.env.DB.prepare(
      "SELECT *, 'CMS' as SOURCE_TABLE FROM ARTICULOS_CMS WHERE ID = ? LIMIT 1"
    ).bind(id).first();
    if (rowCMS) {
      return c.json({
        article: {
          id:          rowCMS.ID,
          title:       rowCMS.TITULO,
          slug:        rowCMS.SLUG,
          content:     rowCMS.CONTENIDO,
          excerpt:     rowCMS.DESCRIPCION,
          category:    rowCMS.CATEGORIA,
          author:      rowCMS.AUTOR || 'Redacción CMS',
          publishedAt: rowCMS.FECHA_PUBLICACION,
          imageUrl:    rowCMS.URL_IMAGEN,
          featured:    Boolean(rowCMS.DESTACADO || 0),
          site:        rowCMS.SITIOS_DESTINO,
          status:      rowCMS.ESTADO,
          sourceTable: 'CMS',
        },
      });
    }

    return c.json({ error: 'Artículo no encontrado' }, 404);
  } catch (e) {
    console.error('Error fetching article by id:', e);
    return c.json({ error: e.message }, 500);
  }
});

// ── GET /articles/:slug — Artículo por slug ──────────────────
articles.get('/:slug', async (c) => {
  const slug = c.req.param('slug');
  try {
    // 1. Buscar por SLUG exacto en PARAFRASEADOS
    const rowPara = await c.env.DB.prepare(
      "SELECT *, 'PARAFRASEADO' as SOURCE_TABLE FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? LIMIT 1"
    ).bind(slug).first();
    if (rowPara) return c.json({ article: parseArticleRow(rowPara) });

    // 2. Buscar en CMS por SLUG
    let rowCMS = null;
    try {
      rowCMS = await c.env.DB.prepare(
        "SELECT *, 'CMS' as SOURCE_TABLE FROM ARTICULOS_CMS WHERE ESTADO = 'PUBLICADO' AND SLUG = ? LIMIT 1"
      ).bind(slug).first();
    } catch (e) {
      console.error('Error fetching CMS article by slug:', e.message);
    }
    if (rowCMS) return c.json({ article: parseArticleRow(rowCMS) });

    // 3. Fallback: artículos con SLUG NULL — comparar slug generado desde título
    const allPara = await c.env.DB.prepare(
      "SELECT *, 'PARAFRASEADO' as SOURCE_TABLE FROM ARTICULOS_PARAFRASEADOS WHERE SLUG IS NULL ORDER BY FECHA_PUBLICACION DESC LIMIT 100"
    ).all();
    const matchPara = (allPara.results || []).find((r) => {
      const generated = slugify(r.TITULO_PARAFRASEADO || r.TITULO || '');
      return generated === slug;
    });
    if (matchPara) return c.json({ article: parseArticleRow(matchPara) });

    return c.json({ error: 'Article not found' }, 404);
  } catch (e) {
    console.error('Error fetching article by slug:', e.message);
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /articles — Crear artículo ──────────────────────────
articles.post('/', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const article = await c.req.json();

    if (!article.title || !article.content) {
      return c.json({ error: 'Título y contenido requeridos' }, 400);
    }

    const wordCount = article.content.trim().split(/\s+/).length;
    const slug      = article.slug || slugify(article.title);
    const now       = new Date().toISOString();
    const articleId = crypto.randomUUID();

    await c.env.DB.prepare(`
      INSERT INTO ARTICULOS_PARAFRASEADOS (
        ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA,
        CATEGORIA, AUTOR, FECHA_PUBLICACION, URL_IMAGEN, SITIO_DESTINO,
        DESTACADO, VISTAS, ESTADO
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      articleId,
      article.title,
      slug,
      article.content,
      article.excerpt || article.content.substring(0, 200) + '...',
      (article.category || 'NACIONAL').toUpperCase(),
      article.author || 'Editorial',
      article.publishedAt || now,
      article.imageUrl || '',
      article.site || 'cbnnoticias',
      article.featured ? 1 : 0,
      0,
      'PUBLICADO'
    ).run();

    return c.json({ success: true, article: { id: articleId, slug, title: article.title, wordCount } });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── POST /articles/bulk — Insertar múltiples artículos ───────
articles.post('/bulk', async (c) => {
  try {
    const { articles: items } = await c.req.json();

    if (!Array.isArray(items) || items.length === 0) {
      return c.json({ error: 'Se requiere array de artículos' }, 400);
    }

    const results = [];
    const errors  = [];

    for (const article of items) {
      try {
        if (!article.title || !article.content || !article.category) {
          errors.push({ article: article.title || 'sin-titulo', error: 'Campos requeridos faltantes' });
          continue;
        }

        const slug = article.slug || slugify(article.title);
        const now  = new Date().toISOString();

        await c.env.DB.prepare(`
          INSERT INTO ARTICULOS_PARAFRASEADOS (
            TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA,
            CATEGORIA, AUTOR, FECHA_PUBLICACION, URL_IMAGEN, SITIO_DESTINO,
            DESTACADO, VISTAS, ESTADO
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `).bind(
          article.title,
          slug,
          article.content,
          article.excerpt || article.description || article.content.substring(0, 200) + '...',
          article.category.toUpperCase(),
          article.author || 'Redacción',
          article.publishedAt || now,
          article.imageUrl || '',
          article.sites || 'cbnnoticias',
          article.featured ? 1 : 0,
          0,
          'PUBLICADO'
        ).run();

        results.push({ title: article.title, slug, status: 'inserted' });
      } catch (e) {
        errors.push({ article: article.title || 'sin-titulo', error: e.message });
      }
    }

    return c.json({
      success:  true,
      inserted: results.length,
      errors:   errors.length > 0 ? errors : undefined,
      total:    items.length,
    });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── PUT /articles/:id — Actualizar artículo ──────────────────
articles.put('/:id', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  const id = c.req.param('id');
  try {
    const { title, slug, content, excerpt, category, author, imageUrl, featured, site, status } =
      await c.req.json();

    if (!title) return c.json({ error: 'Título requerido' }, 400);

    const articleSlug = slug || slugify(title);
    const now         = new Date().toISOString();

    // Intentar actualizar en PARAFRASEADOS primero
    const existingPara = await c.env.DB.prepare(
      'SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE ID = ?'
    ).bind(id).first();

    if (existingPara) {
      await c.env.DB.prepare(`
        UPDATE ARTICULOS_PARAFRASEADOS SET
          TITULO_PARAFRASEADO = ?, SLUG = ?, CONTENIDO = ?,
          DESCRIPCION_PARAFRASEADA = ?, CATEGORIA = ?, AUTOR = ?,
          FECHA_PUBLICACION = ?, URL_IMAGEN = ?, SITIO_DESTINO = ?, DESTACADO = ?
        WHERE ID = ?
      `).bind(
        title, articleSlug, content || '', excerpt || '',
        (category || 'NACIONAL').toUpperCase(), author || 'Redacción',
        now, imageUrl || '', site || '', featured ? 1 : 0, id
      ).run();
      return c.json({ success: true, id, source: 'PARAFRASEADOS' });
    }

    // Si no está en PARA, intentar en CMS
    const existingCMS = await c.env.DB.prepare(
      'SELECT ID FROM ARTICULOS_CMS WHERE ID = ?'
    ).bind(id).first();

    if (existingCMS) {
      await c.env.DB.prepare(`
        UPDATE ARTICULOS_CMS SET
          TITULO = ?, SLUG = ?, CONTENIDO = ?, DESCRIPCION = ?,
          CATEGORIA = ?, URL_IMAGEN = ?, DESTACADO = ?, ESTADO = ?, FECHA_PUBLICACION = ?
        WHERE ID = ?
      `).bind(
        title, articleSlug, content || '', excerpt || '',
        (category || 'NACIONAL').toUpperCase(), imageUrl || '',
        featured ? 1 : 0, status || 'BORRADOR', now, id
      ).run();
      return c.json({ success: true, id, source: 'CMS' });
    }

    return c.json({ error: 'Artículo no encontrado' }, 404);
  } catch (e) {
    console.error('Error updating article:', e);
    return c.json({ error: e.message }, 500);
  }
});

// ── DELETE /articles/:id — Eliminar artículo ─────────────────
articles.delete('/:id', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  const id = c.req.param('id');
  try {
    // 1. Eliminar métricas (FOREIGN KEY)
    await c.env.DB.prepare(
      'DELETE FROM METRICAS_CONTENIDO WHERE ID_ARTICULO_PARAFRASEADO = ?'
    ).bind(id).run();

    // 2. Eliminar de PARAFRASEADOS
    await c.env.DB.prepare(
      'DELETE FROM ARTICULOS_PARAFRASEADOS WHERE ID = ?'
    ).bind(id).run();

    // 3. Intentar eliminar de CMS también
    try {
      await c.env.DB.prepare('DELETE FROM ARTICULOS_CMS WHERE ID = ?').bind(id).run();
    } catch (e) {
      console.error('Error deleting from CMS (may not exist):', e.message);
    }

    return c.json({ success: true });
  } catch (e) {
    console.error('Delete Error:', e.message);
    return c.json({ error: e.message }, 500);
  }
});

export default articles;
