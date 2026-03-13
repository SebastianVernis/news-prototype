# Índice Documental - NexoPress

Plataforma de noticias multi-sitio con **27 sitios** gestionados desde Cloudflare Workers, D1 y Pages.

## Flujo de Publicación Actual

```
RSS Ingesta (3 artículos/30min) → Distribución Aleatoria (9 sitios/artículo) → Upload R2 → Sitios Web → Facebook (3h)
```

## Documentación Principal

| Guía | Descripción |
|------|-------------|
| [Monitor del Sistema](./SYSTEM_MONITOR.md) | Diagnóstico de crons, ingesta y Facebook |
| [Referencia de API](./API_REFERENCE.md) | Endpoints del Worker |
| [Gestión de Usuarios](./PASSWORD_RESET_SYSTEM.md) | Administradores y seguridad |
| [Arquitectura de Rutas](./ROUTE_DOCUMENTATION.md) | URLs en Pages y Worker |
| [Setup Facebook](./FACEBOOK_TOKEN_SETUP.md) | Configuración de tokens |

## Operación

- **Ingesta RSS**: Automática cada 30 min (3 artículos)
- **Distribución**: 9 sitios por artículo (aleatorio)
- **Facebook**: 1 publicación cada 3 horas por sitio
- **Imágenes**: Se suben a R2 automáticamente

## Estructura del Proyecto

```
src/              → Worker API (cron, routes, utils)
sites/            → 27 sitios Pages
public/admin/     → CMS dashboard
docs/             → Documentación
docs/archive/     → Historial de desarrollo
docs/migrations/  → Scripts SQL históricos
```

## URLs de Producción

- **API**: https://news-api.sebastianvernis.workers.dev
- **CMS**: https://cms.sebastianvernis.space/admin/
- **Worker Cron**: */30 * * * *
