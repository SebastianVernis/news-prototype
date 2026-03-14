export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');

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
    let image = article.image || "/logo.png";
    
    // Forzar URL absoluta para Facebook
    if (image.startsWith('/')) {
      image = `${url.origin}${image}`;
    }

    // 3. Inyectar Meta Tags
    return new HTMLRewriter()
      .on('title', { element(el) { el.setInnerContent(title); } })
      .on('meta[property^="og:"]', { element(el) { el.remove(); } })
      .on('meta[name^="twitter:"]', { element(el) { el.remove(); } })
      .on('meta[name="description"]', { element(el) { el.remove(); } })
      .on('head', {
        element(el) {
          el.prepend(`<meta name="description" content="${description.replace(/"/g, '&quot;')}" />`, { html: true });
          el.prepend(`<meta property="og:type" content="article" />`, { html: true });
          el.prepend(`<meta property="og:title" content="${title.replace(/"/g, '&quot;')}" />`, { html: true });
          el.prepend(`<meta property="og:description" content="${description.replace(/"/g, '&quot;')}" />`, { html: true });
          el.prepend(`<meta property="og:image" content="${image}" />`, { html: true });
          el.prepend(`<meta property="og:image:secure_url" content="${image}" />`, { html: true });
          el.prepend(`<meta property="og:image:width" content="1200" />`, { html: true });
          el.prepend(`<meta property="og:image:height" content="630" />`, { html: true });
          el.prepend(`<meta property="og:url" content="${url.href}" />`, { html: true });
          el.prepend(`<meta name="twitter:card" content="summary_large_image" />`, { html: true });
          el.prepend(`<meta name="twitter:title" content="${title.replace(/"/g, '&quot;')}" />`, { html: true });
          el.prepend(`<meta name="twitter:image" content="${image}" />`, { html: true });
        }
      })
      .transform(response);

  } catch (e) {
    console.error("SEO Middleware Error:", e.message);
    return response;
  }
}
