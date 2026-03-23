# NexoPress - Sistema de Noticias Multi-Sitio (Cloudflare)

NexoPress es una plataforma de noticias de alto rendimiento diseñada íntegramente para el ecosistema de **Cloudflare**. Gestiona **35 sitios de noticias independientes** distribuidos en **3 paneles CMS** y un núcleo centralizado en Cloudflare Workers y D1.

**Portal de Administración:** https://nexopress.sebastianvernis.space

## 🚀 Arquitectura del Sistema

El proyecto se basa en una arquitectura de **Worker Unificado** que gestiona tanto la API como las tareas programadas (Cron Jobs).

- **Frontend:** 35 sitios estáticos en Cloudflare Pages (10 originaux + 17 nuevos + 8 nuevos 2)
- **Backend (API):** 3 Cloudflare Workers independientes (Hono framework)
- **Base de Datos:** Cloudflare D1 (SQLite) — una DB por CMS
- **Almacenamiento:** Cloudflare R2 (Imágenes) y KV (Caché/Estado)
- **IA:** Integración con OpenRouter (Gemini 2.0 Flash) para corrección de estilo y parafraseo
- **Portal:** NexoPress Portal — punto de entrada unificado a los 3 CMS

## ✨ Características Principales

- **Ingesta Multi-Formato:** Soporte para RSS y Atom (El País, Proceso, Aristegui, etc.)
- **Parafraseo con IA:** Corrección automática de ortografía y gramática mediante IA
- **Flujo de Facebook Inteligente:**
  - Publicación automática cada 3 horas por sitio
  - Filtro de **"Imagen Perfecta"**: Solo publica en Facebook si el artículo tiene una imagen original (evita imágenes de relleno)
  - Tokens de página permanentes (Never Expire)
  - Soporte para 27 sitios independientes
- **3 Dashboards Administrativos (CMS):**
  - **CMS Originaux** (10 sitios) — Sistema principal
  - **CMS Nuevos** (17 sitios) — Segunda generación
  - **CMS Nuevos 2** (8 sitios) — Tercera generación
  - Cada CMS con: Monitor de Sistema, Editor universal, Mesa de revisión, Ingesta manual
  - Portal NexoPress como punto de acceso unificado

## 🌐 Red de Sitios (35) — 3 CMS

### CMS Originaux (10 sitios) — Sistema Principal

| # | Sitio | Dominio | Slug |
|---|-------|---------|------|
| 1 | Radio Cinco Noticias | https://www.radiocinconoticias.click | `radiocinconoticias` |
| 2 | Central México | https://www.centralmexico.online | `centralmexico` |
| 3 | TV México | https://www.tvmexiconews.site | `tvmexico` |
| 4 | CBN Noticias | https://www.cbnnoticias.click | `cbnnoticias` |
| 5 | México Informado | https://www.mexicoinformado.lat | `mexicoinformado` |
| 6 | Nodo Informativo | https://www.nodoinformativo.lat | `nodoinformativo` |
| 7 | Bitácora Urbana | https://www.bitacoraurbana.lat | `bitacoraurbana` |
| 8 | Reporte Central MX | https://www.reportecentral.site | `reportecentralmx` |
| 9 | Vértice Noticias | https://www.verticenoticias.today | `verticenoticias` |
| 10 | Noticias Objetivo | https://www.noticiasobjetivo.click | `noticiasobjetivo` |

### CMS Nuevos (17 sitios) — Segunda Generación

| # | Sitio | Dominio | Slug |
|---|-------|---------|------|
| 11 | Boominformativo | https://www.boominformativo.site | `boominformativo` |
| 12 | Capital Press | https://www.capitalpress.mx | `capitalpress` |
| 13 | Diario Express | https://www.diarioexpress.news | `diarioexpress` |
| 14 | El Pulso Mexicano | https://www.elpulsomexicano.com | `elpulsomexicano` |
| 15 | Enfoque Capital | https://www.enfoquecapital.mx | `enfoquecapital` |
| 16 | Enfoque Directo | https://www.enfoquedirecto.news | `enfoquedirecto` |
| 17 | Fórmula CDMX | https://www.formulacdmx.mx | `formulacdmx` |
| 18 | The Mexican Times | https://www.mexicantimes.mx | `mexicantimes` |
| 19 | México 360 Noticias | https://www.mexico360noticias.mx | `mexico360noticias` |
| 20 | M Radio | https://www.mradio.mx | `mradio` |
| 21 | Noticias Horizonte | https://www.noticiashorizonte.mx | `noticiashorizonte` |
| 22 | Pulso Diario | https://www.pulsodiario.mx | `pulsodiario` |
| 23 | Punto Clave | https://www.puntoclave.mx | `puntoclave` |
| 24 | Punto Noticias | https://www.puntonoticias.mx | `puntonoticias` |
| 25 | Radar Informativo | https://www.radarinformativo.mx | `radarinformativo` |
| 26 | Reporte Diario | https://www.reportediario.mx | `reportediario` |
| 27 | Televisión ABC | https://www.televisionabc.mx | `televisionabc` |

### CMS Nuevos 2 (8 sitios) — Tercera Generación

| # | Sitio | Slug |
|---|-------|------|
| 28 | Centro News | `centronews` |
| 29 | Noticias 123 | `noticias123` |
| 30 | Breaking Center News México | `breakingcenternews` |
| 31 | A la Vista Noticias | `alavistanoticias` |
| 32 | Social Mexico News | `socialmexiconews` |
| 33 | TMZ News México | `tmznews` |
| 34 | Radio ABC | `radioabc` |
| 35 | Noticias Integra | `noticiasintegra` |

## 📚 Documentación

Para una guía detallada sobre el funcionamiento del sistema, consulta:

| Documento | Descripción |
|-----------|-------------|
| [Índice Documental](./docs/INDEX.md) | Portal de toda la documentación |
| [Guía para Agentes IA](./QWEN.md) | Guía completa para agentes de IA |
| [Monitor de Sistema](./docs/SYSTEM_MONITOR.md) | Diagnóstico y monitoreo |
| [Referencia de API](./docs/API_REFERENCE.md) | Endpoints y autenticación |
| [Portal NexoPress](./nexopress-portal/README.md) | Portal de acceso a los 3 CMS |

## 🛠️ Estructura del Proyecto

```
/home/sebastianvernis/cloudflare-news-project/
├── public/admin/           # Dashboard de Administración (CMS Originaux)
│   ├── views/              # Vistas HTML (dashboard, monitor, etc.)
│   ├── js/                 # Lógica del CMS (router, auth, editor)
│   └── css/                # Estilos del dashboard
├── nexopress-portal/       # Portal de acceso unificado a los 3 CMS
├── src/
│   ├── index.js            # Worker Principal (API + Cron + FB Flow)
│   ├── index_append.js     # Funciones adicionales
│   └── schema.sql          # Schema completo de D1
├── sites/
│   ├── Estables/           # 10 sitios (CMS Originaux)
│   └── Nuevos/             # 17 + 8 sitios (CMS Nuevos + CMS Nuevos 2)
├── scripts/
│   ├── setup/              # Scripts de configuración
│   ├── deploy/             # Scripts de despliegue
│   ├── verify/             # Scripts de verificación
│   └── fixes/              # Scripts de mantenimiento
├── docs/                   # Documentación técnica
├── backups/archive/        # Archivo de backups y scripts obsoletos
├── wrangler.toml           # Configuración de Cloudflare (referencia)
└── package.json            # Dependencias del proyecto
```

## ⚙️ Configuración y Despliegue

### Requisitos
- Cloudflare CLI (`wrangler`)
- Cuenta de OpenRouter (para la IA)
- Tokens de acceso a páginas de Facebook (27 sitios)

### Despliegue del Worker (API)
```bash
cd src
wrangler deploy --config wrangler.toml
```

### Despliegue de Sitios Pages

**Sitios Estables:**
```bash
for site in radiocinconoticias centralmexico tvmexico cbnnoticias mexicoinformado nodoinformativo bitacoraurbana reportecentralmx verticenoticias noticiasobjetivo; do
  cd sites/Estables/$site && wrangler pages deploy . --project-name=$site --branch=master && cd ../../..
done
```

**Nuevos Sitios:**
```bash
./scripts/deploy_new_sites.sh
```

### Variables de Entorno Críticas (Secrets)

**Generales:**
- `OPENROUTER_API_KEY`: Para el parafraseo e ingesta con IA
- `ADMIN_TOKEN`: Token maestro para administración de los CMS

**Facebook Tokens (35 sitios):**
```bash
# Sitios Estables (10)
wrangler secret put FB_TOKEN_RADIOCINCONOTICIAS --name news-api
wrangler secret put FB_TOKEN_CENTRALMEXICO --name news-api
wrangler secret put FB_TOKEN_TVMEXICO --name news-api
wrangler secret put FB_TOKEN_CBNNOTICIAS --name news-api
wrangler secret put FB_TOKEN_MEXICOINFORMADO --name news-api
wrangler secret put FB_TOKEN_NODOINFORMATIVO --name news-api
wrangler secret put FB_TOKEN_BITACORAURBANA --name news-api
wrangler secret put FB_TOKEN_REPORTECENTRALMX --name news-api
wrangler secret put FB_TOKEN_VERTICENOTICIAS --name news-api
wrangler secret put FB_TOKEN_NOTICIASOBJETIVO --name news-api

# Nuevos Sitios (17)
wrangler secret put FB_TOKEN_BOOMINFORMATIVO --name news-api
wrangler secret put FB_TOKEN_CAPITALPRESS --name news-api
wrangler secret put FB_TOKEN_DIARIOEXPRESS --name news-api
# ... (ver QWEN.md para lista completa)
```

**Configuración automática de tokens:**
```bash
python3 scripts/setup_fb_tokens.py
```

## 📊 Monitoreo

El sistema incluye endpoints de diagnóstico protegidos:

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/cron/status` | GET | Estado de las últimas tareas automáticas |
| `/api/facebook/monitor` | GET | Monitor de publicaciones en Facebook |
| `/api/facebook/debug-tokens` | GET | Verifica la validez de los tokens de Facebook |
| `/api/cron/ingest` | POST | Dispara una ingesta manual de noticias |
| `/api/cron/manual` | POST | Ejecuta el cron manualmente |

**Portal NexoPress:** https://nexopress.sebastianvernis.space
**Dashboard Originaux:** https://news-api.sebastianvernis.workers.dev/admin/#/monitor
**Dashboard Nuevos:** https://cms-nuevos.sebastianvernis.workers.dev/admin/#/monitor
**Dashboard Nuevos 2:** https://cms-nuevos2.sebastianvernis.workers.dev/admin/#/monitor

## 🔧 Comandos Útiles

### Desarrollo Local
```bash
# Worker en local
cd src && wrangler dev --config wrangler.toml

# Pages en local
cd sites/Estables/[sitio] && wrangler pages dev .
```

### Producción
```bash
# Deploy del Worker
cd src && wrangler deploy

# Deploy de un sitio
cd sites/Estables/[sitio] && wrangler pages deploy . --project-name=[sitio] --branch=master

# Ver logs en vivo
wrangler tail --name news-api
```

### Base de Datos
```bash
# Query directa
wrangler d1 execute news_db --command "SELECT COUNT(*) FROM ARTICULOS_PARAFRASEADOS" --remote

# Backup
wrangler d1 export news_db --output backup.sql --remote
```

### Verificación
```bash
# Verificar 27 sitios
python3 scripts/verify_27_sites.py

# Reporte de Facebook
python3 scripts/fb_full_report.py

# Ver estado del cron
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status
```

## 🔐 Paneles CMS (Rutas internas)

Cada uno de los 3 CMS comparte la misma estructura de vistas SPA:

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `#/dashboard` | Dashboard | Métricas generales y accesos rápidos |
| `#/articles` | Artículos | Lista de artículos parafraseados |
| `#/cms` | CMS | Artículos creados manualmente |
| `#/revision` | Revisión | Mesa de revisión de contenido |
| `#/monitor` | Monitor | Estado del sistema en vivo |
| `#/sites` | Sitios | Gestión de sitios del CMS |
| `#/users` | Usuarios | Gestión de usuarios y roles |

**URLs de Acceso:**

| CMS | URL | Sitios |
|-----|-----|--------|
| **Portal NexoPress** | https://nexopress.sebastianvernis.space | Punto de entrada |
| **CMS Originaux** | https://news-api.sebastianvernis.workers.dev/admin/ | 10 sitios |
| **CMS Nuevos** | https://cms-nuevos.sebastianvernis.workers.dev/admin/ | 17 sitios |
| **CMS Nuevos 2** | https://cms-nuevos2.sebastianvernis.workers.dev/admin/ | 8 sitios |

## 📈 Estado del Proyecto

| Componente | Estado | Descripción |
|------------|--------|-------------|
| **Workers API (x3)** | ✅ Operativos | 3 Workers independientes (Originaux, Nuevos, Nuevos 2) |
| **10 Sitios Originaux** | ✅ Operativos | Todos desplegados y funcionando |
| **17 Sitios Nuevos** | ✅ Operativos | Desplegados con CMS Nuevos |
| **8 Sitios Nuevos 2** | ✅ Operativos | Desplegados con CMS Nuevos 2 |
| **Base de Datos D1** | ✅ Configurada | Una DB por CMS, schema completo |
| **Portal NexoPress** | ✅ Operativo | Punto de entrada a los 3 CMS |
| **Facebook Tokens** | ✅ Configurados | 24/35 con tokens activos |

## 📝 Scripts Disponibles

| Script | Propósito |
|--------|-----------|
| `scripts/setup_fb_tokens.py` | Configurar tokens de Facebook interactivamente |
| `scripts/verify_fb_tokens.py` | Verificar validez de tokens FB |
| `scripts/verify_27_sites.py` | Verificación completa de los 27 sitios |
| `scripts/deploy_new_sites.sh` | Despliegue automático de 17 nuevos sitios |
| `scripts/fb_full_report.py` | Reporte completo de publicaciones en Facebook |
| `scripts/reset_fb_timers.py` | Resetear timers de Facebook |
| `scripts/force_reset_and_ingest.py` | Forzar reset y ingesta manual |

## 🏗️ Arquitectura

```
                    ┌─────────────────────────┐
                    │   NexoPress Portal      │
                    │  nexopress.sebastian     │
                    │  vernis.space            │
                    └────────┬────────────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
┌───────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  CMS Originaux    │ │  CMS Nuevos      │ │  CMS Nuevos 2    │
│  (news-api)       │ │  (cms-nuevos)    │ │  (cms-nuevos2)   │
│  10 sitios        │ │  17 sitios       │ │  8 sitios        │
│  API + Cron + FB  │ │  API + Cron + FB │ │  API + Cron + FB │
└────────┬──────────┘ └────────┬─────────┘ └────────┬─────────┘
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   D1 (DB)       │  │   R2 (Imgs)     │  │   KV (Caché)    │
│   × 3 DBs       │  │   Compartido    │  │   × 3 KVs       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Cloudflare Pages (35 sitios)                    │
│  Cada sitio tiene:                                              │
│  - Frontend estático (HTML/CSS/JS)                              │
│  - Functions para SSR (middleware de artículos)                 │
│  - Open Graph meta tags dinámicas                               │
│  - Dominio personalizado configurable                           │
└─────────────────────────────────────────────────────────────────┘
```

---

© 2026 NexoPress Network. Todos los derechos reservados.
