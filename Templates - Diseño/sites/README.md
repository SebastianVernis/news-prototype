# Sitios Generados - Cloudflare News Project

## Resumen

Se han generado **10 sitios de noticias completamente independientes** y funcionales, cada uno con su propio diseño único, paleta de colores, configuración tipográfica y **sistema CMS de administración con autenticación por token de 64 dígitos**.

## 📁 Estructura de Archivos

Cada sitio contiene:
```
sites/[nombre-sitio]/
├── index.html                 (Página principal)
├── style.css                  (Estilos personalizados)
├── script.js                  (JavaScript frontend)
├── legal.css                  (Páginas legales)
├── article.css                (Estilos para artículos)
├── terminos.html              (Términos de uso)
├── privacidad.html            (Política de privacidad)
├── acerca-de.html             (Acerca de)
├── contacto.html              (Contacto)
├── admin/                     (✨ CMS de Administración)
│   ├── index.html             (Dashboard)
│   ├── login.html             (Autenticación)
│   ├── style.css              (Estilos CMS)
│   ├── script.js              (Lógica CMS)
│   └── login.js               (Auth script)
├── categoria/                 (Páginas de categoría)
│   ├── nacional.html
│   ├── politica.html
│   ├── economia.html
│   └── deportes.html
└── articulo/                  (Página de artículo)
    └── informe-especial-tecnologia.html
```

**Total por sitio:** 14 archivos HTML + 4 archivos CSS + 2 archivos JS = **20 archivos**

**Total general:** 10 sitios × 20 archivos = **200+ archivos**

---

## 🔐 Sistema CMS (Panel de Administración)

Cada sitio incluye un **CMS completo con autenticación por token de 64 dígitos**.

### Acceder al CMS

1. **Navegue a:** `sites/[sitio]/admin/login.html`
2. **Ingrese el token** correspondiente (ver `CMS_TOKENS.txt`)
3. **Dashboard:** Gestione artículos, categorías y configuración

### Funcionalidades del CMS

✅ **Dashboard** con estadísticas en tiempo real
✅ **Crear artículos** con título, contenido, categoría, imagen, tags
✅ **Editar artículos** existentes
✅ **Eliminar artículos**
✅ **Búsqueda** en tiempo real
✅ **Estados:** Publicado/Borrador
✅ **Artículos destacados** (toggle)
✅ **Exportar datos** en JSON
✅ **Regenerar token** de seguridad

### Tokens de Acceso

Los tokens están en: **`sites/CMS_TOKENS.txt`**

```
radiocinconoticias: REDACTED_TOKEN
centralmexico:      REDACTED_TOKEN
tvmexico:           REDACTED_TOKEN
... (ver archivo completo)
```

⚠️ **IMPORTANTE:** Guarde `CMS_TOKENS.txt` en un lugar seguro.

### Cómo Usar el CMS

**Local:**
```bash
cd sites/radiocinconoticias
python3 -m http.server 8000
# Abrir: http://localhost:8000/admin/login.html
```

**Producción (Cloudflare Pages):**
```bash
wrangler pages deploy ./sites/radiocinconoticias --project-name=radiocinconoticias
# Abrir: https://radiocinconoticias.pages.dev/admin/login.html
```

📖 **Ver documentación completa:** `CMS_GUIDE.md`

---

## Lista de Sitios

### 1. Radio Cinco Noticias
- **Slug:** `radiocinconoticias`
- **Tagline:** "Tu conexión con la actualidad"
- **Colores:** Dark mode (negro/gris con acento dorado)
- **Layout:** 3-1-3 Grid
- **Icono:** `fa-broadcast-tower`
- **Dominio sugerido:** `radiocinconoticias.pages.dev`

### 2. Central México
- **Slug:** `centralmexico`
- **Tagline:** "El pulso de la nación"
- **Colores:** Azul corporativo (#004a99)
- **Layout:** Magazine Stack
- **Icono:** `fa-newspaper`
- **Dominio sugerido:** `centralmexico.pages.dev`

### 3. TV México
- **Slug:** `tvmexico`
- **Tagline:** "Información en movimiento"
- **Colores:** Rojo prensa (#c00000)
- **Layout:** Classic News
- **Icono:** `fa-tv`
- **Dominio sugerido:** `tvmexico.pages.dev`

### 4. CBN Noticias
- **Slug:** `cbnnoticias`
- **Tagline:** "Noticias con credibilidad"
- **Colores:** Azul marino (#003366)
- **Layout:** Masonry Grid
- **Icono:** `fa-globe`
- **Dominio sugerido:** `cbnnoticias.pages.dev`

### 5. México Informado
- **Slug:** `mexicoinformado`
- **Tagline:** "La verdad minuto a minuto"
- **Colores:** Verde México (#006341)
- **Layout:** Magazine
- **Icono:** `fa-check-circle`
- **Dominio sugerido:** `mexicoinformado.pages.dev`

### 6. Nodo Informativo
- **Slug:** `nodoinformativo`
- **Tagline:** "Conectando la información"
- **Colores:** Azul moderno (#1e3a8a)
- **Layout:** Masonry
- **Icono:** `fa-network-wired`
- **Dominio sugerido:** `nodoinformativo.pages.dev`

### 7. Bitácora Urbana
- **Slug:** `bitacoraurbana`
- **Tagline:** "Crónicas de la ciudad"
- **Colores:** Gris minimalista (#4a5568)
- **Layout:** Masonry
- **Icono:** `fa-city`
- **Dominio sugerido:** `bitacoraurbana.pages.dev`

### 8. Reporte Central MX
- **Slug:** `reportecentralmx`
- **Tagline:** "Análisis y profundidad"
- **Colores:** Dark profesional (#2d3748)
- **Layout:** Classic
- **Icono:** `fa-file-alt`
- **Dominio sugerido:** `reportecentralmx.pages.dev`

### 9. Vértice Noticias
- **Slug:** `verticenoticias`
- **Tagline:** "El punto exacto de la noticia"
- **Colores:** Rojo intenso (#9b2c2c)
- **Layout:** Masonry
- **Icono:** `fa-crosshairs`
- **Dominio sugerido:** `verticenoticias.pages.dev`

### 10. Noticias Objetivo (NUEVO)
- **Slug:** `noticiasobjetivo`
- **Tagline:** "Información sin censura"
- **Colores:** Rojo intenso + dorado
- **Layout:** 3-1-3 Grid
- **Icono:** `fa-bullseye`
- **Dominio sugerido:** `noticiasobjetivo.pages.dev`

~~### 10. Vanguardia Tecámac~~ (❌ Eliminado, reemplazado por Noticias Objetivo)

---

## Características Comunes

### Diseño Responsivo
Todos los sitios son completamente responsivos y se adaptan a:
- Móviles (≤480px)
- Tablets (481px - 768px)
- Tablets grandes (769px - 1024px)
- Escritorio (≥1025px)

### Componentes Incluidos
- **Header:** Sticky con logo, navegación y búsqueda
- **Breaking News:** Ticker de última hora
- **Featured Section:** Artículo destacado principal
- **News Grid:** Grid de noticias responsive
- **Footer:** 3 columnas con enlaces y redes sociales
- **Preloader:** Pantalla de carga animada

### Páginas Legales
Cada sitio incluye:
- Términos de uso
- Política de privacidad
- Acerca de
- Contacto
- Descargo de responsabilidad

### Categorías
- Nacional
- Política
- Economía
- Deportes

---

## Cómo Usar

### Opción 1: Despliegue Directo a Cloudflare Pages

Cada sitio puede desplegarse independientemente:

```bash
# Ejemplo para Radio Cinco Noticias
wrangler pages deploy ./sites/radiocinconoticias --project-name=radiocinconoticias
```

### Opción 2: Servidor Local para Pruebas

```bash
# Usar Python HTTP server
cd sites/radiocinconoticias
python3 -m http.server 8000

# Abrir en navegador: http://localhost:8000
```

### Opción 3: VS Code Live Server

1. Instalar extensión "Live Server"
2. Click derecho en `index.html` de cualquier sitio
3. Seleccionar "Open with Live Server"

---

## Personalización

### Cambiar Colores
Editar `style.css` en cada sitio:
```css
:root {
    --primary-color: #TU_COLOR;
    --secondary-color: #TU_COLOR;
    --accent-color: #TU_COLOR;
}
```

### Cambiar Fuentes
Editar Google Fonts en el `<head>` y las variables CSS:
```css
:root {
    --font-primary: 'Tu Fuente', serif;
    --font-secondary: 'Tu Fuente', sans-serif;
}
```

### Agregar Noticias
Editar el HTML en `index.html` y duplicar los bloques `<article class="news-card">`:
```html
<article class="news-card">
    <div class="card-image-wrapper">
        <img src="ruta/a/imagen.jpg" alt="Título">
        <span class="card-category-badge cat-nacional">Categoría</span>
    </div>
    <div class="card-content">
        <h3 class="card-title"><a href="articulo/slug.html">Título</a></h3>
        <p class="card-excerpt">Descripción breve...</p>
        <div class="card-footer">
            <span class="card-author">Por Autor</span>
            <span class="card-date">Fecha</span>
        </div>
    </div>
</article>
```

---

## Imágenes

Las imágenes actuales usan placeholders de `placehold.co`. Para usar imágenes reales:

1. Reemplazar las URLs en el HTML:
```html
<!-- Antes -->
<img src="https://placehold.co/400x250/004a99/ffffff?text=News+1" alt="...">

<!-- Después -->
<img src="assets/images/noticia-1.jpg" alt="...">
```

2. O usar imágenes externas:
```html
<img src="https://tusitio.com/imagen.jpg" alt="...">
```

---

## SEO Básico

Cada página incluye:
- Meta título único
- Meta descripción
- Etiquetas semánticas HTML5
- URLs amigables
- Jerarquía de encabezados (H1, H2, H3)

Para mejorar el SEO:
1. Agregar `sitemap.xml` en cada sitio
2. Configurar `robots.txt`
3. Agregar Open Graph tags para redes sociales
4. Implementar schema.org markup

---

## Próximos Pasos

### Inmediatos
1. [ ] Reemplazar imágenes placeholder con imágenes reales
2. [ ] Personalizar textos legales para cada sitio
3. [ ] Agregar más artículos de ejemplo
4. [ ] Configurar dominios en Cloudflare

### Futuros
1. [ ] Integrar con API de noticias
2. [ ] Agregar sistema de comentarios
3. [ ] Implementar newsletter
4. [ ] Agregar analytics
5. [ ] Optimizar performance (lazy loading, minificación)

---

## Soporte

Para preguntas o problemas, revisar:
- `QWEN.md` - Documentación principal del proyecto
- `docs/INDEX.md` - Índice de documentación
- `README.md` - README del proyecto principal

---

**Generado:** 19 de Febrero, 2026  
**Total de sitios:** 10  
**Total de archivos:** 170  
**Estado:** ✅ Completado
