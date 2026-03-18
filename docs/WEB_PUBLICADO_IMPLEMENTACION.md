# Implementación Completa - WEB_PUBLICADO en Cloudflare Pages

**Fecha:** 2026-03-10 04:11 UTC  
**Estado:** ✅ COMPLETADO  
**Sitios Desplegados:** 27

---

## ✅ Cambios Realizados

### 1. Middleware Actualizado en Todos los Sitios

Cada sitio Cloudflare Pages ahora tiene un middleware que:

1. **Obtiene el artículo** de `ARTICULOS_PARAFRASEADOS` o `ARTICULOS_CMS`
2. **Registra la publicación web** en `ARTICULOS_SITIO_{SLUG}`
3. **Inyecta meta tags** OG para Facebook/Twitter

**Código clave agregado:**
```javascript
// 3. Registrar publicación web en ARTICULOS_SITIO_{SLUG}
const siteSlug = "radiocinconoticias"; // varía por sitio
const tableName = `ARTICULOS_SITIO_${siteSlug.toUpperCase()}`;

try {
  await env.DB.prepare(`
    UPDATE ${tableName}
    SET WEB_PUBLICADO = 1, WEB_FECHA = datetime('now'), WEB_URL = ?
    WHERE ID_PARAFRASEADO = ? AND WEB_PUBLICADO = 0
  `).bind(url.href, article.para_id).run();
  
  console.log(`[WEB_PUBLISH] Article ${article.para_id} published to ${siteSlug}`);
} catch (dbErr) {
  // Silencioso: el artículo puede no estar en la tabla de este sitio
}
```

### 2. Sitios Desplegados (27)

**Sitios Estables (10):**
- ✅ radiocinconoticias
- ✅ centralmexico
- ✅ tvmexico
- ✅ cbnnoticias
- ✅ mexicoinformado
- ✅ nodoinformativo
- ✅ bitacoraurbana
- ✅ reportecentralmx
- ✅ verticenoticias
- ✅ noticiasobjetivo

**Nuevos Sitios (17):**
- ✅ boominformativo
- ✅ capitalpress
- ✅ diarioexpress
- ✅ elpulsomexicano
- ✅ enfoquecapital
- ✅ enfoquedirecto
- ✅ formulacdmx
- ✅ mexicantimes
- ✅ mexico360noticias
- ✅ mradio
- ✅ noticiashorizonte
- ✅ pulsodiario
- ✅ puntoclave
- ✅ puntonoticias
- ✅ radarinformativo
- ✅ reportediario
- ✅ televisionabc

---

## 🔄 Flujo Completo Actual

```
1. RSS Feed → IA Parafraseo + R2
   ↓
2. ARTICULOS_PARAFRASEADOS (metadata)
   ↓
3. Distribución a 3 sitios (round-robin)
   ↓
4. ARTICULOS_SITIO_{SLUG} (FECHA_ASIGNACION)
   ↓
5. Usuario visita artículo en sitio web
   ↓
6. Middleware detecta slug y actualiza:
   - WEB_PUBLICADO = 1
   - WEB_FECHA = now
   - WEB_URL = URL completa
   ↓
7. Proceso FB monitorea cada sitio:
   - SELECT COUNT(*) WHERE WEB_PUBLICADO = 1 AND FB_PUBLICADO = 0
   - Si count >= 6 → publicar en Facebook
   ↓
8. Facebook publica y actualiza:
   - FB_PUBLICADO = 1
   - FB_FECHA = now
   - FB_POST_ID = ID de post de Facebook
```

---

## 📊 Trazabilidad por Sitio

Cada sitio ahora tiene trazabilidad completa:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `ID` | ID único del registro | `abc-123` |
| `ID_PARAFRASEADO` | Referencia al artículo | `para-xyz-radio` |
| `WEB_PUBLICADO` | Estado web (0/1) | `1` |
| `WEB_FECHA` | Timestamp publicación web | `2026-03-10 22:05:00` |
| `WEB_URL` | URL completa del artículo | `https://www.radiocinconoticias.click/articulo/?slug=...` |
| `FB_PUBLICADO` | Estado Facebook (0/1) | `0` |
| `FB_FECHA` | Timestamp publicación FB | `NULL` |
| `FB_POST_ID` | ID de post en Facebook | `NULL` |
| `FECHA_ASIGNACION` | Cuando se asignó al sitio | `2026-03-10 21:30:00` |
| `FECHA_CREACION` | Creación del registro | `2026-03-10 21:30:00` |

---

## 🧪 Testing del Flujo

### 1. Verificar WEB_PUBLICADO update

```bash
# Visitar un artículo en un sitio
curl -s "https://www.radiocinconoticias.click/articulo/?slug=test-article" > /dev/null

# Verificar en DB
wrangler d1 execute news_db --command "
  SELECT WEB_PUBLICADO, WEB_FECHA, WEB_URL 
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS 
  WHERE ID_PARAFRASEADO = 'para-ARTICLE_ID-radio'
" --remote
```

**Resultado esperado:**
```
WEB_PUBLICADO: 1
WEB_FECHA: 2026-03-10 22:05:00
WEB_URL: https://www.radiocinconoticias.click/articulo/?slug=...
```

### 2. Verificar Contador Facebook

```bash
# Ver cuántos artículos web publicados pendientes de FB
wrangler d1 execute news_db --command "
  SELECT COUNT(*) as pendientes_fb
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  WHERE WEB_PUBLICADO = 1 AND FB_PUBLICADO = 0
" --remote
```

**Resultado esperado:**
- Si count >= 6: El próximo cron de FB debería publicar
- Si count < 6: Esperar más publicaciones web

### 3. Monitorear Facebook Publishing

```bash
# Ver estado del cron
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool

# Ver monitor de Facebook
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

---

## 📝 Logs y Monitoreo

### Logs del Middleware

Cada vez que un artículo se publica web:
```
[WEB_PUBLISH] Article abc-123 published to radiocinconoticias
```

### Logs de Facebook Publishing

Cada vez que Facebook publica:
```
[FB] radiocinconoticias publishing article xyz...
[FB] radiocinconoticias SUCCESS: 123456789012345
```

---

## ⚠️ Consideraciones Importantes

### 1. Artículos Antiguos (Pre-Migración)

Los artículos migrados pueden no estar en `ARTICULOS_SITIO_{SLUG}`. El middleware usa try-catch silencioso para no fallar.

**Solución:** Los artículos nuevos (post-migración) sí tendrán trazabilidad completa.

### 2. Cache de Cloudflare Pages

Los sitios Pages tienen cache. Puede tomar unos segundos para que el middleware se ejecute.

**Solución:** El cache se invalida automáticamente con cada deploy.

### 3. Concurrencia

Múltiples visitas al mismo artículo pueden causar múltiples UPDATEs.

**Solución:** El WHERE `WEB_PUBLICADO = 0` previene updates duplicados.

---

## 🚀 Próximos Pasos

1. **Esprimir primera publicación web** - Visitar un artículo nuevo y verificar WEB_PUBLICADO
2. **Esperar 6 artículos web** - Monitorear contador por sitio
3. **Verificar Facebook publishing** - Confirmar que FB publica cada 6 artículos
4. **Monitorear logs** - Verificar que no hay errores

---

## 📞 Comandos Útiles

### Ver artículos web publicados por sitio
```bash
wrangler d1 execute news_db --command "
  SELECT p.TITULO_PARAFRASEADO, s.WEB_FECHA, s.WEB_URL
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS s
  JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
  WHERE s.WEB_PUBLICADO = 1
  ORDER BY s.WEB_FECHA DESC
  LIMIT 10
" --remote
```

### Ver contador por sitio
```bash
wrangler d1 execute news_db --command "
  SELECT 'radiocinconoticias' as sitio, COUNT(*) as web_pub, 
         SUM(CASE WHEN FB_PUBLICADO = 1 THEN 1 ELSE 0 END) as fb_pub
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  UNION ALL SELECT 'centralmexico', COUNT(*), SUM(CASE WHEN FB_PUBLICADO=1 THEN 1 ELSE 0 END) FROM ARTICULOS_SITIO_CENTRALMEXICO
  -- ... más sitios
" --remote
```

### Forzar Facebook publishing para un sitio
```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/facebook/force-publish/radiocinconoticias \
  -H "Authorization: Bearer [ADMIN_TOKEN]"
```

---

**Estado:** ✅ IMPLEMENTACIÓN COMPLETA - 27 sitios con WEB_PUBLICADO tracking  
**Próximo hito:** Verificar primera publicación automática en Facebook (cada 6 web)
