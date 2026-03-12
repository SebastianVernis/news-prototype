export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');

  // Si no hay slug, redirigir al index
  if (!slug) {
    return Response.redirect(url.origin, 302);
  }

  try {
    if (!env.DB) return await next();

    // 1. Intentar buscar en ARTICULOS_PARAFRASEADOS (Automáticos)
    let article = await env.DB.prepare(
      "SELECT ID as para_id, TITULO_PARAFRASEADO as title, DESCRIPCION_PARAFRASEADA as desc, URL_IMAGEN as image FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? LIMIT 1"
    ).bind(slug).first();

    let isCMS = false;

    // 2. Si no existe, buscar en ARTICULOS_CMS (Manuales)
    if (!article) {
      article = await env.DB.prepare(
        "SELECT ID as para_id, TITULO as title, DESCRIPCION as desc, URL_IMAGEN as image FROM ARTICULOS_CMS WHERE SLUG = ? LIMIT 1"
      ).bind(slug).first();
      isCMS = true;
    }

    // 3. Si el artículo no existe, redirigir al index
    if (!article) {
      console.log(`[404] Article not found: ${slug}, redirecting to index`);
      return Response.redirect(url.origin, 302);
    }

    // Obtener la respuesta de la página estática
    const response = await next();

    const title = article.title;
    const description = (article.desc || "").substring(0, 200);
    let image = article.image || "/logo.png";

    // Forzar URL absoluta para Facebook - CRÍTICO para que cargue miniaturas
    if (image.startsWith('/')) {
      image = `${url.origin}${image}`;
    }
    
    // Asegurar que la imagen sea accesible públicamente
    // Si es R2, verificar que sea URL completa
    if (image.includes('uploads.sebastianvernis.space') && !image.startsWith('https://')) {
      image = `https://${image}`;
    }
    
    // Fallback a logo si la imagen es inválida
    if (!image || image.includes('undefined') || image.trim() === '') {
      image = `${url.origin}/logo.png`;
    }

    // 3. Registrar publicación web en ARTICULOS_SITIO_{SLUG}
    // NOTA: WEB_PUBLICADO ya debería ser 1 por defecto al insertar
    // Este update es solo para asegurar WEB_URL y WEB_FECHA
    const siteSlug = "radiocinconoticias";
    const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;
    
    try {
      // Actualizar WEB_URL (WEB_PUBLICADO ya debería ser 1)
      await env.DB.prepare(`
        UPDATE ${tableName}
        SET WEB_URL = ?, WEB_FECHA = CASE WHEN WEB_FECHA IS NULL THEN datetime('now') ELSE WEB_FECHA END
        WHERE ID_PARAFRASEADO = ?
      `).bind(url.href, article.para_id).run();
      
      console.log(`[WEB_PUBLISH] Article ${article.para_id} accessed on ${siteSlug}`);
    } catch (dbErr) {
      // El artículo puede no estar en la tabla de este sitio aún
      // Esto es normal para artículos antiguos
    }

    // Escapar caracteres especiales para HTML
    const escapeHtml = (text) => {
      if (!text) return '';
      return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    };

    const escapedTitle = escapeHtml(title);
    const escapedDescription = escapeHtml(description);

    // 4. Inyectar Meta Tags OPTIMIZADOS para Facebook
    return new HTMLRewriter()
      .on('title', { element(el) { el.setInnerContent(title); } })
      .on('meta[property^="og:"]', { element(el) { el.remove(); } })
      .on('meta[name^="twitter:"]', { element(el) { el.remove(); } })
      .on('meta[name="description"]', { element(el) { el.remove(); } })
      .on('head', {
        element(el) {
          el.prepend(`
            <!-- Facebook / Meta Tags -->
            <meta property="og:type" content="article" />
            <meta property="og:title" content="${escapedTitle}" />
            <meta property="og:description" content="${escapedDescription}" />
            <meta property="og:image" content="${image}" />
            <meta property="og:image:secure_url" content="${image}" />
            <meta property="og:image:width" content="1200" />
            <meta property="og:image:height" content="630" />
            <meta property="og:image:alt" content="${escapedTitle}" />
            <meta property="og:url" content="${url.href}" />
            <meta property="og:site_name" content="NexoPress" />
            <meta property="og:locale" content="es_MX" />
            <meta property="og:updated_time" content="${new Date().toISOString()}" />
            
            <!-- Twitter Card Tags -->
            <meta name="twitter:card" content="summary_large_image" />
            <meta name="twitter:title" content="${escapedTitle}" />
            <meta name="twitter:description" content="${escapedDescription}" />
            <meta name="twitter:image" content="${image}" />
            <meta name="twitter:image:alt" content="${escapedTitle}" />
            
            <!-- SEO Meta Tags -->
            <meta name="description" content="${escapedDescription}" />
            <meta name="robots" content="index, follow" />
          `, { html: true });
        }
      })
      .transform(response);

  } catch (e) {
    console.error("SEO Middleware Error:", e.message);
    return response;
  }
}
