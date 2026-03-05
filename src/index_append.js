
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

app.post('/articles/publish-fb/:id', async (c) => {
  if (!checkAuth(c)) return c.json({ error: '401' }, 401);
  const id = c.req.param('id');
  await c.env.DB.prepare("UPDATE ARTICULOS_PARAFRASEADOS SET FB_REQUERIDO = 1, FB_PUBLICADO = 0 WHERE ID = ?").bind(id).run();
  await c.env.DB.prepare("UPDATE ARTICULOS_CMS SET FB_REQUERIDO = 1, FB_PUBLICADO = 0 WHERE ID = ?").bind(id).run();
  if (c.executionCtx) c.executionCtx.waitUntil(processFB(c.env));
  return c.json({ success: true });
});

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function publishToFB(env, article, type) {
  if (!article.SITIOS_DESTINO) return;
  const slugs = article.SITIOS_DESTINO.split(",").map(s => s.trim());
  for (const s of slugs) {
    const site = await env.DB.prepare("SELECT * FROM SITIOS WHERE SLUG = ? AND FACEBOOK_ACTIVO = 1").bind(s).first();
    if (!site || !site.FACEBOOK_PAGE_ID || !site.FACEBOOK_TOKEN_SECRET) continue;
    const token = env[site.FACEBOOK_TOKEN_SECRET];
    const url = `https://${site.DOMINIO}/articulo/?slug=${article.SLUG}`;
    try { 
      await fetch(`https://graph.facebook.com/v19.0/${site.FACEBOOK_PAGE_ID}/feed`, { 
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify({ message: article.TITULO, link: url, access_token: token }) 
      }); 
      
      // Delay entre peticiones a Meta (2-5 segundos)
      await sleep(2000 + Math.random() * 3000);
    } catch (e) {}
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
  try { await processFB(env); } catch (e) {}
  try { await updateFinancials(env); await updateWeather(env); } catch (e) {}
  try {
    const now = new Date();
    const mxHour = (now.getUTCHours() - 6 + 24) % 24;
    const last = await env.ARTICLES_KV.get("last_ingest_hour");
    if (last !== mxHour.toString()) {
      const ok = await autoIngestNews(env, mxHour);
      if (ok) await env.ARTICLES_KV.put("last_ingest_hour", mxHour.toString());
    }
  } catch (e) {}
}

async function autoIngestNews(env, hour) {
  // Bitácora Urbana ahora usa el flujo principal con scraping de imágenes reales
  // Esta función está deprecated - el ingesta se hace desde runRSSDirectIngest en index.js
  try {
    const FEEDS = [
      "https://www.jornada.com.mx/rss/politica.xml?v=1",
      "https://expansion.mx/rss",
      "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada"
    ];
    let art = null;
    for (const f of FEEDS) {
      try {
        const r = await fetch(f);
        const x = await r.text();
        const items = x.match(/<item>([\s\S]*?)<\/item>/g) || [];
        for (const i of items) {
          const titleMatch = i.match(/<title><!\[CDATA\[([\s\S]*?)\]\]><\/title>/) || i.match(/<title>([\s\S]*?)<\/title>/);
          if (!titleMatch) continue;
          const title = titleMatch[1];
          const exist = await env.DB.prepare("SELECT ID FROM ARTICULOS_ORIGINALES WHERE TITULO = ?").bind(title).first();
          if (!exist) {
            const linkMatch = i.match(/<link>([\s\S]*?)<\/link>/);
            const descMatch = i.match(/<description><!\[CDATA\[([\s\S]*?)\]\]><\/description>/) || i.match(/<description>([\s\S]*?)<\/description>/);
            art = { title, link: linkMatch ? linkMatch[1] : "", desc: descMatch ? descMatch[1] : "" };
            break;
          }
        }
      } catch (e) {}
      if (art) break;
    }
    if (!art) return false;
    
    // Usar el flujo principal con scraping de imagen real
    const id = crypto.randomUUID();
    const imageUrl = await getOGImageReal(art.link);
    const finalImage = imageUrl || "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=1000&auto=format&fit=crop";
    
    await env.DB.prepare("INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, DESCRIPCION, URL_IMAGEN, FECHA, CONTENIDO, CATEGORIA, LONGITUD) VALUES (?,?,?,?,?,datetime('now'),?,'NACIONAL',?)").bind(id, art.link, art.title, art.desc, finalImage, art.desc, art.desc.length).run();
    await env.DB.prepare("INSERT INTO REVISION_CONTENIDO (ID_ORIGEN, TIPO_ORIGEN, TITULO_PROPUESTO, CONTENIDO_PROPUESTO, DESCRIPCION_PROPUESTA, SITIO_DESTINO, CATEGORIA, ESTADO, URL_IMAGEN, FB_REQUERIDO, ES_BREVE) VALUES (?, 'API', ?, ?, ?, 'bitacoraurbana', 'NACIONAL', 'PENDIENTE', ?, 0, 0)").bind(id, art.title, art.desc, art.title, finalImage).run();
    return true;
  } catch (e) { return false; }
}

async function getOGImageReal(url) {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    const html = await res.text();
    const ogMatch = html.match(/<meta[^>]*property=["']og:image["'][^>]*content=["']([^"']+)["']/i) ||
                    html.match(/<meta[^>]*content=["']([^"']+)["'][^>]*property=["']og:image["']/i);
    return ogMatch ? ogMatch[1] : null;
  } catch(e) { return null; }
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/api/cron/manual') { await runMasterCron(env); return new Response("OK"); }
    if (url.pathname.startsWith('/api')) return app.fetch(request, env, ctx);
    const res = await fetch(request);
    return injectMetaTags(request, env, res);
  },
  async scheduled(event, env, ctx) { ctx.waitUntil(runMasterCron(env)); }
};
