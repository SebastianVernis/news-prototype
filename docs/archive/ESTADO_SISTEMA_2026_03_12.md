# Estado del Sistema - NexoPress

**Fecha:** 2026-03-12 23:28 UTC  
**Versión Worker:** e456ab67-701d-44ec-a2f9-04a3ea485b30

---

## ✅ Sistema Operativo

### Cron Job (Cada 30 minutos)

| Tarea | Estado | Detalles |
|-------|--------|----------|
| **RSS Ingest** | ✅ OK | 0 articles (última ejecución) |
| **Facebook** | ✅ OK | 0/27 sitios (timers activos) |
| **Ticker** | ✅ OK | Actualizado correctamente |

**Próxima ejecución:** En ~2 minutos

---

## 📊 Métricas de Ingesta

### Artículos por Día

| Fecha | Cantidad |
|-------|----------|
| 2026-03-12 | 8 artículos |
| 2026-03-11 | 140 artículos |
| 2026-03-10 | 1 artículo |
| 2026-03-09 | 16 artículos |

**Total en base de datos:** ~428 artículos publicados

### Feeds RSS Activos

1. ✅ El País México
2. ✅ Expansión MX
3. ✅ Proceso (Nacional)
4. ✅ SinEmbargo

---

## 📘 Facebook Publishing

### Estado por Sitio

- **25/27 sitios** tienen Facebook activo y configurado
- **2 sitios** con Facebook desactivado: `enfoquedirecto`, `noticiashorizonte`

### Timers de Publicación

Cada sitio publica **1 artículo cada 3 horas**. Los timers están activos, por eso el cron muestra "0/27".

**Artículos pendientes de Facebook:** ~100+ artículos en cola

### URLs Correctas

✅ Fix implementado: Ahora usa `{site}.pages.dev` en lugar de `main.{site}.pages.dev`

Esto asegura que Facebook pueda scrapear los OG tags correctamente.

---

## 🔧 Fixes Implementados Hoy

### 1. Facebook URL Fix

**Problema:** La URL `main.{site}.pages.dev` no generaba OG tags.

**Solución:** Cambiar a `{site}.pages.dev` (producción)

**Archivos:**
- `src/cron/facebook.js` (línea 38)
- `src/routes/facebook.js` (líneas 269, 346)

### 2. RSS Ingest Bug Fix

**Problema:** Variables `imageUrl`, `isPaywall`, `html`, `content` sin inicializar.

**Solución:** Reescribir sección de scraping para inicializar variables correctamente.

**Archivo:** `src/cron/rss-ingest.js` (líneas 196-230)

---

## 📁 Artículos Recientes (Hoy)

1. **Caso Waldo's:** cambio en reglamento podría dejar libre a titular de Planeación Urbana de Hermosillo
   - Fuente: Proceso
   - Imagen: R2 ✅

2. **Alejandro Armenta acusa a Ricardo Salinas Pliego** de prostituir al Club Puebla
   - Fuente: Proceso
   - Imagen: R2 ✅

3. **Sheinbaum firma acuerdo con Google, Meta y TikTok** para combatir violencia digital contra mujeres
   - Fuente: Proceso
   - Imagen: R2 ✅

4. **Le explota el celular y cae de las escaleras** de la estación Camarones del Metro
   - Fuente: Proceso
   - Imagen: R2 ✅

5. **Congresistas de EU exigen a la FIFA reducir precios** de boletos para el Mundial 2026
   - Fuente: SinEmbargo
   - Imagen: R2 ✅

---

## 🎯 Próximas Acciones

### Automáticas (Cron)

- ⏳ RSS Ingest: En ~2 minutos
- ⏳ Facebook Timer: Cuando los timers expiren (3 horas)

### Manuales (Opcionales)

1. **Monitorear próxima ingesta RSS**
   ```bash
   curl https://news-api.sebastianvernis.workers.dev/api/cron/status
   ```

2. **Forzar publicación Facebook en un sitio**
   ```bash
   curl -X POST https://news-api.sebastianvernis.workers.dev/api/facebook/force-publish/radiocinconoticias
   ```

3. **Verificar OG tags de un artículo**
   ```bash
   curl https://radiocinconoticias.pages.dev/articulo/?slug=[SLUG] | grep "og:"
   ```

---

## 📈 Health Check

| Componente | Estado | Notas |
|------------|--------|-------|
| Worker API | ✅ | Deployed v e456ab67 |
| D1 Database | ✅ | 7.78 MB, 428 artículos |
| R2 Bucket | ✅ | Imágenes funcionando |
| KV Store | ✅ | Timers activos |
| RSS Feeds | ✅ | 4 feeds activos |
| Facebook | ✅ | 25/27 sitios activos |
| OG Tags | ✅ | Middleware funcionando |
| Cron Triggers | ✅ | Ejecutando cada 30 min |

---

## 🔍 Comandos de Diagnóstico

```bash
# Estado del cron
curl https://news-api.sebastianvernis.workers.dev/api/cron/status

# Artículos pendientes de Facebook
curl https://news-api.sebastianvernis.workers.dev/api/facebook/monitor

# Tokens de Facebook
curl https://news-api.sebastianvernis.workers.dev/api/facebook/debug-tokens

# Lista de sitios
curl https://news-api.sebastianvernis.workers.dev/api/sites

# Logs en vivo
wrangler tail news-api
```

---

**Resumen:** El sistema está funcionando correctamente. La ingesta RSS ingestó 8 artículos hoy, y Facebook está esperando a que los timers de 3 horas expiren para publicar.

**Última actualización:** 2026-03-12 23:28 UTC
