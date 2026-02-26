# Estructura del Proyecto

## Descripción General

Este es un proyecto de Cloudflare News que integra Cloudflare Workers, Pages, D1 Database, R2 Storage y herramientas de procesamiento de noticias.

---

## Raíz del Proyecto (`/`)

```
├── wrangler.toml           # Configuración de Cloudflare
├── package.json            # Dependencias Node.js
├── .env                    # Variables de entorno (local)
├── .dev.vars               # Variables de desarrollo (Wrangler)
├── README.md               # Documentación principal
├── TODO.md                 # Lista de tareas pendientes
├── AGENTS.md               # Directrices para agentes/colaboradores
└── PROJECT_STRUCTURE.md    # Este archivo
```

---

## Carpetas Principales

### 📁 `src/` - Código del Worker API
- **Contenido**: Cloudflare Worker principal (`index.js`)
- **Propósito**: Endpoints API para ingesta, paráfrasis, filtros de artículos
- **Subcarpetas**:
  - `wrangler.toml` - Configuración específica del Worker

### 📁 `public/` - Sitio Estático (Cloudflare Pages)
- **Contenido**: `index.html`, `admin.html`, `script.js`, estilos CSS
- **Propósito**: Interfaz web (CMS + sitio público)
- **Se despliega en**: Raíz del dominio

### 📁 `tools/` - Utilidades Python Organizadas
```
tools/
├── news/                   # Scripts de descarga de noticias
│   ├── master-news-flow.py # Orquestador principal
│   ├── newsapi.py
│   ├── newsdata.py
│   └── worldnews.py
├── site/                   # Generador de sitios
│   └── generate-sites.py
├── images/                 # Manejo de imágenes
│   ├── cache_original_images.py
│   └── resize_images.py
└── api/                    # Utilidades API
    ├── newsapi.py
    ├── newsdata.py
    └── worldnews.py
```

### 📁 `scripts/` - Scripts Organizados por Función
```
scripts/
├── deploy/                 # Scripts de despliegue
│   ├── deploy.sh
│   ├── deploy_all_sites.sh
│   ├── deploy_preview.sh
│   ├── deploy_to_cloudflare.py
│   ├── run-news-pipeline.sh
│   └── download_and_seed_example.sh
├── fixes/                  # Scripts de corrección/mantenimiento
│   ├── fix_article_links.py
│   ├── fix_article_logos.py
│   ├── fix_urls.py
│   ├── fix_duplicates.py
│   └── ... (y más)
├── utilities/              # Herramientas generales
│   ├── seed_db.py
│   ├── regenerate_index.py
│   ├── news-downloader.js
│   ├── seed_news_to_db.js
│   ├── serve-admin.js
│   ├── *.sql              # Scripts SQL
│   └── ... (y más)
└── archive/               # Scripts deprecados/antigos
```

### 📁 `docs/` - Documentación
```
docs/
├── INDEX.md                      # Índice de documentación
├── DOCUMENTACION.md              # Documentación general
├── IMPLEMENTACION_FINAL.md       # Notas de implementación
├── DEPLOYMENT_SUMMARY.md         # Resumen de despliegues
├── GEMINI.md                     # Notas sobre Gemini
├── QWEN.md                       # Notas sobre Qwen
├── PROJET_SUMMARY.md             # Resumen del proyecto
├── legal/                        # Documentos legales
│   └── TEXTOS_LEGALES.md
└── ... (más documentación)
```

### 📁 `data/` - Datos y Registros
```
data/
├── newsapi_*.csv/.json           # Descargas de noticias
├── noticias_paraphased_*.json    # Noticias procesadas
├── logs/                         # Registros de ejecución
├── news_queue/                   # Cola de noticias pendientes
├── published_news/               # Noticias ya publicadas
└── sites_metadata/               # Metadata de sitios
```

### 📁 `sites/` - Sitios Generados
```
sites/
├── site_1/
│   ├── index.html
│   ├── logo.png
│   └── site_config.json
├── site_2/
│   ├── index.html
│   ├── logo.png
│   └── site_config.json
└── ... (uno por cada sitio)
```

### 📁 `assets/` - Recursos Estáticos
```
assets/
└── images/                 # Caché de imágenes de artículos
    └── *.jpg/png
```

### 📁 `workers/` - Worker Adicionales (si los hay)
- Código de Cloudflare Workers adicionales

### 📁 `tests/` - Pruebas Automatizadas
- Test suite del proyecto

### 📁 `backups/` - Copias de Seguridad
- Backups de BD, configuración, etc.

### 📁 `.crush/`, `.wrangler/`, `dist/`, `build/`, `node_modules/` - Sistema
- Generados por Wrangler, npm y build tools
- No deben versionarse (en `.gitignore`)

---

## Flujo de Trabajo Típico

### 1. **Descarga y Procesamiento de Noticias**
```bash
python tools/news/master-news-flow.py \
  --source newsapi \
  --query "technology" \
  --count 50
```

### 2. **Ingesta en BD**
```bash
# Vía API
curl -X POST http://localhost:8787/api/ingest \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d @data/noticias_paraphased.json
```

### 3. **Generar Sitios**
```bash
python tools/site/generate-sites.py \
  --data data/noticias_*.json \
  --output sites/
```

### 4. **Desplegar**
```bash
npm run deploy              # Deploy Pages a Cloudflare
wrangler deploy src/index.js  # Deploy Worker API
```

---

## Variables de Entorno

### `.dev.vars` (desarrollo local)
```
ADMIN_TOKEN=tu_token_secreto
NEWSAPI_KEY=key_aqui
WORLDNEWS_KEY=key_aqui
NEWSDATA_KEY=key_aqui
```

### Wrangler (producción)
```bash
wrangler secret put ADMIN_TOKEN
wrangler secret put NEWSAPI_KEY
# etc.
```

---

## Comandos Clave

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Dev local (Pages) |
| `npm run preview` | Preview con live reload |
| `npx wrangler dev src/index.js --port 8787` | Dev local API |
| `npm run deploy` | Deploy Pages a Cloudflare |
| `wrangler deploy src/index.js` | Deploy Worker API |
| `python tools/news/master-news-flow.py` | Descarga + procesa noticias |
| `python tools/site/generate-sites.py` | Genera sitios |

---

## Notas Importantes

- **Secrets**: Nunca committear `.env` o `.dev.vars` a git
- **Logs**: Los logs se guardan en `data/logs/` para debugging
- **Backups**: Se crean automáticamente en `backups/` antes de cambios mayores
- **Staging**: Usar `deploy_preview.sh` para enviar a staging antes de prod

---

**Última actualización**: Febrero 2026
