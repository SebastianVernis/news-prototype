# 📊 Análisis de Diseño - Sitios de Referencia

Análisis de los principales sitios de noticias mexicanos para mejorar nuestros layouts generados.

---

## 🎨 MILENIO

### Paleta de Colores
```css
--color-primary: #B10B1F      /* Rojo Milenio */
--color-secondary: #F1F1F1    /* Gris muy claro */
--color-accent: #D1D1D1       /* Gris medio */
--color-base-light: #FFFFFF
--color-base-dark: #000000
--color-background: #FFFFFF
--color-background-2: #EDEDED
--color-urgent: #FDE636       /* Amarillo */
```

### Tipografía
- **Principal**: Source Sans Pro (400, 600, 700)
- **Serif**: Source Serif Pro (400, 600, 900, italic)
- **Tamaños**:
  - H1: 36px
  - H2: 30px
  - H3: 24px
  - Body: 14px

### Header/Navegación
- **Navbar altura**: 65px
- **Background**: Color primario (#B10B1F)
- **Logo**: Centrado, color blanco
- **Estructura**: 
  - Menú hamburguesa (izquierda)
  - Logo (centro)
  - Account/Search (derecha)
- **Nav secundaria**: 50px, background blanco
- **Secciones**: Links horizontales con scroll

### Layout Homepage
- **Máximo ancho**: 960px (móvil), 1204px (desktop)
- **Grid**: Flexible, card-based
- **Separadores**: Bordes 2px solid en color secondary
- **Gap**: 9px-10px entre elementos
- **Cards**: Borde top 1px solid #e9e9e9

### Características Distintivas
- ✅ Barra "Hoy interesa:" con temas trending
- ✅ Color de marca fuerte y consistente
- ✅ Tipografía clara y legible
- ✅ Diseño limpio, mucho espacio blanco
- ✅ Separadores sutiles pero claros

---

## 🌐 EL UNIVERSAL

### Observaciones Generales
- Diseño más complejo y denso
- Múltiples secciones en homepage
- Grid más compacto
- Más contenido visible simultáneamente

### Colores Principales (inferidos de HTML)
- Azul oscuro para links
- Rojo para destacados
- Mucho uso de grises

### Características
- Header más complejo con múltiples niveles
- Secciones bien diferenciadas
- Uso intensivo de imágenes
- Cards con overlay de texto en imágenes

---

## 📰 EXCELSIOR

### Características Visuales
- Diseño tradicional de periódico
- Alto contraste
- Tipografía serif para títulos
- Layout en columnas clásico

### Elementos Destacados
- Sección de "Urgente" o "Breaking"
- Timeline de noticias
- Widgets laterales informativos

---

## 💼 EL ECONOMISTA

### Enfoque
- Diseño más sobrio, profesional
- Énfasis en datos y gráficos
- Colores corporativos
- Menos imágenes decorativas, más funcionales

---

## 📋 Patrones Comunes Encontrados

### 1. **Header**
Todos usan estructura de 2-3 niveles:
1. Barra superior (thin) - Utilidades/fecha
2. Main navbar (65-80px) - Logo + menú principal
3. Navegación secundaria (40-50px) - Secciones

### 2. **Colores**
- **Color primario**: Rojo (#B10B1F, #C41E3A) o Azul (#1A5490)
- **Background**: Siempre blanco o gris muy claro
- **Acentos**: Grises (#D1D1D1, #EDEDED, #F5F5F5)
- **Texto**: Negro o gris oscuro (#333)

### 3. **Tipografía**
Combinación común:
- **Sans-serif moderna** para UI y cuerpo: 
  - Source Sans Pro
  - Roboto
  - Arial/Helvetica
- **Serif para títulos** (opcional):
  - Source Serif Pro
  - Georgia
  - Playfair Display

### 4. **Espaciado**
- **Gap entre cards**: 9-15px
- **Padding interno**: 10-20px
- **Max-width contenedor**: 960-1200px
- **Margin vertical secciones**: 20-35px

### 5. **Cards de Noticias**
Estructura típica:
```
┌─────────────────────┐
│     [IMAGEN]        │ ← 16:9 o 4:3
├─────────────────────┤
│ [CATEGORÍA]         │ ← Pequeño, color
│ Título de noticia   │ ← Grande, bold
│ Breve descripción   │ ← Regular, gris
│ Autor • Fecha       │ ← Pequeño, gris
└─────────────────────┘
```

### 6. **Componentes Clave**

✅ **Breaking News Bar**
- Background: Amarillo (#FDE636) o Rojo
- Texto: Bold, scroll horizontal
- Posición: Top de página

✅ **Sección Destacada/Hero**
- Imagen grande (full-width o 60%)
- Overlay de gradiente para texto
- Título grande sobre imagen
- 1-3 noticias secundarias al lado

✅ **Grid de Noticias**
- Desktop: 3-4 columnas
- Tablet: 2 columnas  
- Mobile: 1 columna
- Gap consistente

✅ **Sidebar** (Desktop)
- Ancho: 300px
- Contenido:
  - Trending topics
  - Redes sociales
  - Newsletter signup
  - Publicidad

---

## 🎯 Recomendaciones para Implementar

### Actualizar Paletas CSS
Agregar paletas inspiradas en sitios reales:

```python
PALETAS_PROFESIONALES = {
    "periodistico_rojo": {
        "primary": "#B10B1F",      # Milenio
        "secondary": "#F1F1F1",
        "accent": "#D1D1D1",
        "urgent": "#FDE636"
    },
    "periodistico_azul": {
        "primary": "#1A5490",      # Universal
        "secondary": "#F5F5F5",
        "accent": "#C41E3A",       # Rojo complementario
        "urgent": "#FFD700"
    },
    "sobrio_corporativo": {
        "primary": "#2C3E50",      # Azul oscuro
        "secondary": "#ECF0F1",
        "accent": "#E74C3C",
        "urgent": "#F39C12"
    }
}
```

### Actualizar Tipografías
Priorizar:
1. **Source Sans Pro** (usar como default)
2. **Roboto** (alternativa moderna)
3. **Merriweather** (serif para contraste)
4. **Montserrat** (headers impactantes)

### Mejorar Layouts
Crear templates inspirados en:

**Template "Milenio-style"**:
- Header: 3 niveles (thin top + main 65px + sections 50px)
- Hero: Imagen grande + 2 secundarias
- Grid: 3 columnas con gaps 10px
- Cards: Separador top 1px #e9e9e9
- Colores: Rojo fuerte + grises suaves

**Template "Universal-style"**:
- Header: Complejo, múltiples utilidades
- Grid: Más denso, 4 columnas
- Sidebar: Sticky con widgets
- Más imágenes grandes

**Template "Economista-style"**:
- Diseño limpio, profesional
- Menos decoración
- Énfasis en contenido
- Colores sobrios

### Componentes Nuevos a Crear

1. **BreakingNewsBar**
```html
<div class="breaking-news-bar">
    <span class="label">URGENTE</span>
    <marquee>Última hora: ...</marquee>
</div>
```

2. **HeroSection** mejorado
```html
<section class="hero-split">
    <article class="hero-main"><!-- 60% --></article>
    <aside class="hero-secondary"><!-- 40%, 2 cards --></aside>
</section>
```

3. **CategoryTag** consistente
```html
<span class="category-tag" style="background: var(--primary)">
    POLÍTICA
</span>
```

4. **SocialShare** integrado
```html
<div class="article-meta">
    <span class="author">Por Juan Pérez</span>
    <span class="date">19 Ene 2026</span>
    <div class="social-share">
        <button>📘</button>
        <button>🐦</button>
        <button>📧</button>
    </div>
</div>
```

---

## ✅ Próximos Pasos

1. ✅ Crear esta documentación
2. ⏳ Actualizar `palette_generator.py` con paletas profesionales
3. ⏳ Actualizar `typography_generator.py` con fuentes de referencia
4. ⏳ Crear nuevos layouts en `layout_generator.py`:
   - `milenio_style`
   - `universal_dense`
   - `economista_clean`
5. ⏳ Implementar componentes nuevos:
   - BreakingNewsBar
   - HeroSplit
   - CategoryTags
6. ⏳ Ajustar `header_generator.py` para 3 niveles
7. ⏳ Mejorar cards con estructura estándar
8. ⏳ Actualizar CSS base con variables de referencia

---

## 📚 Recursos de Diseño

### Fuentes a Descargar
- **Source Sans Pro**: https://fonts.google.com/specimen/Source+Sans+Pro
- **Source Serif Pro**: https://fonts.google.com/specimen/Source+Serif+4
- **Merriweather**: https://fonts.google.com/specimen/Merriweather
- **Montserrat**: https://fonts.google.com/specimen/Montserrat

### Paletas de Color Verificadas
- Milenio: #B10B1F (verificado en sitio)
- Universal: Azul/Rojo (inferido)
- Excelsior: Rojo/Negro (tradicional)

### Grid Systems
- Max width: 960px (mobile-first) → 1200px (desktop)
- Gaps: 10px base, 20px secciones
- Columnas: 1 (mobile) → 3-4 (desktop)
