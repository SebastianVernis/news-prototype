# Referencia de API - NexoPress

Esta es la lista de endpoints disponibles en el worker unificado `news-api` (`src/index.js`). Todas las rutas (excepto login y health) requieren el header `Authorization: Bearer [ADMIN_TOKEN]`.

## 🔐 Autenticación
- `POST /api/auth/login`: Iniciar sesión.
- `POST /api/auth/users`: Crear usuario.
- `GET /api/auth/users`: Listar usuarios.
- `POST /api/auth/generate-password-token`: Generar link de recuperación.
- `GET /api/auth/validate-password-token`: Validar token de correo.
- `POST /api/auth/setup-password`: Establecer nueva contraseña.

## 📰 Artículos (Público/CMS)
- `GET /api/articles`: Listar artículos filtrados.
- `GET /api/articles/:slug`: Obtener artículo por slug.
- `GET /api/articles/id/:id`: Obtener artículo por ID.
- `POST /api/articles`: Crear artículo.
- `PUT /api/articles/:id`: Actualizar artículo.
- `DELETE /api/articles/:id`: Eliminar artículo.
- `POST /api/articles/bulk`: Carga masiva.
- `GET /api/articles/timeline`: Cronología de publicaciones.

## ✍️ Mesa de Revisión (Ingesta Automática)
- `GET /api/revision/pending`: Listar artículos pendientes de parafraseo/aprobación.
- `PUT /api/revision/:id`: Editar propuesta de revisión.
- `POST /api/revision/approve/:id`: Aprobar y publicar en los sitios elegidos.

## 📊 Dashboard y Estadísticas
- `GET /api/stats/dashboard`: Resumen de métricas para el home del CMS.
- `GET /api/health`: Estado de salud del worker (Público).

## 🚀 Automatización y Redes Sociales
- `GET /api/cron/status`: Estado de las últimas tareas programadas.
- `POST /api/cron/ingest`: Disparar ingesta manual de RSS/Atom.
- `GET /api/facebook/monitor`: Historial de publicaciones en Facebook.
- `GET /api/facebook/debug-tokens`: Diagnóstico de validez de secretos de FB.
- `POST /api/articles/publish-fb/:id`: Forzar publicación de un artículo en FB.

## 🌍 Sitios y Configuración
- `GET /api/sites`: Listar los 10 sitios configurados.
- `POST /api/sites`: Actualizar configuración de sitio.
- `GET /api/sites/legals/:id`: Textos legales del sitio.
- `GET /api/sites/channels/:id`: Canales externos.
- `GET /api/sites/menus/:id`: Menús de navegación.
- `GET /api/categories`: Listar categorías maestras.

## 📈 Ticker y Servicios
- `GET /api/ticker/financials`: Obtener datos de mercado (Dólar, BTC, etc.).
- `GET /api/ticker/headlines`: Obtener titulares de última hora.
- `GET /api/weather`: Obtener datos del clima (OpenWeather).
- `GET /api/rss/:site`: Generar feed RSS dinámico para un sitio.

## 🖼️ Multimedia
- `POST /api/upload`: Subir imagen a Cloudflare R2.
- `GET /api/images/*`: Proxy/Servidor de imágenes desde R2.

---
*Actualizado: 26 de Febrero, 2026*
