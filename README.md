# 🗞️ News Prototype - Generador Automatizado de Sitios de Noticias de Política

Sistema completo para **generar automáticamente múltiples sitios de noticias de política mexicana** con contenido único, layouts diversos y metadatos completos.

---

## ✨ Características Principales

### 🎮 Modo Interactivo
- Interfaz guiada paso a paso
- Configuración intuitiva
- Validación de inputs
- Confirmación antes de ejecutar

### 🎨 Layouts Dinámicos
- **8 tipos de layouts** diferentes por sitio
- **5 estilos de header** únicos
- **5 estilos de navegación** variados
- **5 disposiciones de destacados**
- Categorías randomizadas por sitio
- Distribución dinámica de contenido

### 📦 Sistema de Pre-Creación
- Generación automática de nombres convincentes
- Verificación de disponibilidad de dominios (opcional)
- Metadatos completos en JSON
- Paletas de colores únicas
- Especificaciones de logo

### 🚀 Flujo Automatizado
```
Configuración → Metadatos → Noticias → Layouts → Sitios HTML
```

---

## 🏃 Inicio Rápido

### 1. Instalación

```bash
# Clonar repositorio
git clone <repo-url>
cd news-prototype

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r core/requirements.txt
```

### 2. Generar Sitios (Modo Interactivo)

```bash
python3 core/scripts/generate-sites.py
```

El sistema te preguntará:
- **Cantidad de sitios** (1-100)
- **Verificar dominios** con whois (s/n)
- **Usar metadatos existentes** o generar nuevos
- **Confirmación** de la configuración

### 3. Ver Resultados

```bash
# Los sitios se generan en output/sites/
open ../output/sites/site1.html  # macOS
xdg-open ../output/sites/site1.html  # Linux
start ../output/sites/site1.html  # Windows
```

---

## 💻 Uso

### Modo Interactivo (Recomendado)

```bash
python3 core/scripts/generate-sites.py
```

### Modo No-Interactivo (CLI)

```bash
# Generar 5 sitios
python3 core/scripts/generate-sites.py --cantidad 5 --no-interactivo

# Generar 10 sitios con verificación de dominios
python3 core/scripts/generate-sites.py --cantidad 10 --verificar-dominios --no-interactivo

# Usar metadatos existentes
python3 core/scripts/generate-sites.py --cantidad 20 --metadata-file ../content/data/sites_metadata/sites_metadata_20260108.json
```

### Script Rápido

```bash
cd core/scripts
./run.sh              # Modo interactivo
./run.sh --cantidad 5 # Generar 5 sitios rápido
```

---

## 📊 Parámetros CLI

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--cantidad N` | Número de sitios a crear (1-100) | `--cantidad 10` |
| `--verificar-dominios` | Verificar disponibilidad con whois | `--verificar-dominios` |
| `--metadata-file PATH` | Usar metadatos específicos | `--metadata-file ../content/data/sites_metadata/archivo.json` |
| `--generar-metadata` | Forzar generación de metadatos nuevos | `--generar-metadata` |
| `--no-interactivo` | Desactivar modo interactivo | `--no-interactivo` |

---

## 🏗️ Estructura del Proyecto

```
news-prototype/
├── apps/
│   ├── backend/                  # Flask API
│   ├── frontend/                 # React + Vite
│   └── workers/                  # Cloudflare Workers
├── core/
│   ├── scripts/                  # Generación + utilidades + tests
│   ├── core/menu.py                   # Menú interactivo
│   ├── core/menu.sh                   # Launcher
│   └── requirements.txt          # Dependencias del generador
├── content/
│   ├── data/                     # JSON y metadatos
│   ├── templates/                # CSS templates
│   ├── layout/                   # Layout demos
│   ├── reference-sites/          # Referencias
│   ├── demos/                    # Demos HTML
│   └── samples/                  # Muestras (categorías, meta tags)
├── assets/                       # Fonts, SVG, CSS base
├── output/
│   ├── generated_sites/          # Sitios completos (site_N/)
│   ├── sites/                    # HTML single-file
│   ├── generated_images/         # Imágenes generadas
│   ├── public/og-images/         # OG images
│   └── tests/                    # Artefactos de testing
├── infra/                        # Deploy y config
└── docs/                         # Documentación
```

---

## 🎨 Diversidad de Layouts

Cada sitio generado tiene estructura **única**:

### Tipos de Layout
- **Classic** - Periódico tradicional
- **Magazine** - Estilo revista con grid
- **Modern Cards** - Tarjetas modernas
- **Masonry** - Tipo Pinterest
- **Featured Sidebar** - Destacado con sidebar
- **Grid Equal** - Grid uniforme
- **Timeline** - Línea de tiempo vertical
- **Asymmetric** - Asimétrico moderno

### Estilos de Header
- **Centered** - Logo centrado
- **Left Aligned** - Logo a la izquierda
- **Split** - Logo izq, menú der
- **Minimal** - Minimalista
- **Bold** - Audaz con espacio

### Navegación
- Horizontal
- Horizontal Center
- Hamburger Menu
- Sidebar Nav
- Mega Menu

### Sección Destacada
- Hero Full Width
- Hero Split (60/40)
- Carousel
- Grid Featured
- Stacked

---

## 📋 Metadatos Generados

Cada sitio incluye metadatos completos en JSON:

```json
{
  "id": "site_20260108_162536_1234",
  "nombre": "El Diario Nacional",
  "dominio": "eldiario.mx",
  "dominio_disponible": true,
  "tagline": "La Verdad en Cada Historia",
  "colores": {
    "primario": "#2C3E50",
    "secundario": "#3498DB",
    "acento": "#E74C3C"
  },
  "logo": {
    "estilo": "moderno",
    "prompt": "modern newspaper logo..."
  },
  "categorias": ["Inicio", "Nacional", "Internacional"],
  "contacto": {
    "email": "contacto@eldiario.mx",
    "telefono": "+52 55 1234 5678"
  },
  "seo": {
    "title": "El Diario Nacional - Noticias...",
    "description": "Tu fuente confiable...",
    "keywords": ["noticias", "méxico", ...]
  }
}
```

---

## 🎯 Casos de Uso

### Desarrollo Rápido (3-5 sitios)
```bash
python3 core/scripts/generate-sites.py
# Cantidad: 3
# Verificar: No
# ~10 segundos
```

### Producción (40+ sitios)
```bash
python3 core/scripts/generate-sites.py --cantidad 40 --no-interactivo
# ~2 minutos sin verificación
```

### Con Verificación de Dominios
```bash
python3 core/scripts/generate-sites.py --cantidad 10 --verificar-dominios --no-interactivo
# ~3-5 minutos (rate limiting whois)
```

### CI/CD Automatizado
```bash
python3 core/scripts/generate-sites.py --cantidad 25 --no-interactivo --generar-metadata
# Completamente automatizado
```

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
# APIs de Noticias
NEWSAPI_KEY=tu_api_key_aqui
NEWSDATA_KEY=tu_api_key_aqui

# AI para Parafraseo e Imágenes
BLACKBOX_API_KEY=tu_api_key_aqui
```

### Personalización

#### Cambiar Cantidad de Templates CSS
```python
# En generate-sites.py
MAX_TEMPLATES = 100  # Ajustar según templates disponibles
```

#### Agregar Más Estilos de Nombres
```python
# En site_name_generator.py
self.prefijos_clasicos = ["El", "La", "Periódico", ...]
self.nucleos = ["Diario", "Prensa", "Noticias", ...]
```

---

## 📚 Documentación Completa

- **[docs/README.md](docs/README.md)** - Documentación del sistema de automatización
- **[docs/SITE-PRE-CREATION.md](docs/SITE-PRE-CREATION.md)** - Protocolo técnico completo
- **[docs/CHANGELOG.md](docs/CHANGELOG.md)** - Historial de cambios

### Documentación Archivada
- **[docs/archive/GUIA-INTERACTIVA.md](docs/archive/GUIA-INTERACTIVA.md)** - Guía detallada del modo interactivo
- **[docs/archive/FLUJO-OPTIMIZADO.md](docs/archive/FLUJO-OPTIMIZADO.md)** - Optimizaciones del flujo
- **[docs/archive/README-SITE-PRE-CREATION.md](docs/archive/README-SITE-PRE-CREATION.md)** - Resumen del protocolo

---

## 🚀 Flujo Completo del Sistema

### 1. Recopilación de Noticias
```bash
python3 core/scripts/api/newsapi.py   # Obtener noticias de NewsAPI
python3 core/scripts/api/newsdata.py  # Obtener noticias de NewsData
python3 core/scripts/api/worldnews.py # Obtener noticias de WorldNews
```

### 2. Parafraseo con AI
```bash
python3 core/scripts/paraphrase.py     # Parafrasear noticias
```

### 3. Generación de Imágenes
```bash
python3 core/scripts/generate-images-ai.py  # Generar imágenes con AI
```

### 4. Generación de Sitios
```bash
python3 core/scripts/generate-sites.py      # Generar sitios HTML
```

---

## 📊 Rendimiento

| Operación | Sin Verificación | Con Verificación |
|-----------|------------------|------------------|
| 5 sitios | ~15 segundos | ~1-2 minutos |
| 10 sitios | ~30 segundos | ~3-5 minutos |
| 40 sitios | ~2 minutos | ~10-15 minutos |
| 100 sitios | ~5 minutos | ~25-30 minutos |

*Tiempos aproximados en hardware moderno con conexión estable*

---

## ✅ Verificación

El sistema siempre:
- ✅ Genera **exactamente** la cantidad de sitios solicitada
- ✅ Limpia sitios antiguos antes de generar nuevos
- ✅ Crea metadatos únicos por sitio
- ✅ Asigna layouts diferentes a cada sitio
- ✅ Randomiza categorías por sitio
- ✅ Distribuye contenido dinámicamente
- ✅ Valida imágenes y usa placeholders si faltan

---

## 🛠️ Solución de Problemas

### Error: "whois no está instalado"
```bash
# Ubuntu/Debian
sudo apt-get install whois

# Fedora
sudo dnf install whois

# macOS (preinstalado)
```

### Error: "No se pudieron cargar las noticias"
```bash
# Verificar archivo de noticias
ls ../content/data/noticias_final_*.json

# Regenerar si es necesario
python3 paraphrase.py
```

### Los sitios no tienen CSS
```bash
# Verificar templates CSS
ls ../content/templates/css/template*.css
```

---

## 🧹 Organización del Proyecto

### Archivos Activos
- **Root**: Scripts principales, configuración
- **content/data/**: Últimas noticias y 3 metadatos más recientes
- **docs/**: Documentación vigente

### Archivos Archivados
- **content/data/archive/**: Datos históricos
- **content/data/sites_metadata/archive/**: Metadatos antiguos
- **docs/archive/**: Documentación histórica
- **core/scripts/archive/**: Scripts deprecated

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles

---

## 👤 Autor

**Sebastián Vernis**
- GitHub: [@sebastianvernis](https://github.com/sebastianvernis)

---

## 🎉 ¡Comienza Ahora!

```bash
python3 core/scripts/generate-sites.py
```

**Genera sitios de noticias únicos en minutos** 🚀
