export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');
  const canonicalUrl = url.toString();

  if (!slug) return await next();

  // Obtener la respuesta de la página estática
  const response = await next();

  try {
    if (!env.DB) return response;

    // 1. Intentar buscar en ARTICULOS_PARAFRASEADOS (Automáticos)
    let article = await env.DB.prepare(
      "SELECT TITULO_PARAFRASEADO as title, DESCRIPCION_PARAFRASEADA as desc, URL_IMAGEN as image FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? LIMIT 1"
    ).bind(slug).first();

    // 2. Si no existe, buscar en ARTICULOS_CMS (Manuales)
    if (!article) {
      article = await env.DB.prepare(
        "SELECT TITULO as title, DESCRIPCION as desc, URL_IMAGEN as image FROM ARTICULOS_CMS WHERE SLUG = ? LIMIT 1"
      ).bind(slug).first();
    }

    if (!article) return response;

    const title = article.title;
    const description = (article.desc || "").substring(0, 200);
    const normalizeImageUrl = (value) => {
      if (!value || typeof value !== 'string') return `${url.origin}/logo.png`;

      let normalized = value.trim();

      if (!normalized || normalized.includes('undefined')) {
        return `${url.origin}/logo.png`;
      }

      if (normalized.startsWith('//')) {
        normalized = `https:${normalized}`;
      } else if (normalized.startsWith('/')) {
        normalized = `${url.origin}${normalized}`;
      } else if (normalized.includes('uploads.sebastianvernis.space') && !/^https?:\/\//i.test(normalized)) {
        normalized = `https://${normalized.replace(/^\/+/, '')}`;
      }

      if (/^http:\/\//i.test(normalized)) {
        normalized = normalized.replace(/^http:\/\//i, 'https://');
      }

      if (!/^https:\/\//i.test(normalized)) {
        return `${url.origin}/logo.png`;
      }

      return normalized;
    };

    const image = normalizeImageUrl(article.image || '/logo.png');
    const escapeHtml = (text) => (text || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');

    const escapedTitle = escapeHtml(title);
    const escapedDescription = escapeHtml(description);
    const escapedImage = escapeHtml(image);
    const escapedCanonicalUrl = escapeHtml(canonicalUrl);

    // 3. Inyectar Meta Tags
    return new HTMLRewriter()
      .on('title', { element(el) { el.setInnerContent(title); } })
      .on('meta#page-desc', { element(el) { el.setAttribute('content', description); } })
      .on('meta#og-title', { element(el) { el.setAttribute('content', title); } })
      .on('meta#og-desc', { element(el) { el.setAttribute('content', description); } })
      .on('meta#og-image', { element(el) { el.setAttribute('content', image); } })
      .on('meta#og-url', { element(el) { el.setAttribute('content', canonicalUrl); } })
      .on('meta[property="og:type"]', { element(el) { el.setAttribute('content', 'article'); } })
      .on('head', {
        element(el) {
          el.prepend(`<meta name="description" content="${escapedDescription}" />`, { html: true });
          el.prepend(`<meta property="og:type" content="article" />`, { html: true });
          el.prepend(`<meta property="og:title" content="${escapedTitle}" />`, { html: true });
          el.prepend(`<meta property="og:description" content="${escapedDescription}" />`, { html: true });
          el.prepend(`<meta property="og:image" content="${escapedImage}" />`, { html: true });
          el.prepend(`<meta property="og:image:secure_url" content="${escapedImage}" />`, { html: true });
          el.prepend(`<meta property="og:image:width" content="1200" />`, { html: true });
          el.prepend(`<meta property="og:image:height" content="630" />`, { html: true });
          el.prepend(`<meta property="og:url" content="${escapedCanonicalUrl}" />`, { html: true });
          el.prepend(`<meta name="twitter:card" content="summary_large_image" />`, { html: true });
          el.prepend(`<meta name="twitter:title" content="${escapedTitle}" />`, { html: true });
          el.prepend(`<meta name="twitter:image" content="${escapedImage}" />`, { html: true });
        }
      })
      .transform(response);

  } catch (e) {
    console.error("SEO Middleware Error:", e.message);
    return response;
  }
}
