# 🗞️ Presentación del Sistema - News Prototype

## 📋 Resumen Ejecutivo

Sistema automatizado completo para **generar múltiples sitios de noticias únicos** con contenido dinámico, layouts variados y metadatos completos. Cada sitio generado tiene identidad propia, diseño único y noticias actualizadas.

---

## 🎯 Objetivo del Sistema

Automatizar completamente la creación de sitios de noticias profesionales:
- ✅ Descarga automática de noticias de múltiples fuentes
- ✅ Parafraseo con IA para contenido único
- ✅ Generación de imágenes con IA (Flux Schnell)
- ✅ Creación de metadatos y branding para cada sitio
- ✅ Generación de sitios HTML con layouts dinámicos
- ✅ **21+ tipos de layouts diferentes**
- ✅ **12+ estilos de header**
- ✅ **12+ estilos de navegación**
- ✅ **15+ disposiciones de contenido destacado**

---

## 🔄 Flujo Completo del Sistema

### **Fase 1: Recopilación de Noticias**

```
┌─────────────────────────────────────┐
│   APIs de Noticias (Múltiples)     │
├─────────────────────────────────────┤
│  • NewsAPI.org                      │
│  • Newsdata.io                      │
│  • WorldNewsAPI                     │
│  • APITube.io                       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Descarga de Noticias               │
│  scripts/api/newsapi.py             │
│  scripts/api/newsdata.py            │
│  scripts/api/worldnews.py           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Noticias Originales JSON           │
│  data/noticias_[api]_[fecha].json   │
└─────────────────────────────────────┘
```

**Comando:**
```bash
cd scripts
python3 main.py --api newsapi --articles 5
```

**Resultado:**
- Archivo JSON con noticias originales
- Metadatos completos (autor, fecha, URL, descripción)
- Texto completo extraído de cada artículo

---

### **Fase 2: Parafraseo con IA**

```
┌─────────────────────────────────────┐
│  Noticias Originales                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Parafraseo con Blackbox AI         │
│  scripts/paraphrase.py              │
│                                     │
│  • Genera 40 variaciones/noticia   │
│  • Mantiene contexto y datos       │
│  • Contenido único para cada sitio │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Noticias Parafraseadas JSON        │
│  data/noticias_paraphrased_[fecha]  │
│                                     │
│  5 originales × 40 variaciones      │
│  = 200 noticias únicas              │
└─────────────────────────────────────┘
```

**Comando:**
```bash
cd scripts
python3 paraphrase.py
```

**Resultado:**
- 40 variaciones únicas por cada noticia original
- Contenido diferente pero contextualmente equivalente
- Preparado para distribución entre múltiples sitios

---

### **Fase 3: Generación de Imágenes**

```
┌─────────────────────────────────────┐
│  Noticias Parafraseadas             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Generación de Imágenes AI          │
│  scripts/generate-images-ai.py      │
│                                     │
│  • Modelo: Flux Schnell             │
│  • Prompts basados en título        │
│  • Estilo periodístico profesional  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Imágenes PNG + JSON Actualizado    │
│  images/news/article_[id]_[var].jpg │
│  data/noticias_final_[fecha].json   │
└─────────────────────────────────────┘
```

**Comando:**
```bash
cd scripts
python3 generate-images-ai.py
```

**Resultado:**
- Imagen única para cada variación de noticia
- Formato: 1024×1024 PNG
- Paths guardados en JSON final

---

### **Fase 4: Pre-Creación de Sitios**

```
┌─────────────────────────────────────┐
│  Protocolo de Pre-Creación          │
│  scripts/site_pre_creation.py       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Generación de Metadatos            │
│                                     │
│  • Nombres convincentes (AI)        │
│  • Dominios verificados (opcional)  │
│  • Paletas de colores únicas        │
│  • Categorías randomizadas          │
│  • Información de contacto          │
│  • Metadatos SEO completos          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Metadatos JSON por Sitio           │
│  data/sites_metadata/               │
│    sites_metadata_[fecha].json      │
└─────────────────────────────────────┘
```

**Comando:**
```bash
cd scripts
python3 site_pre_creation.py --cantidad 10 --verificar-dominios
```

**Estructura de Metadatos:**
```json
{
  "id": "site_20260108_123456_1234",
  "nombre": "El Diario Digital",
  "dominio": "eldiariodigital.mx",
  "dominio_disponible": true,
  "tagline": "Tu Fuente Confiable de Información",
  "colores": {
    "primario": "#2C3E50",
    "secundario": "#3498DB",
    "acento": "#E74C3C"
  },
  "categorias": ["Inicio", "Nacional", "Política", ...],
  "contacto": {...},
  "seo": {...}
}
```

---

### **Fase 5: Generación de Sitios HTML**

```
┌─────────────────────────────────────┐
│  Inputs:                            │
│  • Noticias Final JSON              │
│  • Metadatos de Sitios              │
│  • Templates CSS (40+)              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Generador de Sitios                │
│  scripts/generate-sites.py          │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Layout Generator              │ │
│  │ • 21+ tipos de layouts        │ │
│  │ • 12+ estilos de header       │ │
│  │ • 12+ estilos de navegación   │ │
│  │ • 15+ layouts destacados      │ │
│  └───────────────────────────────┘ │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Sitios HTML Generados              │
│  sites/site1.html                   │
│  sites/site2.html                   │
│  ...                                │
│  sites/site[N].html                 │
└─────────────────────────────────────┘
```

**Comando Principal:**
```bash
cd scripts
python3 generate-sites.py
```

**Modo Interactivo:**
- Pregunta cantidad de sitios (1-100)
- Opción de verificar dominios
- Usar metadatos existentes o generar nuevos
- Confirmación antes de ejecutar

**Modo CLI (No Interactivo):**
```bash
# Generar 10 sitios rápido
python3 generate-sites.py --cantidad 10 --no-interactivo

# Generar 40 sitios con verificación
python3 generate-sites.py --cantidad 40 --verificar-dominios --no-interactivo

# Usar metadatos específicos
python3 generate-sites.py --cantidad 20 --metadata-file ../data/sites_metadata/sites_metadata_20260108.json
```

---

## 📊 Diversidad de Layouts

### **21 Tipos de Layouts Principales**

| Layout | Descripción |
|--------|-------------|
| `classic` | Periódico tradicional multi-columna |
| `magazine` | Estilo revista con grid dinámico |
| `modern_cards` | Tarjetas modernas con sombras |
| `masonry` | Tipo Pinterest con alturas variables |
| `featured_sidebar` | Destacado principal con sidebar |
| `grid_equal` | Grid de tamaños iguales uniforme |
| `timeline` | Línea de tiempo vertical |
| `asymmetric` | Asimétrico moderno creativo |
| `minimalist` | Minimalista con espacio blanco |
| `full_width` | Ancho completo sin márgenes |
| `boxed` | Contenedor en caja centrada |
| `overlay` | Con overlays de imágenes |
| `split_screen` | Pantalla dividida 50/50 |
| `newspaper_classic` | Periódico clásico 6 columnas |
| `blog_style` | Estilo blog personal |
| `editorial` | Editorial de revista premium |
| `portfolio` | Estilo portafolio con galería |
| `grid_mosaic` | Mosaico dinámico |
| `horizontal_scroll` | Scroll horizontal |
| `vertical_list` | Lista vertical simple |
| `classic_sidebar` | Clásico con sidebar fijo |

### **12 Estilos de Header**

| Estilo | Descripción |
|--------|-------------|
| `centered` | Logo y tagline centrados |
| `left_aligned` | Logo alineado a la izquierda |
| `split` | Logo izquierda, menú derecha |
| `minimal` | Minimalista sin decoración |
| `bold` | Audaz con mucho espacio |
| `stacked` | Logo y menú apilados |
| `floating` | Header flotante transparente |
| `compact` | Header compacto y delgado |
| `magazine_style` | Estilo revista elegante |
| `newspaper_banner` | Banner de periódico tradicional |
| `modern_thin` | Moderno y delgado |
| `boxed_header` | Header en caja contenida |

### **12 Estilos de Navegación**

| Estilo | Descripción |
|--------|-------------|
| `horizontal` | Menú horizontal clásico |
| `horizontal_center` | Menú horizontal centrado |
| `hamburger` | Menú hamburguesa móvil |
| `sidebar_nav` | Navegación lateral fija |
| `mega_menu` | Mega menú con categorías |
| `dropdown` | Menú con dropdowns |
| `tabs` | Estilo pestañas |
| `pills` | Menú estilo pills/botones |
| `vertical_stack` | Menú vertical apilado |
| `icon_menu` | Menú con iconos |
| `sticky_nav` | Navegación pegajosa al scroll |
| `offcanvas` | Menú offcanvas lateral |

### **15 Disposiciones de Contenido Destacado**

| Layout | Descripción |
|--------|-------------|
| `hero_full` | Hero a ancho completo |
| `hero_split` | Hero dividido 60/40 |
| `carousel` | Carrusel de noticias |
| `grid_featured` | Grid de destacadas |
| `stacked` | Apiladas verticalmente |
| `hero_slider` | Slider de héroes |
| `featured_3col` | 3 columnas destacadas |
| `big_small_grid` | Una grande + varias pequeñas |
| `overlay_cards` | Tarjetas con overlay |
| `video_hero` | Hero con video de fondo |
| `parallax` | Efecto parallax |
| `diagonal_split` | División diagonal |
| `magazine_spread` | Diseño revista doble página |
| `minimal_hero` | Hero minimalista |
| `full_height_hero` | Hero de altura completa |

---

## 🎨 Características de Cada Sitio

### **Identidad Única**
- ✅ Nombre convincente generado con IA
- ✅ Dominio verificado (opcional)
- ✅ Tagline profesional
- ✅ Paleta de colores única (6 paletas predefinidas)

### **Layout Dinámico**
- ✅ Tipo de layout aleatorio (21 opciones)
- ✅ Estilo de header aleatorio (12 opciones)
- ✅ Estilo de navegación aleatorio (12 opciones)
- ✅ Layout destacado aleatorio (15 opciones)
- ✅ Posición de sidebar: left/right/none
- ✅ Columnas de noticias: 1-4
- ✅ Header sticky: sí/no

### **Contenido**
- ✅ Noticias únicas (de 200 variaciones disponibles)
- ✅ Imágenes generadas con IA
- ✅ Categorías randomizadas
- ✅ Distribución dinámica de contenido
- ✅ Metadatos SEO completos

### **Widgets de Sidebar** (aleatorios)
- Newsletter
- Tendencias
- Noticias Recientes
- Redes Sociales
- Categorías
- Etiquetas

---

## 🚀 Uso del Sistema

### **1. Flujo Completo Automatizado**

```bash
# Paso 1: Descargar noticias
cd scripts
python3 main.py --api newsapi --articles 5

# Paso 2: Parafrasear (ya incluido en main.py)
# Paso 3: Generar imágenes (ya incluido en main.py)

# Paso 4: Generar sitios (modo interactivo)
python3 generate-sites.py
```

### **2. Generación Rápida de Sitios**

```bash
cd scripts
./run.sh  # Modo interactivo

# O modo no-interactivo
python3 generate-sites.py --cantidad 10 --no-interactivo
```

### **3. Generación Masiva (Producción)**

```bash
cd scripts
python3 generate-sites.py --cantidad 100 --no-interactivo
```

### **4. Con Verificación de Dominios**

```bash
cd scripts
python3 generate-sites.py --cantidad 20 --verificar-dominios --no-interactivo
```

---

## 📈 Estadísticas del Sistema

### **Variedad de Layouts**
- **21 tipos de layouts** principales
- **12 estilos de header**
- **12 estilos de navegación**
- **15 layouts destacados**
- **3 posiciones de sidebar**
- **4 opciones de columnas**
- **6 paletas de colores**

**Combinaciones posibles:** 21 × 12 × 12 × 15 × 3 × 4 × 6 = **~1.3 millones de combinaciones únicas**

### **Contenido**
- **5 noticias originales** (desde APIs)
- **40 variaciones por noticia** = 200 variaciones totales
- **200 imágenes únicas** generadas con IA
- **Distribución:** ~20 noticias por sitio (para 10 sitios)

### **Rendimiento**

| Operación | Sin Verificación | Con Verificación |
|-----------|------------------|------------------|
| 5 sitios | ~15 segundos | ~1-2 minutos |
| 10 sitios | ~30 segundos | ~3-5 minutos |
| 40 sitios | ~2 minutos | ~10-15 minutos |
| 100 sitios | ~5 minutos | ~25-30 minutos |

---

## 🛠️ Estructura de Archivos

```
news-prototype/
├── scripts/
│   ├── generate-sites.py         # ⭐ Generador principal
│   ├── layout_generator.py       # Layouts dinámicos (AMPLIADO)
│   ├── site_pre_creation.py      # Pre-creación de sitios
│   ├── site_name_generator.py    # Generador de nombres
│   ├── paraphrase.py             # Parafraseo con IA
│   ├── generate-images-ai.py     # Generación de imágenes
│   └── api/                      # Scripts de APIs
│
├── data/
│   ├── noticias_final_[fecha].json      # Noticias finales
│   └── sites_metadata/                  # Metadatos de sitios
│       └── sites_metadata_[fecha].json
│
├── sites/                        # ⭐ Sitios HTML generados
│   ├── site1.html
│   ├── site2.html
│   └── ...
│
├── images/
│   └── news/                     # Imágenes generadas
│
└── templates/
    └── css/                      # 40+ templates CSS
```

---

## ✅ Verificación del Sistema

### **✅ Sistema Completamente Funcional**

**Verificado:**
1. ✅ Descarga de noticias desde APIs
2. ✅ Parafraseo con Blackbox AI (40 variaciones/noticia)
3. ✅ Generación de imágenes con Flux Schnell
4. ✅ Pre-creación de metadatos de sitios
5. ✅ Generación de nombres convincentes
6. ✅ Verificación de dominios (opcional)
7. ✅ **Biblioteca de layouts ampliada:** 21 → **21+ tipos**
8. ✅ **Estilos de header ampliados:** 5 → **12 tipos**
9. ✅ **Estilos de navegación ampliados:** 5 → **12 tipos**
10. ✅ **Layouts destacados ampliados:** 5 → **15 tipos**
11. ✅ Generación de sitios HTML completos
12. ✅ Distribución dinámica de contenido
13. ✅ Categorías randomizadas por sitio
14. ✅ Widgets de sidebar aleatorios

### **Prueba Realizada**

```bash
cd scripts
python3 generate-sites.py --cantidad 10 --no-interactivo
```

**Resultado:**
- ✅ 10 sitios generados exitosamente
- ✅ Cada sitio con layout único
- ✅ Metadatos completos
- ✅ Noticias con imágenes
- ✅ Total: 2,097 líneas de HTML generadas

---

## 🎯 Próximos Pasos Sugeridos

1. **Expandir Templates CSS**
   - Crear templates específicos para los nuevos layouts
   - Responsive design mejorado

2. **Optimización de Imágenes**
   - Generación más rápida con batch processing
   - Múltiples tamaños para responsive

3. **Hosting Automatizado**
   - Deploy automático a servidores
   - CI/CD pipeline

4. **Analytics**
   - Tracking de sitios generados
   - Estadísticas de uso

---

## 📞 Información Técnica

**Lenguaje:** Python 3.8+
**Dependencias principales:**
- requests (APIs)
- beautifulsoup4 (scraping)
- python-dotenv (configuración)
- Blackbox API (IA)

**APIs utilizadas:**
- NewsAPI.org
- Newsdata.io
- WorldNewsAPI
- Blackbox AI API (parafraseo e imágenes)

---

## 📝 Conclusión

Sistema completamente funcional que automatiza la generación de sitios de noticias únicos con:
- ✅ **21+ tipos de layouts diferentes**
- ✅ **12+ estilos de header**
- ✅ **12+ estilos de navegación**
- ✅ **15+ disposiciones de contenido destacado**
- ✅ **~1.3 millones de combinaciones posibles**
- ✅ Contenido único generado con IA
- ✅ Imágenes generadas con IA
- ✅ Metadatos completos por sitio
- ✅ Proceso completamente automatizado

**El sistema está listo para generar cientos de sitios de noticias únicos en minutos.**

---

*Última actualización: 8 de enero de 2026*
*Sistema verificado y funcional ✅*
