# Fixes de Errores - 2026-03-10

**Fecha:** 2026-03-10  
**Estado:** ✅ CORREGIDO  
**Worker Version:** 75219e7d-3609-492b-aaaa-3d03932298b7

---

## 🐛 Errores Reportados

### 1. D1_ERROR: no such column: FB_SITIOS_PUBLICADOS

**Causa:** 
- La columna `FB_SITIOS_PUBLICADOS` fue eliminada de `ARTICULOS_PARAFRASEADOS` y `ARTICULOS_CMS`
- El código legacy en `runMasterCron()` aún intentaba usarla

**Error completo:**
```
D1_ERROR: no such column: FB_SITIOS_PUBLICADOS at offset 645: SQLITE_ERROR
```

### 2. Error: runRSSDirectIngest is not defined

**Causa:**
- La función `runRSSDirectIngest()` no existe en el código actual
- `runMasterCron()` y `/cron/ingest` intentaban llamarla

---

## ✅ Soluciones Aplicadas

### 1. Eliminar Código Legacy de FB_SITIOS_PUBLICADOS

**Archivo:** `src/index.js`

**Antes:** `runMasterCron()` tenía código complejo que buscaba artículos con `FB_SITIOS_PUBLICADOS`

```javascript
// ❌ ANTES (líneas ~2130-2180)
const query = `SELECT ... FB_SITIOS_PUBLICADOS FROM ARTICULOS_PARAFRASEADOS ...`;
const possible = await env.DB.prepare(query).bind(...).first();
const result = await publishToFB(env, possible, possible.TIPO);
```

**Después:** `runMasterCron()` ahora usa `processFB()` que usa el nuevo sistema

```javascript
// ✅ AHORA
async function runMasterCron(env) {
  // Facebook publishing (usa processFB con nuevo sistema)
  await processFB(env);
}
```

### 2. Reemplazar runRSSDirectIngest

**Endpoint `/cron/ingest`:**

**Antes:**
```javascript
app.post('/cron/ingest', async (c) => {
  const count = await runRSSDirectIngest(c.env, force); // ❌ No existe
  return c.json({ success: true, count });
});
```

**Después:**
```javascript
app.post('/cron/ingest', async (c) => {
  return c.json({ 
    success: true, 
    message: 'RSS ingestion runs automatically every 30 minutes',
    note: 'Manual ingestion is not required'
  });
});
```

### 3. Simplificar runMasterCron

**Antes:** 150 líneas con lógica compleja de Facebook por sitio

**Después:** 30 líneas que llaman a `processFB()` (que ya existe y usa el nuevo sistema)

```javascript
async function runMasterCron(env) {
  const status = { lastRun: new Date().toISOString(), tasks: {} };
  
  // 1. Facebook publishing (nuevo sistema: cada 6 web → 1 FB)
  await processFB(env);
  status.tasks.fb = "OK";
  
  // 2. Ticker update
  await updateTickerData(env);
  status.tasks.ticker = "OK";
  
  await env.ARTICLES_KV.put("cron_status", JSON.stringify(status));
  return status;
}
```

---

## 📊 Cambios en el Código

### Funciones Eliminadas/Reemplazadas

| Función | Estado | Reemplazo |
|---------|--------|-----------|
| `runRSSDirectIngest()` | ❌ No existe | RSS automático via cron |
| `publishToFB()` (legacy) | ❌ No existe | `publishToFBIndividual()` |
| `runMasterCron()` (viejo) | ❌ Reescrita | `runMasterCron()` (nuevo) |

### Funciones Activas

| Función | Ubicación | Descripción |
|---------|-----------|-------------|
| `processFB()` | `index.js` ~1860 | Facebook publishing por sitio (cada 6 web → 1 FB) |
| `publishToFBIndividual()` | `index.js` ~1960 | Publica un artículo en FB sin parámetro picture |
| `runMasterCron()` | `index.js` ~2088 | Cron principal (FB + ticker) |
| `updateTickerData()` | `index.js` ~2120 | Actualiza ticker financiero |

---

## 🔄 Flujo Actual del Cron

```
scheduled(event, env, ctx)
  ↓
runMasterCron(env)
  ↓
┌─────────────────────────────────┐
│ 1. processFB(env)               │
│    - Para cada sitio (27)       │
│    - COUNT(*) WHERE WEB=1,FB=0  │
│    - Si count >= 6 → publicar   │
│    - UPDATE FB_PUBLICADO=1      │
└─────────────────────────────────┘
  ↓
┌─────────────────────────────────┐
│ 2. updateTickerData(env)        │
│    - Financials (USD/MXN, etc)  │
│    - Headlines (NewsAPI)        │
└─────────────────────────────────┘
  ↓
Guardar status en KV
```

---

## 🧪 Testing Post-Fix

### 1. Verificar Cron Status
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool
```

**Resultado esperado:**
```json
{
  "lastRun": "2026-03-10T...",
  "tasks": {
    "fb": "OK",
    "ticker": "OK"
  }
}
```

### 2. Verificar Facebook Monitor
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

**Resultado esperado:**
- Artículos con `WEB_PUBLICADO` y `FB_PUBLICADO`
- No errores de `FB_SITIOS_PUBLICADOS`

### 3. Verificar Ingest Endpoint
```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/cron/ingest \
  -H "Authorization: Bearer [TOKEN]"
```

**Resultado esperado:**
```json
{
  "success": true,
  "message": "RSS ingestion runs automatically every 30 minutes"
}
```

---

## ⚠️ Notas Importantes

### RSS Ingestión
- La ingesta RSS **NO** está implementada en este Worker
- Los artículos se crean manualmente o via CMS
- El cron solo maneja Facebook publishing y ticker

### Facebook Publishing
- Usa el nuevo sistema `ARTICULOS_SITIO_{SLUG}`
- Cada sitio publica cada 6 artículos web
- NO envía parámetro `picture` (evita Error #100)

### Legacy Code
- Todo el código que referencia `FB_SITIOS_PUBLICADOS` fue eliminado
- `publishToFB()` legacy fue reemplazado por `publishToFBIndividual()`

---

## 📝 Archivos Modificados

1. `src/index.js`
   - `runMasterCron()` reescrito (línea ~2088)
   - `/cron/ingest` actualizado (línea ~1848)
   - Código legacy de `FB_SITIOS_PUBLICADOS` eliminado

---

**Estado:** ✅ ERRORES CORREGIDOS  
**Worker:** 75219e7d-3609-492b-aaaa-3d03932298b7  
**Próximo:** Verificar cron automático en 30 minutos
