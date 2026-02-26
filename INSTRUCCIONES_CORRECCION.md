# Protocolo de Corrección - Worker API NexoPress

## Estado Actual
El archivo `src/index.js` presenta errores de sintaxis (`Unexpected export`, `Expected ; but found $`) localizados entre las líneas 1370 y el final. Esto se debe a intentos fallidos de concatenación que mutilaron el cierre de las funciones de RSS e inyectaron código con errores de escape.

## Instrucciones para el nuevo Agente

### 1. Saneamiento del Archivo
Se debe limpiar el archivo `src/index.js` eliminando todo el contenido a partir de la definición de `fetchRSSArticles` (aproximadamente línea 1370), asegurando que no queden bloques `export default` huérfanos.

### 2. Inyección del Bloque Maestro
Se debe inyectar el siguiente bloque de código **puro** (evitando el uso de `cat` o redirecciones de shell que interpreten `${}`) al final del archivo:

```javascript
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
app.post('/articles/publish-fb/:id', async (c) => {
  if (!checkAuth(c)) return c.json({ error: '401' }, 401);
  const id = c.req.param('id');
  await c.env.DB.prepare("UPDATE ARTICULOS_PARAFRASEADOS SET FB_REQUERIDO = 1, FB_PUBLICADO = 0 WHERE ID = ?").bind(id).run();
  await c.env.DB.prepare("UPDATE ARTICULOS_CMS SET FB_REQUERIDO = 1, FB_PUBLICADO = 0 WHERE ID = ?").bind(id).run();
  if (c.executionCtx) c.executionCtx.waitUntil(processFB(c.env));
  return c.json({ success: true });
});

async function publishToFB(env, article, type) {
  if (!article.SITIOS_DESTINO) return;
  const slugs = article.SITIOS_DESTINO.split(",").map(s => s.trim());
  for (const slug of slugs) {
    const site = await env.DB.prepare("SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1").bind(slug).first();
    if (!site || !site.FACEBOOK_PAGE_ID || !site.FACEBOOK_TOKEN_SECRET) continue;
    const token = env[site.FACEBOOK_TOKEN_SECRET];
    const domain = site.DOMINIO || `${slug}.pages.dev`;
    const url = `https://${domain}/articulo/?slug=${article.SLUG}`;
    try { await fetch(`https://graph.facebook.com/v19.0/${site.FACEBOOK_PAGE_ID}/feed`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: article.TITULO, link: url, access_token: token }) }); } catch (e) {}
  }
  const table = type === 'CMS' ? 'ARTICULOS_CMS' : 'ARTICULOS_PARAFRASEADOS';
  await env.DB.prepare(`UPDATE ${table} SET FB_PUBLICADO = 1, FB_FECHA = datetime('now') WHERE ID = ?`).bind(article.ID).run();
}

async function processFB(env) {
  try {
    const cms = await env.DB.prepare("SELECT ID, TITULO, SLUG, SITIOS_DESTINO FROM ARTICULOS_CMS WHERE ESTADO = 'PUBLICADO' AND FB_REQUERIDO = 1 AND FB_PUBLICADO = 0 LIMIT 2").all();
    for (const a of (cms.results || [])) await publishToFB(env, a, 'CMS');
    const para = await env.DB.prepare("SELECT ID, TITULO_PARAFRASEADO as TITULO, SLUG, SITIO_DESTINO as SITIOS_DESTINO FROM ARTICULOS_PARAFRASEADOS WHERE FB_REQUERIDO = 1 AND FB_PUBLICADO = 0 LIMIT 2").all();
    for (const a of (para.results || [])) await publishToFB(env, a, 'PARA');
  } catch (e) {}
}

async function runMasterCron(env) {
  const status = { time: new Date().toISOString(), tasks: {} };
  try { await processFB(env); status.tasks.fb = "OK"; } catch (e) {}
  try { await updateFinancials(env); await updateWeather(env); status.tasks.stats = "OK"; } catch (e) {}
  try {
    const now = new Date();
    const mxHour = (now.getUTCHours() - 6 + 24) % 24;
    const last = await env.ARTICLES_KV.get("last_ingest_hour");
    if (last !== mxHour.toString()) {
      const ok = await autoIngestNews(env, mxHour);
      if (ok) { await env.ARTICLES_KV.put("last_ingest_hour", mxHour.toString()); status.tasks.ingest = "OK"; }
    }
  } catch (e) {}
  await env.ARTICLES_KV.put("cron_status", JSON.stringify(status));
}

async function mirrorImageToR2(url, env) {
  if (!url || !url.startsWith('http')) return '/logo.png';
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    if (!res.ok) return '/logo.png';
    const key = `auto/${crypto.randomUUID()}.jpg`;
    await env.UPLOADS.put(key, res.body, { httpMetadata: { contentType: 'image/jpeg' } });
    return `/api/images/${key}`;
  } catch (e) { return '/logo.png'; }
}

async function autoIngestNews(env, hour) {
  try {
    const FEEDS = ["https://www.jornada.com.mx/rss/politica.xml?v=1","https://expansion.mx/rss","https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada"];
    let art = null;
    for (const f of FEEDS) {
      try {
        const r = await fetch(f);
        const x = await r.text();
        const items = x.match(/<item>([\s\S]*?)<\/item>/g) || [];
        for (const i of items) {
          const title = (i.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) || i.match(/<title>([\s\S]*?)<\/title>/))[1].trim();
          const exist = await env.DB.prepare("SELECT ID FROM ARTICULOS_ORIGINALES WHERE TITULO = ?").bind(title).first();
          if (!exist) {
            const link = (i.match(/<link>([\s\S]*?)<\/link>/))[1].trim();
            const desc = (i.match(/<description><!\[CDATA\[([\s\S]*?)\]\]><\/description>/) || i.match(/<description>([\s\S]*?)<\/description>/))[1].trim();
            const img = i.match(/<media:content[^>]+url=["']([^"']+)["']/) || i.match(/<img[^>]+src=["']([^"']+)["']/);
            art = { title, link, desc, img: img ? img[1] : null };
            break;
          }
        }
      } catch (e) {}
      if (art) break;
    }
    if (!art) return false;
    const mirImg = await mirrorImageToR2(art.img, env);
    const id = crypto.randomUUID();
    await env.DB.prepare("INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, DESCRIPCION, URL_IMAGEN, FECHA, CONTENIDO, CATEGORIA, LONGITUD) VALUES (?,?,?,?,?,datetime('now'),?,'NACIONAL',?)").bind(id, art.link, art.title, art.desc, mirImg, art.desc, art.desc.length).run();
    await env.DB.prepare("INSERT INTO REVISION_CONTENIDO (ID_ORIGEN, TIPO_ORIGEN, TITULO_PROPUESTO, CONTENIDO_PROPUESTO, DESCRIPCION_PROPUESTA, SITIO_DESTINO, CATEGORIA, ESTADO, URL_IMAGEN, FB_REQUERIDO, ES_BREVE) VALUES (?, 'API', ?, ?, ?, 'bitacoraurbana,nodoinformativo', 'NACIONAL', 'PENDIENTE', ?, 0, 0)").bind(id, art.title, art.desc, art.title, mirImg).run();
    return true;
  } catch (e) { return false; }
}

async function injectMetaTags(request, env, response) {
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');
  if (!slug || !url.pathname.includes('/articulo')) return response;
  try {
    let article = await env.DB.prepare("SELECT TITULO_PARAFRASEADO as t, DESCRIPCION_PARAFRASEADA as d, URL_IMAGEN as i FROM ARTICULOS_PARAFRASEADOS WHERE SLUG = ? LIMIT 1").bind(slug).first();
    if (!article) article = await env.DB.prepare("SELECT TITULO as t, DESCRIPCION as d, URL_IMAGEN as i FROM ARTICULOS_CMS WHERE SLUG = ? LIMIT 1").bind(slug).first();
    if (!article) return response;
    const img = article.i && article.i.startsWith('http') ? article.i : `${url.origin}/logo.png`;
    return new HTMLRewriter()
      .on('title', { element(el) { el.setInnerContent(article.t); } })
      .on('head', {
        element(el) {
          el.prepend(`<meta property="og:title" content="${article.t}" /><meta property="og:description" content="${article.d}" /><meta property="og:image" content="${img}" /><meta property="og:type" content="article" /><meta name="twitter:card" content="summary_large_image" />`, { html: true });
        }
      }).transform(response);
  } catch (e) { return response; }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/api/cron/manual') { await runMasterCron(env); return new Response("OK"); }
    if (url.pathname === '/api/cron/status') { const s = await env.ARTICLES_KV.get("cron_status"); return new Response(s || "{}", { headers: { 'Content-Type': 'application/json' } }); }
    if (url.pathname.startsWith('/api')) return app.fetch(request, env, ctx);
    const originalRes = await fetch(request);
    return injectMetaTags(request, env, originalRes);
  },
  async scheduled(event, env, ctx) { ctx.waitUntil(runMasterCron(env)); }
};
```

### 3. Validación y Despliegue
Una vez corregido el archivo, ejecutar:
`wrangler deploy src/index.js --name news-api --config src/wrangler.toml`
