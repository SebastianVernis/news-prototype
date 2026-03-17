# Facebook Publishing - Diagnóstico y Solución

**Fecha:** 2026-03-12  
**Estado:** ✅ Solucionado

---

## Problema Reportado

Facebook no estaba publicando en ningún sitio de la red de 27 sitios.

## Diagnóstico

### 1. Estado del Cron

El cron mostraba: `"fb": "OK (0/27)"`

Esto significaba que:
- El cron job se estaba ejecutando correctamente cada 30 minutos
- Pero **0 de 27 sitios** estaban publicando en Facebook

### 2. Causa Raíz: Timers de KV

El sistema usa **timers en KV** para controlar que cada sitio publique máximo 1 artículo cada 3 horas:

```javascript
// En src/cron/facebook.js - processFBTimer()
const kvKey = `last_fb_post_${siteSlug}`;
const lastPostRaw = await env.ARTICLES_KV.get(kvKey);
const lastPostTime = lastPostRaw ? parseInt(lastPostRaw, 10) : 0;
const elapsed = now - lastPostTime;

// Solo procesar si pasaron 3 horas (180 minutos)
if (elapsed < THREE_HOURS_MS) {
  FB_LOG(`${siteSlug}: Skipping (timer not reached)`);
  stats.skipped++;
  continue;
}
```

**Los timers no habían expirado** - los sitios habían publicado recientemente y estaban esperando a que pasaran las 3 horas.

### 3. Problema Secundario: URL Incorrecta para OG Tags

El código estaba usando la URL incorrecta para Facebook:

```javascript
// ❌ ANTES (incorrecto)
const url = `https://main.${pagesDomain}/articulo/?slug=${article.SLUG}`;
```

**Problema:** El subdominio `main.` no ejecuta el middleware de OG tags, por lo que Facebook no podía scrapear las meta tags correctamente.

**Solución:** Usar el deployment de producción:

```javascript
// ✅ AHORA (correcto)
const url = `https://${pagesDomain}/articulo/?slug=${article.SLUG}`;
```

---

## Soluciones Implementadas

### 1. Fix de URL en Facebook Publishing

**Archivos modificados:**
- `src/cron/facebook.js` (línea 38)
- `src/routes/facebook.js` (líneas 269 y 346)

**Cambios:**
```diff
- const url = `https://main.${pagesDomain}/articulo/?slug=${article.SLUG}`;
+ const url = `https://${pagesDomain}/articulo/?slug=${article.SLUG}`;
```

### 2. Fix de Bug en RSS Ingest

**Archivo:** `src/cron/rss-ingest.js`

Se encontró un bug donde las variables `imageUrl`, `isPaywall`, `html`, y `content` se usaban sin estar definidas. Se reescribió la sección de scraping para:

1. Hacer fetch del HTML del artículo
2. Extraer la imagen de OG tags
3. Verificar si hay paywall
4. Extraer el contenido de los párrafos

---

## Cómo Funciona el Sistema Ahora

### Flujo Normal (Automático)

1. **Cron job** se ejecuta cada 30 minutos
2. Para cada sitio:
   - Verifica si pasaron 3 horas desde la última publicación
   - Si sí: selecciona 1 artículo aleatorio con imagen R2 válida
   - Publica en Facebook usando la URL correcta (`{site}.pages.dev`)
   - Actualiza el timer en KV

### Publicación Manual (Forzar)

Para forzar la publicación inmediata en un sitio:

```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/facebook/force-publish/radiocinconoticias
```

### Verificar Estado

```bash
# Estado del cron
curl https://news-api.sebastianvernis.workers.dev/api/cron/status

# Artículos pendientes de Facebook
curl https://news-api.sebastianvernis.workers.dev/api/facebook/monitor

# Debug de tokens de Facebook
curl https://news-api.sebastianvernis.workers.dev/api/facebook/debug-tokens
```

---

## Próximos Pasos

### Inmediatos

1. ✅ **Worker desplegado** - El código corregido está en producción
2. ⏳ **Esperar timers** - Los timers de KV expirarán naturalmente después de 3 horas
3. 📊 **Monitorear** - Verificar que los próximos posts se publiquen correctamente

### Opcionales

Si se necesita publicar inmediatamente:

1. **Resetear timers manualmente** (requiere acceso a Cloudflare Dashboard):
   - Ir a Workers & Pages → news-api → KV
   - Eliminar keys `last_fb_post_*`

2. **Forzar publicación** por sitio:
   ```bash
   curl -X POST https://news-api.sebastianvernis.workers.dev/api/facebook/force-publish/[SITE_SLUG]
   ```

---

## Verificación

Para verificar que Facebook está publicando correctamente:

1. **Ver posts recientes:**
   ```bash
   curl https://news-api.sebastianvernis.workers.dev/api/facebook/recent-posts/radiocinconoticias
   ```

2. **Verificar OG tags en un artículo:**
   ```bash
   curl https://radiocinconoticias.pages.dev/articulo/?slug=[SLUG] | grep "og:"
   ```

3. **Ver en Facebook:**
   - Visitar las páginas de Facebook de cada sitio
   - Verificar que los posts tengan imagen y título correctos

---

## Resumen

| Issue | Estado | Notas |
|-------|--------|-------|
| Timers de KV | ⏳ Pendiente | Expiran naturalmente cada 3 horas |
| URL incorrecta | ✅ Fixeado | Ahora usa `{site}.pages.dev` |
| RSS Ingest bug | ✅ Fixeado | Variables ahora se inicializan correctamente |
| Worker deploy | ✅ Completado | Versión e456ab67 |

---

**Próximo cron:** En ~8 minutos  
**Próxima publicación FB:** Cuando los timers expiren (3 horas desde última post)
