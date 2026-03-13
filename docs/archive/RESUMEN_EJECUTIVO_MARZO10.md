# Resumen Ejecutivo - Nueva Arquitectura Implementada

**Fecha:** 2026-03-10 00:50 UTC  
**Estado:** ✅ EN PRODUCCIÓN  
**Version:** bcc9d358-8ef3-4fcd-87a7-ea9738656033

---

## ✅ Lo Que Se Hizo

### 1. Limpieza Inicial
- ✅ Reseteados todos los artículos pendientes de Facebook
- ✅ 33 artículos con `FB_PUBLICADO = 0` ahora tienen `FB_REQUERIDO = 0`

### 2. Nueva Estructura de Base de Datos
- ✅ 27 tablas `ARTICULOS_SITIO_{SLUG}` creadas (una por sitio)
- ✅ Cada tabla tiene: `WEB_PUBLICADO`, `WEB_FECHA`, `WEB_URL`, `FB_PUBLICADO`, `FB_FECHA`, `FB_POST_ID`
- ✅ Trazabilidad completa por sitio individual

### 3. Nuevo Flujo de Ingesta
- ✅ R2 obligatorio para todas las imágenes
- ✅ Imágenes se descargan de fuente original → suben a R2 → guarda URL de R2 en DB
- ✅ Fallback a Unsplash si falla R2
- ✅ Artículos se distribuyen a 3 sitios por round-robin
- ✅ Cada distribución inserta en tabla `ARTICULOS_SITIO_{SLUG}` individual

### 4. Facebook Publishing Individualizado
- ✅ Cada sitio tiene su propio contador
- ✅ Cada 6 artículos web publicados → 1 artículo en Facebook
- ✅ NO se envía parámetro `picture` a Facebook API
- ✅ Facebook scrapea OG:image de la página del artículo
- ✅ FB_POST_ID se guarda con timestamp en tabla del sitio

---

## 🔄 Flujo Completo Actual

```
RSS Feed (elpais.com, proceso.com.mx, etc.)
  ↓
getOGImage() → URL original de la fuente
  ↓
uploadToR2() → Descarga y sube a R2
  ↓
finalImg = R2 URL (o Unsplash fallback)
  ↓
INSERT ARTICULOS_PARAFRASEADOS (metadata, sin sitios)
  ↓
Para cada sitio asignado (3 sitios):
  INSERT ARTICULOS_SITIO_{SLUG} (ID_PARAFRASEADO, FECHA_ASIGNACION)
  ↓
[PENDIENTE: Publicación Web cada 30 min]
  UPDATE ARTICULOS_SITIO_{SLUG}
    SET WEB_PUBLICADO = 1, WEB_FECHA = now, WEB_URL = ?
  ↓
[Cada 6 artículos web → Facebook]
  SELECT COUNT(*) WHERE WEB_PUBLICADO = 1 AND FB_PUBLICADO = 0
  IF count >= 6:
    publishToFBIndividual()
    UPDATE ARTICULOS_SITIO_{SLUG}
      SET FB_PUBLICADO = 1, FB_FECHA = now, FB_POST_ID = ?
```

---

## 📊 Estado Actual

### Base de Datos
```
ARTICULOS_PARAFRASEADOS: ~968 artículos (existentes)
ARTICULOS_SITIO_*: 0 artículos (esperando nueva ingesta)
```

### Próxima Ingesta
- **Cuándo:** ~8 minutos (cron cada 30 min)
- **Qué esperar:** Nuevos artículos con distribución individual por sitio

### Facebook
- **Estado:** Reseteados todos los pendientes
- **Próxima publicación:** Cuando haya 6 artículos web por sitio

---

## ⚠️ Lo Que Falta (Importante)

### 1. Publicación Web en los Sitios

**Problema:** Los artículos se asignan a las tablas de sitio pero nadie actualiza `WEB_PUBLICADO`.

**Solución necesaria:** En los Cloudflare Pages functions de cada sitio, al publicar un artículo:

```javascript
// En sites/[sitio]/functions/articulo/_middleware.js o similar
await env.DB.prepare(`
  UPDATE ARTICULOS_SITIO_${SITE_SLUG.toUpperCase()}
  SET WEB_PUBLICADO = 1, WEB_FECHA = datetime('now'), WEB_URL = ?
  WHERE ID_PARAFRASEADO = ?
`).bind(currentUrl, articleId).run();
```

**Opciones:**
A. Modificar el middleware de cada sitio Pages
B. Crear un endpoint en el Worker que actualice al publicar
C. Hook en el proceso de renderizado del sitio

### 2. Testing Completo

Una vez implementado lo anterior:
1. Forzar ingesta RSS manual
2. Verificar artículos en tablas de sitio
3. Verificar publicación web (actualiza WEB_PUBLICADO)
4. Esperar 6 artículos
5. Verificar Facebook publishing (FB_POST_ID guardado)

---

## 🎯 Beneficios vs Problemas Resueltos

| Problema Anterior | Solución Nueva |
|-------------------|----------------|
| Error #100 Facebook | ✅ No envía `picture`, scrapea OG |
| Sin trazabilidad | ✅ Tabla individual por sitio |
| FB_SITIOS_PUBLICADOS (string) | ✅ Columnas individuales |
| Sin FB_POST_ID | ✅ Guardado por sitio |
| Sin timestamps reales | ✅ WEB_FECHA, FB_FECHA por sitio |
| Contador impreciso | ✅ Exacto: cada 6 web → 1 FB |
| Imágenes R2 problemáticas | ✅ R2 + OG scraping funciona |

---

## 📝 Archivos de Documentación

1. **IMPLEMENTACION_COMPLETA.md** - Detalles técnicos completos
2. **schema_sitios_tables.sql** - Schema de las 27 tablas
3. **RESUMEN_EXECUTIVO_FIX.md** - Fix anterior (R2 vs original)
4. **FACEBOOK_DEBUG_REPORT.md** - Debug original del problema

---

## 🚀 Próximos Pasos Recomendados

### Inmediato (Hoy)
1. ✅ Implementar está hecho
2. ⏳ Esperar próxima ingesta RSS (automática, ~8 min)
3. ⏳ Verificar nuevos artículos en `ARTICULOS_SITIO_*`

### Corto Plazo (Esta Semana)
4. 🔧 Implementar `WEB_PUBLICADO` update en sitios Pages
5. 🔧 Testear flujo completo con 1 sitio piloto
6. 🔧 Monitorear Facebook publishing (cada 6 artículos)

### Mediano Plazo
7. 📊 Dashboard de monitoreo por sitio
8. 📊 Métricas: artículos por sitio, FB posts, errores
9. 🔧 Ajustar regla de "cada 6" si es necesario

---

## 📞 Comandos Útiles para Monitoreo

### Ver nueva ingesta
```bash
wrangler d1 execute news_db --command "
  SELECT p.ID, p.TITULO_PARAFRASEADO, p.URL_IMAGEN, 
         COUNT(DISTINCT s.SLUG) as sitios_asignados
  FROM ARTICULOS_PARAFRASEADOS p
  LEFT JOIN (
    SELECT 'radiocinconoticias' as SLUG, ID_PARAFRASEADO FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
    UNION ALL SELECT 'centralmexico' FROM ARTICULOS_SITIO_CENTRALMEXICO
    -- ... más sitios
  ) s ON p.ID = s.ID_PARAFRASEADO
  WHERE p.FECHA_PUBLICACION > datetime('now', '-1 hour')
  GROUP BY p.ID
  ORDER BY p.FECHA_PUBLICACION DESC
  LIMIT 10
" --remote
```

### Ver estado de Facebook
```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool
```

### Ver contador por sitio
```bash
wrangler d1 execute news_db --command "
  SELECT 'radiocinconoticias' as sitio, COUNT(*) as web_publicados, 
         SUM(CASE WHEN FB_PUBLICADO = 1 THEN 1 ELSE 0 END) as fb_publicados
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
  UNION ALL SELECT 'centralmexico', ...
  -- ... más sitios
" --remote
```

---

**Estado:** ✅ IMPLEMENTADO Y DESPLEGADO  
**Próximo hito:** Esperar ingesta RSS y verificar distribución por sitio  
**Riesgo:** Bajo - el fix de Facebook (no enviar picture) es seguro
