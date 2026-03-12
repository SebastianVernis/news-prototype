// src/routes/rss.js — Feeds RSS 2.0 por sitio y global

import { Hono } from 'hono';
import { parseArticleRow } from '../utils/helpers.js';
import { SITES_CONFIG } from '../config.js';

const rss = new Hono();

// ── Helpers RSS ───────────────────────────────────────────────

// Escapa caracteres especiales XML
const xmlEsc = (str) => {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
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

  const items = articles.map((a) => {
    const articleUrl = `${dominio}/articulo/index.html?slug=${encodeURIComponent(a.slug || '')}`;
    const imageUrl   = a.imageUrl && a.imageUrl.startsWith('http') ? a.imageUrl : null;
    const enclosure  = imageUrl
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

// Obtiene artículos desde DB para RSS
const fetchRSSArticles = async (db, siteSlug, limit = 20) => {
  try {
    const s         = siteSlug ? `%${siteSlug}%` : '%';
    const queryPara = 'SELECT ID, TITULO_PARAFRASEADO as TITULO, SLUG, DESCRIPCION_PARAFRASEADA as DESCRIPCION, FECHA_PUBLICACION, URL_IMAGEN, CATEGORIA, SITIO_DESTINO FROM ARTICULOS_PARAFRASEADOS WHERE SITIO_DESTINO LIKE ? ORDER BY FECHA_PUBLICACION DESC LIMIT ?';
    const queryCMS  = "SELECT ID, TITULO, SLUG, DESCRIPCION, FECHA_PUBLICACION, URL_IMAGEN, CATEGORIA, SITIOS_DESTINO FROM ARTICULOS_CMS WHERE ESTADO = 'PUBLICADO' AND SITIOS_DESTINO LIKE ? ORDER BY FECHA_PUBLICACION DESC LIMIT ?";

    const [resPara, resCMS] = await Promise.all([
      db.prepare(queryPara).bind(s, limit).all(),
      db.prepare(queryCMS).bind(s, limit).all(),
    ]);

    return [...(resPara.results || []), ...(resCMS.results || [])]
      .map(parseArticleRow)
      .filter(Boolean)
      .sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt))
      .slice(0, limit);
  } catch (_) {
    return [];
  }
};

// ── GET /rss/:site — Feed RSS de un sitio específico ─────────
rss.get('/:site', async (c) => {
  const siteSlug  = c.req.param('site').toLowerCase().trim();
  const siteConfig = SITES_CONFIG[siteSlug];
  if (!siteConfig) return c.text('404', 404);

  const feedUrl = `${siteConfig.dominio}/rss.xml`;
  const kvKey   = `rss:${siteSlug}`;

  // Intentar servir desde caché KV
  try {
    const cached = await c.env.ARTICLES_KV.get(kvKey);
    if (cached) {
      return new Response(cached, { headers: { 'Content-Type': 'application/rss+xml' } });
    }
  } catch (_) {}

  const articles = await fetchRSSArticles(c.env.DB, siteSlug, 20);
  const xml      = buildRSSXml(articles, siteConfig, feedUrl);

  // Guardar en caché KV por 30 minutos
  try {
    await c.env.ARTICLES_KV.put(kvKey, xml, { expirationTtl: 1800 });
  } catch (_) {}

  return new Response(xml, { headers: { 'Content-Type': 'application/rss+xml' } });
});

// ── GET /rss — Feed RSS global (todos los sitios) ────────────
rss.get('/', async (c) => {
  const articles = await fetchRSSArticles(c.env.DB, null, 30);
  const xml = buildRSSXml(
    articles,
    { nombre: 'Red Noticias', tagline: 'En vivo', dominio: 'https://www.noticiasobjetivo.click' },
    'https://api.com/rss'
  );
  return new Response(xml, { headers: { 'Content-Type': 'application/rss+xml' } });
});

export default rss;
