# Scripts - Referencia Rápida

## 📁 Estructura

```
scripts/
├── deploy/        # Scripts de despliegue a Cloudflare
├── fixes/         # Scripts de corrección y mantenimiento
├── utilities/     # Herramientas generales
└── archive/       # Scripts deprecados
```

---

## 🚀 Scripts de Deploy (`deploy/`)

| Script | Propósito |
|--------|-----------|
| `deploy-full.sh` | **NUEVO** Deploy completo: Worker API → CMS → Todos los sitios |
| `deploy.sh` | Deploy principal (Pages + Worker) |
| `deploy_all_sites.sh` | Deploy todos los sitios generados |
| `deploy_all_sites_preview.sh` | Deploy preview de todos los sitios |
| `deploy_preview.sh` | Deploy a preview/staging |
| `deploy_to_cloudflare.py` | Helper Python para deploy |
| `run-news-pipeline.sh` | Ejecuta pipeline completo: descarga → procesa → genera → deploy |
| `download_and_seed_example.sh` | Descarga ejemplo y seedea base de datos |
| `DEPLOYMENT_GUIDE.md` | Guía de despliegue detallada |

**Uso rápido**:
```
bash
cd scripts/deploy/
bash deploy-full.sh               # Deploy completo (Worker + CMS + Sitios)
bash deploy.sh                    # Deploy principal
bash run-news-pipeline.sh        # Pipeline automático
```

---

## 🔧 Scripts de Fixes (`fixes/`)

Scripts para correcciones comunes y mantenimiento:

| Script | Propósito |
|--------|-----------|
| `fix_article_links.py` | Corrige URLs/links en artículos |
| `fix_article_logos.py` | Corrige imágenes de logos |
| `fix_article_headers.py` | Corrige headers HTML |
| `fix_broken_logos.py` | Repara logos rotos |
| `fix_category_images.py` | Corrige imágenes de categorías |
| `fix_duplicate_content.py` | Detecta y elimina duplicados |
| `fix_html_structure.py` | Valida/corrige estructura HTML |
| `fix_images.py` | Arregla problemas con imágenes |
| `fix_categories.py` | Corrige categorización |
| `fix_authors.py` | Normaliza info de autores |
| `fix_thumbnails.py` | Optimiza miniaturas |
| `fix_titles.py` | Limpia/normaliza títulos |
| `fix_ui_issues.py` | Corrige problemas de UI |
| `fix_all_articulo_urls.py` | Corrige URLs de artículos |
| `fix_api_urls.py` | Corrige URLs de API |
| `fix_articulo_api_urls.py` | Corrige URLs API específicas |
| `fix_articulo_paths.py` | Corrige paths de artículos |
| `fix_category_api_urls.py` | Corrige URLs API de categorías |
| `fix_index_api_urls.py` | Corrige URLs API en índice |

**Uso general**:
```
bash
cd scripts/fixes/
python fix_article_links.py        # Ejecuta corrección
```

---

## ⚙️ Herramientas Generales (`utilities/`)

| Script | Propósito |
|--------|-----------|
| `seed_db.py` | Seedea base de datos con datos iniciales |
| `regenerate_index.py` | Regenera índice de artículos |
| `recreate_sites.py` | Recrea sitios generados |
| `redownload_images.py` | Redescarga todas las imágenes |
| `force_redownload.py` | Força descargas nuevas forzando caché |
| `generate_slugs.py` | Genera slugs para URLs |
| `convert_to_dynamic.py` | Convierte sitios estáticos a dinámicos |
| `optimize_article_flow.py` | Optimiza flujo de artículos |
| `remove_tags.py` | Elimina tags HTML innecesarios |
| `improve_card_design.py` | Mejora diseño de tarjetas |
| `news_selector.py` | Selector interactivo de noticias |
| `update_legal_emails.py` | Actualiza emails legales |
| `update_favicons_headers.py` | Actualiza favicons y headers |
| **Node.js Scripts**: |
| `news-downloader.js` | Descargador de noticias (Node) |
| `seed_news_to_db.js` | Seedea noticias a BD (Node) |
| `serve-admin.js` | Sirve panel admin local |
| `serve-local.js` | Sirve aplicación local |
| **SQL Scripts**: |
| `seed_articles.sql` | SQL para seedear artículos |
| `reseed_articles.sql` | SQL para re-seedear |
| `update_slugs.sql` | SQL para actualizar slugs |

**Uso**:
```
bash
cd scripts/utilities/
python seed_db.py                    # Seedea BD
node serve-admin.js                  # Sirve admin
```

---

## 📦 Archive (`archive/`)

Scripts deprecados o no activos. Solo consultar como referencia.

---

## 🔄 Pipeline Automático Recomendado

Para un flujo completo automatizado:

```
bash
cd scripts/deploy/
bash run-news-pipeline.sh

# O paso a paso:
# 1. Descargar noticias
python tools/news/master-news-flow.py --source newsapi --count 50

# 2. Generar sitios
python tools/site/generate-sites.py

# 3. Deploy
npm run deploy && wrangler deploy src/index.js --name news-api
```

---

## 💡 Consejos

- Los scripts están organizados por función (deploy, fixes, utilities)
- Usa `--help` en scripts Python para ver opciones: `python script.py --help`
- Muchos scripts permiten filtros: `--source`, `--query`, `--count`, etc.
- Siempre crear backup antes de ejecutar fix scripts en producción
- Para debugging, ver logs en `data/logs/`

---

**Última actualización**: Febrero 2026
