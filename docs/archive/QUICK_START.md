# 🚀 Quick Start - Cloudflare News Project

## Estructura Reorganizada ✨

El proyecto ha sido reorganizado para mayor claridad:

```
/                      # Archivos de config raíz
├── scripts/
│   ├── deploy/        # Scripts de despliegue
│   ├── fixes/         # Scripts de corrección
│   ├── utilities/     # Herramientas generales
│   └── archive/       # Scripts deprecados
├── tools/
│   ├── news/          # Descarga/procesamiento de noticias
│   ├── site/          # Generador de sitios
│   ├── images/        # Manejo de imágenes
│   └── api/           # Utilidades API
├── src/               # Worker API
├── public/            # Sitio estático (Pages)
├── docs/              # Documentación
└── data/              # Datos & logs
```

## Desarrollo Local 🛠️

### 1. Primeros pasos
```bash
npm install
echo "ADMIN_TOKEN=test123" > .dev.vars
echo "NEWSAPI_KEY=tu_clave_aqui" >> .dev.vars
```

### 2. Ejecutar localmente
```bash
# Terminal 1: API en puerto 8787
npx wrangler dev src/index.js --port 8787

# Terminal 2: Pages en puerto 8788
npx wrangler pages dev ./public --port 8788

# Acceder: http://localhost:8788/admin.html
```

### 3. Descargar & Procesar Noticias
```bash
python tools/news/master-news-flow.py \
  --source newsapi \
  --query "technology" \
  --count 50
```

## Despliegue 🌐

```bash
# Deploy Pages
npm run deploy

# Deploy Worker API
wrangler deploy src/index.js --name news-api
```

## Scripts Principales

### Fixes/Mantenimiento
```bash
cd scripts/fixes/
# fix_article_links.py, fix_urls.py, etc.
```

### Utilities
```bash
cd scripts/utilities/
# seed_db.py, regenerate_index.py, serve-admin.js, etc.
```

### Deploy
```bash
cd scripts/deploy/
# deploy.sh, deploy_all_sites.sh, run-news-pipeline.sh, etc.
```

## Documentación

- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Estructura completa
- [README.md](README.md) - Documentación principal
- [docs/](docs/) - Documentación detallada
- [AGENTS.md](AGENTS.md) - Directrices para contribuidores

## Comandos Frecuentes

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Desarrollo local |
| `npm run deploy` | Deploy a producción |
| `python tools/news/master-news-flow.py` | Pipeline completo de noticias |
| `python tools/site/generate-sites.py` | Generar sitios HTML |

---

**Nota**: Ver [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) para la estructura completa y flujos detallados.
