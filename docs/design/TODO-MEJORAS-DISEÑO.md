# ✅ TODO: Mejoras de Diseño Basadas en Análisis

## 🎯 Prioridad ALTA (Impacto Inmediato)

### 1. **Logos SVG sin IA** 
**Archivo**: Crear `core/scripts/logo_generator_svg.py`

**Implementar**:
- Logos tipográficos puros (solo texto + CSS)
- Badges circulares con iniciales
- Combinación ícono SVG + texto
- Biblioteca de 20-30 iconos SVG base

**Beneficios**:
- ✅ No requiere IA (sin fallos)
- ✅ Instantáneo
- ✅ Escalable (SVG)
- ✅ Profesional

**Recursos necesarios**:
```bash
# Crear estructura
mkdir -p Politica/assets/fonts/{headlines,modern,classic}
mkdir -p Politica/assets/svg-icons/{news,shapes,political}
```

**Fuentes a descargar** (Google Fonts, gratis):
- Bebas Neue (display, impacto)
- Poppins (moderna, completa)
- Montserrat (geométrica, fuerte)
- Source Sans Pro (profesional)
- Playfair Display (elegante, serif)

---

### 2. **Paletas Profesionales Verificadas**
**Archivo**: `core/scripts/palette_generator.py`

**Agregar paletas extraídas**:

```python
PALETAS_PROFESIONALES = {
    "milenio_rojo": {
        "primary": "#B10B1F",
        "secondary": "#F1F1F1", 
        "accent": "#D1D1D1",
        "background": "#FFFFFF",
        "background_2": "#EDEDED",
        "text": "#202124",
        "urgent": "#FDE636"
    },
    
    "radio_m_azul": {
        "primary": "#3D55EF",
        "secondary": "#F7F9F8",
        "accent": "#0693E3",
        "background": "#FFFFFF",
        "background_2": "#EFEFEF",
        "text": "#202124",
        "urgent": "#CF2E2E"
    },
    
    "sobrio_corporativo": {
        "primary": "#1C1C1C",
        "secondary": "#F5F5F5",
        "accent": "#3D55EF",
        "background": "#FFFFFF",
        "background_2": "#F7F9F8",
        "text": "#161617",
        "urgent": "#FF6900"
    },
    
    "periodistico_clasico": {
        "primary": "#000000",
        "secondary": "#EFEFEF",
        "accent": "#CF2E2E",
        "background": "#FFFFFF",
        "background_2": "#F7F9F8",
        "text": "#333333",
        "urgent": "#FDE636"
    }
}
```

**Cambios en generador**:
- Reemplazar colores aleatorios con paletas verificadas
- Agregar variable `--urgent` para breaking news
- Incluir `background_2` para áreas secundarias

---

### 3. **Tipografías de Sitios Reales**
**Archivo**: `core/scripts/typography_generator.py`

**Agregar combinaciones verificadas**:

```python
FUENTES_PROFESIONALES = {
    # Display (títulos impactantes)
    "bebas_neue": {
        "name": "Bebas Neue",
        "google_url": "Bebas+Neue:400",
        "type": "display",
        "weights": [400]
    },
    "montserrat": {
        "name": "Montserrat", 
        "google_url": "Montserrat:400,600,700,800,900",
        "type": "sans-serif",
        "weights": [400, 600, 700, 800, 900]
    },
    "oswald": {
        "name": "Oswald",
        "google_url": "Oswald:400,500,600,700",
        "type": "display",
        "weights": [400, 500, 600, 700]
    },
    
    # Body (texto principal)
    "poppins": {
        "name": "Poppins",
        "google_url": "Poppins:300,400,500,600,700",
        "type": "sans-serif",
        "weights": [300, 400, 500, 600, 700]
    },
    "source_sans_pro": {
        "name": "Source Sans Pro",
        "google_url": "Source+Sans+Pro:400,600,700",
        "type": "sans-serif", 
        "weights": [400, 600, 700]
    },
    "roboto": {
        "name": "Roboto",
        "google_url": "Roboto:300,400,500,700",
        "type": "sans-serif",
        "weights": [300, 400, 500, 700]
    },
    
    # Serif (elegancia, contraste)
    "playfair_display": {
        "name": "Playfair Display",
        "google_url": "Playfair+Display:400,600,700,800,900",
        "type": "serif",
        "weights": [400, 600, 700, 800, 900]
    },
    "merriweather": {
        "name": "Merriweather",
        "google_url": "Merriweather:300,400,700,900",
        "type": "serif",
        "weights": [300, 400, 700, 900]
    },
    "source_serif_pro": {
        "name": "Source Serif Pro",
        "google_url": "Source+Serif+Pro:400,600,700,900",
        "type": "serif",
        "weights": [400, 600, 700, 900]
    }
}

COMBINACIONES_PROFESIONALES = [
    # Verificadas en sitios reales
    {
        "heading": "Bebas Neue",
        "body": "Poppins",
        "accent": None,
        "name": "Radio M Style"
    },
    {
        "heading": "Source Serif Pro", 
        "body": "Source Sans Pro",
        "accent": None,
        "name": "Milenio Style"
    },
    {
        "heading": "Montserrat",
        "body": "Roboto",
        "accent": None,
        "name": "Modern Professional"
    },
    {
        "heading": "Playfair Display",
        "body": "Poppins",
        "accent": None,
        "name": "Elegant Editorial"
    }
]
```

---

### 4. **Sistema de Variables CSS**
**Archivo**: Crear `Politica/assets/css/variables-base.css`

```css
:root {
    /* Dimensiones */
    --site-width: 1070px;
    --content-width: 69%;
    --sidebar-width: 300px;
    
    /* Espaciado */
    --gap-xs: 5px;
    --gap-sm: 10px;
    --gap-md: 20px;
    --gap-lg: 35px;
    
    /* Border Radius */
    --radius-box: 6px;
    --radius-button: 10px;
    --radius-image: 10px;
    
    /* Tipografía */
    --font-body: "Poppins", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    --font-heading: "Bebas Neue", Impact, "Arial Black", sans-serif;
    --font-size-base: 14px;
    --font-size-small: 12px;
    --line-height-base: 1.7;
    --line-height-heading: 1.2;
    
    /* Colores (se sobrescriben por tema) */
    --color-primary: #B10B1F;
    --color-secondary: #F1F1F1;
    --color-accent: #D1D1D1;
    --color-bg: #FFFFFF;
    --color-bg-alt: #EDEDED;
    --color-text: #202124;
    --color-text-light: #999999;
    --color-urgent: #FDE636;
    --color-border: #EFEFEF;
    
    /* Header */
    --header-height: 65px;
    --header-secondary-height: 50px;
    
    /* Sombras */
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
    
    /* Z-index */
    --z-header: 100;
    --z-offcanvas: 200;
    --z-modal: 300;
}
```

**Integración**:
- Generar este archivo en cada sitio
- Template combiner debe incluirlo
- Todos los CSS deben usar estas variables

---

## 🎨 Prioridad MEDIA (Mejoras Visuales)

### 5. **Header Mejorado**
**Archivo**: `core/scripts/header_generator.py`

**Implementar**:
- Sticky header por defecto
- Offcanvas menu para mobile
- Logo con `<img>` y srcset
- Menú en UPPERCASE
- 3 niveles opcionales:
  1. Top bar (utilidades, fecha)
  2. Main navbar (logo + menú)
  3. Secciones secundarias

### 6. **Cards de Noticias Mejoradas**
**Archivo**: `core/scripts/layout_generator.py`

**Estructura estándar**:
```html
<article class="news-card">
    <div class="card-image">
        <img src="..." alt="..." loading="lazy">
        <span class="category-badge">POLÍTICA</span>
    </div>
    <div class="card-content">
        <h3 class="card-title">
            <a href="...">Título de la Noticia</a>
        </h3>
        <p class="card-excerpt">Breve descripción...</p>
        <div class="card-meta">
            <span class="author">Por Juan Pérez</span>
            <span class="date">19 Ene 2026</span>
        </div>
    </div>
</article>
```

**CSS**:
```css
.news-card {
    border-radius: var(--radius-box);
    background: var(--color-bg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s;
}

.news-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
}

.category-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: var(--color-primary);
    color: white;
    padding: 5px 12px;
    border-radius: var(--radius-button);
    font-size: var(--font-size-small);
    font-weight: 700;
    text-transform: uppercase;
}
```

### 7. **Grid System Mejorado**
**Archivo**: `core/scripts/layout_generator.py`

**Implementar**:
```python
GRID_CONFIGS = {
    "classic_3col": {
        "desktop": 3,
        "tablet": 2,
        "mobile": 1,
        "gap": "var(--gap-md)",
        "max_width": "1070px"
    },
    "dense_4col": {
        "desktop": 4,
        "tablet": 2,
        "mobile": 1,
        "gap": "var(--gap-sm)",
        "max_width": "1200px"
    },
    "wide_2col": {
        "desktop": 2,
        "tablet": 2,
        "mobile": 1,
        "gap": "var(--gap-lg)",
        "max_width": "960px"
    }
}
```

---

## 🔧 Prioridad BAJA (Pulido)

### 8. **Breaking News Bar**
Componente animado para últimas noticias

### 9. **Reading Progress Indicator**
Barra de progreso al leer artículo

### 10. **Social Share Buttons**
Iconos SVG para compartir en redes

### 11. **Newsletter Signup**
Widget en sidebar/footer

### 12. **Dark Mode Toggle**
Switcher entre light/dark theme

---

## 📦 Recursos a Descargar

### Fuentes (Google Fonts - Gratuitas)
```bash
# En assets/fonts/
wget "https://fonts.google.com/download?family=Poppins" -O poppins.zip
wget "https://fonts.google.com/download?family=Bebas%20Neue" -O bebas-neue.zip
wget "https://fonts.google.com/download?family=Montserrat" -O montserrat.zip
wget "https://fonts.google.com/download?family=Source%20Sans%20Pro" -O source-sans-pro.zip
wget "https://fonts.google.com/download?family=Playfair%20Display" -O playfair.zip
```

### Iconos SVG (Gratuitos)
```bash
# Font Awesome Free
wget https://use.fontawesome.com/releases/v6.5.1/fontawesome-free-6.5.1-web.zip

# O usar SVG inline de sitios como:
# - Heroicons: https://heroicons.com/
# - Bootstrap Icons: https://icons.getbootstrap.com/
# - Material Icons: https://fonts.google.com/icons
```

---

## 🚀 Plan de Ejecución

### Sprint 1: Fundamentos (2-3 horas)
1. ✅ Crear notas de análisis
2. ⏳ Descargar fuentes profesionales
3. ⏳ Crear biblioteca SVG básica (10 iconos)
4. ⏳ Implementar `logo_generator_svg.py`
5. ⏳ Actualizar `palette_generator.py` con paletas profesionales

### Sprint 2: Variables y Tipografía (1-2 horas)
6. ⏳ Crear `variables-base.css`
7. ⏳ Actualizar `typography_generator.py`
8. ⏳ Integrar Google Fonts en templates
9. ⏳ Agregar combinaciones tipográficas verificadas

### Sprint 3: Componentes (2-3 horas)
10. ⏳ Mejorar `header_generator.py` (sticky, offcanvas)
11. ⏳ Actualizar cards de noticias
12. ⏳ Implementar grid system mejorado
13. ⏳ Agregar category badges

### Sprint 4: Integración (1 hora)
14. ⏳ Integrar logos SVG al flujo principal
15. ⏳ Testing completo
16. ⏳ Ajustes finales de CSS
17. ⏳ Documentación

---

## 📊 Impacto Esperado

### Antes (Actual)
- ❌ Logos con IA fallan frecuentemente
- ❌ Colores poco profesionales
- ❌ Tipografía básica (Arial/Helvetica)
- ❌ Headers simples
- ❌ CSS inline mezclado

### Después (Mejorado)
- ✅ Logos SVG siempre funcionan
- ✅ Paletas verificadas de sitios reales
- ✅ Tipografía profesional (Poppins + Bebas Neue)
- ✅ Headers sticky con offcanvas
- ✅ Sistema de variables CSS limpio
- ✅ Componentes consistentes y profesionales

---

## 🎯 Quick Wins (Cambios Rápidos)

### Cambio 1: Paletas Profesionales (15 min)
Reemplazar paletas actuales con las 4 verificadas

### Cambio 2: Fuentes Google (10 min)
Agregar Poppins + Bebas Neue como primeras opciones

### Cambio 3: Menú UPPERCASE (5 min)
```css
.nav a {
    text-transform: uppercase;
    font-size: 12px;
    font-weight: 700;
}
```

### Cambio 4: Border Radius Consistente (5 min)
```css
--radius-box: 6px;
--radius-button: 10px;
--radius-image: 10px;
```

### Cambio 5: Category Badges (15 min)
Agregar badges de categoría sobre imágenes de noticias

---

## 📝 Notas Técnicas

### Google Fonts Integration
```html
<!-- En <head> de cada sitio -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### SVG Logo Generation
```python
def generar_logo_svg_simple(site_name, color_primary):
    """Genera logo tipográfico sin IA"""
    initials = ''.join([word[0] for word in site_name.split()[:3]]).upper()
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="90" fill="{color_primary}"/>
        <text x="100" y="130" 
              font-family="Bebas Neue, Impact" 
              font-size="80"
              font-weight="bold"
              text-anchor="middle"
              fill="white">
            {initials}
        </text>
    </svg>'''
```

### CSS Variables Integration
```python
def generar_css_con_variables(paleta, tipografia, layout):
    """Genera CSS usando sistema de variables"""
    return f'''
    @import url('variables-base.css');
    
    :root {{
        /* Override con paleta específica */
        --color-primary: {paleta['primary']};
        --color-secondary: {paleta['secondary']};
        --font-body: "{tipografia['body']}", sans-serif;
        --font-heading: "{tipografia['heading']}", sans-serif;
    }}
    
    /* Resto del CSS usa variables */
    body {{
        font-family: var(--font-body);
        font-size: var(--font-size-base);
        line-height: var(--line-height-base);
        color: var(--color-text);
        background: var(--color-bg);
    }}
    
    h1, h2, h3 {{
        font-family: var(--font-heading);
        line-height: var(--line-height-heading);
    }}
    
    .nav a {{
        text-transform: uppercase;
        font-size: var(--font-size-small);
        font-weight: 700;
    }}
    '''
```

---

## ✅ Criterios de Éxito

Un diseño mejorado debe tener:

- [x] Logo que siempre funciona (SVG o fallback sólido)
- [ ] Paleta de colores profesional (extraída de referencias)
- [ ] Tipografía de Google Fonts (Poppins + Bebas Neue o similar)
- [ ] Sistema de variables CSS limpio
- [ ] Header sticky funcional
- [ ] Grid responsive con max-width 1070px
- [ ] Cards con hover effects
- [ ] Category badges sobre imágenes
- [ ] Menú en UPPERCASE
- [ ] Border radius consistente (6-10px)
- [ ] Espaciado generoso (line-height 1.7)
- [ ] Separadores sutiles (1px #efefef)

---

## 🔗 Referencias

- **NOTA-LOGOS-SVG.md** - Sistema de logos sin IA
- **ANALISIS-DISEÑO-REFERENCIA.md** - Análisis de Milenio, Universal, Excelsior
- **ANALISIS-EJEMPLO-HTML.md** - Análisis detallado de Radio M

---

**Última actualización**: 19 Enero 2026
**Próxima revisión**: Después de implementar Sprint 1
