# Diagnóstico de Ingesta RSS - NexoPress

**Fecha:** 2026-03-12  
**Estado:** ⚠️ Investigando

---

## Síntoma

El cron muestra: `"ingest: OK (0 articles)"`

Esto significa que:
- ✅ El cron job se ejecuta correctamente cada 30 minutos
- ❌ Pero no se están ingiriendo artículos nuevos

---

## Posibles Causas

### 1. Artículos Ya Existen (SOURCE_URL duplicada)

El código verifica si la URL ya existe antes de ingerir:

```javascript
const urlExists = await env.DB.prepare(
  'SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE SOURCE_URL = ?'
).bind(link).first();

if (urlExists) {
  RSS_LOG(`Skip: Already exists (${link})`);
  continue;
}
```

**Verificación:**
```bash
wrangler d1 execute news_db --command "
  SELECT SOURCE_URL, COUNT(*) as count 
  FROM ARTICULOS_PARAFRASEADOS 
  GROUP BY SOURCE_URL 
  HAVING count > 1 
  ORDER BY count DESC 
  LIMIT 5
" --remote
```

### 2. Sin Imagen OG

El código salta artículos sin imagen OG:

```javascript
if (!imageUrl) {
  RSS_LOG('Skip: No OG Image, using fallback.');
  continue;
}
```

### 3. Contenido Muy Corto

El código requiere mínimo 300 caracteres:

```javascript
if (content.length < 300) {
  console.log(`[RSS INGEST] Skip: Content too short (${content.length} chars).`);
  continue;
}
```

### 4. Paywall Detectado

El código detecta y salta contenido con paywall:

```javascript
if (
  content.toLowerCase().includes('suscripción') ||
  content.toLowerCase().includes('premium') ||
  content.toLowerCase().includes('compartir tu cuenta')
) {
  console.log('[RSS INGEST] Skip: Paywall content detected');
  continue;
}
```

### 5. Error en IA

Si la IA falla, el artículo se salta:

```javascript
try {
  const aiTitle   = await proofreadTextAI(title, 'título', env);
  const aiContent = await proofreadTextAI(content, 'contenido', env);
  
  if (!aiTitle || !aiContent) {
    console.error('[RSS INGEST] AI returned empty results.');
    continue;
  }
} catch (aiErr) {
  console.error('[RSS INGEST] AI Error:', aiErr.message);
  continue;
}
```

---

## Feeds RSS Configurados

```javascript
const FEEDS = [
  'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada',
  'https://expansion.mx/rss',
  'https://www.proceso.com.mx/rss/feed.html?id=12',
  'https://www.sinembargo.mx/feed',
];
```

**Estado verificado:** ✅ Todos los feeds están accesibles y devolviendo XML válido.

---

## Artículos Ingestados por Día

```
2026-03-12: 8 artículos
2026-03-11: 140 artículos
2026-03-10: 1 artículo
2026-03-09: 16 artículos
2026-03-08: 15 artículos
```

**Análisis:**
- Ayer (Mar 11) se ingestaron 140 artículos - ¡funcionó bien!
- Hoy (Mar 12) solo 8 artículos - algo está pasando

---

## Posible Problema: TIMEOUT del Cron

El cron manual está haciendo timeout (60 segundos). Esto podría indicar:

1. **La IA está tardando demasiado** - Llama a 4 feeds × múltiples artículos
2. **Los feeds están muy grandes** - Más artículos de los esperados
3. **Rate limiting de la IA** - OpenRouter podría estar limitando requests

---

## Soluciones Propuestas

### 1. Agregar Logging Más Detallado

Agregar logs para ver por qué se saltan los artículos:

```javascript
RSS_LOG(`Processing: ${title} (${link})`);
RSS_LOG(`Image: ${imageUrl ? 'OK' : 'MISSING'}`);
RSS_LOG(`Content length: ${content.length} chars`);
```

### 2. Reducir Cantidad de Feeds

Si el timeout es el problema, reducir a 2 feeds:

```javascript
const FEEDS = [
  'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada',
  'https://expansion.mx/rss',
];
```

### 3. Aumentar Timeout del Cron

Los Cron Triggers de Workers tienen timeout de 15 minutos por defecto, pero el fetch puede timeoutear antes.

### 4. Verificar OpenRouter

```bash
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{"model": "google/gemini-2.0-flash-exp:free", "messages": [{"role": "user", "content": "test"}]}'
```

---

## Próximos Pasos

1. ✅ Verificar logs del Worker con `wrangler tail`
2. ✅ Verificar si OpenRouter está respondiendo
3. ✅ Revisar si los artículos nuevos tienen SOURCE_URL null
4. ⏳ Esperar próximo cron automático (en ~5 minutos)
5. 📊 Monitorear si se ingestan artículos

---

## Comandos Útiles

```bash
# Ver estado del cron
curl https://news-api.sebastianvernis.workers.dev/api/cron/status

# Ver artículos recientes
wrangler d1 execute news_db --command "
  SELECT TITULO_PARAFRASEADO, FECHA_PUBLICACION, SOURCE_URL 
  FROM ARTICULOS_PARAFRASEADOS 
  ORDER BY FECHA_PUBLICACION DESC 
  LIMIT 10
" --remote

# Ver logs en vivo
wrangler tail news-api

# Forzar ingesta manual (puede timeout)
curl https://news-api.sebastianvernis.workers.dev/api/cron/manual
```

---

**Última actualización:** 2026-03-12 23:25 UTC
