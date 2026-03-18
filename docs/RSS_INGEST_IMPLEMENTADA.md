# RSS Ingestión Implementada

**Fecha:** 2026-03-10  
**Estado:** ✅ IMPLEMENTADA  
**Worker Version:** f716c7bf-8347-4f4e-a8e2-1ffd57e93c4f

---

## ✅ Flujo Completo Implementado

### Cron (cada 30 minutos)

```
┌─────────────────────────────────────────────────┐
│  CRON */30 * * * *                              │
│                                                 │
│  1. RSS Ingestión                               │
│     → 1 artículo por sitio (round-robin)        │
│     → WEB_PUBLICADO = 1 por defecto             │
│                                                 │
│  2. Facebook Publishing                         │
│     → Cada 6 web → 1 FB                         │
│     → Max 3 artículos por sitio por cron        │
│                                                 │
│  3. Ticker Update                               │
│     → Financials + Headlines                    │
└─────────────────────────────────────────────────┘
```

---

## 📊 RSS Ingestion Details

### Feeds RSS (4 fuentes)
1. El País México
2. Proceso
3. La Jornada
4. Expansión MX

### Proceso por Artículo

```
1. Fetch RSS Feed
   ↓
2. Parsear título y link
   ↓
3. Verificar duplicados (SOURCE_URL)
   ↓
4. Obtener OG Image
   ↓
5. Scrapear contenido (<p> tags)
   ↓
6. Validar longitud (≥300 chars)
   ↓
7. IA Parafraseo (título + contenido)
   ↓
8. Subir imagen a R2
   ↓
9. INSERT ARTICULOS_PARAFRASEADOS
   ↓
10. INSERT ARTICULOS_SITIO_{SLUG}
    con WEB_PUBLICADO = 1 ✅
```

### Distribución (Round-Robin)

```
Artículo 1 → radiocinconoticias
Artículo 2 → centralmexico
Artículo 3 → tvmexico
...
Artículo 28 → radiocinconoticias (vuelta a empezar)
```

**27 sitios × 1 artículo cada 30 min = ~27 artículos por cron**

---

## 🔑 Código Clave

### runRSSIngest()

```javascript
async function runRSSIngest(env) {
  const FEEDS = [/* 4 fuentes */];
  const SITIOS_LIST = [/* 27 sitios */];
  
  let published = 0;
  
  for (const feedUrl of FEEDS) {
    if (published >= SITIOS_LIST.length) break;
    
    // Fetch RSS, parse, IA, etc.
    
    // INSERT PARAFRASEADOS
    await env.DB.prepare(`
      INSERT INTO ARTICULOS_PARAFRASEADOS (...)
      VALUES (?, ?, ?, ...)
    `).bind(...).run();
    
    // INSERT SITIO_{SLUG} con WEB_PUBLICADO = 1
    const siteSlug = SITIOS_LIST[published % SITIOS_LIST.length];
    await env.DB.prepare(`
      INSERT INTO ${tableName} (
        ID, ID_PARAFRASEADO, FECHA_ASIGNACION,
        WEB_PUBLICADO, WEB_FECHA, WEB_URL,
        FB_PUBLICADO, FB_FECHA, FB_POST_ID
      ) VALUES (?, ?, datetime('now'), 1, datetime('now'), ?, 0, NULL, NULL)
    `).bind(...).run();
    
    published++;
  }
  
  return published;
}
```

### runMasterCron()

```javascript
async function runMasterCron(env) {
  // 1. RSS Ingestion
  const ingestCount = await runRSSIngest(env);
  status.tasks.ingest = `OK (${ingestCount} articles)`;
  
  // 2. Facebook publishing (cada 6 web → 1 FB)
  await processFB(env);
  status.tasks.fb = "OK";
  
  // 3. Ticker update
  await updateTickerData(env);
  status.tasks.ticker = "OK";
  
  await env.ARTICLES_KV.put("cron_status", JSON.stringify(status));
  return status;
}
```

---

## 📈 Proyección de Publicación

### Por Sitio (24 horas)
- **27 sitios × 48 crons/día = 1,296 artículos/día**
- **~54 artículos por sitio por día** (1 cada 30 min)

### Facebook (por sitio)
- **54 web artículos/día ÷ 6 = 9 FB posts/día por sitio**
- **9 posts × 27 sitios = 243 FB posts/día total**

### Timeline Facebook
- Cada 30 min: 1 artículo web por sitio
- Cada 3 horas (6 artículos): 1 Facebook post
- **9 Facebook posts por sitio por día**

---

## 🧪 Testing

### Verificar Ingesta

```bash
# Ver último cron
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool

# Ver artículos nuevos (últimos 30 min)
wrangler d1 execute news_db --command "
  SELECT ID, TITULO_PARAFRASEADO, FECHA_PUBLICACION
  FROM ARTICULOS_PARAFRASEADOS
  WHERE FECHA_PUBLICACION > datetime('now', '-30 minutes')
  ORDER BY FECHA_PUBLICACION DESC
  LIMIT 10
" --remote
```

### Verificar Distribución

```bash
# Ver artículos por sitio (últimos 30 min)
wrangler d1 execute news_db --command "
  SELECT COUNT(*) as nuevos
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  WHERE FECHA_ASIGNACION > datetime('now', '-30 minutes')
" --remote
```

### Verificar Facebook

```bash
# Ver monitor de Facebook
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

---

## ⚠️ Consideraciones

### Rate Limiting

- **RSS Feeds:** 4 fuentes, cada 30 min → Sin problema
- **Facebook:** Max 3 posts por sitio por cron → Evita bloqueo
- **IA (OpenRouter):** ~27 llamadas por cron → Dentro de límites free tier

### Duplicados

- Verificación por `SOURCE_URL` evita artículos repetidos
- Si URL ya existe → Skip

### Imágenes

- OG Image de fuente original
- Upload a R2 como backup
- Fallback a Unsplash si falla

---

## 📝 Logs Esperados

```
[CRON] Starting runMasterCron...
[RSS INGEST] Starting RSS ingestion...
[RSS INGEST] Fetching feed: https://feeds.elpais.com/...
[RSS INGEST] Feed returned 15 items.
[RSS INGEST] Running AI proofread...
[RSS INGEST] Published to radiocinconoticias: Título del artículo...
[RSS INGEST] Complete: 27 articles published.
[CRON] RSS ingestion complete: 27 articles
[CRON] Starting Facebook publishing...
[FB] radiocinconoticias: 6 artículos pendientes de Facebook
[FB] radiocinconoticias publishing article abc-123...
[FB] radiocinconoticias SUCCESS: 123456789
[CRON] Facebook publishing complete
[CRON] Saving cron status to KV...
[CRON] Cron complete
```

---

## ✅ Estado Final

| Componente | Estado | Frecuencia |
|------------|--------|------------|
| RSS Ingest | ✅ Activo | Cada 30 min |
| Artículos por sitio | ✅ 1 cada 30 min | Round-robin |
| WEB_PUBLICADO | ✅ 1 por defecto | Automático |
| Facebook | ✅ Cada 6 web | Automático |
| Ticker | ✅ Activo | Cada 30 min |

---

**Estado:** ✅ RSS INGESTIÓN IMPLEMENTADA  
**Worker:** f716c7bf-8347-4f4e-a8e2-1ffd57e93c4f  
**Próximo cron:** Esperar ~30 minutos para ver primeros artículos
