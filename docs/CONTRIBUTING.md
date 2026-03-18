# Guía de Contribución - Cloudflare News Project

## Bienvenido 👋

Gracias por tu interés en contribuir al proyecto. Por favor sigue estas guías para mantener el código organizado.

---

## Estructura del Proyecto

```
/
├── src/                # Worker API (Cloudflare)
├── public/             # Sitio estático (Cloudflare Pages)
├── tools/              # Herramientas Python (noticias, imágenes, etc.)
├── scripts/            # Scripts organizados por función
│   ├── deploy/         # Deploy a Cloudflare
│   ├── fixes/          # Correcciones y mantenimiento
│   ├── utilities/      # Herramientas generales
│   └── archive/        # Scripts deprecados
├── docs/               # Documentación
├── data/               # Datos, logs (NO committear archivos generados)
└── tests/              # Tests automatizados
```

Ver [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) para detalles completos.

---

## Setup Local

```bash
# 1. Clonar
git clone https://github.com/tuuser/cloudflare-news-project.git
cd cloudflare-news-project

# 2. Instalar dependencias
npm install
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt  # Si existe

# 3. Configurar variables
echo "ADMIN_TOKEN=dev123" > .dev.vars
echo "NEWSAPI_KEY=tu_clave_aqui" >> .dev.vars

# 4. Iniciar dev local
npm run dev
```

---

## Tipos de Cambios

### 🐛 Bug Fixes (`scripts/fixes/`)

Crea un script nuevo si es un fix recurrente:

```bash
cd scripts/fixes/
# Nombra como: fix_[descripcion].py
touch fix_broken_images.py
```

**Estructura mínima**:
```python
#!/usr/bin/env python3
"""Fix para [descripción corta]."""

import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Input file/dir')
    args = parser.parse_args()
    
    # Tu lógica aquí
    print("✓ Fix ejecutado")

if __name__ == '__main__':
    main()
```

### 🚀 Nuevas Features

- **API routes**: Editar `src/index.js`
- **Frontend**: Editar `public/` (HTML/CSS/JS)
- **Herramientas**: Agregar a `tools/` o `scripts/utilities/`

### 📚 Documentación

- Actualizar [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) si cambias estructura
- Agregar notas a [docs/](docs/)
- Documentar scripts nuevos en [scripts/README.md](scripts/README.md)

---

## Convenciones de Código

### Python

```python
# Indentación: 4 espacios
# Nombres: snake_case
def process_articles(file_path: str) -> list:
    """Procesa artículos desde archivo.
    
    Args:
        file_path: Ruta del archivo
        
    Returns:
        Lista de artículos procesados
    """
    pass
```

### JavaScript

```javascript
// Indentación: 2 espacios (según existente)
// Nombres: camelCase
function processArticles(filePath) {
  // ...
}

// Strings: usa template literals cuando sea apropiado
const msg = `Procesados ${count} artículos`;
```

### Shell Scripts

```bash
#!/bin/bash
# Comentarios con descripción clara

set -e  # Exit on error

# Mensajes: con emojis para claridad
echo "✓ Paso completado"
echo "✗ Error detectado"
```

---

## Workflow de Cambios

### 1. Branch por Feature

```bash
git checkout -b feature/mi-feature
# o
git checkout -b fix/mi-fix
```

### 2. Commit Descriptivos

```bash
git add .
git commit -m "feat: agregar nueva fuente de noticias"
# o
git commit -m "fix: corregir URLs de imágenes"
```

### 3. Testing Local

- Si es backend: `npm run dev` en `src/`
- Si es frontend: `npm run dev` en `public/`
- Si es script: ejecuta manualmente

```bash
# Ejemplo: testear fix script
python scripts/fixes/fix_broken_images.py --input data/

# Ejemplo: testear utilidad
python tools/news/master-news-flow.py --source newsapi --count 10 --dry-run
```

### 4. Push & Pull Request

```bash
git push origin feature/mi-feature
```

En la PR incluye:
- Descripción de cambios
- Por qué ese cambio
- Cómo testearlo
- Screenshots si es UI

---

## Dónde Agregar Qué

| Tipo de código | Ubicación | Script? | Template |
|---|---|---|---|
| Corrección de datos | `scripts/fixes/` | `fix_*.py` | Ver arriba |
| Herramienta general | `scripts/utilities/` | `*.py` o `*.js` | - |
| Deploy/CI | `scripts/deploy/` | `*.sh` o `*.py` | - |
| Descarga de noticias | `tools/news/` | `*.py` | newsapi.py |
| Generación de sitios | `tools/site/` | `*.py` | generate-sites.py |
| API endpoint | `src/` | JavaScript | index.js |
| Frontend | `public/` | HTML/CSS/JS | - |
| Test | `tests/` | - | - |
| Doc | `docs/` | Markdown | - |

---

## Buena Practices

### ✅ DO

- ✅ Nombra scripts descriptivamente: `fix_article_urls.py` no `script1.py`
- ✅ Agregar docstrings/comentarios
- ✅ Testear cambios localmente antes de commit
- ✅ Mantener `.env` y `.dev.vars` fuera de git
- ✅ Actualizar documentación con tus cambios
- ✅ Usar rutas relative/absolutas según contexto

### ❌ DON'T

- ❌ Committear archivos `data/*.json`, `data/logs/`, `sites/`
- ❌ Hardcodear secrets o API keys
- ❌ Dejar scripts sin documentar
- ❌ Cambiar estructura sin actualizar docs
- ❌ Crear `fix_` scripts si es mejor una utilidad centralizada

---

## Deployment

### Cloudflare Pages (Frontend)

```bash
# Deploy automático: push a main → trigger en Cloudflare
# O manual:
npm run deploy
```

### Cloudflare Workers (API)

```bash
wrangler deploy src/index.js --name news-api
# O con wrangler en scripts/deploy/:
bash deploy.sh
```

### Variables Secretas

```bash
# Local development
echo "API_KEY=test" > .dev.vars

# Production
wrangler secret put NEWSAPI_KEY
wrangler secret put ADMIN_TOKEN
```

---

## Testing

Si hay tests:
```bash
npm test              # Si hay test runner
python -m pytest      # Si hay pytest
```

---

## Preguntas?

- Ver [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- Leer [AGENTS.md](AGENTS.md)
- Revisar docs en `docs/`
- Contactar al equipo

---

**Última actualización**: Febrero 2026

Gracias por contribuir! 🎉
