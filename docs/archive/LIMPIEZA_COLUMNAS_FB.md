# Limpieza de Columnas Facebook - Completada

**Fecha:** 2026-03-10 01:15 UTC  
**Estado:** ✅ COMPLETADO  
**Version:** 5071ee87-dd43-49ea-aae8-18720558ae74

---

## ✅ Cambios Realizados

### 1. Base de Datos - Columnas Eliminadas

**ARTICULOS_PARAFRASEADOS:**
- ❌ `FB_REQUERIDO` (eliminado)
- ❌ `FB_PUBLICADO` (eliminado)
- ❌ `FB_FECHA` (eliminado)
- ❌ `FB_SITIOS_PUBLICADOS` (eliminado)

**ARTICULOS_CMS:**
- ❌ `FB_PUBLICADO` (eliminado)
- ❌ `FB_FECHA` (eliminado)
- ❌ `FB_REQUERIDO` (eliminado)
- ❌ `FB_SITIOS_PUBLICADOS` (eliminado)

**ARTICULOS_ORIGINALES:**
- ✅ Sin cambios (nunca tuvo columnas FB)

### 2. Nueva Fuente de Verdad para Facebook

**ARTICULOS_SITIO_{SLUG} (27 tablas):**
- ✅ `WEB_PUBLICADO` - Estado de publicación web
- ✅ `WEB_FECHA` - Timestamp publicación web
- ✅ `WEB_URL` - URL del artículo publicado
- ✅ `FB_PUBLICADO` - Estado de publicación Facebook
- ✅ `FB_FECHA` - Timestamp publicación Facebook
- ✅ `FB_POST_ID` - ID de la publicación en Facebook
- ✅ `FECHA_ASIGNACION` - Cuando se asignó al sitio
- ✅ `FECHA_CREACION` - Timestamp de creación

---

## 🔄 Endpoints Actualizados

### `/articles/publish-fb/:id` (Legacy)
**Antes:** Marcaba artículos como `FB_REQUERIDO = 1` y publicaba inmediatamente

**Ahora:** Solo retorna información del artículo
```json
{
  "success": true,
  "message": "Facebook publishing is now managed per-site via ARTICULOS_SITIO tables",
  "article": { "id": "...", "title": "...", "slug": "..." }
}
```

### `/facebook/monitor`
**Antes:** Listaba artículos de PARAFRASEADOS y CMS con columnas FB

**Ahora:** Muestra estado por sitio desde tablas ARTICULOS_SITIO_{SLUG}
```json
[
  {
    "SITIO_ID": "...",
    "SITIO": "radiocinconoticias",
    "TITULO": "...",
    "WEB_PUBLICADO": 1,
    "WEB_FECHA": "2026-03-10T01:00:00Z",
    "FB_PUBLICADO": 0,
    "FB_POST_ID": null
  }
]
```

### `/facebook/force-publish/:siteSlug`
**Antes:** Buscaba en PARAFRASEADOS/CMS con FB_SITIOS_PUBLICADOS

**Ahora:** Busca en ARTICULOS_SITIO_{SLUG} artículos con WEB_PUBLICADO = 1 y FB_PUBLICADO = 0
```javascript
// Nuevo flujo:
SELECT FROM ARTICULOS_SITIO_{SLUG}
  WHERE WEB_PUBLICADO = 1 AND FB_PUBLICADO = 0
  → publishToFBIndividual()
  → UPDATE ARTICULOS_SITIO_{SLUG} SET FB_PUBLICADO = 1, FB_POST_ID = ?
```

---

## 📊 Estado del Sistema

### Tablas Limpias (Sin columnas FB)
```
✅ ARTICULOS_ORIGINALES (18 columnas)
✅ ARTICULOS_PARAFRASEADOS (18 columnas)
✅ ARTICULOS_CMS (13 columnas)
```

### Tablas con Control FB (Única fuente de verdad)
```
✅ ARTICULOS_SITIO_RADIOCINCONOTICIAS (10 columnas)
✅ ARTICULOS_SITIO_CENTRALMEXICO (10 columnas)
... (27 tablas en total)
```

---

## 🎯 Flujo Actual Limpio

```
ARTICULOS_ORIGINALES (fuente RSS)
  ↓ (IA parafraseo + R2)
ARTICULOS_PARAFRASEADOS (metadata limpia, SIN FB)
  ↓ (distribución a 3 sitios)
ARTICULOS_SITIO_{SLUG} (trazabilidad individual, CON FB)
  ↓ (web publishing)
WEB_PUBLICADO = 1, WEB_FECHA, WEB_URL
  ↓ (cada 6 artículos web)
FB_PUBLICADO = 1, FB_FECHA, FB_POST_ID
```

---

## ⚠️ Breaking Changes

### Lo Que Ya No Funciona

1. **Marcar artículos como FB_REQUERIDO manualmente**
   - Antes: `UPDATE ARTICULOS_PARAFRASEADOS SET FB_REQUERIDO = 1`
   - Ahora: Automático por sitio (cada 6 web → 1 FB)

2. **Consultar FB_PUBLICADO en PARAFRASEADOS/CMS**
   - Antes: `SELECT FB_PUBLICADO FROM ARTICULOS_PARAFRASEADOS`
   - Ahora: `SELECT FB_PUBLICADO FROM ARTICULOS_SITIO_{SLUG}`

3. **FB_SITIOS_PUBLICADOS como string**
   - Antes: `"radiocinconoticias,centralmexico"`
   - Ahora: Una fila por sitio en tabla individual

### Migración para Queries Existentes

```sql
-- ANTES (ya no funciona):
SELECT ID, TITULO, FB_PUBLICADO, FB_FECHA
FROM ARTICULOS_PARAFRASEADOS
WHERE FB_PUBLICADO = 0;

-- AHORA (correcto):
SELECT s.ID, p.TITULO_PARAFRASEADO as TITULO, s.FB_PUBLICADO, s.FB_FECHA
FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS s
JOIN ARTICULOS_PARAFRASEADOS p ON s.ID_PARAFRASEADO = p.ID
WHERE s.FB_PUBLICADO = 0;
```

---

## 🧪 Testing Post-Limpieza

### 1. Verificar columnas eliminadas
```bash
wrangler d1 execute news_db --command "PRAGMA table_info(ARTICULOS_PARAFRASEADOS)" --remote
# No debe mostrar: FB_REQUERIDO, FB_PUBLICADO, FB_FECHA, FB_SITIOS_PUBLICADOS
```

### 2. Verificar monitor de Facebook
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
# Debe mostrar artículos por sitio con WEB_PUBLICADO y FB_PUBLICADO
```

### 3. Verificar force-publish
```bash
curl -X POST https://news-api.sebastianvernis.workers.dev/api/facebook/force-publish/radiocinconoticias \
  -H "Authorization: Bearer [TOKEN]"
# Debe buscar en ARTICULOS_SITIO_RADIOCINCONOTICIAS
```

---

## 📝 Notas Importantes

### Por Qué Se Hizo Esta Limpieza

1. **Separación de responsabilidades:**
   - `ARTICULOS_PARAFRASEADOS`: Solo metadata del artículo
   - `ARTICULOS_SITIO_{SLUG}`: Trazabilidad por sitio (web + FB)

2. **Evitar errores de generalización:**
   - Antes: Un artículo multi-sitio con FB_SITIOS_PUBLICADOS como string
   - Ahora: Cada sitio tiene su propia fila con estado individual

3. **Trazabilidad completa:**
   - Antes: No se sabía cuándo se publicó en cada sitio
   - Ahora: WEB_FECHA y FB_FECHA por sitio individual

4. **FB_POST_ID correcto:**
   - Antes: Un solo ID para múltiples sitios (incorrecto)
   - Ahora: Un ID por sitio (correcto, cada post es único)

---

## 🚀 Deploy

**Comando:**
```bash
cd /home/sebastianvernis/cloudflare-news-project/src
wrangler deploy --config wrangler.toml
```

**Resultado:**
- ✅ Version: `5071ee87-dd43-49ea-aae8-18720558ae74`
- ✅ Columnas FB eliminadas de tablas antiguas
- ✅ Endpoints actualizados para nuevo esquema
- ✅ 27 tablas ARTICULOS_SITIO_{SLUG} como única fuente de verdad para FB

---

**Estado:** ✅ LIMPIEZA COMPLETADA - Sistema listo para operación normal
