// workers/cron-worker.js - Orquestador Autónomo de Noticias + Ticker en Vivo

const slugify = (text) => text.toString().toLowerCase().trim()
  .replace(/\s+/g, '-').replace(/[^\w\-]+/g, '')
  .replace(/\-\-+/g, '-').replace(/^-+/, '').replace(/-+$/, '');

// ============================================================
// 1. Detección de Duplicados en D1
// ============================================================
async function isDuplicate(db, title) {
  const normalizedTitle = title.toLowerCase().substring(0, 50);
  const { results } = await db.prepare(
    "SELECT TITULO FROM ARTICULOS_ORIGINALES WHERE LOWER(TITULO) LIKE ? LIMIT 1"
  ).bind(`%${normalizedTitle}%`).all();
  return results.length > 0;
}

// ============================================================
// 2. Parafraseo Profesional via OpenRouter
// ============================================================
async function paraphraseWithAI(env, article) {
  const prompt = `Eres un periodista senior. Expande esta noticia a 800-1000 palabras directamente en formato HTML profesional.
  
  REGLAS DE FORMATO:
  - Usa <p> para párrafos.
  - Usa <h2> para los títulos de sección.
  - Usa <strong> para resaltar nombres y datos.
  - Mantén los hechos, añade contexto y análisis.
  
  TÍTULO: ${article.title}
  NOTICIA: ${article.content || article.description}`;

  try {
    const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.OPENROUTER_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: env.PARAPHRASE_MODEL || "arcee-ai/trinity-large-preview:free",
        messages: [{ role: "user", content: prompt }]
      })
    });
    const data = await res.json();
    return data.choices[0].message.content;
  } catch (e) {
    console.error("Error OpenRouter:", e);
    return null;
  }
}

// ============================================================
// 3. Helpers de formato para datos financieros
// ============================================================
function fmtMXN(val) {
  if (!val || isNaN(val)) return 'N/D';
  return '$' + parseFloat(val).toFixed(2);
}

function fmtPct(val) {
  if (!val || isNaN(val)) return '0.00%';
  const n = parseFloat(val);
  return (n >= 0 ? '+' : '') + n.toFixed(2) + '%';
}

function fmtNum(val, decimals = 2) {
  if (!val || isNaN(val)) return 'N/D';
  return parseFloat(val).toLocaleString('es-MX', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });
}

// ============================================================
// 4. Fetch Yahoo Finance (Oro, Petróleo, IPC BMV)
// ============================================================
async function fetchYahoo(symbol) {
  try {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1d&range=2d`;
    const res = await fetch(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)' }
    });
    const data = await res.json();
    const meta = data?.chart?.result?.[0]?.meta;
    if (!meta) return null;
    const price = meta.regularMarketPrice;
    const prev  = meta.chartPreviousClose || meta.previousClose || price;
    const pct   = prev ? ((price - prev) / prev) * 100 : 0;
    return { price, pct };
  } catch (e) {
    console.error(`Yahoo fetch error for ${symbol}:`, e.message);
    return null;
  }
}

// ============================================================
// 5. Actualización del Ticker (Financieros + Headlines)
// ============================================================
async function runTickerUpdate(env) {
  console.log('📊 Actualizando ticker en vivo...');
  const API_BASE = env.API_BASE || 'https://news-api.sebastianvernis.workers.dev/api';
  const ADMIN_TOKEN = env.ADMIN_TOKEN || '';

  const financials = [];

  // ── A. Tipos de cambio (USD/MXN, EUR/MXN) via open.er-api.com ──────────
  try {
    const ratesRes = await fetch('https://open.er-api.com/v6/latest/USD');
    const rates = await ratesRes.json();
    if (rates?.rates?.MXN) {
      const usdMxn = rates.rates.MXN;
      financials.push({
        simbolo: 'USD',
        nombre: 'Dólar USD',
        valor: fmtMXN(usdMxn),
        cambio: '+0.00%',
        tendencia: 'up',
        unidad: 'MXN'
      });

      if (rates.rates.EUR) {
        const eurMxn = usdMxn / rates.rates.EUR;
        financials.push({
          simbolo: 'EUR',
          nombre: 'Euro EUR',
          valor: fmtMXN(eurMxn),
          cambio: '+0.00%',
          tendencia: 'up',
          unidad: 'MXN'
        });
      }
    }
  } catch (e) {
    console.error('Error exchange rates:', e.message);
  }

  // ── B. Bitcoin via CoinGecko ────────────────────────────────────────────
  try {
    const btcRes = await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd',
      { headers: {
          'Accept': 'application/json',
          'User-Agent': 'NodoInformativo-NewsBot/1.0 (https://www.nodoinformativo.lat)'
        }
      }
    );
    if (!btcRes.ok) {
      const text = await btcRes.text();
      throw new Error(`CoinGecko HTTP ${btcRes.status}: ${text.substring(0, 100)}`);
    }
    const btcData = await btcRes.json();
    const btcUsd = btcData?.bitcoin?.usd;
    if (btcUsd) {
      financials.push({
        simbolo: 'BTC',
        nombre: 'Bitcoin',
        valor: '$' + fmtNum(btcUsd, 0),
        cambio: '+0.00%',
        tendencia: 'up',
        unidad: 'USD'
      });
    }
  } catch (e) {
    console.error('Error Bitcoin:', e.message);
  }

  // ── C. Oro (Yahoo Finance GC=F) ─────────────────────────────────────────
  const gold = await fetchYahoo('GC=F');
  if (gold) {
    financials.push({
      simbolo: 'ORO',
      nombre: 'Oro',
      valor: '$' + fmtNum(gold.price, 2) + '/oz',
      cambio: fmtPct(gold.pct),
      tendencia: gold.pct >= 0 ? 'up' : 'down',
      unidad: 'USD'
    });
  }

  // ── D. Petróleo WTI (Yahoo Finance CL=F) ───────────────────────────────
  const oil = await fetchYahoo('CL=F');
  if (oil) {
    financials.push({
      simbolo: 'PETROLEO',
      nombre: 'Petróleo WTI',
      valor: '$' + fmtNum(oil.price, 2) + '/bbl',
      cambio: fmtPct(oil.pct),
      tendencia: oil.pct >= 0 ? 'up' : 'down',
      unidad: 'USD'
    });
  }

  // ── E. IPC BMV (Yahoo Finance ^MXX) ────────────────────────────────────
  const ipc = await fetchYahoo('^MXX');
  if (ipc) {
    financials.push({
      simbolo: 'IPC',
      nombre: 'IPC BMV',
      valor: fmtNum(ipc.price, 0) + ' pts',
      cambio: fmtPct(ipc.pct),
      tendencia: ipc.pct >= 0 ? 'up' : 'down',
      unidad: 'MXN'
    });
  }

  // ── F. Guardar financieros en DB via API ────────────────────────────────
  if (financials.length > 0) {
    try {
      const r = await fetch(`${API_BASE}/ticker/financials`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${ADMIN_TOKEN}`
        },
        body: JSON.stringify(financials)
      });
      console.log(`✅ Financieros actualizados: ${financials.length} items (${r.status})`);
    } catch (e) {
      console.error('Error guardando financieros:', e.message);
    }
  }

  // ── G. Headlines de México via NewsAPI ─────────────────────────────────
  try {
    const newsRes = await fetch(
      `https://newsapi.org/v2/top-headlines?country=mx&pageSize=15&apiKey=${env.NEWSAPI_KEY}`,
      { headers: { 'User-Agent': 'NodoInformativo-NewsBot/1.0 (https://www.nodoinformativo.lat)' } }
    );
    const newsData = await newsRes.json();
    const articles = newsData?.articles || [];

    const headlines = articles
      .filter(a => a.title && a.title !== '[Removed]')
      .slice(0, 12)
      .map(a => ({
        titulo: a.title.replace(/\s*[-–|]\s*[^-–|]+$/, '').trim(), // Quitar " - Fuente" del final
        url: a.url || null,
        fuente: a.source?.name || null
      }));

    if (headlines.length > 0) {
      const r = await fetch(`${API_BASE}/ticker/headlines`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${ADMIN_TOKEN}`
        },
        body: JSON.stringify(headlines)
      });
      console.log(`✅ Headlines actualizados: ${headlines.length} titulares (${r.status})`);
    }
  } catch (e) {
    console.error('Error headlines:', e.message);
  }

  return { success: true, financials: financials.length };
}

// ============================================================
// 6. Flujo Principal de Ingesta de Noticias
// ============================================================
async function runIngestion(env) {
  console.log("🎬 Iniciando ciclo de ingesta...");

  // A. Fetch de NewsAPI
  let articles = [];
  try {
    const newsRes = await fetch(
      `https://newsapi.org/v2/everything?q=${encodeURIComponent(env.NEWS_QUERY)}&language=es&pageSize=5&apiKey=${env.NEWSAPI_KEY}`,
      { headers: { 'User-Agent': 'NodoInformativo-NewsBot/1.0 (https://www.nodoinformativo.lat)' } }
    );
    if (!newsRes.ok) {
      const text = await newsRes.text();
      throw new Error(`NewsAPI HTTP ${newsRes.status}: ${text.substring(0, 150)}`);
    }
    const data = await newsRes.json();
    if (data.status === 'error') {
      throw new Error(`NewsAPI error: ${data.code} — ${data.message}`);
    }
    articles = Array.isArray(data.articles) ? data.articles : [];
    console.log(`📡 NewsAPI devolvió ${articles.length} artículos`);
  } catch (e) {
    console.error('❌ Error fetching NewsAPI:', e.message);
    return { success: false, error: e.message };
  }

  for (const art of articles) {
    if (await isDuplicate(env.DB, art.title)) {
      console.log(`⏭️ Duplicado: ${art.title.substring(0, 30)}`);
      continue;
    }

    console.log(`📝 Procesando: ${art.title.substring(0, 30)}`);
    const origId = crypto.randomUUID();

    // B. Guardar Original
    await env.DB.prepare(
      "INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, DESCRIPCION, URL_IMAGEN, FECHA, CONTENIDO, CATEGORIA, LONGITUD) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    ).bind(
      origId, art.url, art.title, art.description,
      art.urlToImage, art.publishedAt, art.content,
      env.DEFAULT_CATEGORY, (art.content || "").length
    ).run();

    // C. Parafrasear
    const paraphrased = await paraphraseWithAI(env, art);
    const status = paraphrased ? 'PENDIENTE' : 'ERROR_IA';
    const notas  = paraphrased
      ? 'IA: Procesado con Arcee Trinity'
      : 'Error: Requiere Validación Manual Forzada';

    // D. Enviar a Mesa de Revisión
    const sitios = (env.DEFAULT_SITES || "noticiasobjetivo,mexicoinformado,cbnnoticias,centralmexico,bitacoraurbana").split(',');
    for (const site of sitios) {
      await env.DB.prepare(
        "INSERT INTO REVISION_CONTENIDO (ID_ORIGEN, TIPO_ORIGEN, TITULO_PROPUESTO, DESCRIPCION_PROPUESTA, CONTENIDO_PROPUESTO, SITIO_DESTINO, CATEGORIA, ESTADO, NOTAS_REVISOR) VALUES (?, 'API', ?, ?, ?, ?, ?, ?, ?)"
      ).bind(
        origId, art.title, art.description,
        paraphrased || art.content, site.trim(),
        env.DEFAULT_CATEGORY, status, notas
      ).run();
    }
  }
  return { success: true };
}

// ============================================================
// 7. Refresco de caché RSS en KV
// ============================================================
const RSS_SITES = [
  'noticiasobjetivo', 'mexicoinformado', 'bitacoraurbana', 'nodoinformativo',
  'cbnnoticias', 'centralmexico', 'verticenoticias', 'radiocinconoticias',
  'reportecentralmx', 'tvmexico'
];

async function refreshRSSCache(env) {
  console.log('📡 Refrescando caché RSS...');
  const API_BASE    = env.API_BASE || 'https://news-api.sebastianvernis.workers.dev/api';
  const ADMIN_TOKEN = env.ADMIN_TOKEN || '';
  try {
    const res = await fetch(`${API_BASE}/rss/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${ADMIN_TOKEN}` }
    });
    const data = await res.json();
    console.log(`✅ Caché RSS invalidado: ${data.invalidated || 0} feeds (${res.status})`);
    // Pre-calentar los feeds (genera y guarda en KV)
    const warmUp = RSS_SITES.map(site =>
      fetch(`${API_BASE}/rss/${site}`, { headers: { 'User-Agent': 'NewsBot-CronWorker/1.0' } })
        .catch(e => console.error(`Warm-up RSS ${site}:`, e.message))
    );
    await Promise.allSettled(warmUp);
    console.log('✅ RSS warm-up completado para todos los sitios');
    return { success: true };
  } catch (e) {
    console.error('Error refrescando RSS:', e.message);
    return { success: false, error: e.message };
  }
}

// ============================================================
// Export
// ============================================================
export default {
  async scheduled(event, env, ctx) {
    // Ejecutar ingesta, ticker Y refresco RSS en paralelo
    ctx.waitUntil(Promise.all([
      runIngestion(env),
      runTickerUpdate(env),
      refreshRSSCache(env)
    ]));
  },

  // Disparo manual via URL para pruebas
  async fetch(request, env) {
    const url = new URL(request.url);

    // GET /ticker → solo actualizar ticker
    if (url.pathname === '/ticker') {
      return Response.json(await runTickerUpdate(env));
    }

    // GET /ingest → solo ingesta de noticias
    if (url.pathname === '/ingest') {
      return Response.json(await runIngestion(env));
    }

    // GET /rss → solo refresco de RSS
    if (url.pathname === '/rss') {
      return Response.json(await refreshRSSCache(env));
    }

    // GET / → los tres en paralelo
    const [ingestion, ticker, rss] = await Promise.all([
      runIngestion(env),
      runTickerUpdate(env),
      refreshRSSCache(env)
    ]);
    return Response.json({ ingestion, ticker, rss });
  }
};
