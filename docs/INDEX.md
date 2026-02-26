# Índice Documental - NexoPress

Bienvenido a la documentación oficial del sistema **NexoPress**. Aquí encontrarás las guías necesarias para operar, mantener y escalar la red de 10 sitios de noticias.

## 📌 Documentación Principal

1.  **[Monitor del Sistema](./SYSTEM_MONITOR.md)**
    *   Guía de diagnóstico de crons, ingesta y Facebook.
    *   Cómo interpretar el dashboard de monitoreo.

2.  **[Referencia de API](./API_REFERENCE.md)**
    *   Listado completo de endpoints del Worker Unificado.
    *   Formatos de petición y autenticación.

3.  **[Gestión de Usuarios y Seguridad](./PASSWORD_RESET_SYSTEM.md)**
    *   Cómo crear administradores y recuperar contraseñas.
    *   Uso de tokens de seguridad.

4.  **[Arquitectura de Rutas](./ROUTE_DOCUMENTATION.md)**
    *   Cómo funcionan las URLs en los sitios Pages y el Worker.
    *   Configuración de `_routes.json`.

## 🛠️ Guías de Operación

- **Ingesta de Noticias:** La ingesta es automática cada 30 min. Para forzarla, usa el botón en el dashboard o el endpoint `POST /api/cron/ingest`.
- **Publicación en Facebook:** Se requiere un "Page Access Token" por sitio. Consulta el Monitor para ver el estado de los tokens.
- **Backups:** Los scripts de mantenimiento antiguos y backups SQL se encuentran en `backups/archive/`.

## 📁 Archivo Histórico
La documentación de las fases de desarrollo anteriores se ha movido a:
- `docs/archive/`

---
*NexoPress - Plataforma de alto rendimiento para el ecosistema Cloudflare.*
