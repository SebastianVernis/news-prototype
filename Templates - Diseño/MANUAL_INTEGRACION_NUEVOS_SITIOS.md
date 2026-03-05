# 📘 Manual Técnico: Integración de Nuevos Sitios (Cloudflare News)

Este manual detalla el procedimiento técnico exacto para integrar un nuevo sitio de noticias en el ecosistema. El sistema utiliza una arquitectura **Multi-Tenant** basada en Cloudflare Pages, donde la lógica se separa en: **Frontend Estático (Sites)**, **Backend Serverless (Functions)** y **Capa de Datos (Metadata/KV)**.

---

## 1. Lógica de Enrutamiento (Routing Engine)

El sistema utiliza `_redirects` y `_headers` de Cloudflare para manejar el tráfico. La lógica de rutas sigue este patrón:

### A. Mapeo de Subcarpetas
Cada sitio tiene su propia ruta física en el sistema de archivos, pero la API es compartida.
- **Ruta del Sitio:** `https://midominio.com/sites/nombre-sitio/`
- **Ruta de la API:** `https://midominio.com/api/news?site=nombre-sitio`

### B. Configuración de `_redirects` (Ejemplo Exacto)
Para asegurar que las URLs sean limpias y que el nuevo sitio cargue correctamente, se debe añadir al archivo `public/_redirects`:
```text
/nuevo-sitio/*  /sites/nuevo-sitio/:splat  200
/api/nuevo-sitio/*  /functions/api/news?site=nuevo-sitio  200
```

---

## 2. Definición del Data Model (Metadata)

Para que el backend "reconozca" el sitio, debe existir un archivo de configuración en `data/sites_metadata/nuevo-sitio.json`. 

### Ejemplo de `data/sites_metadata/nuevo-sitio.json`:
```json
{
  "id": "nuevo-sitio",
  "name": "Nuevo Portal de Noticias",
  "category_default": "General",
  "facebook_page_id": "1234567890",
  "theme": {
    "primary": "#1a73e8",
    "secondary": "#ffffff",
    "accent": "#fbbc04"
  },
  "selectors": {
    "container": "#news-grid",
    "template": "card-modern"
  }
}
```

---

## 3. Lógica JS de Integración (Cliente)

El JavaScript en cada sitio debe consumir la API de forma dinámica. Se recomienda usar un patrón de **Inyección de Dependencias** basado en el `siteId`.

### Estructura sugerida para `sites/nuevo-sitio/js/main.js`:
```javascript
/**
 * Lógica de Inicialización Dinámica
 */
const AppConfig = {
    // Detecta el ID del sitio desde la URL o el JSON de metadata
    siteId: window.location.pathname.split('/')[2] || 'default',
    apiEndpoint: `/api/news`,
    container: document.getElementById('news-container')
};

async function fetchSiteContent() {
    try {
        const response = await fetch(`${AppConfig.apiEndpoint}?site=${AppConfig.siteId}`);
        if (!response.ok) throw new Error('Error al cargar noticias');
        
        const data = await response.json();
        renderArticles(data.articles);
    } catch (err) {
        console.error(`[${AppConfig.siteId}] Critical Error:`, err);
        AppConfig.container.innerHTML = '<p>Error cargando noticias.</p>';
    }
}

function renderArticles(articles) {
    if (!articles || articles.length === 0) {
        AppConfig.container.innerHTML = '<p>No hay noticias disponibles.</p>';
        return;
    }
    
    AppConfig.container.innerHTML = articles.map(article => `
        <article class="news-card" data-id="${article.id}">
            <img src="${article.image || '/assets/images/fallback-1.svg'}" alt="${article.title}">
            <div class="content">
                <span class="category">${article.category}</span>
                <h3>${article.title}</h3>
                <p>${article.excerpt}</p>
                <a href="/article/${article.slug}" class="read-more">Leer más</a>
            </div>
        </article>
    `).join('');
}

document.addEventListener('DOMContentLoaded', fetchSiteContent);
```

---

## 4. Generación de Estilos (Tailored UI)

El script `sites/generate-style-custom.js` automatiza la creación del CSS temático. 

**Lógica interna:**
1. Lee `data/sites_metadata/{site}.json`.
2. Procesa el objeto `theme`.
3. Genera variables CSS en `:root`.

### Ejemplo de Salida en `sites/{site}/css/style-custom.css`:
```css
/* AUTO-GENERATED - DO NOT EDIT MANUALLY */
:root {
    --site-primary: #1a73e8;
    --site-bg: #ffffff;
    --site-accent: #fbbc04;
    --site-name: "Nuevo Portal de Noticias";
}

.news-card:hover {
    border-bottom: 4px solid var(--site-primary);
    transform: translateY(-5px);
}
```

---

## 5. Vinculación con la API (Cloudflare Workers)

La API en `public/functions/api/news.js` utiliza el parámetro `site` para filtrar los contenidos. La vinculación es directa:

1.  **Validación:** El Worker verifica si el `siteId` existe en el sistema de archivos de metadata.
2.  **Filtrado:** Se consultan los artículos cuya propiedad `site_target` coincida con el ID solicitado.
3.  **Respuesta:** Devuelve un JSON con los artículos procesados y parafraseados.

---

## 6. Checklist de Despliegue

1.  **Directorio:** Crear carpeta `sites/nombre-sitio/`.
2.  **Metadata:** Crear `data/sites_metadata/nombre-sitio.json`.
3.  **Assets:** Asegurar que `index.html` referencia a `/api/news?site=nombre-sitio`.
4.  **Estilos:** Ejecutar `node sites/generate-style-custom.js --site=nombre-sitio`.
5.  **RRSS:** Vincular Facebook Page ID en `scripts/setup_fb_tokens.py`.
6.  **Verificación:** Navegar a `https://midominio.com/api/news?site=nombre-sitio` para confirmar la salida de datos.

---
*Documento generado para la estandarización del proceso de expansión de la red de noticias.*
