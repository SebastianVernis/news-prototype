async function resolveArticleBySlug(db, slug) {
  let article = await db.prepare(
    "SELECT ID as para_id, SLUG as canonical_slug, LEGACY_SLUG as legacy_slug, TITULO_PARAFRASEADO as title, DESCRIPCION_PARAFRASEADA as desc, URL_IMAGEN as image FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? LIMIT 1"
  ).bind(slug).first();

  let isCMS = false;

  if (!article) {
    article = await db.prepare(
      "SELECT ID as para_id, SLUG as canonical_slug, LEGACY_SLUG as legacy_slug, TITULO as title, DESCRIPCION as desc, URL_IMAGEN as image FROM ARTICULOS_CMS WHERE SLUG = ? LIMIT 1"
    ).bind(slug).first();
    isCMS = Boolean(article);
  }

  if (!article) {
    article = await db.prepare(
      "SELECT ID as para_id, SLUG as canonical_slug, LEGACY_SLUG as legacy_slug, TITULO_PARAFRASEADO as title, DESCRIPCION_PARAFRASEADA as desc, URL_IMAGEN as image FROM ARTICULOS_PARAFRASEADOS WHERE LEGACY_SLUG = ? LIMIT 1"
    ).bind(slug).first();
  }

  if (!article) {
    article = await db.prepare(
      "SELECT ID as para_id, SLUG as canonical_slug, LEGACY_SLUG as legacy_slug, TITULO as title, DESCRIPCION as desc, URL_IMAGEN as image FROM ARTICULOS_CMS WHERE LEGACY_SLUG = ? LIMIT 1"
    ).bind(slug).first();
    isCMS = Boolean(article);
  }

  return { article, isCMS };
}

export async function handleArticleRequest(context, siteSlug) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const requestedSlug = url.searchParams.get('slug');

  if (!requestedSlug) {
    return Response.redirect(url.origin, 302);
  }

  try {
    if (!env.DB) return await next();

    const { article } = await resolveArticleBySlug(env.DB, requestedSlug);
    if (!article) {
      return await next();
    }

    if (article.canonical_slug && article.canonical_slug !== requestedSlug) {
      const redirectUrl = new URL(url.href);
      redirectUrl.searchParams.set('slug', article.canonical_slug);
      return Response.redirect(redirectUrl.toString(), 302);
    }

    const response = await next();
    const title = article.title;
    const description = (article.desc || '').substring(0, 200);
    let image = article.image || '/logo.png';

    if (image.startsWith('/')) {
      image = `${url.origin}${image}`;
    }

    if (image.includes('uploads.sebastianvernis.space') && !image.startsWith('https://')) {
      image = `https://${image}`;
    }

    if (!image || image.includes('undefined') || image.trim() === '') {
      image = `${url.origin}/logo.png`;
    }

    const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

    try {
      await env.DB.prepare(`
        UPDATE ${tableName}
        SET WEB_URL = ?, WEB_FECHA = CASE WHEN WEB_FECHA IS NULL THEN datetime('now') ELSE WEB_FECHA END
        WHERE ID_PARAFRASEADO = ?
      `).bind(url.href, article.para_id).run();
    } catch (_) {}

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

    return new HTMLRewriter()
      .on('title', { element(el) { el.setInnerContent(title); } })
      .on('meta[property^="og:"]', { element(el) { el.remove(); } })
      .on('meta[name^="twitter:"]', { element(el) { el.remove(); } })
      .on('meta[name="description"]', { element(el) { el.remove(); } })
      .on('head', {
        element(el) {
          el.prepend(`
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
            <meta name="twitter:card" content="summary_large_image" />
            <meta name="twitter:title" content="${escapedTitle}" />
            <meta name="twitter:description" content="${escapedDescription}" />
            <meta name="twitter:image" content="${image}" />
            <meta name="twitter:image:alt" content="${escapedTitle}" />
            <meta name="description" content="${escapedDescription}" />
            <meta name="robots" content="index, follow" />
          `, { html: true });
        }
      })
      .transform(response);
  } catch (e) {
    console.error('SEO Middleware Error:', e.message);
    return await next();
  }
}
