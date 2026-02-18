# 📂 Estructura del Proyecto

Organización estricta por dominios, con raíz limpia y rutas consistentes.

---

## 📌 Índice De Directorios
- `apps/`: Aplicaciones ejecutables (backend, frontend, workers).
- `core/`: Lógica y herramientas del generador (scripts, CLI, utilidades).
- `content/`: Datos y plantillas fuente (JSON, CSS, layouts, referencias, demos).
- `assets/`: Recursos estáticos reutilizables (fonts, SVG, CSS base).
- `output/`: Resultados generados (sites, generated_sites, imágenes, tests).
- `infra/`: Deployment y scripts de infraestructura.
- `docs/`: Documentación completa del proyecto.
- `.github/`, `.vscode/`, `venv/`, `.venv/`, `__pycache__/`: tooling y entornos locales.

---

## 🗂️ Árbol De Directorios (Resumen)

```
news-prototype/
├── AGENTS.md
├── README.md
├── apps/
│   ├── backend/           # Flask API (apps/backend/app.py)
│   ├── frontend/          # React + Vite (apps/frontend/)
│   └── workers/           # Cloudflare Workers prototype
├── core/
│   ├── scripts/           # Generación + utilidades + tests
│   ├── core/menu.py            # Menú interactivo
│   ├── core/menu.sh            # Launcher del menú
│   ├── main.py            # Orquestador legacy
│   ├── manage-news-sites.py
│   ├── news.py            # Descarga de noticias
│   └── requirements.txt   # Dependencias del generador
├── content/
│   ├── data/              # JSONs, metadatos, snapshots
│   ├── templates/         # CSS templates y assets de generación
│   ├── layout/            # Layouts de demo
│   ├── reference-sites/   # Referencias de diseño
│   ├── demos/             # HTML de demos
│   └── samples/           # HTML de muestras (categorías, meta tags)
├── assets/
│   ├── fonts/
│   ├── images/
│   ├── css/
│   └── svg-icons/
├── output/
│   ├── generated_sites/   # Pipeline completo (site_N/)
│   ├── sites/             # HTML single-file
│   ├── generated_images/  # Imágenes generadas
│   ├── public/og-images/  # Open Graph images
│   └── tests/             # Artefactos de testing
├── infra/
│   ├── render.yaml
│   └── deploy/            # Scripts de deploy
└── docs/
    ├── guides/
    ├── design/
    ├── integration/
    ├── testing/
    └── archive/
```

---

## ✅ Notas Clave
- Los **outputs** siempre viven en `output/`.
- Los **datos fuente** están en `content/data/`.
- Las **plantillas CSS** se mantienen en `content/templates/css/`.
- El **frontend** se ejecuta desde `apps/frontend/`.
- El **backend** usa `apps/backend/app.py` y escribe en `output/sites/`.
