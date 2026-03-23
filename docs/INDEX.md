# Indice Documental - NexoPress

Plataforma de noticias multi-sitio con **35 sitios** distribuidos en **3 CMS independientes**, gestionados con Cloudflare Workers, D1 y Pages.

## Arquitectura Operativa (3 CMS)

```
                    NexoPress Portal
                    nexopress.sebastianvernis.space
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     CMS Originaux      CMS Nuevos      CMS Nuevos 2
      10 sitios          17 sitios        8 sitios
      (news-api)        (cms-nuevos)    (cms-nuevos2)
```

Cada CMS es un Worker independiente con su propia base de datos D1, KV y cron jobs. El flujo es idéntico en los 3:

```
RSS Ingesta (3 articulos/30min) → Distribucion Aleatoria (9 sitios/articulo) → Upload R2 → Sitios Web → Facebook (3h)
```

## Documentacion Principal

- [README.md](../README.md)
- [Portal NexoPress](../nexopress-portal/README.md)

| Guia | Descripcion |
|------|-------------|
| [Monitor del Sistema](./SYSTEM_MONITOR.md) | Diagnostico de crons, ingesta y Facebook |
| [Referencia de API](./API_REFERENCE.md) | Endpoints del Worker |
| [Gestion de Usuarios](./PASSWORD_RESET_SYSTEM.md) | Administradores y seguridad |
| [Arquitectura de Rutas](./ROUTE_DOCUMENTATION.md) | URLs en Pages y Worker |
| [Setup Facebook](./FACEBOOK_TOKEN_SETUP.md) | Configuracion de tokens |

## Operacion

- **Ingesta RSS**: Automatica cada 30 min (3 articulos) — en cada CMS de forma independiente
- **Distribucion**: 9 sitios por articulo (aleatorio dentro de cada CMS)
- **Facebook**: 1 publicacion cada 3 horas por sitio
- **Imagenes**: Se suben a R2 automaticamente

## Estructura del Proyecto

```
src/              → Worker API (cron, routes, utils) — base para los 3 CMS
sites/            → 35 sitios Pages
nexopress-portal/ → Portal de acceso a los 3 CMS
public/admin/     → CMS dashboard (SPA compartida)
docs/             → Documentacion
docs/archive/     → Historial de desarrollo y docs obsoletas
docs/migrations/  → Scripts SQL historicos
```

## URLs de Produccion

| Servicio | URL |
|----------|-----|
| **Portal NexoPress** | https://nexopress.sebastianvernis.space |
| **CMS Originaux** | https://news-api.sebastianvernis.workers.dev/admin/ |
| **CMS Nuevos** | https://cms-nuevos.sebastianvernis.workers.dev/admin/ |
| **CMS Nuevos 2** | https://cms-nuevos2.sebastianvernis.workers.dev/admin/ |
| **API Originaux** | https://news-api.sebastianvernis.workers.dev |
| **API Nuevos** | https://cms-nuevos.sebastianvernis.workers.dev |
| **API Nuevos 2** | https://cms-nuevos2.sebastianvernis.workers.dev |

## Documentacion Archivada

Los siguientes documentos describen el flujo antiguo del CMS unico y se han movido a `docs/archive/`:
- `CMS_GUIDE.md` — Guia del CMS por sitio con tokens de 64 digitos (obsoleta)
- `CMS_VERIFICATION.md` — Verificacion del CMS por sitio (obsoleta)
