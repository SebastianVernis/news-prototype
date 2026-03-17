# 🚀 Quick Start - NexoPress

Guía rápida para comenzar a trabajar con el proyecto NexoPress (28 sitios de noticias).

## 📁 Ubicación del Proyecto

```
/mnt/hdd/Multimedia/Datasets/cloudflare-news-project/
```

## 🏗️ Estructura del Proyecto

```
cloudflare-news-project/
├── src/                    # Worker API (Cloudflare Workers)
│   ├── index.js           # Entry point principal
│   ├── config.js          # Configuración global
│   ├── cron/              # Cron jobs
│   │   ├── master.js      # Coordinador principal
│   │   ├── facebook.js    # Publicación Facebook
│   │   ├── rss-ingest.js  # Ingesta RSS
│   │   └── ticker.js      # News ticker
│   ├── routes/            # API Routes (13 módulos)
│   │   ├── auth.js
│   │   ├── articles.js
│   │   ├── cms.js
│   │   ├── facebook.js
│   │   └── ...
│   ├── middleware/        # Middleware
│   └── utils/             # Utilidades
├── sites/                  # 28 sitios Cloudflare Pages
│   ├── _shared/           # Assets compartidos
│   ├── radiocinconoticias/
│   ├── centralmexico/
│   ├── tvmexico/
│   └── ... (27 sitios más)
├── public/admin/          # CMS Dashboard (SPA)
├── scripts/               # Scripts de utilidad
└── docs/                  # Documentación
```

## 🛠️ Desarrollo Local

### 1. Variables de Entorno

Crear archivo `.dev.vars` en `/src/`:
```bash
cd /mnt/hdd/Multimedia/Datasets/cloudflare-news-project/src

cat > .dev.vars << 'EOF'
ADMIN_TOKEN=test_admin_token
OPENROUTER_API_KEY=sk-or-v1-...
NEWSAPI_KEY=...
EOF
```

### 2. Iniciar Worker Local

```bash
cd /mnt/hdd/Multimedia/Datasets/cloudflare-news-project/src

# Opción A: Con wrangler dev
wrangler dev --config wrangler.toml

# Opción B: Puerto específico
wrangler dev src/index.js --port 8781
```

### 3. Iniciar Pages Local (CMS)

```bash
cd /mnt/hdd/Multimedia/Datasets/cloudflare-news-project

# Development server
wrangler pages dev ./public --port 8888 --proxy 8781
```

### 4. Comando Completo (Worker + Pages)

```bash
cd /mnt/hdd/Multimedia/Datasets/cloudflare-news-project

# Terminal 1: Worker
npm run worker

# Terminal 2: Pages
npm run dev

# O todo junto:
npm start
```

## 🌐 URLs Importantes

| Servicio | Producción | Local |
|----------|------------|-------|
| API Worker | `https://news-api.sebastianvernis.workers.dev/api` | `http://localhost:8781/api` |
| CMS Admin | `https://cms.sebastianvernis.space/admin/` | `http://localhost:8888/admin/` |
| Uploads R2 | `https://uploads.sebastianvernis.space/` | - |

## 📤 Despliegue a Producción

### Deploy Worker API

```bash
cd /mnt/hdd/Multimedia/Datasets/cloudflare-news-project/src

wrangler deploy --config wrangler.toml

# Verificar deploy
curl https://news-api.sebastianvernis.workers.dev/api/health
```

### Deploy Sitio Individual

```bash
cd /mnt/hdd/Multimedia/Datasets/cloudflare-news-project/sites/[NOMBRE_SITIO]

wrangler pages deploy . --project-name=[NOMBRE_SITIO] --branch=master

# Ejemplo:
cd sites/radiocinconoticias
wrangler pages deploy . --project-name=radiocinconoticias --branch=master
```

### Deploy Todos los Sitios

```bash
cd /mnt/hdd/Multimedia/Datasets/cloudflare-news-project

for site in radiocinconoticias centralmexico tvmexico cbnnoticias mexicoinformado nodoinformativo bitacoraurbana reportecentralmx verticenoticias noticiasobjetivo boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  echo "Deploying $site..."
  cd sites/$site && wrangler pages deploy . --project-name=$site --branch=master && cd ../..
done
```

## 🗄️ Base de Datos D1

### Consultas Útiles

```bash
# Contar artículos
wrangler d1 execute news_db --command "SELECT COUNT(*) FROM ARTICULOS_PARAFRASEADOS" --remote

# Ver sitios
wrangler d1 execute news_db --command "SELECT SLUG, NOMBRE, FACEBOOK_ACTIVO FROM SITIOS" --remote

# Artículos pendientes de Facebook
wrangler d1 execute news_db --command "
  SELECT ID, TITULO_PARAFRASEADO, SITIO_DESTINO 
  FROM ARTICULOS_PARAFRASEADOS 
  WHERE FB_PUBLICADO = 0 AND FB_REQUERIDO = 1 
  LIMIT 10
" --remote

# Actualizar artículo
wrangler d1 execute news_db --command "
  UPDATE ARTICULOS_PARAFRASEADOS 
  SET FB_PUBLICADO = 0 
  WHERE ID = 'ARTICLE_ID'
" --remote
```

### Backup y Restore

```bash
# Exportar backup
wrangler d1 export news_db --output backup_$(date +%Y%m%d).sql --remote

# Importar (CUIDADO: elimina datos existentes)
wrangler d1 execute news_db --file backup.sql --remote
```

## 🔑 KV Storage

```bash
# Listar keys
wrangler kv:key list --binding ARTICLES_KV

# Obtener valor
wrangler kv:key get cron_status --binding ARTICLES_KV

# Limpiar (ej: resetear timers FB)
wrangler kv:key delete last_fb_post_radiocinconoticias --binding ARTICLES_KV
```

## 📊 Logs y Monitoreo

```bash
# Ver logs en tiempo real
wrangler tail --name news-api

# Estado del sistema
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool

# Monitor de Facebook
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

## 🔧 Comandos de Utilidad

### Scripts Python

```bash
cd /mnt/hdd/Multimedia/Datasets/cloudflare-news-project

# Verificar tokens de Facebook
python3 scripts/verify_fb_tokens.py

# Configurar tokens
python3 scripts/setup_fb_tokens.py
```

### Pruebas API

```bash
# Health check
curl https://news-api.sebastianvernis.workers.dev/api/health

# Forzar cron manual
curl -X POST https://news-api.sebastianvernis.workers.dev/api/cron/manual \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Publicar artículo en Facebook
curl -X POST https://news-api.sebastianvernis.workers.dev/api/articles/publish-fb/ARTICLE_ID \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## 📚 Documentación Adicional

| Documento | Descripción |
|-----------|-------------|
| [AGENTS.md](AGENTS.md) | Guía completa para desarrolladores |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Estructura detallada del proyecto |
| [IMPLEMENTACION_COMPLETA.md](IMPLEMENTACION_COMPLETA.md) | Arquitectura e implementación |
| [RESUMEN_FACEBOOK_FIX.md](RESUMEN_FACEBOOK_FIX.md) | Fixes aplicados a Facebook |
| [TODO.md](TODO.md) | Tareas pendientes |

## ⚡ Troubleshooting

### Error: `No account found`
```bash
wrangler login
```

### Error: `D1_ERROR: no such table`
```bash
# Aplicar schema
wrangler d1 execute news_db --file src/schema.sql --remote
```

### Worker no se actualiza
```bash
# Forzar redeploy
wrangler deploy --config wrangler.toml --force
```

---

**Versión:** 2.0.0 | **Última actualización:** Marzo 2026
