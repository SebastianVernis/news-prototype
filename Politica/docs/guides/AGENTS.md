# 🤖 AGENTS.md - Guía de Gestión del Proyecto

## 📋 Información del Proyecto

**Nombre**: News Prototype - Generador Automático de Sitios de Noticias  
**Objetivo**: Sistema automatizado que genera sitios web de noticias únicos con contenido parafraseado, imágenes AI y diseños variados  
**Stack**: Python, CSS (sin frameworks), HTML5, IA (Blackbox Pro)

---

## 📊 DIAGRAMA DE FLUJO COMPLETO

**Ver diagrama detallado en:** `DIAGRAMA-FLUJO-COMPLETO.md`

### Resumen Visual del Flujo:
```
NewsAPI → Parafraseo → Expansión → Imágenes AI → Metadata → Logos → CSS → HTML → Sitios
```

---

## 🏗️ Arquitectura del Sistema

### Flujo Principal (master_orchestrator.py)
```
FASE 1: CONTENIDO
1. Descargar Noticias → NewsAPI (20 noticias)

FASE 2: TRANSFORMACIÓN
2A. Parafraseo → NewsParaphraser (8 estilos)
2B. Expansión → ArticleExpander (800 palabras, 8 estructuras)
2C. Asignar Autores → LegalPagesGenerator (20 autores)

FASE 3: IMÁGENES
3. Generar Imágenes → AIImageGenerator (Flux Schnell, 20 imágenes)

FASE 4: METADATA
4. Crear Metadata → SitePreCreation + SiteNameGenerator + DomainVerifier
   - 12 estilos de nombres
   - Verificación WHOIS (opcional)
   - Colores, categorías, contacto, SEO

FASE 5: LOGO
5. Generar Logo → AIImageGenerator (Flux Schnell, 1 logo)

FASE 6: CSS
6. Generar CSS → TemplateCombiner
   - ColorPaletteGenerator (20 paletas)
   - FontFamilyGenerator (15 fuentes)
   - LayoutCSSGenerator (20 layouts)
   - 6,000 combinaciones posibles

FASE 7: HTML
7. Generar HTML → LayoutGenerator + HTMLLayoutBuilder
   - HeaderGenerator (12 estilos)
   - FooterGenerator (3 columnas)
   - LegalPagesGenerator (4 páginas legales)
   - 25 páginas HTML totales
```

### Componentes Clave

#### 📁 `/scripts/`
- **master_orchestrator.py**: Orquestador principal del flujo
- **article-expander.py**: Expande noticias cortas a artículos completos
- **layout_generator.py**: Genera layouts HTML y configuraciones
- **template_combiner.py**: Combina CSS (paletas + fuentes + layouts)
- **header_generator.py**: Genera headers con diferentes estilos
- **footer_generator.py**: Genera footers con grid responsivo
- **color_palette_generator.py**: 20 paletas de color
- **font_family_generator.py**: 15 combinaciones de fuentes
- **layout_css_generator.py**: 20 layouts estructurales
- **generate-images-ai.py**: Genera imágenes con IA

#### 📁 `/data/`
- **noticias_newsapi_*.json**: Noticias originales de NewsAPI
- **noticias_paraphrased_*.json**: Noticias parafraseadas
- **sites_metadata/**: Metadata de sitios generados

#### 📁 `/generated_sites/`
- **site_N/**: Carpeta por sitio con index.html, style.css, imágenes, artículos

---

## 🎯 Reglas Críticas para Agentes

### ❌ NO HACER NUNCA
1. **NO editar archivos sin leerlos primero** - Siempre usar `view` antes de `edit`
2. **NO cambiar la estructura de datos** sin actualizar todos los consumidores
3. **NO modificar variables CSS** sin verificar su uso en componentes
4. **NO eliminar archivos de data/** sin confirmación explícita
5. **NO hacer commits** a menos que se solicite explícitamente
6. **NO agregar comentarios innecesarios** en el código

### ✅ HACER SIEMPRE
1. **Leer archivos antes de editar** - Verificar formato exacto (espacios, tabs, líneas)
2. **Copiar texto exacto** con todo el whitespace al usar `edit`
3. **Usar variables CSS** existentes en lugar de valores hardcoded
4. **Probar después de cambios** - Regenerar sitios y verificar en navegador
5. **Mantener consistencia** - Seguir patrones existentes en el código
6. **Documentar cambios** en este archivo si son arquitecturales

---

## 🎮 Menú Principal Interactivo

**RECOMENDADO:** Usar el menú interactivo para todas las operaciones

```bash
# Ejecutar menú principal
./menu.sh
# o
python menu.py
```

**Features:**
- ✅ Generación de sitios (5 modos)
- ✅ Tests y verificación (6 tests)
- ✅ Documentación completa (8 documentos)
- ✅ Utilidades del sistema (6 herramientas)

**Ver:** `MENU-PRINCIPAL.md` para guía completa

---

## 🔧 Comandos Comunes

### Menú Interactivo (Recomendado)
```bash
./menu.sh                           # Menú principal
# → 1 (Generación) → 1 (Rápido)    # Generar sitio
# → 2 (Tests) → 1 (Módulos)        # Verificar módulos
# → 3 (Docs) → 4 (Diagrama)        # Ver documentación
```

### CLI Directo

#### Generar Sitios
```bash
# Flujo completo (modo rápido)
python scripts/master_orchestrator.py

# Con verificación de dominios
python scripts/master_orchestrator.py --verificar-dominios

# Usar cache de noticias
python scripts/master_orchestrator.py --usar-cache

# Directorio personalizado
python scripts/master_orchestrator.py --output-dir /custom/path
```

#### Tests
```bash
# Verificar 16 módulos
python scripts/test/test_modulos_completo.py

# Test flujo completo (2 artículos)
python scripts/test/test_flujo_completo.py

# Test Blackbox API
python scripts/test/test_blackbox.py
```

#### Servir Sitio Local
```bash
cd generated_sites/site_1
python -m http.server 8001
# Abrir: http://localhost:8001
```

#### Limpiar
```bash
# Desde el menú: ./menu.sh → 4 → 1
# O manual:
rm -rf generated_sites generated_sites_test test_output_modules
```

---

## 📐 Sistema de Variables CSS

### Spacing Scale
```css
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */
--space-3xl: 4rem;     /* 64px */
```

### Breakpoints
```css
--breakpoint-sm: 640px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;
```

### Radius & Shadows
```css
--radius-sm: 0.25rem;
--radius-md: 0.5rem;
--radius-lg: 0.75rem;
--radius-xl: 1rem;

--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
```

---

## 🎨 CSS Grid Best Practices (Aplicadas)

### Grid Responsivo Moderno
```css
/* Auto-fit con minmax - Se adapta automáticamente */
.news-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(1rem, 3vw, 2rem);
}

/* Footer Grid */
.footer-grid.cols-3 {
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
}
```

### Tipografía Fluida
```css
/* Clamp para responsive sin media queries */
font-size: clamp(1.1rem, 2vw, 1.3rem);
```

### Mobile-First Breakpoints
```css
/* Base: Mobile */
@media (max-width: 640px) { ... }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { ... }

/* Desktop */
@media (min-width: 1025px) { ... }
```

---

## 🐛 Problemas Comunes y Soluciones

### Error: "old_string not found"
**Causa**: Whitespace no coincide exactamente  
**Solución**: 
1. Ver el archivo con `view`
2. Copiar el texto EXACTO (contar espacios/tabs)
3. Incluir 3-5 líneas de contexto
4. Verificar líneas en blanco

### Header/Footer se ven mal
**Causa**: CSS no tiene estilos completos  
**Solución**: Verificar que template_combiner.py incluya todos los estilos en `_get_common_components()`

### Imágenes no se generan
**Causa**: API key de Blackbox no configurada  
**Solución**: Verificar que la API key esté en el entorno

### Grid no es responsivo
**Causa**: Usando valores fijos en lugar de auto-fit  
**Solución**: Usar `repeat(auto-fit, minmax(min(100%, Xpx), 1fr))`

---

## 📝 Checklist Pre-Edición

Antes de editar cualquier archivo:

- [ ] Leer el archivo con `view` tool
- [ ] Identificar la sección exacta a modificar
- [ ] Copiar el texto EXACTO incluyendo whitespace
- [ ] Verificar cuántas veces aparece el texto
- [ ] Incluir contexto suficiente (3-5 líneas)
- [ ] Contar espacios/tabs para indentación
- [ ] Verificar líneas en blanco antes/después

Después de editar:

- [ ] Regenerar sitios de prueba
- [ ] Verificar en navegador
- [ ] Revisar CSS generado
- [ ] Verificar responsive design
- [ ] Actualizar esta documentación si aplica

---

## 🚀 Mejoras Recientes Aplicadas

### Context7 CSS Best Practices (13/01/2026)
- ✅ Sistema de variables CSS moderno (spacing, breakpoints, shadows)
- ✅ CSS Grid con auto-fit y minmax
- ✅ Tipografía fluida con clamp()
- ✅ Mobile-first responsive design
- ✅ Footer grid responsivo
- ✅ Header flexible con flexbox
- ✅ Cards con aspect-ratio y mejores transiciones
- ✅ Focus states y mejoras de accesibilidad

### Corrección Headers/Footers (13/01/2026)
- ✅ Clases CSS correctamente mapeadas
- ✅ Navegación separada del header principal
- ✅ Header-branding como contenedor consistente
- ✅ Footer sin espaciado extra en listas

---

## 📚 Referencias Útiles

### Context7 Libraries Consultadas
- `/websites/css-tricks_almanac` - CSS Grid y Flexbox
- `/websites/v3_tailwindcss` - Sistema de diseño moderno
- Benchmark Score: 85.9 (Tailwind v3)

### Documentación Interna
- `test_headers_footers.py` - Ejemplos de uso
- `layout_css_generator.py` - 20 layouts disponibles
- `color_palette_generator.py` - 20 paletas de color
- `font_family_generator.py` - 15 combinaciones de fuentes

---

## 💡 Notas para Futuros Agentes

1. **Siempre leer antes de editar** - No puedo enfatizar esto suficiente
2. **El CSS usa variables** - Reutilizar `--space-*`, `--radius-*`, etc.
3. **Los grids son auto-fit** - No hardcodear número de columnas
4. **Mobile-first** - Estilos base para móvil, luego desktop
5. **Componentes modulares** - Header, Footer, Cards son independientes
6. **Test después de cada cambio** - Regenerar y verificar visualmente

---

## 📄 Estructura de Páginas de Artículos

### HTML Semántico
```html
<main class="article-page">
  <div class="article-layout"> <!-- Grid 2 columnas -->
    <article class="article-full">
      <header class="article-header">
        <div class="article-category-badge">Categoría</div>
        <h1 class="article-title">Título</h1>
        <div class="article-meta">Autor • Fecha</div>
      </header>
      <figure class="article-image-wrapper">
        <img class="article-image">
      </figure>
      <div class="article-content">
        <p class="lead">Primer párrafo destacado</p>
        <p>Párrafos siguientes...</p>
      </div>
    </article>
    
    <aside class="article-sidebar">
      <div class="sidebar-section">
        <h2>Más Noticias</h2>
        <div class="sidebar-articles">
          <!-- 6 miniaturas de otros artículos -->
        </div>
      </div>
      <div class="sidebar-newsletter">
        <!-- Formulario de suscripción -->
      </div>
    </aside>
  </div>
</main>
```

### CSS Layout
```css
.article-layout {
    display: grid;
    grid-template-columns: 1fr 350px; /* Artículo + Sidebar */
    gap: var(--space-2xl);
}

.article-content .lead {
    font-size: 1.25rem; /* Primer párrafo más grande */
    font-weight: 500;
}
```

---

## 📚 Generador de Páginas Legales

### Módulo: legal_pages_generator.py

**Funcionalidades:**
- ✅ Términos y Condiciones completos
- ✅ Política de Privacidad (GDPR-compliant)
- ✅ FAQs con 10 preguntas frecuentes
- ✅ Acerca de Nosotros
- ✅ Generador de autores aleatorios (20 nombres)

**Uso:**
```python
from legal_pages_generator import LegalPagesGenerator

generator = LegalPagesGenerator()

# Generar autor aleatorio
autor = generator.generar_autor_aleatorio()

# Generar páginas
terms = generator.generar_terminos_condiciones(site_name, domain)
privacy = generator.generar_politica_privacidad(site_name, domain)
faqs = generator.generar_faqs(site_name)
about = generator.generar_acerca_de(site_name, tagline, domain)
```

**Páginas generadas automáticamente:**
- `/terminos.html` - Términos y Condiciones
- `/privacidad.html` - Política de Privacidad
- `/faqs.html` - Preguntas Frecuentes
- `/acerca.html` - Acerca de Nosotros

**Enlaces en footer:**
Las páginas legales están enlazadas automáticamente en la sección "Legal" del footer.

---

## 🔄 Historial de Cambios

### 2026-01-18 - 02:30 ✅ INTEGRACIÓN APILAYER WHOIS
- **Verificación dual de dominios**: Ahora soporta whois local + APILayer WHOIS API
- **Nuevo parámetro CLI**: `--api-whois` para usar APILayer en master_orchestrator.py
- **4 archivos nuevos**: domain_verifier_apilayer.py, test_apilayer_whois.py, APILAYER-WHOIS.md, APILAYER-SETUP.md
- **100% compatible**: Ambos métodos usan la misma interfaz
- **Parsing mejorado**: Manejo correcto de respuestas 404 (dominio disponible)
- **Tests completos**: 4/4 tests pasando con 100% de éxito
- **Free plan**: 100 requests/mes gratuitas de APILayer
- **Configuración**: Solo requiere `APILAYER_API_KEY` en .env

### 2026-01-15 - 16:30 ✅ VALIDADO
- **Sistema de imágenes con fallback**: Completamente funcional y validado
- **Todos los flujos integrados**: master_orchestrator.py, generate-interactive.py
- **Tests automatizados**: 7/7 tests pasando (100% éxito)
- **Compatibilidad**: Métodos generate_image() y process_articles() funcionando
- **Documentación final**: VALIDACION-IMAGEN-FALLBACK.md con tests completos
- **Estado**: ✅ LISTO PARA PRODUCCIÓN con Unsplash

### 2026-01-15 - 16:00
- **Corrección sistema de imágenes**: Flux Schnell no disponible (balance agotado fal.ai)
- **Nuevo módulo**: `generate-images-unsplash.py` (alternativa gratuita confiable)
- **Generador unificado**: `generate-images-unified.py` (IA + fallback automático)
- **Master orchestrator**: Ahora usa UnifiedImageGenerator con resiliencia total
- **Documentación**: IMAGEN-GENERATION-FIX.md con guía completa
- **Testing**: Verificado funcionamiento con Unsplash API + Picsum fallback

### 2026-01-15 - 15:40
- **Menú interactivo unificado**: `menu.py` con 4 secciones principales
- **Servidor HTTP integrado**: Servir sitios directamente desde el menú (4 modos)
- **Script auxiliar**: `scripts/serve_sites.py` para CLI directo
- **Documentación actualizada**: MENU-PRINCIPAL.md, ORGANIZACION-FINAL.md
- **30 opciones en menú**: Generación (6), Tests (6), Docs (8), Utilidades (6), Servidor (4)

### 2026-01-15 - 14:35
- **Diagrama de flujo completo**: Documentación exhaustiva del sistema completo
- **Verificación de módulos**: Confirmación de integración de todos los 16 módulos
- **Estadísticas del sistema**: 6,000 combinaciones CSS × 43,200 configuraciones HTML
- **Estructura de archivos**: Documentación de 27 archivos por sitio generado
- **Tiempos de ejecución**: ~2-3 minutos por sitio completo
- **Referencias actualizadas**: Links a DIAGRAMA-FLUJO-COMPLETO.md

### 2026-01-13 - 23:17
- **Generador de páginas legales**: Términos, Privacidad, FAQs, Acerca de
- **Autores aleatorios**: 20 nombres ficticios, sin usar fuentes originales
- **Enlaces funcionales**: Footer enlaza a páginas legales generadas
- **CSS para páginas legales**: Estilos consistentes y responsive

### 2026-01-13 - 23:08
- **Mejora de páginas de artículos**: Grid 2 columnas con sidebar
- **Marcado semántico**: Header, figure, article-content con clases
- **Sidebar con miniaturas**: 6 artículos relacionados con imágenes
- **Tipografía mejorada**: Párrafo lead destacado, jerarquía clara
- **Responsive**: Sidebar colapsa en mobile

### 2026-01-13 - 22:07
- Implementación completa de Context7 CSS best practices
- Sistema de variables moderno (spacing, breakpoints, shadows, radius)
- CSS Grid responsivo con auto-fit y minmax
- Mobile-first breakpoints (640px, 768px, 1024px, 1280px, 1536px)
- Corrección de mapeo de clases CSS en headers y footers
- Tipografía fluida con clamp()
- Mejoras de UX (transiciones, focus states, hover effects)

---

## 🔗 Referencias

- **Diagrama completo:** `DIAGRAMA-FLUJO-COMPLETO.md` - Flujo detallado con todos los módulos, estadísticas y ejemplos
- **Context7 Libraries:** `/websites/css-tricks_almanac`, `/websites/v3_tailwindcss`
- **Test files:** `scripts/test/test_*.py`

---

**Última actualización**: 2026-01-15 14:35  
**Versión**: 2.0  
**Mantenido por**: Agentes IA asistiendo el desarrollo
