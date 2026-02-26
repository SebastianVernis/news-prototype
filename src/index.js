// src/index.js - API News Profesional (ULTRA-ESTABLE)
import { Hono } from 'hono';
import { cors } from 'hono/cors';

const app = new Hono().basePath('/api');

// Dominios permitidos (sitios de la red) - con y sin www
const ALLOWED_ORIGINS = [
  // Con www
  'https://www.noticiasobjetivo.click',
  'https://www.mexicoinformado.lat',
  'https://www.bitacoraurbana.lat',
  'https://www.nodoinformativo.lat',
  'https://www.cbnnoticias.click',
  'https://www.centralmexico.online',
  'https://www.verticenoticias.today',
  'https://www.radiocinconoticias.click',
  'https://www.reportecentral.site',
  'https://www.tvmexiconews.site',
  // Sin www (root domains)
  'https://noticiasobjetivo.click',
  'https://mexicoinformado.lat',
  'https://bitacoraurbana.lat',
  'https://nodoinformativo.lat',
  'https://cbnnoticias.click',
  'https://centralmexico.online',
  'https://verticenoticias.today',
  'https://radiocinconoticias.click',
  'https://reportecentral.site',
  'https://tvmexiconews.site',
  'https://cms.sebastianvernis.space',
];

app.use('*', cors({
  origin: (origin) => {
    if (!origin) return '*'; // peticiones server-side / curl
    if (ALLOWED_ORIGINS.includes(origin)) return origin;
    if (origin.endsWith('.pages.dev')) return origin; // contingencia pages.dev
    if (origin.includes('localhost') || origin.includes('127.0.0.1')) return origin; // desarrollo local
    return null; // bloquear otros orígenes
  },
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization'],
}));

// ============================================================
// AUTH HELPER
// ============================================================
const checkAuth = (c) => {
  const token = (c.req.header('Authorization') || '').replace('Bearer ', '').trim();
  const adminToken = c.env.ADMIN_TOKEN;
  if (adminToken && token !== adminToken) return false;
  return true;
};

// Función para verificar contraseña con hash simple (SHA-256 simulado)
// En producción, usar bcrypt o argon2
const verifyPassword = async (password, storedHash) => {
  // Hash simple para demo - en producción usar bcrypt
  const simpleHash = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString(16);
  };
  return simpleHash(password) === storedHash;
};

// ── Crear nuevo usuario (solo admin) ────────────────────────────────────────
app.post('/auth/users', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const { username, email, role } = await c.req.json();
    if (!username) return c.json({ error: 'Nombre de usuario requerido' }, 400);

    const existing = await c.env.DB.prepare(
      'SELECT ID FROM USUARIOS WHERE NOMBRE = ?'
    ).bind(username).first();
    if (existing) return c.json({ error: 'El usuario ya existe' }, 409);

    const userId = crypto.randomUUID();
    await c.env.DB.prepare(
      'INSERT INTO USUARIOS (ID, NOMBRE, EMAIL, ROL, ACTIVO) VALUES (?, ?, ?, ?, 1)'
    ).bind(userId, username, email || '', role || 'editor').run();

    return c.json({ success: true, id: userId, username });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── Listar usuarios (solo admin) ─────────────────────────────────────────────
app.get('/auth/users', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const res = await c.env.DB.prepare(
      'SELECT ID, NOMBRE, EMAIL, ROL, ACTIVO FROM USUARIOS ORDER BY NOMBRE'
    ).all();
    return c.json(res.results || []);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── Generar token temporal para configuración de contraseña ─────────────────
// Requiere el ADMIN_TOKEN en Authorization header
// Genera un token único que expira en 24 horas
app.post('/auth/generate-password-token', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Token de administrador inválido' }, 401);
  try {
    const { username } = await c.req.json();
    if (!username) {
      return c.json({ error: 'Usuario requerido' }, 400);
    }

    // Verificar que el usuario existe
    const user = await c.env.DB.prepare(
      'SELECT ID FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
    ).bind(username).first();
    if (!user) return c.json({ error: 'Usuario no encontrado o inactivo' }, 404);

    // Crear token único temporal
    const tempToken = crypto.randomUUID();
    const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(); // 24 horas

    // Crear tabla de tokens temporales si no existe
    try {
      await c.env.DB.prepare(`
        CREATE TABLE IF NOT EXISTS PASSWORD_RESET_TOKENS (
          ID TEXT PRIMARY KEY,
          USER_ID TEXT NOT NULL,
          TOKEN TEXT UNIQUE NOT NULL,
          EXPIRES_AT TEXT NOT NULL,
          USED INTEGER DEFAULT 0,
          CREATED_AT TEXT NOT NULL
        )
      `).run();
    } catch (_) { /* tabla ya existe */ }

    // Guardar token en la base de datos
    await c.env.DB.prepare(`
      INSERT INTO PASSWORD_RESET_TOKENS (ID, USER_ID, TOKEN, EXPIRES_AT, CREATED_AT)
      VALUES (?, ?, ?, ?, ?)
    `).bind(crypto.randomUUID(), user.ID, tempToken, expiresAt, new Date().toISOString()).run();

    // Generar URL de configuración
    const baseUrl = c.env.SITE_URL || 'https://news-admin-cms.pages.dev';
    const setupUrl = `${baseUrl}/admin/setup-password.html?user=${encodeURIComponent(username)}&t=${tempToken}`;

    return c.json({
      success: true,
      token: tempToken,
      expiresAt,
      setupUrl,
      message: 'Token generado exitosamente. Válido por 24 horas.'
    });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// ── Validar token de configuración de contraseña ────────────────────────────
app.get('/auth/validate-password-token', async (c) => {
  try {
    const username = c.req.query('user');
    const token = c.req.query('t');

    if (!username || !token) {
      return c.json({ valid: false, error: 'Parámetros requeridos' }, 400);
    }

    const user = await c.env.DB.prepare(
      'SELECT ID FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
    ).bind(username).first();
    if (!user) return c.json({ valid: false, error: 'Usuario no encontrado' }, 404);

    const tokenRecord = await c.env.DB.prepare(`
      SELECT * FROM PASSWORD_RESET_TOKENS
      WHERE TOKEN = ? AND USER_ID = ? AND USED = 0 AND EXPIRES_AT > ?
    `).bind(token, user.ID, new Date().toISOString()).first();

    if (!tokenRecord) {
      return c.json({ valid: false, error: 'Token inválido o expirado' }, 404);
    }

    return c.json({ valid: true, username });
  } catch (e) {
    return c.json({ valid: false, error: e.message }, 500);
  }
});

// ── Establecer contraseña para un usuario ────────────────────────────────────
// Requiere ADMIN_TOKEN o token temporal válido
app.post('/auth/setup-password', async (c) => {
  const token = (c.req.header('Authorization') || '').replace('Bearer ', '').trim();
  
  // Verificar autenticación: puede ser ADMIN_TOKEN o token temporal
  let isAdmin = false;
  let username = null;
  
  // 1. Verificar si es ADMIN_TOKEN
  const adminToken = c.env.ADMIN_TOKEN;
  if (adminToken && token === adminToken) {
    isAdmin = true;
    // Necesitamos el username del body
    const body = await c.req.json();
    username = body.username;
  } else {
    // 2. Verificar si es token temporal
    try {
      // Primero necesitamos el username para validar el token
      const body = await c.req.json();
      username = body.username;
      
      if (!username) {
        return c.json({ error: 'Usuario requerido' }, 400);
      }
      
      const user = await c.env.DB.prepare(
        'SELECT ID FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
      ).bind(username).first();
      
      if (!user) {
        return c.json({ error: 'Usuario no encontrado o inactivo' }, 404);
      }
      
      const tokenRecord = await c.env.DB.prepare(`
        SELECT * FROM PASSWORD_RESET_TOKENS
        WHERE TOKEN = ? AND USER_ID = ? AND USED = 0 AND EXPIRES_AT > ?
      `).bind(token, user.ID, new Date().toISOString()).first();
      
      if (!tokenRecord) {
        return c.json({ error: 'Token temporal inválido o expirado' }, 401);
      }
      
      // Token válido - marcar como usado
      await c.env.DB.prepare(`
        UPDATE PASSWORD_RESET_TOKENS SET USED = 1 WHERE TOKEN = ?
      `).bind(token).run();
      
      isAdmin = true;
    } catch (e) {
      return c.json({ error: 'Token inválido' }, 401);
    }
  }
  
  if (!isAdmin) {
    return c.json({ error: 'No autorizado' }, 401);
  }
  
  try {
    const { username: bodyUsername, passwordHash } = await c.req.json();
    const finalUsername = username || bodyUsername;
    
    if (!finalUsername || !passwordHash) {
      return c.json({ error: 'Usuario y hash de contraseña requeridos' }, 400);
    }

    // Verificar que el usuario existe
    const user = await c.env.DB.prepare(
      'SELECT ID FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
    ).bind(finalUsername).first();
    if (!user) return c.json({ error: 'Usuario no encontrado o inactivo' }, 404);

    // Guardar el hash en la tabla USUARIOS (columna PASSWORD_HASH)
    // Si la columna no existe, la creamos con ALTER TABLE
    try {
      await c.env.DB.prepare(
        'ALTER TABLE USUARIOS ADD COLUMN PASSWORD_HASH TEXT'
      ).run();
    } catch (_) { /* columna ya existe */ }

    await c.env.DB.prepare(
      'UPDATE USUARIOS SET PASSWORD_HASH = ? WHERE NOMBRE = ?'
    ).bind(passwordHash, finalUsername).run();

    return c.json({ success: true, message: 'Contraseña configurada correctamente' });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// Login de usuario
app.post('/auth/login', async (c) => {
  try {
    const { username, password } = await c.req.json();
    
    if (!username || !password) {
      return c.json({ error: 'Usuario y contraseña requeridos' }, 400);
    }
    
    // Buscar usuario en la base de datos
    const user = await c.env.DB.prepare(
      'SELECT * FROM USUARIOS WHERE NOMBRE = ? AND ACTIVO = 1'
    ).bind(username).first();
    
    if (!user) {
      return c.json({ error: 'Usuario o contraseña incorrectos' }, 401);
    }
    
    // Generar hash SHA-256 de la contraseña ingresada
    const inputHash = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(password))
      .then(buf => Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join(''));

    let isValid = false;

    // 1. Verificar contra PASSWORD_HASH del usuario en la BD (por usuario)
    if (user.PASSWORD_HASH) {
      isValid = inputHash === user.PASSWORD_HASH;
    }
    // 2. Fallback: verificar contra USER_PASSWORD_HASH global (env var)
    else if (c.env.USER_PASSWORD_HASH) {
      isValid = inputHash === c.env.USER_PASSWORD_HASH;
    }
    // 3. Sin hash configurado: acceso libre (solo para desarrollo)
    else {
      isValid = true;
    }
    
    if (!isValid) {
      return c.json({ error: 'Usuario o contraseña incorrectos' }, 401);
    }
    
    // Generar token simple
    const token = crypto.randomUUID();
    
    // Guardar token en la base de datos (opcional para sesiones)
    // Por ahora retornamos el token directamente
    
    return c.json({
      success: true,
      token: token,
      user: {
        id: user.ID,
        name: user.NOMBRE,
        email: user.EMAIL,
        role: user.ROL
      }
    });
  } catch (e) {
    console.error('Error en login:', e);
    return c.json({ error: e.message }, 500);
  }
});

// ============================================================
// ARTICLES - CRUD Completo para Artículos Publicados
// ============================================================

// GET /api/stats/dashboard - Estadísticas reales para el admin
app.get('/stats/dashboard', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const totalPub = await c.env.DB.prepare("SELECT COUNT(*) as count FROM ARTICULOS_PARAFRASEADOS").first();
    const totalCMS = await c.env.DB.prepare("SELECT COUNT(*) as count FROM ARTICULOS_CMS WHERE ESTADO = 'BORRADOR'").first();
    const totalRev = await c.env.DB.prepare("SELECT COUNT(*) as count FROM REVISION_CONTENIDO WHERE ESTADO = 'PENDIENTE'").first();
    const totalFB  = await c.env.DB.prepare("SELECT COUNT(*) as count FROM ARTICULOS_CMS WHERE FB_PUBLICADO = 1").first();
    const totalSites = await c.env.DB.prepare("SELECT COUNT(*) as count FROM SITIOS").first();

    return c.json({
      articles: totalPub ? totalPub.count : 0,
      drafts: totalCMS ? totalCMS.count : 0,
      pending: totalRev ? totalRev.count : 0,
      facebook: totalFB ? totalFB.count : 0,
      sites: totalSites ? totalSites.count : 0
    });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// GET /api/articles/id/:id - obtener artículo por ID
app.get('/articles/id/:id', async (c) => {
  const id = c.req.param('id');
  try {
    // Buscar en ARTICULOS_PARAFRASEADOS
    const rowPara = await c.env.DB.prepare(
      "SELECT *, 'PARAFRASEADO' as SOURCE_TABLE FROM ARTICULOS_PARAFRASEADOS WHERE ID = ? LIMIT 1"
    ).bind(id).first();
    if (rowPara) return c.json({ article: parseArticleRow(rowPara) });
    
    // Buscar en ARTICULOS_CMS
    const rowCMS = await c.env.DB.prepare(
      "SELECT *, 'CMS' as SOURCE_TABLE FROM ARTICULOS_CMS WHERE ID = ? LIMIT 1"
    ).bind(id).first();
    if (rowCMS) {
      return c.json({
        article: {
          id: rowCMS.ID,
          title: rowCMS.TITULO,
          slug: rowCMS.SLUG,
          content: rowCMS.CONTENIDO,
          excerpt: rowCMS.DESCRIPCION,
          category: rowCMS.CATEGORIA,
          author: rowCMS.AUTOR || 'Redacción CMS',
          publishedAt: rowCMS.FECHA_PUBLICACION,
          imageUrl: rowCMS.URL_IMAGEN,
          featured: Boolean(rowCMS.DESTACADO || 0),
          site: rowCMS.SITIOS_DESTINO,
          status: rowCMS.ESTADO,
          sourceTable: 'CMS'
        }
      });
    }
    
    return c.json({ error: 'Artículo no encontrado' }, 404);
  } catch (e) {
    console.error('Error fetching article by id:', e);
    return c.json({ error: e.message }, 500);
  }
});

// PUT /api/articles/:id - actualizar artículo publicado
app.put('/articles/:id', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  
  const id = c.req.param('id');
  try {
    const body = await c.req.json();
    const { 
      title, slug, content, excerpt, category, author, 
      imageUrl, featured, site, status 
    } = body;
    
    if (!title) {
      return c.json({ error: 'Título requerido' }, 400);
    }
    
    const articleSlug = slug || slugify(title);
    const now = new Date().toISOString();
    
    // Intentar actualizar en ARTICULOS_PARAFRASEADOS primero
    const existingPara = await c.env.DB.prepare(
      'SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE ID = ?'
    ).bind(id).first();
    
    if (existingPara) {
      await c.env.DB.prepare(`
        UPDATE ARTICULOS_PARAFRASEADOS SET
          TITULO_PARAFRASEADO = ?,
          SLUG = ?,
          CONTENIDO = ?,
          DESCRIPCION_PARAFRASEADA = ?,
          CATEGORIA = ?,
          AUTOR = ?,
          FECHA_PUBLICACION = ?,
          URL_IMAGEN = ?,
          SITIO_DESTINO = ?,
          DESTACADO = ?
        WHERE ID = ?
      `).bind(
        title,
        articleSlug,
        content || '',
        excerpt || '',
        (category || 'NACIONAL').toUpperCase(),
        author || 'Redacción',
        now,
        imageUrl || '',
        site || '',
        featured ? 1 : 0,
        id
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
          TITULO = ?,
          SLUG = ?,
          CONTENIDO = ?,
          DESCRIPCION = ?,
          CATEGORIA = ?,
          URL_IMAGEN = ?,
          DESTACADO = ?,
          ESTADO = ?,
          FECHA_PUBLICACION = ?
        WHERE ID = ?
      `).bind(
        title,
        articleSlug,
        content || '',
        excerpt || '',
        (category || 'NACIONAL').toUpperCase(),
        imageUrl || '',
        featured ? 1 : 0,
        status || 'BORRADOR',
        now,
        id
      ).run();
      
      return c.json({ success: true, id, source: 'CMS' });
    }
    
    return c.json({ error: 'Artículo no encontrado' }, 404);
  } catch (e) {
    console.error('Error updating article:', e);
    return c.json({ error: e.message }, 500);
  }
});

// POST /api/articles - crear nuevo artículo publicado
app.post('/articles', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  
  try {
    const article = await c.req.json();
    
    // Validaciones
    if (!article.title || !article.content) {
      return c.json({ error: 'Título y contenido requeridos' }, 400);
    }

    const wordCount = article.content.trim().split(/\s+/).length;
    // Restricción eliminada
    
    const slug = article.slug || slugify(article.title);
    const now = new Date().toISOString();
    
    const articleId = crypto.randomUUID();

    const result = await c.env.DB.prepare(`
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

    return c.json({
      success: true,
      article: {
        id: articleId,
        slug,
        title: article.title,
        wordCount
      }
    });

  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

const slugify = (text) => {
  return text.toString().toLowerCase().trim()
    .replace(/[áàäâã]/g, 'a').replace(/[éèëê]/g, 'e').replace(/[íìïî]/g, 'i')
    .replace(/[óòöôõ]/g, 'o').replace(/[úùüû]/g, 'u').replace(/[ñ]/g, 'n')
    .replace(/[ç]/g, 'c').replace(/[ý]/g, 'y')
    .replace(/\s+/g, '-').replace(/[^\w\-]+/g, '').replace(/\-\-+/g, '-')
    .replace(/^-+/, '').replace(/-+$/, '').substring(0, 100);
};

const parseArticleRow = (row) => {
  if (!row) return null;
  const category = row.CATEGORIA || row.category || 'General';
  return {
    id: row.ID || row.id,
    title: row.TITULO_PARAFRASEADO || row.TITULO || row.title || '',
    slug: row.slug || row.SLUG || slugify(row.TITULO_PARAFRASEADO || row.TITULO || 'articulo'),
    content: row.CONTENIDO || row.content || '',
    excerpt: row.DESCRIPCION_PARAFRASEADA || row.DESCRIPCION || row.excerpt || '',
    category: category,
    author: 'Redacción ' + category,
    publishedAt: row.FECHA_PUBLICACION || row.published_at || null,
    imageUrl: row.URL_IMAGEN || row.image_url || '',
    featured: Boolean(row.DESTACADO || row.featured || 0),
    site: row.SITIO_DESTINO || row.SITIOS_DESTINO || row.site || '',
    fb_published: Boolean(row.FB_PUBLICADO || 0)
  };
};

app.get('/articles', async (c) => {
  const { site, limit = 20, category } = c.req.query();
  const l = parseInt(limit);
  const MIN_ARTICLES = 8; // mínimo para llenar el layout

  try {
    const fetchArticles = async (siteFilter) => {
      const s = siteFilter ? `%${siteFilter}%` : '%';
      let queryPara = "SELECT *, 'PARAFRASEADO' as SOURCE_TABLE FROM ARTICULOS_PARAFRASEADOS WHERE SITIO_DESTINO LIKE ?";
      let paramsPara = [s];
      let queryCMS = "SELECT *, 'CMS' as SOURCE_TABLE FROM ARTICULOS_CMS WHERE ESTADO = 'PUBLICADO' AND SITIOS_DESTINO LIKE ?";
      let paramsCMS = [s];

      if (category) {
        queryPara += " AND LOWER(CATEGORIA) = LOWER(?)";
        paramsPara.push(category);
        queryCMS += " AND LOWER(CATEGORIA) = LOWER(?)";
        paramsCMS.push(category);
      }

      // Filtrar solo artículos con imágenes válidas para el index/listados
      queryPara += " AND URL_IMAGEN IS NOT NULL AND URL_IMAGEN != '' AND URL_IMAGEN NOT LIKE '%logo.png%'";
      queryCMS += " AND URL_IMAGEN IS NOT NULL AND URL_IMAGEN != '' AND URL_IMAGEN NOT LIKE '%logo.png%'";

      queryPara += " ORDER BY FECHA_PUBLICACION DESC LIMIT ?";
      paramsPara.push(l);
      queryCMS += " ORDER BY FECHA_PUBLICACION DESC LIMIT ?";
      paramsCMS.push(l);

      const [resPara, resCMS] = await Promise.all([
        c.env.DB.prepare(queryPara).bind(...paramsPara).all(),
        c.env.DB.prepare(queryCMS).bind(...paramsCMS).all()
      ]);

      return [...(resPara.results || []), ...(resCMS.results || [])]
        .map(parseArticleRow)
        .filter(Boolean)
        .sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt))
        .slice(0, l);
    };

    // 1. Obtener artículos del sitio específico
    let articles = site ? await fetchArticles(site) : await fetchArticles(null);

    // 2. Si hay menos del mínimo, complementar con artículos de todos los sitios
    if (site && articles.length < MIN_ARTICLES) {
      const allArticles = await fetchArticles(null);
      const existingIds = new Set(articles.map(a => a.id));
      const extras = allArticles.filter(a => !existingIds.has(a.id));
      articles = [...articles, ...extras].slice(0, l);
    }

    return c.json({ articles });
  } catch (e) {
    console.error('Error fetching articles:', e.message);
    return c.json({ articles: [] });
  }
});

// GET /api/articles/:slug — artículo individual por slug
app.get('/articles/:slug', async (c) => {
  const slug = c.req.param('slug');
  try {
    // 1. Buscar por columna SLUG exacta en ARTICULOS_PARAFRASEADOS
    const rowPara = await c.env.DB.prepare(
      "SELECT *, 'PARAFRASEADO' as SOURCE_TABLE FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? LIMIT 1"
    ).bind(slug).first();
    if (rowPara) return c.json({ article: parseArticleRow(rowPara) });

    // 2. Buscar en ARTICULOS_CMS por SLUG
    let rowCMS = null;
    try {
      rowCMS = await c.env.DB.prepare(
        "SELECT *, 'CMS' as SOURCE_TABLE FROM ARTICULOS_CMS WHERE ESTADO = 'PUBLICADO' AND SLUG = ? LIMIT 1"
      ).bind(slug).first();
    } catch (_) {}
    if (rowCMS) return c.json({ article: parseArticleRow(rowCMS) });

    // 3. Fallback: buscar en todos los artículos y comparar slug generado desde título
    //    (cubre artículos cuya columna SLUG es NULL)
    const allPara = await c.env.DB.prepare(
      "SELECT *, 'PARAFRASEADO' as SOURCE_TABLE FROM ARTICULOS_PARAFRASEADOS WHERE SLUG IS NULL ORDER BY FECHA_PUBLICACION DESC LIMIT 100"
    ).all();
    const matchPara = (allPara.results || []).find(r => {
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

// POST /api/articles/bulk — insertar múltiples artículos (para seed de noticias)
app.post('/articles/bulk', async (c) => {
  try {
    const body = await c.req.json();
    const { articles } = body;
    
    if (!Array.isArray(articles) || articles.length === 0) {
      return c.json({ error: 'Se requiere array de artículos' }, 400);
    }

    const results = [];
    const errors = [];

    for (const article of articles) {
      try {
        // Validar campos requeridos
        if (!article.title || !article.content || !article.category) {
          errors.push({ article: article.title || 'sin-titulo', error: 'Campos requeridos faltantes' });
          continue;
        }

        // Validar mínimo de palabras
        const wordCount = article.content.trim().split(/\s+/).length;
        // Restricción eliminada

        const slug = article.slug || slugify(article.title);
        const now = new Date().toISOString();
        
        // Insertar en ARTICULOS_PARAFRASEADOS
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
      success: true,
      inserted: results.length,
      errors: errors.length > 0 ? errors : undefined,
      total: articles.length
    });

  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// POST /api/articles — insertar artículo individual
app.post('/articles', async (c) => {
  try {
    const article = await c.req.json();
    
    // Validaciones
    if (!article.title || !article.content) {
      return c.json({ error: 'Título y contenido requeridos' }, 400);
    }

    const wordCount = article.content.trim().split(/\s+/).length;
    // Restricción eliminada

    const slug = slugify(article.title);
    const now = new Date().toISOString();

    const result = await c.env.DB.prepare(`
      INSERT INTO ARTICULOS_PARAFRASEADOS (
        TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA,
        CATEGORIA, AUTOR, FECHA_PUBLICACION, URL_IMAGEN, SITIO_DESTINO,
        DESTACADO, VISTAS, ESTADO
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      article.title,
      slug,
      article.content,
      article.excerpt || article.content.substring(0, 200) + '...',
      (article.category || 'NACIONAL').toUpperCase(),
      article.author || 'Redacción',
      article.publishedAt || now,
      article.imageUrl || '',
      article.sites || 'cbnnoticias',
      article.featured ? 1 : 0,
      0,
      'PUBLICADO'
    ).run();

    return c.json({
      success: true,
      article: {
        id: result.meta?.last_row_id,
        slug,
        title: article.title,
        wordCount
      }
    });

  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

app.get('/health', (c) => c.json({
  status: 'OK',
  timestamp: new Date().toISOString(),
  version: '2.0.0'
}));

// ============================================================
// IMAGENES - Servir imágenes desde R2
// ============================================================

// GET /api/images/:key — sirve imágenes almacenadas en R2
app.get('/images/*', async (c) => {
  const key = c.req.param('*');
  if (!key) return c.text('Not Found', 404);

  try {
    const object = await c.env.UPLOADS.get(key);
    if (!object) return c.text('Not Found', 404);

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    headers.set('X-Content-Type-Options', 'nosniff');

    return new Response(object.body, {
      status: 200,
      headers
    });
  } catch (e) {
    console.log('Image serve error:', e.message);
    return c.text('Not Found', 404);
  }
});

// POST /api/upload — sube imagen a R2 y devuelve URL
app.post('/upload', async (c) => {
  try {
    const formData = await c.req.formData();
    const file = formData.get('file');
    
    if (!file || !(file instanceof File)) {
      return c.json({ error: 'No file provided' }, 400);
    }

    // Validate file type is image
    const contentType = file.type;
    if (!contentType.startsWith('image/')) {
      return c.json({ error: 'File must be an image' }, 400);
    }

    // Determine extension from MIME type
    let ext = '.jpg';
    if (contentType.includes('png')) ext = '.png';
    else if (contentType.includes('gif')) ext = '.gif';
    else if (contentType.includes('webp')) ext = '.webp';

    const key = `uploads/${crypto.randomUUID()}${ext}`;
    const arrayBuffer = await file.arrayBuffer();

    // Upload to R2
    await c.env.UPLOADS.put(key, arrayBuffer, { httpMetadata: { contentType } });
    
    const imageUrl = `https://uploads.sebastianvernis.space/${key}`;
    return c.json({ success: true, url: imageUrl, key });
  } catch (e) {
    console.log('Upload error:', e.message);
    return c.json({ error: e.message }, 500);
  }
});
// ============================================================
// TICKER EN VIVO
// ============================================================

// GET /api/ticker/financials — datos financieros para el finance ticker
app.get('/ticker/financials', async (c) => {
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
    return c.json([], 200); // Retorna array vacío en caso de error (fallback a estáticos)
  }
});

// GET /api/ticker/headlines?limit=10 — titulares para el breaking news ticker
app.get('/ticker/headlines', async (c) => {
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

    return c.json(res.results || []);
  } catch (e) {
    return c.json([], 200); // Retorna array vacío en caso de error (fallback a estáticos)
  }
});

// POST /api/ticker/financials — upsert datos financieros (solo cron/admin)
app.post('/ticker/financials', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const items = await c.req.json(); // Array de { simbolo, nombre, valor, cambio, tendencia, unidad }
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

// POST /api/ticker/headlines — insertar titulares (solo cron/admin)
app.post('/ticker/headlines', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const items = await c.req.json(); // Array de { titulo, url, fuente }
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

// ============================================================
// CATEGORIES
// ============================================================
app.get('/categories', async (c) => {
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM CATEGORIAS WHERE ACTIVA = 1 ORDER BY NOMBRE'
    ).all();
    return c.json(res.results || []);
  } catch (e) { return c.json({ error: e.message }, 500); }
});

app.post('/categories', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const { nombre } = await c.req.json();
    if (!nombre) return c.json({ error: 'Nombre requerido' }, 400);
    const slug = slugify(nombre);
    await c.env.DB.prepare(
      'INSERT INTO CATEGORIAS (NOMBRE, SLUG, ACTIVA) VALUES (?, ?, 1)'
    ).bind(nombre.toUpperCase(), slug).run();
    return c.json({ success: true, slug });
  } catch (e) { return c.json({ error: e.message }, 500); }
});

// ============================================================
// CMS ARTICLES (Borradores internos)
// ============================================================
app.get('/cms/articles', async (c) => {
  try {
    const res = await c.env.DB.prepare(
      "SELECT * FROM ARTICULOS_CMS ORDER BY FECHA_CREACION DESC LIMIT 50"
    ).all();
    return c.json(res.results || []);
  } catch (e) { return c.json({ error: e.message }, 500); }
});

app.post('/cms/articles', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const body = await c.req.json();
    const { id, titulo, contenido, descripcion, categoria, url_imagen, destacado, estado } = body;
    if (!titulo) return c.json({ error: 'Título requerido' }, 400);

    const now = new Date().toISOString();
    const articleId = id || crypto.randomUUID();
    const slug = slugify(titulo);

    if (id) {
      await c.env.DB.prepare(`
        UPDATE ARTICULOS_CMS SET
          TITULO = ?, SLUG = ?, CONTENIDO = ?, DESCRIPCION = ?,
          CATEGORIA = ?, URL_IMAGEN = ?, DESTACADO = ?, ESTADO = ?
        WHERE ID = ?
      `).bind(
        titulo, slug, contenido || '', descripcion || '',
        (categoria || 'NACIONAL').toUpperCase(), url_imagen || '',
        destacado || 0, estado || 'BORRADOR', id
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

    return c.json({ success: true, id: articleId });
  } catch (e) { return c.json({ error: e.message }, 500); }
});

// Generar variaciones parafraseadas → Mesa de Revisión
app.post('/cms/generate-variations', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
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
          (ID_ORIGEN, TIPO_ORIGEN, TITULO_PROPUESTO, CONTENIDO_PROPUESTO, DESCRIPCION_PROPUESTA, SITIO_DESTINO, CATEGORIA, ESTADO, FECHA_CREACION)
        VALUES (?, 'CMS', ?, ?, ?, ?, ?, 'PENDIENTE', ?)
      `).bind(
        id, article.TITULO, article.CONTENIDO || '',
        article.DESCRIPCION || '', sitio,
        article.CATEGORIA || 'NACIONAL', now
      ).run();
    }

    return c.json({ success: true, variations: sitios.length });
  } catch (e) { return c.json({ error: e.message }, 500); }
});

// Publicar directamente desde CMS → ARTICULOS_PARAFRASEADOS
app.post('/cms/publish', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const { id, sitios, fb_requerido } = await c.req.json();
    if (!id || !Array.isArray(sitios) || sitios.length === 0) {
      return c.json({ error: 'ID y sitios requeridos' }, 400);
    }

    const article = await c.env.DB.prepare(
      'SELECT * FROM ARTICULOS_CMS WHERE ID = ?'
    ).bind(id).first();
    if (!article) return c.json({ error: 'Artículo no encontrado' }, 404);

    const now = new Date().toISOString();
    const baseSlug = article.SLUG || slugify(article.TITULO);
    const sitiosStr = sitios.join(',');

    // Solo permitir 'destacado' si hay una imagen válida
    const isFeatured = (article.DESTACADO || 0) === 1 && (article.URL_IMAGEN && article.URL_IMAGEN.trim() !== '');

    // Marcar CMS como publicado y guardar intención de FB
    await c.env.DB.prepare(
      "UPDATE ARTICULOS_CMS SET ESTADO = 'PUBLICADO', SITIOS_DESTINO = ?, FECHA_PUBLICACION = ?, FB_REQUERIDO = ?, DESTACADO = ? WHERE ID = ?"
    ).bind(sitiosStr, now, fb_requerido ? 1 : 0, isFeatured ? 1 : 0, id).run();

    // Insertar un ÚNICO registro en ARTICULOS_PARAFRASEADOS con todos los sitios
    const paraId = crypto.randomUUID();
    await c.env.DB.prepare(`
      INSERT INTO ARTICULOS_PARAFRASEADOS
        (ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA, CATEGORIA, AUTOR, FECHA_PUBLICACION, URL_IMAGEN, SITIO_DESTINO, DESTACADO, VISTAS, ESTADO)
      VALUES (?, ?, ?, ?, ?, ?, 'Redacción CMS', ?, ?, ?, ?, 0, 'PUBLICADO')
    `).bind(
      paraId, article.TITULO, baseSlug,
      article.CONTENIDO || '', article.DESCRIPCION || '',
      (article.CATEGORIA || 'NACIONAL').toUpperCase(), now,
      article.URL_IMAGEN || '', sitiosStr, isFeatured ? 1 : 0
    ).run();

    return c.json({ success: true, published: 1, siteCount: sitios.length });
  } catch (e) { return c.json({ error: e.message }, 500); }
});

// ============================================================
// MESA DE REVISIÓN
// ============================================================
app.get('/revision/pending', async (c) => {
  try {
    const res = await c.env.DB.prepare(
      "SELECT * FROM REVISION_CONTENIDO WHERE ESTADO IN ('PENDIENTE','CORREGIDO') ORDER BY FECHA_CREACION DESC LIMIT 50"
    ).all();
    return c.json(res.results || []);
  } catch (e) { return c.json({ error: e.message }, 500); }
});

app.put('/revision/:id', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const id = c.req.param('id');
    const { titulo, descripcion, contenido, url_imagen } = await c.req.json();

    // Intentar actualizar columna URL_IMAGEN si existe, si no, ignorar o alterar tabla
    try {
      await c.env.DB.prepare(`
        UPDATE REVISION_CONTENIDO SET
          TITULO_PROPUESTO = ?, DESCRIPCION_PROPUESTA = ?, CONTENIDO_PROPUESTO = ?, URL_IMAGEN = ?, ESTADO = 'CORREGIDO'
        WHERE ID = ?
      `).bind(titulo, descripcion || '', contenido, url_imagen || '', id).run();
    } catch (e) {
      // Fallback si la columna no existe aún en REVISION_CONTENIDO
      await c.env.DB.prepare(`
        UPDATE REVISION_CONTENIDO SET
          TITULO_PROPUESTO = ?, DESCRIPCION_PROPUESTA = ?, CONTENIDO_PROPUESTO = ?, ESTADO = 'CORREGIDO'
        WHERE ID = ?
      `).bind(titulo, descripcion || '', contenido, id).run();
    }

    return c.json({ success: true });
  } catch (e) { return c.json({ error: e.message }, 500); }
});

// GET /api/articles/timeline - Obtener noticias breves (Timeline)
app.get('/articles/timeline', async (c) => {
  const { site, limit = 20 } = c.req.query();
  try {
    const s = site ? `%${site}%` : '%';
    const res = await c.env.DB.prepare(
      "SELECT * FROM ARTICULOS_PARAFRASEADOS WHERE ES_BREVE = 1 AND SITIO_DESTINO LIKE ? ORDER BY FECHA_PUBLICACION DESC LIMIT ?"
    ).bind(s, parseInt(limit)).all();
    return c.json({ articles: (res.results || []).map(parseArticleRow) });
  } catch (e) { return c.json({ error: e.message }, 500); }
});

app.post('/revision/approve/:id', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const id = c.req.param('id');

    const rev = await c.env.DB.prepare(
      'SELECT * FROM REVISION_CONTENIDO WHERE ID = ?'
    ).bind(id).first();
    if (!rev) return c.json({ error: 'Revisión no encontrada' }, 404);

    const now = new Date().toISOString();
    const slug = slugify(rev.TITULO_PROPUESTO || 'articulo');
    const paraId = crypto.randomUUID();

    // Solo permitir 'destacado' si hay una imagen válida
    const isFeatured = (rev.DESTACADO || 0) === 1 && (rev.URL_IMAGEN && rev.URL_IMAGEN.trim() !== '');

    // Normalizar sitios (asegurar formato coma-separado)
    let sitiosStr = rev.SITIO_DESTINO || '';
    if (sitiosStr.startsWith('[')) {
      try { sitiosStr = JSON.parse(sitiosStr).join(','); } catch(e) {}
    }

    // Publicar en ARTICULOS_PARAFRASEADOS (con ES_BREVE)
    await c.env.DB.prepare(`
      INSERT INTO ARTICULOS_PARAFRASEADOS
        (ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA, CATEGORIA, AUTOR, FECHA_PUBLICACION, SITIO_DESTINO, DESTACADO, VISTAS, ESTADO, URL_IMAGEN, FB_REQUERIDO, ES_BREVE)
      VALUES (?, ?, ?, ?, ?, ?, 'Mesa de Revisión', ?, ?, ?, 0, 'PUBLICADO', ?, ?, ?)
    `).bind(
      paraId, rev.TITULO_PROPUESTO, slug,
      rev.CONTENIDO_PROPUESTO || '', rev.DESCRIPCION_PROPUESTA || '',
      (rev.CATEGORIA || 'NACIONAL').toUpperCase(), now, sitiosStr,
      isFeatured ? 1 : 0, rev.URL_IMAGEN || '', rev.FB_REQUERIDO || 0, rev.ES_BREVE || 0
    ).run();

    // Marcar revisión como aprobada
    await c.env.DB.prepare(
      "UPDATE REVISION_CONTENIDO SET ESTADO = 'APROBADO' WHERE ID = ?"
    ).bind(id).run();

    return c.json({ success: true, articleId: paraId });
  } catch (e) { return c.json({ error: e.message }, 500); }
});

// ============================================================
// WEATHER — OpenWeatherMap (free tier)
// ============================================================
app.get('/weather', async (c) => {
  try {
    const apiKey = c.env.OPENWEATHER_API_KEY;
    if (!apiKey) {
      // Sin API key: devuelve valores por defecto realistas para hoy (CDMX)
      return c.json({ 
        city: 'CDMX', 
        temp: 24, 
        icon: '01d', 
        condition: 'Despejado', 
        description: 'cielo despejado',
        humidity: 30,
        wind: 12
      });
    }

    // Parámetros opcionales de ubicación (por defecto: Ciudad de México)
    const lat   = c.req.query('lat') || '19.4326';
    const lon   = c.req.query('lon') || '-99.1332';
    const units = 'metric'; // Celsius

    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&units=${units}&appid=${apiKey}&lang=es`;
    const res = await fetch(url);

    if (!res.ok) {
      console.error(`OpenWeather HTTP ${res.status}`);
      return c.json({ city: 'CDMX', temp: 22, icon: '01d', condition: 'Clear' });
    }

    const data = await res.json();
    return c.json({
      city:        data.name          || 'CDMX',
      temp:        Math.round(data.main?.temp ?? 22),
      icon:        data.weather?.[0]?.icon        || '01d',
      condition:   data.weather?.[0]?.main        || 'Clear',
      description: data.weather?.[0]?.description || '',
      humidity:    data.main?.humidity            || null,
      wind:        data.wind?.speed               || null
    });
  } catch (e) {
    console.error('Weather API error:', e.message);
    return c.json({ city: 'CDMX', temp: 22, icon: '01d', condition: 'Clear' });
  }
});

// ============================================================
// SITES (Gestión de Red)
// ============================================================
app.get('/sites', async (c) => {
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM SITIOS ORDER BY NOMBRE'
    ).all();
    return c.json(res.results || []);
  } catch (e) { return c.json({ error: e.message }, 500); }
});

app.post('/sites', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  try {
    const body = await c.req.json();
    const { id, nombre, dominio, tagline, activo } = body;
    if (!nombre || !dominio) return c.json({ error: 'Nombre y dominio requeridos' }, 400);

    const siteId = id || crypto.randomUUID();
    const slug = slugify(nombre);

    await c.env.DB.prepare(`
      INSERT INTO SITIOS (ID, SLUG, NOMBRE, DOMINIO, TAGLINE, ACTIVO)
      VALUES (?, ?, ?, ?, ?, ?)
      ON CONFLICT(ID) DO UPDATE SET
        NOMBRE = excluded.NOMBRE, DOMINIO = excluded.DOMINIO,
        TAGLINE = excluded.TAGLINE, ACTIVO = excluded.ACTIVO
    `).bind(siteId, slug, nombre, dominio, tagline || '', activo ? 1 : 0).run();

    return c.json({ success: true, id: siteId });
  } catch (e) { return c.json({ error: e.message }, 500); }
});

app.get('/sites/legals/:id', async (c) => {
  const id = c.req.param('id');
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM LEGALES WHERE ID_SITIO = ?'
    ).bind(id).first();
    return c.json(res || {});
  } catch (e) { return c.json({ error: e.message }, 500); }
});

app.get('/sites/channels/:id', async (c) => {
  const id = c.req.param('id');
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM CANALES_EXTERNOS WHERE ID_SITIO = ? AND ACTIVO = 1 ORDER BY ORDEN'
    ).bind(id).all();
    return c.json(res.results || []);
  } catch (e) { return c.json({ error: e.message }, 500); }
});

app.get('/sites/menus/:id', async (c) => {
  const id = c.req.param('id');
  try {
    const res = await c.env.DB.prepare(
      'SELECT * FROM MENUS_NAVEGACION WHERE ID_SITIO = ? AND ACTIVO = 1 ORDER BY ORDEN'
    ).bind(id).all();
    return c.json(res.results || []);
  } catch (e) { return c.json({ error: e.message }, 500); }
});

// ============================================================
// DELETE ARTICLE
// ============================================================
app.delete('/articles/:id', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  const id = c.req.param('id');
  try {
    // 1. Eliminar métricas primero (debido a FOREIGN KEY)
    await c.env.DB.prepare(
      'DELETE FROM METRICAS_CONTENIDO WHERE ID_ARTICULO_PARAFRASEADO = ?'
    ).bind(id).run();

    // 2. Eliminar de ARTICULOS_PARAFRASEADOS
    await c.env.DB.prepare(
      'DELETE FROM ARTICULOS_PARAFRASEADOS WHERE ID = ?'
    ).bind(id).run();

    // 3. También intentar eliminar de CMS si existe
    try {
      await c.env.DB.prepare(
        'DELETE FROM ARTICULOS_CMS WHERE ID = ?'
      ).bind(id).run();
    } catch (_) {}

    return c.json({ success: true });
  } catch (e) {
    console.error("Delete Error:", e.message);
    return c.json({ error: e.message }, 500);
  }
});

// ============================================================
// RSS FEED — RSS 2.0 optimizado para Buffer / Facebook
// ============================================================

// Mapa de sitios: slug → { nombre, tagline, dominio }
const SITES_CONFIG = {
  noticiasobjetivo:  { nombre: 'Noticias Objetivo',       tagline: 'La Verdad Sin Filtros',                dominio: 'https://www.noticiasobjetivo.click'  },
  mexicoinformado:   { nombre: 'México Informado',         tagline: 'Periodismo con Perspectiva',           dominio: 'https://www.mexicoinformado.lat'      },
  bitacoraurbana:    { nombre: 'Bitácora Urbana',          tagline: 'Crónicas de la ciudad',                dominio: 'https://www.bitacoraurbana.lat'       },
  nodoinformativo:   { nombre: 'Nodo Informativo',         tagline: 'El Centro de las Noticias',            dominio: 'https://www.nodoinformativo.lat'      },
  cbnnoticias:       { nombre: 'CBN Noticias',             tagline: 'Noticias con credibilidad',            dominio: 'https://www.cbnnoticias.click'        },
  centralmexico:     { nombre: 'Central México',           tagline: 'Noticias del Centro del País',         dominio: 'https://www.centralmexico.online'     },
  verticenoticias:   { nombre: 'Vértice Noticias',         tagline: 'Perspectivas Únicas',                  dominio: 'https://www.verticenoticias.today'    },
  radiocinconoticias:{ nombre: 'Radio Cinco Noticias',     tagline: 'Información en Tiempo Real',           dominio: 'https://www.radiocinconoticias.click' },
  reportecentralmx:  { nombre: 'Reporte Central MX',       tagline: 'Periodismo de Investigación',          dominio: 'https://www.reportecentral.site'      },
  tvmexico:          { nombre: 'TV México',                tagline: 'Noticias y Entretenimiento',           dominio: 'https://www.tvmexiconews.site'        },
};

// Escapa caracteres especiales XML
const xmlEsc = (str) => {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '<')
    .replace(/>/g, '>')
    .replace(/"/g, '"')
    .replace(/'/g, '&apos;');
};

// Convierte fecha ISO a RFC-822 (requerido por RSS)
const toRFC822 = (dateStr) => {
  try {
    return new Date(dateStr).toUTCString();
  } catch (_) {
    return new Date().toUTCString();
  }
};

// Genera el XML RSS 2.0 a partir de artículos y config del sitio
const buildRSSXml = (articles, siteConfig, feedUrl) => {
  const { nombre, tagline, dominio } = siteConfig;
  const lastBuild = articles.length > 0
    ? toRFC822(articles[0].publishedAt)
    : new Date().toUTCString();

  const items = articles.map(a => {
    const articleUrl = `${dominio}/articulo/index.html?slug=${encodeURIComponent(a.slug || '')}`;
    const imageUrl = a.imageUrl && a.imageUrl.startsWith('http') ? a.imageUrl : null;
    const enclosure = imageUrl
      ? `\n    <enclosure url="${xmlEsc(imageUrl)}" type="image/jpeg" length="0"/>`
      : '';

    return `
  <item>
    <title>${xmlEsc(a.title)}</title>
    <link>${xmlEsc(articleUrl)}</link>
    <description>${xmlEsc(a.excerpt || a.title)}</description>
    <pubDate>${toRFC822(a.publishedAt)}</pubDate>${enclosure}
  </item>`;
  }).join('');

  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>${xmlEsc(nombre)}</title>
    <description>${xmlEsc(tagline)}</description>
    <link>${dominio}</link>
    <feedUrl>${xmlEsc(feedUrl)}</feedUrl>
    <lastBuildDate>${lastBuild}</lastBuildDate>
    <language>es-MX</language>
    <ttl>60</ttl>
    ${items}
  </channel>
</rss>`;
};

// Función para obtener artículos desde DB para RSS
const fetchRSSArticles = async (db, siteSlug, limit = 20) => {
  try {
    const s = siteSlug ? `%${siteSlug}%` : '%';
    const queryPara = "SELECT ID, TITULO_PARAFRASEADO as TITULO, SLUG, DESCRIPCION_PARAFRASEADA as DESCRIPCION, FECHA_PUBLICACION, URL_IMAGEN, CATEGORIA, SITIO_DESTINO FROM ARTICULOS_PARAFRASEADOS WHERE SITIO_DESTINO LIKE ? ORDER BY FECHA_PUBLICACION DESC LIMIT ?";
    const paramsPara = [s, limit];
    const queryCMS = "SELECT ID, TITULO, SLUG, DESCRIPCION, FECHA_PUBLICACION, URL_IMAGEN, CATEGORIA, SITIOS_DESTINO FROM ARTICULOS_CMS WHERE ESTADO = 'PUBLICADO' AND SITIOS_DESTINO LIKE ? ORDER BY FECHA_PUBLICACION DESC LIMIT ?";
    const paramsCMS = [s, limit];

    const [resPara, resCMS] = await Promise.all([
      db.prepare(queryPara).bind(...paramsPara).all(),
      db.prepare(queryCMS).bind(...paramsCMS).all()
    ]);

    return [...(resPara.results || []), ...(resCMS.results || [])]
      .map(parseArticleRow)
      .filter(Boolean)
      .sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt))
      .slice(0, limit);
  } catch (e) { return []; }
};

// --- ENDPOINTS RSS ---
app.get('/rss/:site', async (c) => {
  const siteSlug = c.req.param('site').toLowerCase().trim();
  const siteConfig = SITES_CONFIG[siteSlug];
  if (!siteConfig) return c.text('404', 404);
  const feedUrl = `${siteConfig.dominio}/rss.xml`;
  const kvKey = `rss:${siteSlug}`;
  try {
    const cached = await c.env.ARTICLES_KV.get(kvKey);
    if (cached) return new Response(cached, { headers: { 'Content-Type': 'application/rss+xml' } });
  } catch (_) {}
  const articles = await fetchRSSArticles(c.env.DB, siteSlug, 20);
  const xml = buildRSSXml(articles, siteConfig, feedUrl);
  try { await c.env.ARTICLES_KV.put(kvKey, xml, { expirationTtl: 1800 }); } catch (_) {}
  return new Response(xml, { headers: { 'Content-Type': 'application/rss+xml' } });
});

app.get('/rss', async (c) => {
  const articles = await fetchRSSArticles(c.env.DB, null, 30);
  const xml = buildRSSXml(articles, { nombre: 'Red Noticias', tagline: 'En vivo', dominio: 'https://www.noticiasobjetivo.click' }, 'https://api.com/rss');
  return new Response(xml, { headers: { 'Content-Type': 'application/rss+xml' } });
});

// --- FACEBOOK & CRON ---
app.get('/facebook/debug-tokens', async (c) => {
  if (!checkAuth(c)) return c.json({ error: '401' }, 401);
  try {
    const sites = await c.env.DB.prepare("SELECT SLUG, FACEBOOK_TOKEN_SECRET, FACEBOOK_PAGE_ID FROM SITIOS").all();
    const report = (sites.results || []).map(s => ({
      slug: s.SLUG,
      token_key: s.FACEBOOK_TOKEN_SECRET,
      has_token: !!c.env[s.FACEBOOK_TOKEN_SECRET],
      has_page_id: !!s.FACEBOOK_PAGE_ID
    }));
    return c.json(report);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

app.post('/articles/publish-fb/:id', async (c) => {
  if (!checkAuth(c)) return c.json({ error: '401' }, 401);
  const id = c.req.param('id');
  
  // Marcar como requerido para el proceso de fondo
  await c.env.DB.prepare("UPDATE ARTICULOS_PARAFRASEADOS SET FB_REQUERIDO = 1, FB_PUBLICADO = 0 WHERE ID = ?").bind(id).run();
  await c.env.DB.prepare("UPDATE ARTICULOS_CMS SET FB_REQUERIDO = 1, FB_PUBLICADO = 0 WHERE ID = ?").bind(id).run();
  
  // Intentar publicación inmediata
  let report = null;
  const para = await c.env.DB.prepare("SELECT * FROM ARTICULOS_PARAFRASEADOS WHERE ID = ?").bind(id).first();
  if (para) {
    report = await publishToFB(c.env, para, 'PARA');
  } else {
    const cms = await c.env.DB.prepare("SELECT * FROM ARTICULOS_CMS WHERE ID = ?").bind(id).first();
    if (cms) report = await publishToFB(c.env, cms, 'CMS');
  }

  // Si hay otros pendientes en la cola, procesarlos en segundo plano
  if (c.executionCtx) c.executionCtx.waitUntil(processFB(c.env));
  
  return c.json({ success: true, report });
});

// Monitor de Facebook - lista artículos de CMS y Parafraseados con estado de FB
app.get('/facebook/monitor', async (c) => {
  try {
    // Obtener artículos de ARTICULOS_CMS
    const cmsArticles = await c.env.DB.prepare(`
      SELECT 
        ID,
        TITULO,
        SITIOS_DESTINO,
        FB_PUBLICADO,
        FB_FECHA,
        'CMS' as TIPO
      FROM ARTICULOS_CMS
      WHERE FB_REQUERIDO = 1 OR ESTADO = 'PUBLICADO'
      ORDER BY FECHA_PUBLICACION DESC
      LIMIT 50
    `).all();

    // Obtener artículos de ARTICULOS_PARAFRASEADOS
    const paraArticles = await c.env.DB.prepare(`
      SELECT 
        ID,
        TITULO_PARAFRASEADO as TITULO,
        SITIO_DESTINO as SITIOS_DESTINO,
        FB_PUBLICADO,
        FB_FECHA,
        'PARA' as TIPO
      FROM ARTICULOS_PARAFRASEADOS
      WHERE FB_REQUERIDO = 1
      ORDER BY FECHA_PUBLICACION DESC
      LIMIT 50
    `).all();

    // Combinar y formatear resultados
    const allArticles = [
      ...(cmsArticles.results || []),
      ...(paraArticles.results || [])
    ].sort((a, b) => {
      const dateA = new Date(a.FB_FECHA || a.FECHA_PUBLICACION || 0);
      const dateB = new Date(b.FB_FECHA || b.FECHA_PUBLICACION || 0);
      return dateB - dateA;
    }).slice(0, 50);

    return c.json(allArticles);
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

// Ruta para forzar ingesta manual (diagnóstico)
app.post('/cron/ingest', async (c) => {
  if (!checkAuth(c)) return c.json({ error: '401' }, 401);
  try {
    const count = await runRSSDirectIngest(c.env);
    return c.json({ success: true, count, message: `Ingesta completada: ${count} artículos.` });
  } catch (e) {
    return c.json({ success: false, error: e.message }, 500);
  }
});

async function processFB(env) {
  try {
    const cms = await env.DB.prepare("SELECT ID, TITULO, SLUG, SITIOS_DESTINO FROM ARTICULOS_CMS WHERE ESTADO = 'PUBLICADO' AND FB_REQUERIDO = 1 AND FB_PUBLICADO = 0 LIMIT 2").all();
    for (const a of (cms.results || [])) await publishToFB(env, a, 'CMS');
    
    // Solo publicar en FB si NO es una imagen de fallback (contiene unsplash)
    const para = await env.DB.prepare("SELECT ID, TITULO_PARAFRASEADO as TITULO, SLUG, SITIO_DESTINO as SITIOS_DESTINO FROM ARTICULOS_PARAFRASEADOS WHERE FB_REQUERIDO = 1 AND FB_PUBLICADO = 0 AND URL_IMAGEN NOT LIKE '%unsplash.com%' LIMIT 2").all();
    for (const a of (para.results || [])) await publishToFB(env, a, 'PARA');
  } catch (e) {
    console.log('processFB Error:', e.message);
  }
}

async function publishToFB(env, article, type) {
  const targetSites = article.SITIOS_DESTINO || article.SITIO_DESTINO;
  const title = article.TITULO || article.TITULO_PARAFRASEADO;
  
  if (!targetSites) return { error: "No target sites" };
  
  const slugs = targetSites.split(",").map(s => s.trim());
  const report = [];
  let successCount = 0;
  
  for (const slug of slugs) {
    try {
      const site = await env.DB.prepare("SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1").bind(slug).first();
      if (!site) { report.push({ slug, error: "Site not found or inactive" }); continue; }
      if (!site.FACEBOOK_PAGE_ID || !site.FACEBOOK_TOKEN_SECRET) { report.push({ slug, error: "Missing config" }); continue; }
      
      const token = env[site.FACEBOOK_TOKEN_SECRET];
      if (!token) { report.push({ slug, error: "Missing secret token" }); continue; }
      
      const domain = site.DOMINIO || `${slug}.pages.dev`;
      const url = `https://${domain}/articulo/?slug=${article.SLUG}`;
      
      const formData = new URLSearchParams();
      formData.append('message', title);
      formData.append('link', url);
      formData.append('access_token', token);
      
      const response = await fetch(`https://graph.facebook.com/v19.0/${site.FACEBOOK_PAGE_ID}/feed`, {
        method: "POST",
        body: formData
      });
      
      const result = await response.json();
      if (response.ok) {
        report.push({ slug, success: true, id: result.id });
        successCount++;
      } else {
        report.push({ slug, success: false, error: result });
      }
    } catch (e) {
      report.push({ slug, success: false, error: e.message });
    }
  }
  
  if (successCount > 0) {
    const table = type === 'CMS' ? 'ARTICULOS_CMS' : 'ARTICULOS_PARAFRASEADOS';
    await env.DB.prepare(`UPDATE ${table} SET FB_PUBLICADO = 1, FB_FECHA = datetime('now') WHERE ID = ?`).bind(article.ID).run();
  }
  return { successCount, report };
}

// ============================================================
// AUTOMATION & CRON (PORTED FROM PYTHON FLOW)
// ============================================================

async function runRSSDirectIngest(env) {
  console.log('Cron: Starting RSS Ingest...');
  const FEEDS = [
    "https://elpais.com/rss/mexico/portada.xml",
    "https://www.proceso.com.mx/rss/feed.html?id=12",
    "https://aristeguinoticias.com/feed/",
    "https://www.animalpolitico.com/feed/",
  ];
  
  const SITIOS_LIST = [
    "radiocinconoticias", "centralmexico", "tvmexico", "cbnnoticias", 
    "mexicoinformado", "nodoinformativo", "bitacoraurbana", 
    "reportecentralmx", "verticenoticias", "noticiasobjetivo"
  ];

  let published = 0;
  for (const feedUrl of FEEDS) {
    if (published >= 5) break; // Limit per run to avoid timeouts
    try {
      const res = await fetch(feedUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
            const xml = await res.text();
            // Support both <item> (RSS) and <entry> (Atom)
            const items = xml.match(/<(item|entry)>([\s\S]*?)<\/\1>/g) || [];
            console.log(`Feed ${feedUrl}: Found ${items.length} items.`);
            
            for (const item of items) {
              if (published >= 5) break;
              
              // Match title and link for both RSS and Atom
              const titleMatch = item.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) || 
                                item.match(/<title>([\s\S]*?)<\/title>/);
              const linkMatch = item.match(/<link>([\s\S]*?)<\/link>/) || 
                               item.match(/<link[^>]+href=["']([^"']+)["']/);
              
              if (!titleMatch || !linkMatch) {
                console.log("Item skip: No title/link match");
                continue;
              }
              
              const title = titleMatch[1].trim();
              // Handle Atom link which might be in the href attribute or simple text
              let link = linkMatch[1].trim();
              if (linkMatch[0].includes('href=')) {
                 // It was an Atom-style link, we already have the URL in linkMatch[1]
              }
        
        // 1. Check if URL exists (Global)
        const urlExists = await env.DB.prepare("SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE SOURCE_URL = ?").bind(link).first();
        if (urlExists) {
          console.log(`Item skip: Already exists (${link.substring(0, 30)}...)`);
          continue;
        }

        // Scrape Image
        let imageUrl = await getOGImage(link);
        if (!imageUrl) {
          console.log(`Cron: No OG Image for ${link}, using fallback.`);
          imageUrl = "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1000&auto=format&fit=crop"; // Placeholder de noticias
        }

        console.log(`Cron: Processing literal article: ${title}`);
        
        // Extract content (simplified)
        let content = "";
        try {
          const pageRes = await fetch(link, { headers: { 'User-Agent': 'Mozilla/5.0' } });
          const html = await pageRes.text();
          const pMatches = html.match(/<p>([\s\S]*?)<\/p>/g) || [];
          content = pMatches.map(p => p.replace(/<[^>]*>/g, '').trim()).filter(p => p.length > 40).join('\n\n');
        } catch(e) { continue; }
        
        if (content.length < 300) continue;

        // Clean & Proofread
        let cleanTitle = title.includes(':') && title.split(':')[0].length < 30 ? title.split(':').slice(1).join(':').trim() : title;
        let cleanContent = content.replace(/Revista Proceso\s*[-–—]\s*Todos los derechos reservados\s*[-–—]\s*202\d/gi, '');
        
        // AI Proofread
        const aiTitle = await proofreadTextAI(cleanTitle, "título", env);
        const aiContent = await proofreadTextAI(cleanContent, "contenido", env);
        const aiDesc = aiContent.substring(0, 200);

        // Select Site
        const site = SITIOS_LIST[Math.floor(Math.random() * SITIOS_LIST.length)];

        // 2. Check if title or description exists FOR THIS SPECIFIC SITE
        const duplicateOnSite = await env.DB.prepare(`
          SELECT ID FROM ARTICULOS_PARAFRASEADOS 
          WHERE (TITULO_PARAFRASEADO = ? OR DESCRIPCION_PARAFRASEADA = ?) 
          AND SITIO_DESTINO LIKE ?
        `).bind(aiTitle, aiDesc, `%${site}%`).first();
        
        if (duplicateOnSite) {
          console.log(`Cron: Duplicate title/desc found for site ${site}, skipping.`);
          continue;
        }

        // Upload image to R2
        const finalImg = await uploadToR2(imageUrl, env);
        if (!finalImg) continue;

        const now = new Date().toISOString();
        const paraId = crypto.randomUUID();
        const slug = slugify(aiTitle);

        await env.DB.prepare(`
          INSERT INTO ARTICULOS_PARAFRASEADOS
            (ID, TITULO_PARAFRASEADO, SLUG, CONTENIDO, DESCRIPCION_PARAFRASEADA, CATEGORIA, AUTOR, FECHA_PUBLICACION, SITIO_DESTINO, DESTACADO, VISTAS, ESTADO, URL_IMAGEN, SOURCE_URL)
          VALUES (?, ?, ?, ?, ?, 'NACIONAL', ?, ?, ?, 1, 0, 'PUBLICADO', ?, ?)
        `).bind(paraId, aiTitle, slug, aiContent, aiDesc, `Redacción ${site}`, now, site, finalImg, link).run();
        
        published++;
      }
    } catch(e) { console.error(`Feed error ${feedUrl}:`, e.message); }
  }
  return published;
}

async function proofreadTextAI(text, role, env) {
  const token = env.OPENROUTER_API_KEY;
  if (!token) return text;
  
  const prompt = `Actúa como un corrector de estilo. Corrige ORTOGRAFÍA, PUNTUACIÓN y GRAMÁTICA en este ${role} en español. REGLAS: 1. No cambies estilo ni significado. 2. NO resumas ni trunques. 3. Elimina firmas editoriales (ej. Revista Proceso). Devuelve SOLO el texto corregido.\n\nTEXTO:\n${text}`;
  
  try {
    const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "google/gemini-2.0-flash-001",
        messages: [{ role: "user", content: prompt }],
        temperature: 0.1
      })
    });
    const data = await res.json();
    return data.choices[0].message.content.trim() || text;
  } catch(e) { return text; }
}

async function getOGImage(url) {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    const html = await res.text();
    const ogMatch = html.match(/<meta[^>]*property=["']og:image["'][^>]*content=["']([^"']+)["']/i) || 
                    html.match(/<meta[^>]*content=["']([^"']+)["'][^>]*property=["']og:image["']/i);
    return ogMatch ? ogMatch[1] : null;
  } catch(e) { return null; }
}

async function uploadToR2(url, env) {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) return null;
    const contentType = res.headers.get('content-type') || 'image/jpeg';
    const buffer = await res.arrayBuffer();
    const key = `auto/${crypto.randomUUID()}.jpg`;
    await env.UPLOADS.put(key, buffer, { httpMetadata: { contentType } });
    return `https://uploads.sebastianvernis.space/${key}`;
  } catch(e) { return null; }
}

async function updateTickerData(env) {
  const newsKey = env.NEWSAPI_KEY;
  if (newsKey) {
    try {
      const res = await fetch(`https://newsapi.org/v2/everything?q=mexico&language=es&sortBy=publishedAt&pageSize=15&apiKey=${newsKey}`);
      const data = await res.json();
      const now = new Date().toISOString();
      for (const art of (data.articles || [])) {
        await env.DB.prepare('INSERT INTO TICKER_HEADLINES (TITULO, URL, FUENTE, FECHA_CREACION) VALUES (?, ?, ?, ?)').bind(art.title, art.url, art.source.name, now).run();
      }
    } catch(e) {}
  }
  
  const financials = [
    {simbolo: "USD/MXN", nombre: "Dólar", valor: "18.45", cambio: "-0.12%", tendencia: "down"},
    {simbolo: "BTC/USD", nombre: "Bitcoin", valor: "96,420", cambio: "+2.4%", tendencia: "up"}
  ];
  const now = new Date().toISOString();
  for (const f of financials) {
    await env.DB.prepare(`INSERT INTO TICKER_FINANCIALS (SIMBOLO, NOMBRE, VALOR, CAMBIO, TENDENCIA, UNIDAD, FECHA_ACTUALIZACION) VALUES (?, ?, ?, ?, ?, 'MXN', ?) ON CONFLICT(SIMBOLO) DO UPDATE SET VALOR=excluded.VALOR, CAMBIO=excluded.CAMBIO, FECHA_ACTUALIZACION=excluded.FECHA_ACTUALIZACION`)
      .bind(f.simbolo, f.nombre, f.valor, f.cambio, f.tendencia, now).run();
  }
}

async function runMasterCron(env) {
  const now = Date.now();
  const status = { lastRun: new Date().toISOString(), tasks: {} };
  
  // 1. Ingest News
  try {
    const count = await runRSSDirectIngest(env);
    status.tasks.ingest = `OK (${count} articles)`;
  } catch(e) { status.tasks.ingest = `Error: ${e.message}`; }
  
  // 2. Ticker
  try { await updateTickerData(env); status.tasks.ticker = "OK"; } catch(e) { status.tasks.ticker = "Error"; }
  
  // 3. Facebook (Multi-Site Intelligent Flow)
  try {
    const SITIOS_LIST = [
      "radiocinconoticias", "centralmexico", "tvmexico", "cbnnoticias", 
      "mexicoinformado", "nodoinformativo", "bitacoraurbana", 
      "reportecentralmx", "verticenoticias", "noticiasobjetivo"
    ];

    for (const siteSlug of SITIOS_LIST) {
      const kvKey = `last_fb_post_${siteSlug}`;
      const lastFB = parseInt(await env.ARTICLES_KV.get(kvKey) || "0");
      
      if (now - lastFB >= 3 * 60 * 60 * 1000) {
        // Buscar el artículo más reciente para ESTE sitio que sea elegible (imagen perfecta)
        // Buscamos en ambas tablas (PARA y CMS)
        const query = `
          SELECT * FROM (
            SELECT ID, TITULO_PARAFRASEADO as TITULO, SLUG, SITIO_DESTINO as SITIOS_DESTINO, URL_IMAGEN, FECHA_PUBLICACION, 'PARA' as TIPO 
            FROM ARTICULOS_PARAFRASEADOS 
            WHERE FB_PUBLICADO = 0 AND SITIO_DESTINO LIKE ? AND URL_IMAGEN NOT LIKE '%unsplash.com%'
            UNION ALL
            SELECT ID, TITULO, SLUG, SITIOS_DESTINO, URL_IMAGEN, FECHA_PUBLICACION, 'CMS' as TIPO 
            FROM ARTICULOS_CMS 
            WHERE FB_PUBLICADO = 0 AND ESTADO = 'PUBLICADO' AND SITIOS_DESTINO LIKE ? AND URL_IMAGEN NOT LIKE '%unsplash.com%'
          ) 
          ORDER BY FECHA_PUBLICACION DESC LIMIT 5
        `;
        
        const possibleArticles = await env.DB.prepare(query).bind(`%${siteSlug}%`, `%${siteSlug}%`).all();
        const results = possibleArticles.results || [];
        
        if (results.length > 0) {
          // El primer resultado ya es el más reciente elegible debido al filtro NOT LIKE unsplash
          const art = results[0];
          await publishToFB(env, art, art.TIPO);
          await env.ARTICLES_KV.put(kvKey, now.toString());
          console.log(`[Cron-FB] Posted to ${siteSlug}: ${art.TITULO}`);
          status.tasks[`fb_${siteSlug}`] = `OK (${art.ID})`;
        } else {
          status.tasks[`fb_${siteSlug}`] = "No eligible articles found in window";
        }
      } else {
        const remaining = Math.round((3*60*60*1000 - (now - lastFB))/60000);
        status.tasks[`fb_${siteSlug}`] = `Waiting (${remaining} mins)`;
      }
    }
  } catch(e) { 
    console.error('MasterCron FB Error:', e.message);
    status.tasks.fb_global_error = e.message; 
  }
  
  await env.ARTICLES_KV.put("cron_status", JSON.stringify(status));
}

async function extractImageFromItem(itemXml) {
  // Try multiple patterns to extract image URL from RSS item
  const patterns = [
    // Media RSS (Yahoo) - most common
    /<media:content[^>]+url=["']([^"']+)["']/i,
    /<media:thumbnail[^>]+url=["']([^"']+)["']/i,
    /<media:content[^>]+url=['"]([^'"]+)['"]/i,
    // Enclosure tag
    /<enclosure[^>]+url=["']([^"']+)["'][^>]*type=["']image\/[^"']*["']/i,
    /<enclosure[^>]+type=["']image\/[^"']*["'][^>]*url=["']([^"']+)["']/i,
    /<enclosure[^>]+url=['"]([^'"]+)['"][^>]*type=['"]image\/[^'']*['"]/i,
    // IMG tag in content/description
    /<img[^>]+src=["']([^"']+)["']/i,
    /<img[^>]+src=['"]([^'"]+)['"]/i,
    // Figure with img
    /<figure[^>]*>[\s\S]*?<img[^>]+src=["']([^"']+)["']/i,
    // Content encoded HTML - look for img in CDATA
    /<img[^>]*src=["']([^"']+)["'][^>]*>/i,
  ];

  for (const pattern of patterns) {
    const match = itemXml.match(pattern);
    if (match && match[1]) {
      const imgUrl = match[1].trim();
      // Validate it looks like a valid image URL
      if (imgUrl.startsWith('http') &&
          !imgUrl.includes('placeholder') &&
          !imgUrl.includes('blank') &&
          !imgUrl.includes('spacer') &&
          !imgUrl.includes('/logo.png') &&
          !imgUrl.includes('logo_default') &&
          imgUrl.length > 30) { // URLs muy cortas suelen ser placeholders
        console.log('ExtractImage: Found via pattern', pattern.toString().substring(0, 50), '->', imgUrl.substring(0, 80));
        return imgUrl;
      }
    }
  }

  console.log('ExtractImage: No valid image found in item XML');
  return null;
}

async function scrapeImageFromUrl(url) {
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml'
      },
      cf: { cacheTtl: 3600 }
    });

    if (!res.ok) {
      console.log('ScrapeImage: HTTP error', res.status, url);
      return null;
    }

    const html = await res.text();

    // Try Open Graph image first (best quality)
    const ogMatch = html.match(/<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["']/i) ||
                    html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:image["']/i);
    if (ogMatch && ogMatch[1]) {
      const ogUrl = ogMatch[1];
      // Validate OG image is not a placeholder
      if (ogUrl.startsWith('http') &&
          !ogUrl.includes('placeholder') &&
          !ogUrl.includes('/logo.png') &&
          !ogUrl.includes('logo_default') &&
          !ogUrl.includes('blank') &&
          ogUrl.length > 30) {
        
        // Verify the image URL is accessible with HEAD request
        try {
          const imgCheck = await fetch(ogUrl, { method: 'HEAD' });
          if (!imgCheck.ok || imgCheck.status === 404) {
            console.log('ScrapeImage: og:image not accessible (HTTP ' + imgCheck.status + ')', ogUrl);
            return null;
          }
          const imgSize = imgCheck.headers.get('content-length') || '0';
          if (parseInt(imgSize) < 5000) { // Less than 5KB, probably a placeholder
            console.log('ScrapeImage: og:image too small (' + imgSize + ' bytes)', ogUrl);
            return null;
          }
          console.log('ScrapeImage: og:image verified (' + imgSize + ' bytes)', ogUrl.substring(0, 80));
          return ogUrl;
        } catch (e) {
          console.log('ScrapeImage: Error checking og:image', e.message);
          return null;
        }
      }
      console.log('ScrapeImage: og:image is placeholder, skipping');
    }

    // Try Twitter card image
    const twitterMatch = html.match(/<meta[^>]+name=["']twitter:image["'][^>]+content=["']([^"']+)["']/i);
    if (twitterMatch && twitterMatch[1]) {
      const twUrl = twitterMatch[1];
      if (twUrl.startsWith('http') &&
          !twUrl.includes('placeholder') &&
          !twUrl.includes('/logo.png') &&
          !twUrl.includes('logo_default') &&
          twUrl.length > 30) {
        
        // Verify accessibility
        try {
          const imgCheck = await fetch(twUrl, { method: 'HEAD' });
          if (imgCheck.ok && imgCheck.status !== 404) {
            console.log('ScrapeImage: twitter:image verified', twUrl.substring(0, 80));
            return twUrl;
          }
        } catch (e) {}
      }
    }

    console.log('ScrapeImage: No valid image found on page');
    return null;
  } catch (e) {
    console.log('ScrapeImage: Error', e.message);
    return null;
  }
}

async function autoIngestNews(env, hour) {
  try {
    const FEEDS = [
      "https://www.jornada.com.mx/rss/politica.xml?v=1",
      "https://expansion.mx/rss",
      "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada"
    ];
    let art = null;
    
    for (const f of FEEDS) {
      try {
        const r = await fetch(f, { 
          headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' },
          cf: { cacheTtl: 300 }
        });
        if (!r.ok) continue;
        
        const x = await r.text();
        const items = x.match(/<item>([\s\S]*?)<\/item>/g) || [];
        
        for (const i of items) {
          // Extract title - try CDATA first, then plain text
          const titleMatch = i.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) || 
                            i.match(/<title>([\s\S]*?)<\/title>/);
          if (!titleMatch) continue;
          
          const title = titleMatch[1].trim();
          
          // Check if article already exists
          const exist = await env.DB.prepare("SELECT ID FROM ARTICULOS_ORIGINALES WHERE TITULO = ?").bind(title).first();
          if (!exist) {
            // Extract link
            const linkMatch = i.match(/<link>([\s\S]*?)<\/link>/);
            if (!linkMatch) continue;
            const link = linkMatch[1].trim();
            
            // Extract description
            const descMatch = i.match(/<description><!\[CDATA\[([\s\S]*?)\]\]><\/description>/) || 
                             i.match(/<description>([\s\S]*?)<\/description>/);
            const desc = descMatch ? descMatch[1].trim().replace(/<[^>]*>/g, '') : "";
            
            // Extract image using enhanced extraction
            const imgUrl = await extractImageFromItem(i);
            
            art = { title, link, desc, img: imgUrl };
            console.log('AutoIngest: Found article', title.substring(0, 50), 'Image:', imgUrl);
            break;
          }
        }
      } catch (e) {
        console.log('AutoIngest: Feed error', f, e.message);
      }
      if (art) break;
    }
    
    if (!art) {
      console.log('AutoIngest: No new articles found');
      return false;
    }
    
    // Mirror image to R2 - with retry logic
    let mirImg = null;
    if (art.img) {
      // First, validate the image URL is valid (not a placeholder)
      const isValidImage = art.img && 
                           art.img.startsWith('http') && 
                           !art.img.includes('/logo.png') && 
                           !art.img.includes('placeholder') &&
                           !art.img.includes('blank');
      
      if (isValidImage) {
        mirImg = await mirrorImageToR2(art.img, env);
        if (!mirImg) {
          // Mirroring failed, keep original URL only if it's valid
          if (art.img.startsWith('http')) {
            mirImg = art.img;
            console.log('AutoIngest: Mirror failed, using original URL', art.img);
          }
        }
      }
    }
    
    // If still no image, try scraping from article URL
    if (!mirImg && art.link) {
      console.log('AutoIngest: Scraping image from article URL:', art.link);
      const scrapedImg = await scrapeImageFromUrl(art.link);
      if (scrapedImg) {
        mirImg = await mirrorImageToR2(scrapedImg, env);
        // If mirror fails, use scraped URL as fallback
        if (!mirImg && scrapedImg.startsWith('http')) {
          mirImg = scrapedImg;
        }
        console.log('AutoIngest: Scraped image result:', mirImg ? 'SUCCESS' : 'FAILED');
      }
    }
    
    if (!mirImg) {
      console.log('AutoIngest: No image available for article:', art.title.substring(0, 50));
    }
    
    const id = crypto.randomUUID();
    
    // Insert into ARTICULOS_ORIGINALES
    await env.DB.prepare(
      "INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, DESCRIPCION, URL_IMAGEN, FECHA, CONTENIDO, CATEGORIA, LONGITUD) VALUES (?,?,?,?,?,datetime('now'),?,'NACIONAL',?)"
    ).bind(id, art.link, art.title, art.desc, mirImg, art.desc, art.desc.length).run();
    
    // Insert into REVISION_CONTENIDO for editorial review
    await env.DB.prepare(
      "INSERT INTO REVISION_CONTENIDO (ID_ORIGEN, TIPO_ORIGEN, TITULO_PROPUESTO, CONTENIDO_PROPUESTO, DESCRIPCION_PROPUESTA, SITIO_DESTINO, CATEGORIA, ESTADO, URL_IMAGEN, FB_REQUERIDO, ES_BREVE) VALUES (?, 'API', ?, ?, ?, 'bitacoraurbana,nodoinformativo', 'NACIONAL', 'PENDIENTE', ?, 0, 0)"
    ).bind(id, art.title, art.desc, art.title, mirImg).run();
    
    console.log('AutoIngest: Successfully ingested article', id, 'Image:', mirImg);
    return true;
  } catch (e) { 
    console.log('AutoIngest: Error', e.message);
    return false; 
  }
}

async function injectMetaTags(request, env, response) {
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');
  if (!slug || !url.pathname.includes('/articulo')) return response;
  try {
    // Intentar obtener de ARTICULOS_PARAFRASEADOS primero
    let article = await env.DB.prepare("SELECT TITULO_PARAFRASEADO as t, DESCRIPCION_PARAFRASEADA as d, URL_IMAGEN as i FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? LIMIT 1").bind(slug).first();
    
    // Si no, intentar con ARTICULOS_CMS
    if (!article) {
      article = await env.DB.prepare("SELECT TITULO as t, DESCRIPCION as d, URL_IMAGEN as i FROM ARTICULOS_CMS WHERE SLUG = ? LIMIT 1").bind(slug).first();
    }
    
    if (!article) return response;
    
    // Determinar imagen para OG
    let ogImg = `${url.origin}/logo.png`; // Default fallback
    
    if (article.i) {
      // Si la imagen empieza con /api/images/, es de R2 → construir URL completa
      if (article.i.startsWith('/api/images/')) {
        ogImg = `${url.origin}${article.i}`;
      }
      // Si es URL absoluta válida, usarla directamente
      else if (article.i.startsWith('http') && 
               !article.i.includes('/logo.png') && 
               !article.i.includes('placeholder')) {
        ogImg = article.i;
      }
    }
    
    console.log('OG Image for', slug, ':', ogImg);
    
    return new HTMLRewriter()
      .on('title', { element(el) { el.setInnerContent(article.t); } })
      .on('head', {
        element(el) {
          el.prepend(`<meta property="og:title" content="${article.t}" /><meta property="og:description" content="${article.d}" /><meta property="og:image" content="${ogImg}" /><meta property="og:type" content="article" /><meta name="twitter:card" content="summary_large_image" />`, { html: true });
        }
      }).transform(response);
  } catch (e) { 
    console.log('injectMetaTags error:', e.message);
    return response; 
  }
}

// ============================================================
// UTILS - Limpieza y mantenimiento
// ============================================================

// POST /admin/cleanup-duplicates - Elimina duplicados usando INSERT OR REPLACE
app.post('/admin/cleanup-duplicates', async (c) => {
  if (!checkAuth(c)) return c.json({ error: 'Unauthorized' }, 401);
  
  try {
    // Paso 1: Obtener artículos únicos (mejor imagen + más reciente)
    const allArticles = await c.env.DB.prepare(`
      SELECT ID, TITULO, URL_IMAGEN, FECHA, DESCRIPCION, CONTENIDO, CATEGORIA, LONGITUD
      FROM ARTICULOS_ORIGINALES 
      ORDER BY TITULO, FECHA DESC
    `).all();
    
    const byTitle = new Map();
    for (const article of (allArticles.results || [])) {
      if (!byTitle.has(article.TITULO)) byTitle.set(article.TITULO, []);
      byTitle.get(article.TITULO).push({
        ...article,
        hasValidImage: article.URL_IMAGEN && article.URL_IMAGEN !== '' && !article.URL_IMAGEN.includes('/logo.png')
      });
    }
    
    // Seleccionar mejores
    const articlesToKeep = [];
    let duplicatesCount = 0;
    
    for (const [titulo, items] of byTitle.entries()) {
      if (items.length > 1) duplicatesCount++;
      items.sort((a, b) => {
        if (a.hasValidImage && !b.hasValidImage) return -1;
        if (!a.hasValidImage && b.hasValidImage) return 1;
        return new Date(b.fecha || 0) - new Date(a.fecha || 0);
      });
      articlesToKeep.push(items[0]);
    }
    
    const originalCount = allArticles.results?.length || 0;
    const newCount = articlesToKeep.length;
    
    if (originalCount === newCount) {
      return c.json({ success: true, message: 'No hay duplicados', originalCount, newCount });
    }
    
    // Paso 2: Crear nueva tabla SIN foreign keys
    const backupId = Date.now();
    await c.env.DB.prepare(`
      CREATE TABLE ARTICULOS_ORIGINALES_NEW (
        ID TEXT PRIMARY KEY,
        TITULO TEXT NOT NULL,
        URL_IMAGEN TEXT,
        FECHA TEXT,
        DESCRIPCION TEXT,
        CONTENIDO TEXT,
        CATEGORIA TEXT,
        LONGITUD INTEGER
      )
    `).run();
    
    // Paso 3: Insertar solo los que queremos conservar
    const insertStmt = c.env.DB.prepare(`
      INSERT OR REPLACE INTO ARTICULOS_ORIGINALES_NEW 
      (ID, TITULO, URL_IMAGEN, FECHA, DESCRIPCION, CONTENIDO, CATEGORIA, LONGITUD)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);
    
    for (const article of articlesToKeep) {
      await insertStmt.bind(
        article.ID, article.TITULO, article.URL_IMAGEN, article.FECHA,
        article.DESCRIPCION, article.CONTENIDO, article.CATEGORIA, article.LONGITUD
      ).run();
    }
    
    // Paso 4: Renombrar tablas (DROP old, rename new)
    await c.env.DB.prepare(`ALTER TABLE ARTICULOS_ORIGINALES RENAME TO ARTICULOS_ORIGINALES_OLD`).run();
    await c.env.DB.prepare(`ALTER TABLE ARTICULOS_ORIGINALES_NEW RENAME TO ARTICULOS_ORIGINALES`).run();
    
    // Paso 5: Recrear índice
    await c.env.DB.prepare(`CREATE INDEX IF NOT EXISTS idx_art_orig_url ON ARTICULOS_ORIGINALES(URL)`).run();
    
    // Paso 6: Verificar
    const remaining = await c.env.DB.prepare(`
      SELECT COUNT(*) as count FROM (
        SELECT TITULO FROM ARTICULOS_ORIGINALES GROUP BY TITULO HAVING COUNT(*) > 1
      )
    `).first();
    
    const finalCount = (await c.env.DB.prepare("SELECT COUNT(*) as c FROM ARTICULOS_ORIGINALES").first()).c;
    
    return c.json({
      success: true,
      message: 'Limpieza completada',
      originalCount,
      newCount: finalCount,
      deleted: originalCount - finalCount,
      duplicatesFound: duplicatesCount,
      remainingDuplicates: remaining.count || 0,
      oldTablePreserved: 'ARTICULOS_ORIGINALES_OLD (puedes eliminarla manualmente)'
    });
  } catch (e) {
    return c.json({ error: e.message }, 500);
  }
});

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/api/cron/manual') { await runMasterCron(env); return new Response("OK"); }
    if (url.pathname === '/api/cron/status') { 
      const s = await env.ARTICLES_KV.get("cron_status"); 
      const data = s ? JSON.parse(s) : { lastRun: "Never" };
      
      // Calcular tiempo para la siguiente (intervalo 30 min)
      if (data.lastRun !== "Never") {
        const lastTs = new Date(data.lastRun).getTime();
        const nextTs = lastTs + (30 * 60 * 1000);
        const diff = Math.max(0, nextTs - Date.now());
        data.nextRunInMinutes = Math.floor(diff / 60000);
        data.nextRunInSeconds = Math.floor((diff % 60000) / 1000);
      }
      
      return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } }); 
    }
    if (url.pathname.startsWith('/api')) return app.fetch(request, env, ctx);
    const originalRes = await fetch(request);
    return injectMetaTags(request, env, originalRes);
  },
  async scheduled(event, env, ctx) { ctx.waitUntil(runMasterCron(env)); }
};
