#!/usr/bin/env python3
"""
Script para agregar estilos responsive completos a los 10 sitios
"""

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))

# CSS Responsive completo
responsive_css = """
/* ============================================
   ESTILOS RESPONSIVE PARA MÓVILES
   ============================================ */

/* Base responsive */
* {
    box-sizing: border-box;
}

body {
    overflow-x: hidden;
}

.container {
    width: 100%;
    padding: 0 15px;
}

/* Header responsive */
.header, .main-header {
    position: relative;
}

.logo-bold, .site-logo {
    font-size: 1.5em !important;
}

.tagline-bold, .site-tagline {
    font-size: 0.9em !important;
}

/* Navegación móvil */
.nav {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.nav-link {
    padding: 8px 12px;
    font-size: 0.9em;
}

/* Grid de noticias responsive */
.news-grid, .featured-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    padding: 15px;
}

/* Tarjetas de noticias responsive */
.news-card, .featured-card {
    width: 100%;
    margin-bottom: 20px;
}

.card-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.card-image-wrapper {
    width: 100%;
    overflow: hidden;
}

.card-content {
    padding: 15px;
}

.card-title {
    font-size: 1.1em;
    line-height: 1.4;
}

.card-excerpt {
    font-size: 0.9em;
    line-height: 1.5;
}

/* Carrusel responsive */
section[style*="background:#f5f5f5"] {
    padding: 20px 10px !important;
}

section[style*="background:#f5f5f5"] h2 {
    font-size: 1.5em !important;
}

section[style*="background:#f5f5f5"] article {
    margin-bottom: 20px;
}

section[style*="background:#f5f5f5"] img {
    height: 180px !important;
}

/* Artículos completos responsive */
.complete-articles {
    padding: 20px 10px !important;
}

.complete-articles h2 {
    font-size: 1.8em !important;
}

.complete-articles article {
    width: 100%;
}

.complete-articles img {
    height: 180px !important;
}

.complete-articles h3 {
    font-size: 1.2em !important;
}

.complete-articles p {
    font-size: 0.9em !important;
}

/* Footer responsive */
.footer, .main-footer {
    padding: 30px 15px !important;
}

.footer-grid {
    grid-template-columns: 1fr !important;
    gap: 20px !important;
}

.footer-column {
    margin-bottom: 20px;
}

/* Preloader responsive */
#preloader {
    width: 100%;
    height: 100%;
}

/* Breaking news ticker */
.breaking-news-ticker {
    font-size: 0.9em;
}

/* Featured section */
.featured-section {
    padding: 20px 15px !important;
}

/* Sidebar responsive - ocultar en móviles */
.sidebar {
    display: none;
}

.main-with-sidebar {
    display: block !important;
}

/* Media Queries específicos */
@media (max-width: 768px) {
    /* Ajustes para tablets y móviles */
    .container {
        max-width: 100%;
    }
    
    .header-bold {
        padding: 15px 0;
    }
    
    .logo-bold {
        font-size: 1.3em !important;
    }
    
    .nav {
        justify-content: center;
    }
    
    .nav-link {
        font-size: 0.85em;
        padding: 6px 10px;
    }
    
    /* Grid de 1 columna */
    .news-grid,
    .featured-grid,
    .categories-grid {
        grid-template-columns: 1fr;
    }
    
    /* Imágenes más pequeñas */
    .card-image,
    .featured-article img {
        height: 180px !important;
    }
    
    /* Textos más legibles */
    h1 { font-size: 1.8em !important; }
    h2 { font-size: 1.5em !important; }
    h3 { font-size: 1.2em !important; }
    h4 { font-size: 1em !important; }
    p { font-size: 0.95em !important; }
    
    /* Padding reducido */
    section {
        padding: 20px 10px !important;
    }
    
    /* Footer en una columna */
    .footer-grid {
        grid-template-columns: 1fr !important;
    }
}

@media (max-width: 480px) {
    /* Ajustes para móviles pequeños */
    .logo-bold {
        font-size: 1.2em !important;
    }
    
    .tagline-bold {
        font-size: 0.8em !important;
    }
    
    .nav-link {
        font-size: 0.8em;
        padding: 5px 8px;
    }
    
    /* Imágenes aún más pequeñas */
    .card-image {
        height: 160px !important;
    }
    
    /* Contenido compacto */
    .card-content {
        padding: 12px;
    }
    
    .card-title {
        font-size: 1em !important;
    }
    
    .card-excerpt {
        font-size: 0.85em !important;
    }
}

/* Utilidades responsive */
.mobile-only {
    display: none;
}

@media (max-width: 768px) {
    .mobile-only {
        display: block;
    }
    
    .desktop-only {
        display: none;
    }
}

/* Touch-friendly buttons */
button, .btn-subscribe, .nav-link {
    min-height: 44px;
    min-width: 44px;
}

/* Evitar zoom en inputs en iOS */
input, textarea, select {
    font-size: 16px !important;
}
"""

def update_site_css(site_num):
    """Agrega CSS responsive a un sitio"""
    site_file = SITES_DIR / f'site{site_num}.html'
    
    if not site_file.exists():
        print(f"⚠️ Archivo no encontrado: {site_file}")
        return False
    
    with open(site_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar CSS responsive antes del </head>
    responsive_styles = f'\n    <style id="responsive-styles">\n{responsive_css}\n    </style>\n'
    
    if '</head>' in content:
        content = content.replace('</head>', responsive_styles + '\n</head>')
    
    # Agregar meta viewport si no existe
    if '<meta name="viewport"' not in content:
        viewport_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">'
        if '</head>' in content:
            content = content.replace('</head>', viewport_meta + '\n</head>')
    
    # Agregar script para menú móvil
    mobile_menu_script = '''
    <script>
        // Menú móvil responsive
        document.addEventListener('DOMContentLoaded', function() {
            var nav = document.querySelector('.nav');
            if (nav) {
                // Crear botón de menú móvil
                var menuButton = document.createElement('button');
                menuButton.innerHTML = '☰ Menú';
                menuButton.style.cssText = 'display:none;background:#3498db;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;font-size:1em;margin:10px 0;';
                menuButton.onclick = function() {
                    nav.style.display = nav.style.display === 'none' ? 'flex' : 'none';
                };
                
                // Mostrar botón en móviles
                if (window.innerWidth <= 768) {
                    menuButton.style.display = 'block';
                    nav.style.display = 'none';
                }
                
                // Insertar botón antes del nav
                nav.parentNode.insertBefore(menuButton, nav);
                
                // Ajustar en resize
                window.addEventListener('resize', function() {
                    if (window.innerWidth > 768) {
                        menuButton.style.display = 'none';
                        nav.style.display = 'flex';
                    } else {
                        menuButton.style.display = 'block';
                        nav.style.display = 'none';
                    }
                });
            }
        });
    </script>
'''
    
    if '</body>' in content:
        content = content.replace('</body>', mobile_menu_script + '\n</body>')
    
    # Guardar archivo actualizado
    with open(site_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Sitio {site_num} actualizado con CSS responsive")
    return True

def main():
    print("📱 Agregando estilos responsive a los 10 sitios...")
    print("="*60)
    
    # Actualizar los 10 sitios
    for i in range(1, 11):
        update_site_css(i)
    
    print("="*60)
    print("✅ Los 10 sitios actualizados con:")
    print("   📱 Meta viewport para móviles")
    print("   🎨 CSS responsive completo")
    print("   🍔 Menú móvil hamburguesa")
    print("   📐 Grids adaptables (1 columna en móvil)")
    print("   👆 Botones touch-friendly (44px mín)")
    print("   📏 Media queries (768px, 480px)")

if __name__ == "__main__":
    main()
