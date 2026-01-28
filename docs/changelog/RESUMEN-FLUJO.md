# 🚀 RESUMEN EJECUTIVO - Flujo de Generación

## ⚡ Quick Start

```bash
# Generar 1 sitio completo (2-3 minutos)
python scripts/master_orchestrator.py

# Con verificación de dominios (más lento)
python scripts/master_orchestrator.py --verificar-dominios

# Usar cache de noticias
python scripts/master_orchestrator.py --usar-cache
```

---

## 📊 Input → Output

```
INPUT:
├── API Key de Blackbox AI
├── API Key de NewsAPI (opcional si usas --usar-cache)
└── Categoría: "tecnología"

OUTPUT:
generated_sites/site_1/
├── index.html (1)
├── article_1.html ... article_20.html (20)
├── terminos.html, privacidad.html, faqs.html, acerca.html (4)
├── style.css (1)
├── logo.jpg (1)
└── images/
    └── news_1.jpg ... news_20.jpg (20)

TOTAL: 27 archivos por sitio
```

---

## 🔄 7 Pasos del Flujo

| Paso | Módulo | Entrada | Salida | Tiempo |
|------|--------|---------|--------|--------|
| **1** | NewsAPI | Query "tecnología" | 20 noticias originales | 5-10s |
| **2** | NewsParaphraser + ArticleExpander | 20 noticias | 20 artículos 800 palabras | 30-60s |
| **3** | AIImageGenerator | 20 artículos | 20 imágenes JPG | 40-80s |
| **4** | SitePreCreation | - | Metadata del sitio | 2-5s |
| **5** | AIImageGenerator | Metadata | 1 logo JPG | 3-5s |
| **6** | TemplateCombiner | Paleta+Fuente+Layout | 1 CSS file | 1-2s |
| **7** | HTMLLayoutBuilder | Todo lo anterior | 25 páginas HTML | 2-5s |

**TOTAL: ~2-3 minutos por sitio completo**

---

## 🎨 Variabilidad del Sistema

```
20 paletas × 15 fuentes × 20 layouts = 6,000 CSS templates
20 layouts × 12 headers × 12 navs × 15 featured = 43,200 HTML configs
8 estilos × 8 estructuras = 64 variaciones de contenido

TOTAL: ~16.5 millones de combinaciones únicas posibles
```

---

## 📁 Estructura del Sitio Generado

```
site_1/
├── 📄 index.html              ← 12 noticias en grid
├── 📄 article_1.html          ← Artículo completo con sidebar
│   ...
├── 📄 article_20.html         ← 800 palabras cada uno
├── 📄 terminos.html           ← Términos y Condiciones
├── 📄 privacidad.html         ← Política de Privacidad GDPR
├── 📄 faqs.html               ← 10 preguntas frecuentes
├── 📄 acerca.html             ← Acerca de Nosotros
├── 🎨 style.css               ← CSS modular completo
├── 🖼️ logo.jpg                ← Logo generado con AI
└── 📁 images/
    ├── news_1.jpg
    ...
    └── news_20.jpg
```

---

## 🔧 Módulos del Sistema

### Core (Orquestación)
- `master_orchestrator.py` - Flujo completo

### Contenido
- `api/newsapi.py` - Descarga de noticias
- `paraphrase.py` - Parafraseo (8 estilos)
- `article-expander.py` - Expansión a 800 palabras (8 estructuras)
- `generate-images-ai.py` - Imágenes AI (Flux Schnell)

### Branding
- `site_name_generator.py` - Nombres únicos (12 estilos)
- `domain_verifier.py` - Verificación WHOIS
- `site_pre_creation.py` - Metadata completa

### Diseño CSS
- `color_palette_generator.py` - 20 paletas
- `font_family_generator.py` - 15 fuentes
- `layout_css_generator.py` - 20 layouts
- `template_combiner.py` - Combinación modular

### Diseño HTML
- `layout_generator.py` - Configuraciones
- `header_generator.py` - 12 headers
- `footer_generator.py` - Footers responsivos
- `legal_pages_generator.py` - 4 páginas legales + 20 autores

**TOTAL: 16 módulos integrados**

---

## 📈 Estadísticas Clave

| Métrica | Valor |
|---------|-------|
| Noticias procesadas | 20 |
| Palabras por artículo | 800 |
| Imágenes AI generadas | 21 (20 + logo) |
| Páginas HTML | 25 |
| CSS Variables | 28 |
| Breakpoints responsivos | 5 |
| Combinaciones únicas | 16.5 millones |
| Tiempo de generación | 2-3 minutos |

---

## 🎯 Features CSS Modernas

✅ **Variables CSS** - 28 variables (colores, spacing, shadows, radius)  
✅ **CSS Grid responsivo** - `auto-fit` con `minmax`  
✅ **Tipografía fluida** - `clamp()` para tamaños adaptativos  
✅ **Mobile-first** - 5 breakpoints (640, 768, 1024, 1280, 1536px)  
✅ **Spacing scale** - 7 niveles (xs, sm, md, lg, xl, 2xl, 3xl)  
✅ **Box shadows** - 4 niveles de profundidad  
✅ **Border radius** - 4 niveles de redondeo  
✅ **Transiciones suaves** - Hover y focus states  
✅ **Aspect ratio** - Para imágenes consistentes  
✅ **Grid auto-fit** - Sin media queries para columnas  

---

## 🔐 Variables de Entorno

```bash
# .env
BLACKBOX_API_KEY=your_api_key_here
NEWS_API_KEY=your_newsapi_key_here  # Opcional con --usar-cache
```

---

## 📚 Documentación Completa

- **Diagrama detallado:** `DIAGRAMA-FLUJO-COMPLETO.md` (flujo paso a paso con ejemplos)
- **Guía de agentes:** `AGENTS.md` (reglas, mejores prácticas, historial)

---

## ✅ Checklist de Verificación

### Antes de generar:
- [ ] `.env` configurado con API keys
- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas: `pip install -r requirements.txt`

### Archivos generados:
- [ ] 1 index.html
- [ ] 20 article_N.html
- [ ] 4 páginas legales
- [ ] 1 style.css
- [ ] 1 logo.jpg
- [ ] 20 images/news_N.jpg

### Verificación visual:
- [ ] Abrir `generated_sites/site_1/index.html` en navegador
- [ ] Verificar grid de noticias
- [ ] Clic en artículo → verificar sidebar
- [ ] Verificar páginas legales en footer
- [ ] Probar en mobile (DevTools)

---

**Última actualización:** 2026-01-15 14:40  
**Versión:** 2.0
