# Diagnóstico del Flujo de Facebook Publishing

**Fecha:** 2026-03-10 14:45 UTC  
**Estado:** ⚠️ PROBLEMA IDENTIFICADO

---

## 📊 Estado Actual

### Cron Status
```
Last Run: 2026-03-10T14:30:01.957Z
Next Run: 19 minutos
Tasks: fb=OK, ticker=OK
```

### Facebook Monitor
```
Total artículos en monitor: 6
Web publicados: 6
Facebook publicados: 6 ✅
Pendientes: 0 ✅
```

### Estado por Sitio (ejemplo de 5 sitios)

| Sitio | Total | WEB=1 | FB=1 | Pendientes |
|-------|-------|-------|------|------------|
| radiocinconoticias | 284 | 1 | 1 | 283 |
| centralmexico | 282 | 1 | 1 | 281 |
| tvmexico | 281 | 1 | 1 | 280 |
| cbnnoticias | 282 | 1 | 1 | 281 |
| mexicoinformado | 289 | 1 | 1 | 288 |

---

## 🐛 Problema Identificado

**Los artículos migrados NO tienen `WEB_PUBLICADO = 1`**

### Análisis

1. **Artículos de prueba (6)**: ✅ Funcionan perfectamente
   - Creados con distribución automática
   - `WEB_PUBLICADO = 1` por defecto
   - Facebook publicó correctamente

2. **Artículos migrados (~280 por sitio)**: ❌ No se publican
   - Migrados manualmente vía SQL
   - `WEB_PUBLICADO = 0` (o NULL)
   - El cron NO los ve porque filtra `WHERE WEB_PUBLICADO = 1`

---

## 🔍 Causa Raíz

El código de distribución (implementado hoy) establece `WEB_PUBLICADO = 1` por defecto:

```javascript
// Código NUEVO (funciona ✅)
INSERT INTO ARTICULOS_SITIO_{SLUG} (
  WEB_PUBLICADO, WEB_FECHA, WEB_URL, ...
) VALUES (?, ?, datetime('now'), ?, datetime('now'), ?, 1, ...)  -- ✅ WEB_PUBLICADO = 1
```

Pero los artículos migrados manualmente usaron:

```sql
-- Migración MANUAL (no funciona ❌)
INSERT INTO ARTICULOS_SITIO_{SLUG} (
  ID, ID_PARAFRASEADO, FECHA_ASIGNACION
  -- WEB_PUBLICADO no se especificó, default = 0
) VALUES (?, ?, datetime('now'))
```

---

## ✅ Solución

### Opción 1: Actualizar artículos existentes (Recomendado)

```sql
-- Para CADA sitio, actualizar WEB_PUBLICADO = 1
UPDATE ARTICULOS_SITIO_RADIOCINCONOTICIAS SET WEB_PUBLICADO = 1 WHERE WEB_PUBLICADO = 0;
UPDATE ARTICULOS_SITIO_CENTRALMEXICO SET WEB_PUBLICADO = 1 WHERE WEB_PUBLICADO = 0;
-- ... repetir para los 27 sitios
```

**Ventajas:**
- Simple y directo
- Todos los artículos existentes se publicarán en Facebook
- El cron los procesará automáticamente

**Desventajas:**
- ~280 artículos × 27 sitios = ~7,560 publicaciones de Facebook
- Puede tomar tiempo (el cron publica max 3 por ejecución)
- Posible rate limiting de Facebook

### Opción 2: Actualizar solo artículos recientes

```sql
-- Solo artículos de los últimos 7 días
UPDATE ARTICULOS_SITIO_RADIOCINCONOTICIAS 
SET WEB_PUBLICADO = 1 
WHERE WEB_PUBLICADO = 0 
  AND FECHA_ASIGNACION > datetime('now', '-7 days');
```

**Ventajas:**
- Menos publicaciones de Facebook
- Más controlado

**Desventajas:**
- Artículos antiguos nunca se publicarán en Facebook

### Opción 3: No hacer nada (Status Quo)

- Artículos migrados nunca se publicarán en Facebook
- Solo artículos nuevos (creados con distribución automática) se publicarán
- El sistema funciona correctamente para contenido nuevo

---

## 📋 Recomendación

**Opción 2: Actualizar solo artículos recientes (últimos 7 días)**

Razones:
1. Balance entre publicación histórica y volumen manejable
2. Evita saturar Facebook con miles de publicaciones antiguas
3. El contenido reciente es más relevante

---

## 🔧 Comandos para Implementar Solución

### Script de Actualización (Opción 2)

```bash
# Actualizar WEB_PUBLICADO = 1 para artículos recientes (7 días)
for site in radiocinconoticias centralmexico tvmexico cbnnoticias mexicoinformado nodoinformativo bitacoraurbana reportecentralmx verticenoticias noticiasobjetivo boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  echo "Actualizando $site..."
  wrangler d1 execute news_db --command "
    UPDATE ARTICULOS_SITIO_${site^^} 
    SET WEB_PUBLICADO = 1 
    WHERE WEB_PUBLICADO = 0 
      AND FECHA_ASIGNACION > datetime('now', '-7 days')
  " --remote
done

echo "✅ Actualización completada"
```

### Verificar Resultado

```bash
# Verificar cuántos artículos ahora tienen WEB_PUBLICADO = 1
wrangler d1 execute news_db --command "
  SELECT COUNT(*) as total, SUM(WEB_PUBLICADO) as web, SUM(FB_PUBLICADO) as fb
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS
" --remote
```

### Monitorear Facebook Publishing

```bash
# El cron publicará automáticamente cada 30 minutos
# Verificar estado
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool

# Ver monitor de Facebook
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

---

## ⏱️ Timeline Estimado (Opción 2)

Si hay ~50 artículos recientes por sitio:
- 50 artículos × 27 sitios = 1,350 publicaciones pendientes
- Cron publica 3 artículos por ejecución (cada 30 min)
- 1,350 ÷ 3 = 450 ejecuciones de cron
- 450 × 30 min = 13,500 minutos = **~9 días**

**Nota:** El cron publica max 3 artículos por sitio por ejecución, así que en realidad será más rápido.

---

## ✅ Conclusión

**El cron SÍ está funcionando correctamente.**

El problema es que los artículos migrados manualmente no tienen `WEB_PUBLICADO = 1`, por lo que el cron no los "ve".

**Solución:** Actualizar `WEB_PUBLICADO = 1` para artículos recientes (últimos 7 días).

---

**Estado:** ⚠️ REQUIERE ACCIÓN  
**Acción recomendada:** Ejecutar script de actualización para artículos recientes
