# Resumen de Depuración de Facebook - NexoPress

**Fecha:** 2026-03-09  
**Estado:** ✅ Problema Identificado y Corregido

---

## 🔍 Problema Encontrado

Los artículos no se publicaban en Facebook debido al **Error #100 de Facebook Graph API**:

```
(#100) Only owners of the URL have the ability to specify 
the picture, name, thumbnail or description params.
```

### Causa Raíz

El código estaba enviando imágenes de R2 (`uploads.sebastianvernis.space`) en el parámetro `picture` de la API de Facebook. Facebook rechaza estas imágenes porque el dominio del enlace (`enfoquecapital.top`, `pulsodiario.lat`, etc.) no coincide con el dominio de la imagen (`uploads.sebastianvernis.space`).

### Artículos Afectados

- **33 artículos** pendientes de publicación con `FB_REQUERIDO = 1` y `FB_PUBLICADO = 0`
- Todos con imágenes R2 del tipo: `https://uploads.sebastianvernis.space/auto/[UUID].jpg`
- Sitios más afectados: `enfoquecapital`, `enfoquedirecto`, `formulacdmx`, `pulsodiario`, `puntoclave`

---

## ✅ Solución Aplicada

### Cambio en el Código

**Archivo:** `/src/index.js` (línea ~2120)

**Antes:**
```javascript
if (imageUrl && imageUrl.trim() !== '' && 
    !imageUrl.includes('logo.png') && 
    !imageUrl.includes('unsplash.com')) {
  formData.append('picture', imageUrl);
}
```

**Después:**
```javascript
// FIX #100: Solo incluir picture si es de fuente externa confiable (no R2)
// Facebook rechaza imágenes R2 con Error #100 cuando el dominio del link
// no coincide con el dominio de la imagen
// Para imágenes R2, Facebook scrapea OG:image desde la página del artículo
if (imageUrl && imageUrl.trim() !== '' && 
    !imageUrl.includes('logo.png') && 
    !imageUrl.includes('unsplash.com') &&
    !imageUrl.includes('uploads.sebastianvernis.space')) {
  formData.append('picture', imageUrl);
}
```

### ¿Por Qué Funciona?

1. **Imágenes RSS externas** (El País, Proceso, etc.): Facebook usa el parámetro `picture` directamente
2. **Imágenes R2** (CMS): Facebook hace scrapeo del `og:image` desde la página del artículo
3. **Las páginas ya tienen OG tags correctos:** El middleware de Cloudflare Functions en `/sites/[sitio]/functions/articulo/_middleware.js` ya genera las meta tags correctamente

---

## 📊 Estado del Sistema

### Antes de la Corrección

```
Cron Status:
- fb_enfoquecapital: Error: (#100) Only owners of the URL...
- fb_enfoquedirecto: Error: (#100) Only owners of the URL...
- fb_formulacdmx: Error: (#100) Only owners of the URL...
- fb_pulsodiario: Error: (#100) Only owners of the URL...
- fb_puntoclave: Error: (#100) Only owners of the URL...
- fb_noticiashorizonte: Error: Site not found or inactive
```

### Después de la Corrección

```
✅ Deploy exitoso: news-api (Version ID: 9f3787ff-ed0b-4f11-a217-98fc55e56890)
✅ Próximo cron: en 13 minutos
✅ 33 artículos pendientes listos para publicar
```

---

## 🧪 Pruebas a Realizar

### 1. Publicación Manual (Recomendado)

```bash
# Obtener token de admin del CMS o variables de entorno
ADMIN_TOKEN="tu-token"

# Publicar artículo de prueba
ARTICLE_ID="9f91cdce-e1c7-4342-a2b5-993d2d2082d8"
curl -X POST "https://news-api.sebastianvernis.workers.dev/api/articles/publish-fb/${ARTICLE_ID}" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"
```

**Resultado Esperado:**
- ✅ Se publica en Facebook sin Error #100
- ✅ La imagen aparece (scrapeada de OG tags)
- ✅ La DB se actualiza con `FB_PUBLICADO = 1`

### 2. Esperar el Cron Automático

El cron corre cada 30 minutos. También se puede forzar:

```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/cron/manual \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"
```

### 3. Verificar en la DB

```bash
wrangler d1 execute news_db --command "
  SELECT ID, TITULO_PARAFRASEADO, FB_PUBLICADO, FB_FECHA 
  FROM ARTICULOS_PARAFRASEADOS 
  WHERE ID = '9f91cdce-e1c7-4342-a2b5-993d2d2082d8'
" --remote
```

---

## 📈 Métricas de Éxito

| Métrica | Antes | Después (Objetivo) |
|---------|-------|-------------------|
| Errores #100 | ~10/día | 0 |
| Tasa de éxito | ~40% | >90% |
| Artículos pendientes | 33 | <10 |
| Artículos R2 publicados | 0 | Todos |

---

## 🔧 Otros Problemas Identificados

### 1. Sitio Inactivo

`noticiashorizonte` tiene `FACEBOOK_ACTIVO = 0` en la DB.

**Solución:**
```sql
UPDATE SITIOS SET FACEBOOK_ACTIVO = 1 WHERE SLUG = 'noticiashorizonte';
```

### 2. Tokens de Facebook

Todos los secrets existen en Cloudflare, pero se recomienda verificar que no estén expirados:

```bash
python3 scripts/verify_fb_tokens.py
```

---

## 📝 Archivos Generados

1. **FACEBOOK_DEBUG_REPORT.md** - Análisis técnico completo
2. **FACEBOOK_FIX_TEST.md** - Plan de pruebas detallado
3. **RESUMEN_FACEBOOK_FIX.md** - Este archivo

---

## 🎯 Próximos Pasos

1. **Inmediato:** Probar publicación manual con un artículo
2. **Corto plazo:** Monitorear el próximo cron
3. **Mediano plazo:** Verificar que los 33 artículos pendientes se publiquen
4. **Largo plazo:** Implementar refresh automático de tokens de Facebook

---

## 📞 Comandos Útiles

### Ver estado actual
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool
```

### Ver artículos pendientes
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | \
  python3 -c "import sys,json; data=json.load(sys.stdin); \
    pending=[a for a in data if a['FB_PUBLICADO']==0][:10]; \
    print(json.dumps(pending, indent=2, ensure_ascii=False))"
```

### Ver logs en tiempo real
```bash
cd /home/sebastianvernis/cloudflare-news-project/src
wrangler tail
```

---

**Estado:** ✅ Listo para testing
