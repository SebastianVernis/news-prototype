# 📂 Estructura del Proyecto

Organización limpia y clara del proyecto news-prototype.

---

## 🗂️ Árbol de Directorios

```
news-prototype/
├── 📜 Archivos de Configuración
│   ├── .env                        # Variables de entorno (API keys)
│   ├── requirements.txt            # Dependencias Python
│   ├── README.md                   # Documentación principal
│   ├── CHANGELOG.md                # Historial de cambios
│   └── STRUCTURE.md                # Este archivo
│
├── 🎯 Scripts Principales
│   ├── main.py                     # Orquestador principal
│   └── news.py                     # Módulo de noticias
│
├── 📁 scripts/                     # Scripts de generación y utilidades
│   ├── ⭐ generate-sites.py        # Generador principal de sitios
│   ├── layout_generator.py         # Generador de layouts dinámicos
│   ├── site_name_generator.py      # Generador de nombres
│   ├── site_pre_creation.py        # Protocolo de pre-creación
│   ├── domain_verifier.py          # Verificador de dominios
│   ├── paraphrase.py               # Parafraseo con IA
│   ├── generate-images-ai.py       # Generación de imágenes
│   ├── article-expander.py         # Expansión de artículos
│   ├── list_blackbox_models.py     # Listar modelos disponibles
│   ├── run.sh                      # Script de ejecución rápida
│   ├── run-generator.sh            # Generador automatizado
│   ├── run_all_apis.sh             # Ejecutar todas las APIs
│   │
│   ├── 📁 api/                     # Scripts de APIs de noticias
│   │   ├── newsapi.py              # NewsAPI integration
│   │   ├── newsdata.py             # NewsData.io integration
│   │   ├── worldnews.py            # WorldNews API
│   │   └── apitube.py              # YouTube news API
│   │
│   ├── 📁 test/                    # Scripts de testing
│   │   ├── test_integration.py     # Tests de integración
│   │   ├── test_blackbox.py        # Tests de Blackbox API
│   │   ├── test_paraphrase_quick.py # Tests rápidos de parafraseo
│   │   └── test-interactive.sh     # Tests interactivos
│   │
│   ├── 📁 utils/                   # Utilidades compartidas
│   │   └── utils.py                # Funciones comunes
│   │
│   └── 📁 archive/                 # Scripts deprecated
│
├── 📁 data/                        # Datos y metadatos
│   ├── noticias_final_*.json       # Noticias procesadas (activas)
│   ├── noticias.txt                # Texto de noticias
│   │
│   ├── 📁 sites_metadata/          # Metadatos de sitios
│   │   ├── sites_metadata_*.json   # 3 archivos más recientes
│   │   ├── builder_site_*.json     # Metadatos para builder
│   │   └── 📁 archive/             # Metadatos históricos (8 archivos)
│   │
│   └── 📁 archive/                 # Datos históricos
│       ├── newsapi_*.json/csv      # Archivos de NewsAPI
│       ├── noticias_mx_*.json/csv  # Noticias de México
│       ├── noticias_newsapi_*.json # Noticias procesadas
│       └── noticias_paraphrased_*  # Parafraseos antiguos
│
├── 📁 sites/                       # Sitios HTML generados
│   ├── site1.html
│   ├── site2.html
│   ├── site3.html
│   └── ...
│
├── 📁 templates/                   # Plantillas y estilos
│   ├── base.html                   # Plantilla base
│   ├── index.html                  # Index template
│   └── 📁 css/                     # 40 estilos CSS únicos
│       ├── template1.css
│       ├── template2.css
│       └── ...
│
├── 📁 images/                      # Recursos visuales
│   └── 📁 news/                    # Imágenes generadas con IA
│       ├── article_1.jpg
│       ├── article_2.jpg
│       └── ...
│
├── 📁 docs/                        # Documentación
│   ├── README.md                   # Docs del sistema de automatización
│   ├── SITE-PRE-CREATION.md        # Protocolo técnico completo
│   │
│   └── 📁 archive/                 # Documentación histórica
│       ├── GUIA-INTERACTIVA.md     # Guía del modo interactivo
│       ├── FLUJO-OPTIMIZADO.md     # Optimizaciones del flujo
│       ├── README-SITE-PRE-CREATION.md  # Resumen del protocolo
│       ├── INICIO-RAPIDO.md        # Guía de inicio rápido
│       ├── QUICKSTART.md           # Quick start guide
│       ├── INTEGRATION-STATUS.md   # Estado de integraciones
│       ├── MODELS.md               # Documentación de modelos
│       ├── README-APIS.md          # Documentación de APIs
│       ├── README-IMAGES.md        # Generación de imágenes
│       ├── RESUMEN-IMPLEMENTACION.md # Resumen técnico
│       └── NuevasAPI.pdf           # Documentación de APIs
│
├── 📁 js/                          # JavaScript
│   └── news-data.js                # Datos de noticias
│
└── 📁 venv/                        # Entorno virtual Python

```

---

## 📊 Estadísticas del Proyecto

### Archivos Activos
- **Scripts principales**: 13 archivos
- **Scripts de API**: 4 archivos
- **Scripts de testing**: 4 archivos
- **Templates CSS**: 40 archivos
- **Noticias activas**: 1 archivo JSON
- **Metadatos activos**: 3 archivos JSON
- **Documentación activa**: 2 archivos MD

### Archivos Archivados
- **Data histórica**: 13 archivos
- **Metadatos históricos**: 8 archivos
- **Documentación histórica**: 11 archivos
- **Scripts deprecated**: Variable

---

## 🎯 Scripts Clave

### Generación de Sitios
| Script | Propósito |
|--------|-----------|
| `generate-sites.py` | Generador principal de sitios HTML |
| `layout_generator.py` | Crea layouts dinámicos |
| `site_name_generator.py` | Genera nombres de sitios |
| `site_pre_creation.py` | Pre-creación de metadatos |
| `domain_verifier.py` | Verifica dominios con whois |

### Procesamiento de Contenido
| Script | Propósito |
|--------|-----------|
| `paraphrase.py` | Parafrasea noticias con IA |
| `generate-images-ai.py` | Genera imágenes con IA |
| `article-expander.py` | Expande artículos |

### APIs de Noticias
| Script | API |
|--------|-----|
| `api/newsapi.py` | NewsAPI.org |
| `api/newsdata.py` | NewsData.io |
| `api/worldnews.py` | WorldNews API |
| `api/apitube.py` | YouTube News |

### Testing
| Script | Tipo |
|--------|------|
| `test/test_integration.py` | Tests de integración |
| `test/test_blackbox.py` | Tests de Blackbox API |
| `test/test_paraphrase_quick.py` | Tests rápidos |

---

## 📦 Gestión de Datos

### Archivos Activos
Los archivos en uso activo permanecen en `data/`:
- Último archivo `noticias_final_*.json`
- 3 archivos más recientes de `sites_metadata/`

### Política de Archivo
Los archivos antiguos se mueven automáticamente a `*/archive/`:
- Mantiene el directorio limpio
- Preserva historial para referencia
- Fácil restauración si es necesario

### Limpieza Automática
El sistema limpia automáticamente:
- Sitios HTML antiguos antes de generar nuevos
- Metadatos antiguos (mantiene 3 más recientes)
- Datos temporales de procesamiento

---

## 🛠️ Flujos de Trabajo

### 1. Generación de Sitios Completa
```bash
scripts/
  ├── api/newsapi.py              # Paso 1: Obtener noticias
  ├── paraphrase.py               # Paso 2: Parafrasear
  ├── generate-images-ai.py       # Paso 3: Generar imágenes
  └── generate-sites.py           # Paso 4: Crear sitios
```

### 2. Solo Metadatos
```bash
scripts/
  └── site_pre_creation.py        # Generar solo metadatos
```

### 3. Testing
```bash
scripts/test/
  ├── test_integration.py         # Tests completos
  ├── test_blackbox.py            # Tests de API
  └── test_paraphrase_quick.py    # Tests rápidos
```

---

## 📝 Convenciones de Nombres

### Archivos de Datos
- `noticias_final_YYYYMMDD_HHMM.json` - Noticias finales
- `sites_metadata_YYYYMMDD_HHMM.json` - Metadatos de sitios
- `builder_site_YYYYMMDD_HHMM_ID.json` - Metadatos individuales

### Sitios Generados
- `site1.html`, `site2.html`, ... `siteN.html`
- Numeración consecutiva desde 1
- Se regeneran completamente en cada ejecución

### Templates CSS
- `template1.css` a `template40.css`
- Asignación cíclica para más de 40 sitios

---

## 🔄 Mantenimiento

### Limpieza Manual
```bash
# Limpiar archivos antiguos manualmente
rm -rf data/archive/*
rm -rf data/sites_metadata/archive/*
rm -rf docs/archive/*

# Limpiar sitios generados
rm -rf sites/site*.html
```

### Backup
```bash
# Backup de datos activos
tar -czf backup_$(date +%Y%m%d).tar.gz \
  data/noticias_final_*.json \
  data/sites_metadata/*.json \
  sites/*.html
```

### Restauración
```bash
# Restaurar desde archivo
mv data/archive/noticias_final_OLD.json data/
mv data/sites_metadata/archive/sites_metadata_OLD.json data/sites_metadata/
```

---

## 📚 Documentación Relacionada

- **[README.md](README.md)** - Documentación principal
- **[docs/README.md](docs/README.md)** - Docs del sistema
- **[docs/SITE-PRE-CREATION.md](docs/SITE-PRE-CREATION.md)** - Protocolo técnico
- **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios

---

## 🎯 Mejores Prácticas

### Organización
- ✅ Mantener archivos activos en directorios principales
- ✅ Archivar automáticamente datos antiguos
- ✅ Documentar cambios en CHANGELOG.md
- ✅ Usar nombres descriptivos para scripts

### Desarrollo
- ✅ Probar en modo test antes de producción
- ✅ Mantener metadatos de las últimas 3 ejecuciones
- ✅ Verificar disponibilidad de dominios cuando sea importante
- ✅ Usar modo interactivo para experimentación

### Mantenimiento
- ✅ Revisar archivos archivados periódicamente
- ✅ Hacer backup de datos importantes
- ✅ Actualizar documentación con cambios significativos
- ✅ Limpiar archivos temporales regularmente

---

**Última actualización:** 8 de Enero, 2026
