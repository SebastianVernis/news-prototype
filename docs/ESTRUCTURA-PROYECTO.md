# 📂 Estructura del Proyecto - Política

**Versión**: 2.0 (Reorganizada)  
**Fecha**: 19 Enero 2026

---

## 🗂️ Vista General

```
Politica/
│
├── 📜 Raíz (4 archivos + scripts principales)
├── 📁 scripts/ (27 scripts Python)
├── 📁 docs/ (26 documentos organizados)
├── 📁 assets/ (CSS, fuentes, iconos SVG)
├── 📁 backend/ (API Flask)
├── 📁 frontend/ (HTML + src)
├── 📁 data/ (noticias JSON)
├── 📁 generated_sites/ (sitios generados)
├── 📁 public/ (recursos públicos)
└── 📁 templates/ (templates CSS)
```

---

## 📜 Archivos en Raíz

### Documentación Esencial
```
README.md                   # Documentación principal del proyecto
README-GENERADOR.md         # Quick start del generador
QUICK-COMMANDS.md           # Referencia rápida de comandos
REORGANIZACION-PLAN.md      # Plan de reorganización
```

### Scripts Principales
```
main.py                     # Orquestador legacy
news.py                     # Módulo de noticias
menu.py                     # Menú interactivo (ACTUALIZADO)
menu.sh                     # Menú bash
```

### Configuración
```
package.json                # Dependencias Node.js
requirements.txt            # Dependencias Python
render.yaml                 # Config Render.com
vite.config.js              # Config Vite
.gitignore, .renderignore   # Ignorar archivos
```

---

## 📁 scripts/ (27 archivos)

### Flujo Principal
```
master_orchestrator.py      # ⭐ Orquestador completo (ACTUALIZADO)
menu.py                     # Menú interactivo
```

### Generadores de Diseño (Sprint 1)
```
logo_generator_svg.py       # ✨ NUEVO - Logos SVG sin IA
color_palette_generator.py  # ✅ ACTUALIZADO - Paletas profesionales
font_family_generator.py    # ✅ ACTUALIZADO - Tipografías reales
header_generator.py         # ✅ ACTUALIZADO - Sticky + offcanvas
layout_generator.py         # ✅ ACTUALIZADO - Cards profesionales
layout_css_generator.py     # ✅ ACTUALIZADO - Estilo professional
footer_generator.py
```

### Generadores de Contenido
```
site_name_generator.py      # Nombres de sitios
paraphrase.py               # Parafraseo con IA
article-expander.py         # Expansión de artículos
legal_pages_generator.py    # Páginas legales
template_combiner.py        # Combina módulos CSS
```

### Imágenes
```
generate-images-unified.py  # Generador unificado (NewsAPI + Unsplash)
generate-images-newsapi.py  # NewsAPI images
generate-images-unsplash.py # Unsplash fallback
generate-images-ai.py       # IA (Blackbox)
generate-images.py          # Legacy
```

### Utilidades
```
domain_verifier.py          # Verificador WHOIS
domain_verifier_apilayer.py # WHOIS con APILayer
site_pre_creation.py        # Pre-creación de sitios
list_blackbox_models.py     # Listar modelos IA
flujo-completo.sh           # Script bash completo
generate-interactive.py     # Generador interactivo
generate-sites.py           # Legacy
```

---

## 📁 docs/ (26 documentos)

### Estructura
```
docs/
├── README.md                  # Índice de toda la documentación
├── ESTRUCTURA-REORGANIZADA.md # Este documento de reorganización
│
├── design/ (7)               # 🎨 Diseño Sprint 1
├── guides/ (5)               # 📖 Guías principales
├── integration/ (4)          # 🔧 Integraciones
├── testing/ (1)              # 🧪 Tests
├── changelog/ (1)            # 📜 Historial
├── [otros] (7)               # Docs generales
└── archive/                  # Obsoletos
```

### docs/design/ - Sprint 1 ⭐
```
INDICE-MEJORAS-DISEÑO.md           # Índice maestro
TODO-MEJORAS-DISEÑO.md             # Plan ejecutivo
RESUMEN-SPRINT1-COMPLETADO.md      # Resultados
ANALISIS-DISEÑO-REFERENCIA.md      # Análisis sitios
ANALISIS-EJEMPLO-HTML.md           # Análisis Radio M
NOTA-LOGOS-SVG.md                  # Sistema logos
RESUMEN-CAMBIOS-REALIZADOS.md      # Fixes previos
README.md                          # Índice de design/
```

### docs/guides/
```
AGENTS.md                    # Para desarrolladores
DIAGRAMA-FLUJO-COMPLETO.md   # Arquitectura
INDEX-DOCUMENTACION.md       # Índice maestro
MENU-PRINCIPAL.md            # Guía del menú
REORGANIZACION-DOCS.md       # Reorganización anterior
```

### docs/integration/
```
INTEGRACION-NEWSAPI-COMPLETA.md  # NewsAPI
APILAYER-SETUP.md                # APILayer
SOLUCION-IMAGENES-FINAL.md       # Imágenes
OPTIMIZACION-IMAGENES.md         # Optimización
```

### docs/testing/
```
VERIFICACION-MODULOS.md      # Test de 16 módulos
```

### docs/changelog/
```
RESUMEN-FLUJO.md             # Resumen ejecutivo
```

### docs/ (otros)
```
QUICKSTART.md                # Quick start
README_FRONTEND.md           # Frontend
STRUCTURE.md                 # Estructura (old)
FLUJO-ACTUAL.md              # Flujo actual
COMANDOS-FLUJO-COMPLETO.md   # Comandos
PRESENTACION-FLUJO.md        # Presentación
COMANDOS-ACTUALIZADOS.md     # Comandos actualizados
SOLUCION.md                  # Soluciones
CHANGELOG.md                 # Changelog
SITE-PRE-CREATION.md         # Pre-creación
```

---

## 📁 assets/ (NUEVO - Sprint 1)

```
assets/
├── css/
│   └── variables-base.css        # 80+ variables CSS unificadas
│
├── fonts/ (preparado para fuentes)
│
└── svg-icons/
    ├── news/                     # 6 iconos (newspaper, microphone, camera, etc.)
    ├── shapes/                   # 4 iconos (circle, hexagon, badge, shield)
    └── political/                # 3 iconos (flag, capitol, ballot)
```

**Total**: 13 iconos SVG + sistema de variables

---

## 📁 Otras Carpetas

### backend/
```
app.py                       # Flask API
requirements.txt             # Deps backend
```

### frontend/
```
index.html                   # HTML principal
src/                         # Fuentes frontend
```

### data/
```
noticias.txt                 # Datos de prueba
noticias_*.json              # Noticias descargadas
```

### generated_sites/
```
site_1/                      # Sitio generado 1
site_2/                      # Sitio generado 2
...
site_N/                      # Sitio N
test_logos/                  # Logos de prueba
```

### public/
```
images/                      # Imágenes públicas
sites/                       # Sitios de referencia
templates/                   # Templates base
```

### templates/
```
css/                         # Templates CSS generados
```

---

## 🎯 Navegación Rápida

### Para Usuarios
```bash
# Leer documentación principal
cat README.md
cat QUICK-COMMANDS.md

# Generar sitio
python3 menu.py  # Opción 1 → 1
```

### Para Desarrolladores
```bash
# Leer guías técnicas
cat docs/guides/AGENTS.md
cat docs/guides/DIAGRAMA-FLUJO-COMPLETO.md

# Ver estructura
cat docs/STRUCTURE.md
cat docs/ESTRUCTURA-REORGANIZADA.md
```

### Para Diseñadores
```bash
# Sprint 1 de diseño
cd docs/design
cat README.md                      # Índice
cat INDICE-MEJORAS-DISEÑO.md      # Maestro
cat TODO-MEJORAS-DISEÑO.md        # Plan
cat RESUMEN-SPRINT1-COMPLETADO.md # Resultados
```

### Buscar Documentos
```bash
# Por categoría
ls docs/design/      # Diseño
ls docs/guides/      # Guías
ls docs/integration/ # Integraciones

# Por palabra clave
grep -r "logo" docs/design/
grep -r "NewsAPI" docs/integration/
```

---

## 📊 Estadísticas

### Código
- **Scripts Python**: 27
- **Líneas totales**: ~8,000
- **Módulos principales**: 17
- **Tests**: 5

### Documentación
- **Total documentos**: 30
- **En raíz**: 4
- **En docs/**: 26
  - design/: 8 (con README)
  - guides/: 5
  - integration/: 4
  - testing/: 1
  - changelog/: 1
  - otros: 7

### Assets
- **Variables CSS**: 80+
- **Iconos SVG**: 13
- **Layouts**: 20 (2 profesionales)
- **Paletas**: 20 (4 verificadas)
- **Tipografías**: 15 (4 verificadas)

---

## 🔄 Actualizaciones Recientes

### 19 Enero 2026 - Sprint 1
- ✅ Reorganización de documentación
- ✅ Sistema de logos SVG sin IA
- ✅ Paletas profesionales verificadas
- ✅ Variables CSS unificadas
- ✅ Headers sticky + offcanvas
- ✅ Cards profesionales
- ✅ Menu.py actualizado con nuevas rutas

---

## 📞 Enlaces Útiles

### Documentación
- **Índice maestro**: [docs/README.md](docs/README.md)
- **Diseño Sprint 1**: [docs/design/README.md](docs/design/README.md)
- **Quick start**: [docs/QUICKSTART.md](docs/QUICKSTART.md)

### Código
- **Master orchestrator**: [scripts/master_orchestrator.py](scripts/master_orchestrator.py)
- **Logo SVG**: [scripts/logo_generator_svg.py](scripts/logo_generator_svg.py)
- **Variables CSS**: [assets/css/variables-base.css](assets/css/variables-base.css)

---

**Última actualización**: 19 Enero 2026  
**Estado**: ✅ Reorganizada y documentada
