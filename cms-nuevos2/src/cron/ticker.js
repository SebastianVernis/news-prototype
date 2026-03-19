// src/cron/ticker.js — Actualización de datos del ticker financiero y titulares

// ============================================================
// updateTickerData — Obtiene datos financieros y titulares en tiempo real
// ============================================================
function normalizeHeadlineTitle(title) {
  if (!title || title === '[Removed]') return null;

  return String(title)
    .replace(/\s*[-|]\s*[^-|]+$/g, '')
    .replace(/^\s+|\s+$/g, '');
}

export async function updateTickerData(env) {
  const newsKey = env.NEWSAPI_KEY;
  const now = new Date().toISOString();
  const headlines = [];

  try {
    await env.DB.prepare(`
      CREATE TABLE IF NOT EXISTS TICKER_HEADLINES (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        TITULO TEXT NOT NULL,
        URL TEXT,
        FUENTE TEXT,
        FECHA_CREACION TEXT DEFAULT (datetime('now'))
      )
    `).run();
  } catch (_) {}

  // 1. Headlines (NewsAPI)
  if (newsKey) {
    try {
      const res = await fetch(
        `https://newsapi.org/v2/top-headlines?country=mx&pageSize=15&apiKey=${newsKey}`
      );
      const data = await res.json();
      for (const art of (data.articles || [])) {
        const title = normalizeHeadlineTitle(art.title);
        if (title) {
          headlines.push({
            titulo: title,
            url: art.url || null,
            fuente: art.source?.name || 'NewsAPI',
          });
        }
      }
    } catch (e) {
      console.error('[Ticker] Headlines error:', e.message);
    }
  }

  if (headlines.length === 0) {
    try {
      const fallback = await env.DB.prepare(`
        SELECT TITULO_PARAFRASEADO as TITULO, SLUG
        FROM ARTICULOS_PARAFRASEADOS
        WHERE ESTADO = 'PUBLICADO'
        ORDER BY FECHA_PUBLICACION DESC
        LIMIT 15
      `).all();

      for (const art of (fallback.results || [])) {
        const title = normalizeHeadlineTitle(art.TITULO);
        if (title) {
          headlines.push({
            titulo: title,
            url: art.SLUG ? `https://www.radiocinconoticias.click/articulo/?slug=${art.SLUG}` : null,
            fuente: 'NexoPress',
          });
        }
      }
    } catch (e) {
      console.error('[Ticker] Local fallback error:', e.message);
    }
  }

  if (headlines.length > 0) {
    const unique = [];
    const seen = new Set();

    for (const item of headlines) {
      const key = item.titulo.toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);
      unique.push(item);
      if (unique.length >= 15) break;
    }

    try {
      await env.DB.prepare('DELETE FROM TICKER_HEADLINES').run();
      for (const item of unique) {
        await env.DB.prepare(
          'INSERT INTO TICKER_HEADLINES (TITULO, URL, FUENTE, FECHA_CREACION) VALUES (?, ?, ?, ?)'
        ).bind(item.titulo, item.url, item.fuente, now).run();
      }
    } catch (e) {
      console.error('[Ticker] Persist headlines error:', e.message);
    }
  }

  // 2. Financials (Real-time)
  const financials = [];

  // A. USD/MXN
  try {
    const r = await fetch('https://open.er-api.com/v6/latest/USD');
    const d = await r.json();
    if (d?.rates?.MXN) {
      financials.push({
        simbolo: 'USD/MXN', nombre: 'Dólar',
        valor: d.rates.MXN.toFixed(2), cambio: '-0.01%', tendencia: 'down',
      });
    }
  } catch (_) {}

  // B. Bitcoin
  try {
    const r = await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    );
    const d = await r.json();
    if (d?.bitcoin?.usd) {
      financials.push({
        simbolo: 'BTC/USD', nombre: 'Bitcoin',
        valor: d.bitcoin.usd.toLocaleString(), cambio: '+0.00%', tendencia: 'up',
      });
    }
  } catch (_) {}

  // C. Yahoo Finance (Oro & Petróleo)
  const fetchYahoo = async (symbol) => {
    try {
      const r = await fetch(
        `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?interval=1d&range=2d`,
        { headers: { 'User-Agent': 'Mozilla/5.0' } }
      );
      const d = await r.json();
      const m = d?.chart?.result?.[0]?.meta;
      if (!m) return null;
      const price = m.regularMarketPrice;
      const prev  = m.chartPreviousClose || price;
      const pct   = prev ? ((price - prev) / prev) * 100 : 0;
      return { price, pct };
    } catch (_) { return null; }
  };

  const gold = await fetchYahoo('GC=F');
  if (gold) {
    financials.push({
      simbolo: 'ORO', nombre: 'Oro',
      valor: gold.price.toFixed(2),
      cambio: (gold.pct >= 0 ? '+' : '') + gold.pct.toFixed(2) + '%',
      tendencia: gold.pct >= 0 ? 'up' : 'down',
    });
  }

  const oil = await fetchYahoo('CL=F');
  if (oil) {
    financials.push({
      simbolo: 'PETROLEO', nombre: 'Petróleo WTI',
      valor: oil.price.toFixed(2),
      cambio: (oil.pct >= 0 ? '+' : '') + oil.pct.toFixed(2) + '%',
      tendencia: oil.pct >= 0 ? 'up' : 'down',
    });
  }

  for (const f of financials) {
    try {
      await env.DB.prepare(`
        INSERT INTO TICKER_FINANCIALS (SIMBOLO, NOMBRE, VALOR, CAMBIO, TENDENCIA, UNIDAD, FECHA_ACTUALIZACION)
        VALUES (?, ?, ?, ?, ?, 'MXN', ?)
        ON CONFLICT(SIMBOLO) DO UPDATE SET
          VALOR = excluded.VALOR,
          CAMBIO = excluded.CAMBIO,
          FECHA_ACTUALIZACION = excluded.FECHA_ACTUALIZACION
      `).bind(f.simbolo, f.nombre, f.valor, f.cambio, f.tendencia, now).run();
    } catch (_) {}
  }
}
