# Documentación Técnica: Monitoreo del Sistema (NexoPress)

NexoPress integra un sistema de monitoreo de grado industrial para garantizar que las noticias fluyan sin interrupciones y que las publicaciones en redes sociales se realicen correctamente.

## 📡 Endpoints de Monitoreo (Backend)

Todos los endpoints están integrados en el Worker `news-api` y requieren autenticación mediante el header `Authorization: Bearer [TOKEN]`.

### 1. Estado de Tareas Automáticas (Cron)
`GET /api/cron/status`
- **Función:** Recupera de Cloudflare KV el estado de la última ejecución programada.
- **Campos:** `lastRun`, `tasks.ingest`, `tasks.ticker`, `tasks.fb_[siteSlug]`.
- **Lógica:** Calcula también el tiempo restante para la próxima ejecución automática.

### 2. Diagnóstico de Tokens Facebook
`GET /api/facebook/debug-tokens`
- **Función:** Verifica la presencia de los 10 secretos `FB_TOKEN_[SITIO]` en el entorno de Cloudflare.
- **Uso:** Ideal para detectar si una clave ha sido borrada o no se ha configurado tras añadir un sitio nuevo.

### 3. Monitor de Historial de Facebook
`GET /api/facebook/monitor`
- **Función:** Combina artículos de `ARTICULOS_CMS` y `ARTICULOS_PARAFRASEADOS` filtrando los que han solicitado envío a Facebook.
- **Orden:** Los artículos más recientes primero.

### 4. Ingesta Manual Forzada
`POST /api/cron/ingest`
- **Función:** Dispara el proceso `runRSSDirectIngest` inmediatamente.
- **Uso:** Pruebas y diagnóstico de nuevos feeds RSS/Atom.

## 🖥️ Panel de Administración (Frontend)

Se ha añadido la sección **"Monitor Sistema"** en el sidebar del CMS.

- **Dashboard de Cron:** Muestra el resultado (OK/Error) de cada tarea del último ciclo de 30 minutos.
- **Malla de Tokens:** Iconos visuales (Verde/Rojo) que indican la disponibilidad de las API Keys de cada uno de los 10 sitios.
- **Historial Unificado:** Tabla que muestra el artículo, los sitios de destino y si el envío a Facebook fue exitoso o sigue pendiente.

## 🛠️ Lógica de Calidad Editorial (FB Filter)

El monitor también ayuda a supervisar la regla de **"Imagen Perfecta"**. El sistema detecta automáticamente si una noticia tiene una imagen original válida. Si usa una imagen de reserva (`fallback`), el monitor marcará la publicación como **Pendiente** y el proceso automático la ignorará para proteger la calidad estética de los perfiles de Facebook.

---
*Documentación actualizada: 26 de Febrero, 2026*
