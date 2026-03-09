# NexoPress - Sistema de Noticias Multi-Sitio (Cloudflare)

NexoPress es una plataforma de noticias de alto rendimiento diseñada íntegramente para el ecosistema de **Cloudflare**. Gestiona **27 sitios de noticias independientes** desde un único panel de administración y un núcleo centralizado en Cloudflare Workers y D1.

## 🚀 Arquitectura del Sistema

El proyecto se basa en una arquitectura de **Worker Unificado** que gestiona tanto la API como las tareas programadas (Cron Jobs).

- **Frontend:** 27 sitios estáticos en Cloudflare Pages (10 estables + 17 nuevos)
- **Backend (API):** Cloudflare Workers (Hono framework)
- **Base de Datos:** Cloudflare D1 (SQLite)
- **Almacenamiento:** Cloudflare R2 (Imágenes) y KV (Caché/Estado)
- **IA:** Integración con OpenRouter (Gemini 2.0 Flash) para corrección de estilo y parafraseo

## ✨ Características Principales

- **Ingesta Multi-Formato:** Soporte para RSS y Atom (El País, Proceso, Aristegui, etc.)
- **Parafraseo con IA:** Corrección automática de ortografía y gramática mediante IA
- **Flujo de Facebook Inteligente:**
  - Publicación automática cada 3 horas por sitio
  - Filtro de **"Imagen Perfecta"**: Solo publica en Facebook si el artículo tiene una imagen original (evita imágenes de relleno)
  - Tokens de página permanentes (Never Expire)
  - Soporte para 27 sitios independientes
- **Dashboard Administrativo:**
  - Gestión centralizada de 27 sitios
  - **Monitor de Sistema:** Seguimiento en tiempo real de crons, tokens de Facebook e historial de publicaciones
  - Ingesta manual forzada para diagnóstico
  - Editor universal de artículos
  - Mesa de revisión de contenido

## 🌐 Red de Sitios (27)

### Sitios Estables (10) - Operativos

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

### Nuevos Sitios (17) - Listos para Despliegue

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

## 📚 Documentación

Para una guía detallada sobre el funcionamiento del sistema, consulta:

| Documento | Descripción |
|-----------|-------------|
| [Índice Documental](./docs/INDEX.md) | Portal de toda la documentación |
| [Guía para Agentes IA](./QWEN.md) | Guía completa para agentes de IA |
| [Monitor de Sistema](./docs/SYSTEM_MONITOR.md) | Diagnóstico y monitoreo |
| [Referencia de API](./docs/API_REFERENCE.md) | Endpoints y autenticación |
| [27 Sitios Verificados](./27_SITIOS_VERIFICADOS.md) | Estado de implementación |

## 🛠️ Estructura del Proyecto

```
/home/sebastianvernis/cloudflare-news-project/
├── public/admin/           # Dashboard de Administración (CMS)
│   ├── views/              # Vistas HTML (dashboard, monitor, etc.)
│   ├── js/                 # Lógica del CMS (router, auth, editor)
│   └── css/                # Estilos del dashboard
├── src/
│   ├── index.js            # Worker Unificado (API + Cron + FB Flow)
│   ├── index_append.js     # Funciones adicionales
│   └── schema.sql          # Schema completo de D1
├── sites/
│   ├── Estables/           # 10 sitios operativos
│   └── Nuevos/             # 17 sitios listos para deploy
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
- `ADMIN_TOKEN`: Token maestro para administración del CMS

**Facebook Tokens (27 sitios):**
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

**Dashboard de Monitoreo:** https://cms.sebastianvernis.space/admin/#/monitor

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

## 🔐 Endpoints del CMS

| Ruta | Vista | Descripción |
|------|-------|-------------|
| `#/dashboard` | Dashboard | Métricas generales y accesos rápidos |
| `#/articles` | Artículos | Lista de artículos parafraseados |
| `#/cms` | CMS | Artículos creados manualmente |
| `#/revision` | Revisión | Mesa de revisión de contenido |
| `#/monitor` | Monitor | Estado del sistema en vivo |
| `#/sites` | Sitios | Gestión de los 27 sitios |
| `#/users` | Usuarios | Gestión de usuarios y roles |

**URL de Acceso:** https://cms.sebastianvernis.space/admin/

## 📈 Estado del Proyecto

| Componente | Estado | Descripción |
|------------|--------|-------------|
| **Worker API** | ✅ Operativo | API REST, Cron, Facebook Publishing |
| **10 Sitios Estables** | ✅ Operativos | Todos desplegados y funcionando |
| **17 Nuevos Sitios** | ✅ Listos | wrangler.toml, estructura y middleware completos |
| **Base de Datos D1** | ✅ Configurada | Schema completo con índices |
| **CMS Dashboard** | ✅ Operativo | SPA con editor universal |
| **Facebook Tokens** | ⚠️ Parcial | 10/27 configurados (17 pendientes) |

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
┌─────────────────────────────────────────────────────────────────┐
│                    Cloudflare Workers (27 sitios)               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              news-api (Worker Principal)                 │   │
│  │  - API REST (Hono framework)                            │   │
│  │  - Cron Jobs (cada 30 min)                              │   │
│  │  - Facebook Publishing (cada 3 horas x 27 sitios)       │   │
│  │  - RSS Ingestion & Feeds                                │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Cloudflare    │  │   Cloudflare    │  │   Cloudflare    │
│      D1         │  │      R2         │  │       KV        │
│  (SQLite DB)    │  │  (Imágenes)     │  │   (Caché)       │
│                 │  │                 │  │                 │
│ - SITIOS (27)   │  │ - uploads/      │  │ - cron_status   │
│ - ARTICULOS_    │  │ - auto/         │  │ - last_fb_post_ │
│ - REVISION_     │  │                 │  │ - session_      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Cloudflare Pages (27 sitios)                    │
│  Cada sitio tiene:                                              │
│  - Frontend estático (HTML/CSS/JS)                              │
│  - Functions para SSR (middleware de artículos)                 │
│  - Open Graph meta tags dinámicas                               │
│  - Dominio personalizado configurable                           │
└─────────────────────────────────────────────────────────────────┘
```

---

© 2026 NexoPress Network. Todos los derechos reservados.
