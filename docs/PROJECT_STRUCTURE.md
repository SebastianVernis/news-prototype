# Estructura del Proyecto - NexoPress

## Descripcion General

NexoPress es una plataforma unificada para la gestion de **35 sitios de noticias** distribuidos en **3 CMS independientes**, operando sobre el ecosistema Cloudflare.

| CMS | Worker | Sitios | Rol |
|-----|--------|--------|-----|
| **CMS Originaux** | `news-api` | 10 | Sistema principal |
| **CMS Nuevos** | `cms-nuevos` | 17 | Segunda generacion |
| **CMS Nuevos 2** | `cms-nuevos2` | 8 | Tercera generacion |

---

## Raiz del Proyecto (`/`)

```
├── README.md               # Documentacion principal
├── package.json            # Dependencias Node.js
├── nexopress-portal/       # Portal de acceso a los 3 CMS
└── AGENTS.md               # Guia para agentes IA
```

---

## Carpetas Principales

### `src/` - Nucleo del Sistema (Worker Base)
- **index.js**: Worker principal que maneja la API, tareas programadas (Cron) y flujo de Facebook.
- **schema.sql**: Definicion de la base de datos D1.
- **wrangler.toml**: Configuracion de despliegue del backend.
- Los 3 CMS comparten la misma base de codigo; cada uno se despliega como un Worker independiente con sus propios bindings (D1, KV, R2).

### `public/` - Panel de Administracion (CMS Dashboard)
- **admin/**: Interfaz de gestion del sistema (PWA/SPA).
- Compartida entre los 3 CMS — cada Worker sirve la misma SPA.

### `nexopress-portal/` - Portal de Acceso Unificado
- Pagina estatica en Cloudflare Pages.
- Muestra los 3 CMS con sus sitios y enlaces de acceso directo.
- URL: https://nexopress.sebastianvernis.space

### `docs/` - Centro de Documentacion
- **INDEX.md**: Punto de entrada a toda la documentacion.
- **SYSTEM_MONITOR.md**: Guia del sistema de monitoreo.
- **API_REFERENCE.md**: Lista de endpoints y autenticacion.
- **archive/**: Documentacion historica, fases previas y docs obsoletas.

### `sites/` - Sitios de Noticias (Pages)
- Contiene las carpetas individuales para los 35 sitios.
- Organizados en `Estables/` (10 originaux) y `Nuevos/` (17 + 8).

### `tools/` y `scripts/` - Utilidades
- Herramientas auxiliares para mantenimiento, correcciones masivas y despliegues.

### `backups/` - Almacenamiento Local
- **archive/**: Archivos temporales, reportes antiguos y backups de DB.

---

## Flujo Operativo Actual (por CMS)

Cada CMS ejecuta el mismo flujo de forma independiente:

1. **Ingesta Automatica:** El Worker descarga noticias cada 30 min via RSS/Atom.
2. **IA:** Las noticias se procesan con Gemini para corregir estilo y gramatica.
3. **Distribucion:** Cada articulo se asigna aleatoriamente a ~9 sitios del CMS.
4. **Facebook:** El sistema selecciona articulos con "Imagen Perfecta" y los publica cada 3 horas.
5. **Dashboard:** El administrador supervisa todo desde el Monitor del Sistema de cada CMS.

Los 3 CMS se acceden desde el **Portal NexoPress** (https://nexopress.sebastianvernis.space).

---
**Ultima actualizacion**: Marzo 2026
