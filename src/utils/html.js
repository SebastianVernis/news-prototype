// src/utils/html.js — Utilidades HTML: meta tags, OG scraping, R2 upload

// ============================================================
// getOGImage — Extrae og:image de una URL remota
// ============================================================
export const getOGImage = async (url) => {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    const html = await res.text();
    const ogMatch =
      html.match(/<meta[^>]*property=["']og:image["'][^>]*content=["']([^"']+)["']/i) ||
      html.match(/<meta[^>]*content=["']([^"']+)["'][^>]*property=["']og:image["']/i);
    return ogMatch ? ogMatch[1] : null;
  } catch (_) {
    return null;
  }
};

// ============================================================
// uploadToR2 — Descarga imagen remota y la sube a R2
// ============================================================
export const uploadToR2 = async (url, env) => {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) return null;
    const contentType = res.headers.get('content-type') || 'image/jpeg';
    const buffer = await res.arrayBuffer();
    const key = `auto/${crypto.randomUUID()}.jpg`;
    await env.UPLOADS.put(key, buffer, { httpMetadata: { contentType } });
    return `https://uploads.sebastianvernis.space/${key}`;
  } catch (_) {
    return null;
  }
};

// ============================================================
// injectMetaTags — Inyecta OG meta tags en páginas de artículo
// usando HTMLRewriter de Cloudflare Workers
// ============================================================
export const injectMetaTags = async (request, env, response) => {
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');
  if (!slug || !url.pathname.includes('/articulo')) return response;

  try {
    let article = await env.DB.prepare(
      'SELECT TITULO_PARAFRASEADO as t, DESCRIPCION_PARAFRASEADA as d, URL_IMAGEN as i FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? LIMIT 1'
    ).bind(slug).first();

    if (!article) {
      article = await env.DB.prepare(
        'SELECT TITULO as t, DESCRIPCION as d, URL_IMAGEN as i FROM ARTICULOS_CMS WHERE SLUG = ? LIMIT 1'
      ).bind(slug).first();
    }

    if (!article) return response;

    let ogImg = `${url.origin}/logo.png`;
    if (article.i) {
      if (article.i.startsWith('/api/images/')) ogImg = `${url.origin}${article.i}`;
      else if (article.i.startsWith('http') && !article.i.includes('/logo.png')) ogImg = article.i;
    }

    return new HTMLRewriter()
      .on('title', {
        element(el) { el.setInnerContent(article.t); }
      })
      .on('head', {
        element(el) {
          el.prepend(
            `<meta property="og:title" content="${article.t}" />` +
            `<meta property="og:description" content="${article.d}" />` +
            `<meta property="og:image" content="${ogImg}" />` +
            `<meta property="og:type" content="article" />` +
            `<meta name="twitter:card" content="summary_large_image" />`,
            { html: true }
          );
        }
      })
      .transform(response);
  } catch (_) {
    return response;
  }
};
