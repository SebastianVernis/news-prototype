# 📂 Estructura Reorganizada del Proyecto

**Fecha de reorganización**: 19 Enero 2026  
**Versión**: 2.0

---

## 🎯 Cambios Principales

### Antes (Raíz saturada)
- ❌ 20 archivos .md en raíz
- ❌ Difícil encontrar documentos
- ❌ Sin categorización clara

### Ahora (Organizada)
- ✅ 4 archivos .md en raíz (esenciales)
- ✅ 20 archivos en docs/ categorizados
- ✅ Estructura clara por tema

---

## 📁 Estructura Actual

```
Politica/
│
├── 📜 ARCHIVOS ESENCIALES (Raíz)
│   ├── README.md                      # Documentación principal
│   ├── README-GENERADOR.md            # Quick start generador
│   ├── QUICK-COMMANDS.md              # Referencia rápida
│   └── REORGANIZACION-PLAN.md         # Este plan
│
├── 🐍 SCRIPTS PYTHON
│   ├── main.py                        # Orquestador legacy
│   ├── news.py                        # Módulo de noticias
│   ├── core/menu.py                        # Menú interactivo
│   └── core/menu.sh                        # Menú bash
│
├── 📁 core/scripts/ (27 archivos)
│   ├── master_orchestrator.py         # Orquestador principal
│   ├── logo_generator_svg.py          # NUEVO Sprint 1
│   ├── color_palette_generator.py     # Actualizado Sprint 1
│   ├── font_family_generator.py       # Actualizado Sprint 1
│   ├── header_generator.py            # Actualizado Sprint 1
│   ├── layout_generator.py            # Actualizado Sprint 1
│   ├── layout_css_generator.py        # Actualizado Sprint 1
│   ├── template_combiner.py
│   ├── site_name_generator.py
│   ├── domain_verifier.py
│   ├── paraphrase.py
│   ├── article-expander.py
│   ├── generate-images-unified.py
│   ├── generate-images-newsapi.py
│   ├── generate-images-unsplash.py
│   ├── generate-images-ai.py
│   ├── site_pre_creation.py
│   ├── legal_pages_generator.py
│   ├── footer_generator.py
│   └── [13 scripts más]
│
├── 📁 docs/
│   ├── README.md                      # Índice de documentación
│   │
│   ├── 🎨 design/ (Sprint 1 - 7 docs)
│   │   ├── INDICE-MEJORAS-DISEÑO.md          ⭐ Índice maestro
│   │   ├── TODO-MEJORAS-DISEÑO.md            Plan ejecutivo
│   │   ├── ANALISIS-DISEÑO-REFERENCIA.md     Análisis sitios reales
│   │   ├── ANALISIS-EJEMPLO-HTML.md          Análisis Radio M
│   │   ├── NOTA-LOGOS-SVG.md                 Sistema logos SVG
│   │   ├── RESUMEN-CAMBIOS-REALIZADOS.md     Fixes aplicados
│   │   └── RESUMEN-SPRINT1-COMPLETADO.md     Resultados Sprint 1
│   │
│   ├── 📖 guides/ (5 docs)
│   │   ├── AGENTS.md                         Para desarrolladores
│   │   ├── DIAGRAMA-FLUJO-COMPLETO.md        Arquitectura
│   │   ├── INDEX-DOCUMENTACION.md            Índice maestro
│   │   ├── MENU-PRINCIPAL.md                 Guía del menú
│   │   └── REORGANIZACION-DOCS.md            Reorganización anterior
│   │
│   ├── 🔧 integration/ (4 docs)
│   │   ├── INTEGRACION-NEWSAPI-COMPLETA.md   NewsAPI
│   │   ├── APILAYER-SETUP.md                 APILayer
│   │   ├── SOLUCION-IMAGENES-FINAL.md        Sistema imágenes
│   │   └── OPTIMIZACION-IMAGENES.md          Optimización
│   │
│   ├── 🧪 testing/ (1 doc)
│   │   └── VERIFICACION-MODULOS.md           Test 16 módulos
│   │
│   ├── 📜 changelog/ (1 doc)
│   │   └── RESUMEN-FLUJO.md                  Resumen ejecutivo
│   │
│   ├── 📄 Otros
│   │   ├── QUICKSTART.md
│   │   ├── README_FRONTEND.md
│   │   ├── STRUCTURE.md
│   │   ├── FLUJO-ACTUAL.md
│   │   ├── COMANDOS-FLUJO-COMPLETO.md
│   │   ├── PRESENTACION-FLUJO.md
│   │   ├── COMANDOS-ACTUALIZADOS.md
│   │   ├── SOLUCION.md
│   │   ├── CHANGELOG.md
│   │   └── SITE-PRE-CREATION.md
│   │
│   └── archive/ (docs obsoletos)
│
├── 📁 assets/ (NUEVO Sprint 1)
│   ├── css/
│   │   └── variables-base.css         # 80+ variables CSS
│   ├── fonts/ (preparado)
│   └── svg-icons/
│       ├── news/ (6 iconos)
│       ├── shapes/ (4 iconos)
│       └── political/ (3 iconos)
│
├── 📁 apps/backend/
│   ├── app.py
│   └── core/requirements.txt
│
├── 📁 apps/frontend/
│   ├── index.html
│   └── src/
│
├── 📁 content/data/
│   └── [archivos .json de noticias]
│
├── 📁 output/generated_sites/
│   ├── site_1/
│   ├── site_2/
│   └── [... site_N]
│
├── 📁 output/public/
│   ├── images/
│   ├── output/sites/
│   └── content/templates/
│
└── 📁 content/templates/
    └── css/ (templates generados)
```

---

## 🔄 Cambios de Rutas

### Documentación Movida

| Archivo Original | Nueva Ubicación |
|-----------------|-----------------|
| INDICE-MEJORAS-DISEÑO.md | docs/design/ |
| TODO-MEJORAS-DISEÑO.md | docs/design/ |
| ANALISIS-DISEÑO-REFERENCIA.md | docs/design/ |
| ANALISIS-EJEMPLO-HTML.md | docs/design/ |
| NOTA-LOGOS-SVG.md | docs/design/ |
| RESUMEN-CAMBIOS-REALIZADOS.md | docs/design/ |
| RESUMEN-SPRINT1-COMPLETADO.md | docs/design/ |
| INTEGRACION-NEWSAPI-COMPLETA.md | docs/integration/ |
| SOLUCION-IMAGENES-FINAL.md | docs/integration/ |
| APILAYER-SETUP.md | docs/integration/ |
| DIAGRAMA-FLUJO-COMPLETO.md | docs/guides/ |
| MENU-PRINCIPAL.md | docs/guides/ |
| AGENTS.md | docs/guides/ |
| INDEX-DOCUMENTACION.md | docs/guides/ |
| REORGANIZACION-DOCS.md | docs/guides/ |
| VERIFICACION-MODULOS.md | docs/testing/ |
| RESUMEN-FLUJO.md | docs/changelog/ |

### Rutas Actualizadas en Código

**core/menu.py**:
- ✅ Documentación → rutas docs/*
- ✅ Opciones 3-10 → paths correctos

**Scripts** (sin cambios):
- ✅ No hay referencias hardcoded a .md
- ✅ Imports entre scripts funcionan (misma carpeta)

---

## 📊 Resumen de Carpetas

### docs/design/ - 7 archivos
Documentación del Sprint 1 de mejoras de diseño
- Análisis de sitios
- Plan de mejoras
- Implementaciones
- Resultados

### docs/guides/ - 5 archivos
Guías para usuarios y desarrolladores
- Arquitectura
- Menú interactivo
- Para agentes IA
- Índices

### docs/integration/ - 4 archivos
Integraciones con APIs y servicios
- NewsAPI
- APILayer
- Imágenes (AI + Unsplash)

### docs/testing/ - 1 archivo
Testing y verificación
- Test de 16 módulos

### docs/changelog/ - 1 archivo
Historial y resúmenes
- Resumen de flujo

### docs/archive/ - 4+ archivos
Documentos obsoletos

---

## ✅ Verificaciones Realizadas

- [x] Carpetas creadas: design, integration, guides, testing, changelog
- [x] Archivos movidos: 17 documentos
- [x] Rutas actualizadas en core/menu.py: 7 paths
- [x] docs/README.md creado: índice completo
- [x] Assets organizados: css, fonts, svg-icons
- [x] Scripts sin cambios: imports funcionan
- [x] Tests de paths: core/menu.py funciona

---

## 🚀 Acceso Rápido

### Desde Raíz
```bash
# Leer documentos principales
cat README.md
cat QUICK-COMMANDS.md
cat README-GENERADOR.md

# Navegar a documentación
cd docs
cat README.md  # Índice completo
```

### Diseño (Sprint 1)
```bash
cd docs/design
cat INDICE-MEJORAS-DISEÑO.md    # Índice
cat TODO-MEJORAS-DISEÑO.md      # Plan
cat RESUMEN-SPRINT1-COMPLETADO.md  # Resultados
```

### Guías
```bash
cd docs/guides
cat AGENTS.md                    # Para desarrolladores
cat DIAGRAMA-FLUJO-COMPLETO.md  # Arquitectura
```

### Menú Interactivo
```bash
python3 core/menu.py
# Opción 3: Documentación (rutas actualizadas)
# Opción 3 → 8: TODO-MEJORAS-DISEÑO
# Opción 3 → 9: ANALISIS-DISEÑO-REFERENCIA
```

---

## 📝 Mantenimiento

### Al Agregar Nuevo Documento

1. Determinar categoría (design, guides, integration, testing, changelog)
2. Crear en docs/[categoría]/
3. Actualizar docs/README.md
4. Si es acceso frecuente, agregar a core/menu.py
5. Actualizar CHANGELOG.md

### Al Referenciar Documento

Usar rutas relativas desde docs/:
- Mismo nivel: `[doc](NOMBRE.md)`
- Desde design/: `[doc](../guides/NOMBRE.md)`
- Desde raíz a docs: `[doc](docs/design/NOMBRE.md)`

---

## 🎉 Beneficios

### Organización
- ✅ Fácil encontrar documentos por tema
- ✅ Separación clara: diseño, guías, integraciones, testing
- ✅ Raíz limpia y profesional

### Mantenibilidad
- ✅ Nuevos docs tienen ubicación clara
- ✅ Archivos relacionados juntos
- ✅ Archive para obsoletos

### Navegación
- ✅ Menu interactivo con rutas correctas
- ✅ docs/README.md como índice central
- ✅ Links internos actualizados

---

**Reorganización completada**: 19 Enero 2026 16:00  
**Archivos movidos**: 17  
**Carpetas creadas**: 5  
**Rutas actualizadas**: core/menu.py (7 paths)  
**Estado**: ✅ Completo y verificado
