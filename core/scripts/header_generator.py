#!/usr/bin/env python3
"""
Generador Modular de Headers para Sitios de Noticias
Crea componentes de header con diferentes estilos y variaciones
"""

import random
from typing import Dict, List, Optional


class HeaderGenerator:
    """Generador de componentes de header dinámicos"""
    
    # Estilos de header disponibles
    HEADER_STYLES = {
        "centered": {
            "name": "Logo Centrado",
            "description": "Logo y tagline centrados, navegación debajo",
            "classes": "header-centered"
        },
        "left_aligned": {
            "name": "Alineado Izquierda",
            "description": "Logo a la izquierda, navegación a la derecha",
            "classes": "header-left-aligned"
        },
        "split": {
            "name": "Dividido",
            "description": "Logo izquierda, menú derecha, espacio entre ambos",
            "classes": "header-split"
        },
        "minimal": {
            "name": "Minimalista",
            "description": "Diseño minimalista con elementos esenciales",
            "classes": "header-minimal"
        },
        "bold": {
            "name": "Audaz",
            "description": "Header grande y llamativo con tipografía bold",
            "classes": "header-bold"
        },
        "stacked": {
            "name": "Apilado",
            "description": "Logo, tagline y navegación apilados verticalmente",
            "classes": "header-stacked"
        },
        "floating": {
            "name": "Flotante",
            "description": "Header transparente flotante sobre contenido",
            "classes": "header-floating"
        },
        "compact": {
            "name": "Compacto",
            "description": "Header delgado y compacto",
            "classes": "header-compact"
        },
        "magazine_style": {
            "name": "Estilo Revista",
            "description": "Elegante estilo editorial de revista",
            "classes": "header-magazine"
        },
        "newspaper_banner": {
            "name": "Banner Periódico",
            "description": "Estilo banner de periódico tradicional",
            "classes": "header-newspaper"
        },
        "modern_thin": {
            "name": "Moderno Delgado",
            "description": "Header moderno ultra delgado",
            "classes": "header-modern-thin"
        },
        "boxed_header": {
            "name": "Header en Caja",
            "description": "Header contenido en una caja con borde",
            "classes": "header-boxed"
        }
    }
    
    # Estilos de navegación
    NAV_STYLES = {
        "horizontal": {
            "name": "Horizontal",
            "description": "Menú horizontal clásico",
            "classes": "nav-horizontal"
        },
        "horizontal_center": {
            "name": "Horizontal Centrado",
            "description": "Menú horizontal centrado",
            "classes": "nav-horizontal-center"
        },
        "hamburger": {
            "name": "Hamburguesa",
            "description": "Menú hamburguesa colapsable",
            "classes": "nav-hamburger",
            "mobile_friendly": True
        },
        "sidebar_nav": {
            "name": "Navegación Lateral",
            "description": "Navegación en sidebar",
            "classes": "nav-sidebar"
        },
        "mega_menu": {
            "name": "Mega Menú",
            "description": "Mega menú con categorías expandidas",
            "classes": "nav-mega_menu"
        },
        "dropdown": {
            "name": "Dropdown",
            "description": "Menú con submenús dropdown",
            "classes": "nav-dropdown"
        },
        "tabs": {
            "name": "Pestañas",
            "description": "Estilo pestañas",
            "classes": "nav-tabs"
        },
        "pills": {
            "name": "Pills",
            "description": "Menú estilo botones pills",
            "classes": "nav-pills"
        },
        "vertical_stack": {
            "name": "Apilado Vertical",
            "description": "Menú vertical apilado",
            "classes": "nav-vertical"
        },
        "icon_menu": {
            "name": "Menú con Iconos",
            "description": "Menú con iconos y texto",
            "classes": "nav-icon_menu"
        },
        "sticky_nav": {
            "name": "Navegación Pegajosa",
            "description": "Navegación que se mantiene visible al scroll",
            "classes": "nav-sticky",
            "sticky": True
        },
        "offcanvas": {
            "name": "Offcanvas",
            "description": "Menú lateral offcanvas",
            "classes": "nav-offcanvas",
            "mobile_friendly": True
        }
    }
    
    # Elementos adicionales para header
    HEADER_ELEMENTS = [
        "search_bar",      # Barra de búsqueda
        "social_links",    # Enlaces a redes sociales
        "subscribe_button", # Botón de suscripción
        "date_time",       # Fecha y hora actual
        "weather",         # Widget de clima
        "language_selector", # Selector de idioma
        "user_menu",       # Menú de usuario/login
        "breaking_news",   # Ticker de noticias de última hora
        "ad_banner"        # Banner publicitario
    ]
    
    def __init__(self):
        """Inicializa el generador"""
        pass
    
    def generar_header(self, site_name: str, tagline: str, 
                      categorias: List[str],
                      header_style: Optional[str] = None,
                      nav_style: Optional[str] = None,
                      elementos_extra: Optional[List[str]] = None,
                      sticky: bool = False,
                      logo_path: Optional[str] = None) -> str:
        """
        Genera el HTML de un header completo
        
        Args:
            site_name: Nombre del sitio
            tagline: Lema/tagline del sitio
            categorias: Lista de categorías para navegación
            header_style: Estilo de header (aleatorio si es None)
            nav_style: Estilo de navegación (aleatorio si es None)
            elementos_extra: Elementos adicionales a incluir
            sticky: Si el header debe ser sticky
            logo_path: Ruta al archivo de logo (opcional)
            
        Returns:
            str: HTML del header
        """
        # Seleccionar estilos
        if not header_style:
            header_style = random.choice(list(self.HEADER_STYLES.keys()))
        if not nav_style:
            nav_style = random.choice(list(self.NAV_STYLES.keys()))
        
        header_config = self.HEADER_STYLES[header_style]
        nav_config = self.NAV_STYLES[nav_style]
        
        # Determinar clases - NO incluir nav_config['classes'] aquí
        header_classes = f"header {header_config['classes']}"
        if sticky or nav_config.get('sticky', False):
            header_classes += " sticky"
        
        # Generar elementos adicionales
        extras_html = ""
        if elementos_extra:
            extras_html = self._generar_elementos_extra(elementos_extra)
        
        # Generar navegación
        nav_html = self._generar_navegacion(categorias, nav_config)
        
        # Generar logo y tagline
        logo_html = self._generar_logo_tagline(site_name, tagline, header_style, logo_path)
        
        # Ensamblar header según estilo + agregar offcanvas si mobile_friendly
        mobile_menu = ""
        if nav_config.get('mobile_friendly', False):
            # Generar offcanvas menu
            nav_items_offcanvas = []
            for cat in categorias:
                cat_slug = cat.lower().replace(' ', '-')
                nav_items_offcanvas.append(f'<a href="#{cat_slug}" class="nav-link">{cat}</a>')
            
            offcanvas_items = '\n                '.join(nav_items_offcanvas)
            mobile_menu = f"""
    <!-- Offcanvas Menu -->
    <div class="offcanvas" id="offcanvas-menu">
        <button class="offcanvas-close" aria-label="Cerrar menú">&times;</button>
        <nav class="nav">
            {offcanvas_items}
        </nav>
    </div>
    <div class="offcanvas-overlay" id="offcanvas-overlay"></div>"""
        
        # Ensamblar header según estilo
        if header_style in ["centered", "stacked"]:
            header_html = f"""
    <header class="{header_classes}">
        <div class="container">
            {logo_html}
            {nav_html}
            {extras_html}
        </div>
    </header>{mobile_menu}"""
        
        elif header_style in ["split", "left_aligned"]:
            header_html = f"""
    <header class="{header_classes}">
        <div class="container">
            {logo_html}
            {nav_html}
            {extras_html}
        </div>
    </header>{mobile_menu}"""
        
        else:
            # Default layout
            header_html = f"""
    <header class="{header_classes}">
        <div class="container">
            {logo_html}
            {nav_html}
            {extras_html}
        </div>
    </header>{mobile_menu}"""
        
        return header_html
    
    def _generar_logo_tagline(self, site_name: str, tagline: str, 
                             header_style: str, logo_path: str = None) -> str:
        """Genera el HTML del logo y tagline"""
        
        # Usar 'header-branding' como clase consistente para el contenedor
        # Si existe logo, mostrar imagen + texto, sino solo texto
        logo_html = f'<h1 class="logo">{site_name}</h1>'
        
        if logo_path:
            logo_html = f'''<div class="logo-image">
                    <img src="logo.jpg" alt="{site_name}" class="logo-img">
                    <h1 class="logo">{site_name}</h1>
                </div>'''
        
        if header_style in ["minimal", "modern_thin"]:
            return f"""
            <div class="header-branding">
                {logo_html}
            </div>"""
        
        return f"""
            <div class="header-branding">
                {logo_html}
                <p class="tagline">{tagline}</p>
            </div>"""
    
    def _generar_navegacion(self, categorias: List[str], 
                          nav_config: Dict) -> str:
        """Genera el HTML de la navegación"""
        
        nav_classes = nav_config['classes']
        
        # Generar items de navegación
        nav_items = []
        for cat in categorias:
            cat_slug = cat.lower().replace(' ', '-')
            nav_items.append(f'<a href="#{cat_slug}" class="nav-link">{cat}</a>')
        
        nav_items_html = '\n                '.join(nav_items)
        
        if nav_config.get('mobile_friendly', False):
            # Incluir botón hamburguesa para móvil
            return f"""
            <button class="nav-toggle" aria-label="Toggle navigation">
                <span class="hamburger"></span>
            </button>
            <nav class="nav {nav_classes}">
                {nav_items_html}
            </nav>"""
        
        return f"""
            <nav class="nav {nav_classes}">
                {nav_items_html}
            </nav>"""
    
    def _generar_elementos_extra(self, elementos: List[str]) -> str:
        """Genera HTML para elementos adicionales del header"""
        
        html_parts = []
        
        if "search_bar" in elementos:
            html_parts.append('''
            <div class="header-search">
                <input type="search" placeholder="Buscar noticias..." class="search-input">
                <button class="search-btn" aria-label="Buscar">🔍</button>
            </div>''')
        
        if "social_links" in elementos:
            html_parts.append('''
            <div class="header-social">
                <a href="#" class="social-link" aria-label="Facebook">📘</a>
                <a href="#" class="social-link" aria-label="Twitter">🐦</a>
                <a href="#" class="social-link" aria-label="Instagram">📷</a>
            </div>''')
        
        if "subscribe_button" in elementos:
            html_parts.append('''
            <div class="header-cta">
                <button class="btn-subscribe">Suscribirse</button>
            </div>''')
        
        if "date_time" in elementos:
            html_parts.append('''
            <div class="header-datetime">
                <span class="current-date">Martes, 7 de enero 2026</span>
            </div>''')
        
        if "language_selector" in elementos:
            html_parts.append('''
            <div class="header-language">
                <select class="language-selector">
                    <option value="es">ES</option>
                    <option value="en">EN</option>
                </select>
            </div>''')
        
        if "user_menu" in elementos:
            html_parts.append('''
            <div class="header-user">
                <a href="#" class="user-link">👤 Iniciar sesión</a>
            </div>''')
        
        if "breaking_news" in elementos:
            html_parts.append('''
            <div class="breaking-news-ticker">
                <span class="ticker-label">🔴 ÚLTIMA HORA:</span>
                <div class="ticker-content">
                    <span>Noticia importante en desarrollo...</span>
                </div>
            </div>''')
        
        if html_parts:
            return f'''
            <div class="header-actions">
                {''.join(html_parts)}
            </div>'''
        
        return ""
    
    def generar_configuracion_aleatoria(self) -> Dict:
        """
        Genera una configuración aleatoria de header
        
        Returns:
            dict: Configuración del header
        """
        # Seleccionar elementos extra aleatorios (0-3 elementos)
        num_extras = random.randint(0, 3)
        elementos_extra = random.sample(self.HEADER_ELEMENTS, num_extras) if num_extras > 0 else []
        
        config = {
            "header_style": random.choice(list(self.HEADER_STYLES.keys())),
            "nav_style": random.choice(list(self.NAV_STYLES.keys())),
            "elementos_extra": elementos_extra,
            "sticky": random.choice([True, False])
        }
        
        return config
    
    def obtener_estilos_css_base(self) -> str:
        """
        Retorna CSS base para los headers
        
        Returns:
            str: CSS base
        """
        return """
/* ===== BASE HEADER STYLES ===== */
.header {
    background: var(--card-bg);
    border-bottom: 1px solid var(--color-border, rgba(0,0,0,0.1));
    position: relative;
    z-index: var(--z-header, 100);
    transition: var(--transition-base, all 250ms ease-in-out);
}

.header.sticky {
    position: sticky;
    top: 0;
    box-shadow: var(--shadow-md, 0 4px 6px rgba(0,0,0,0.1));
}

.header.sticky .logo {
    font-size: 1.5rem;
    transition: font-size var(--transition-base, 250ms ease-in-out);
}

.header .container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
}

/* Logo and Tagline */
.logo {
    font-size: 1.8rem;
    font-weight: var(--heading-weight);
    color: var(--primary-color);
    margin: 0;
    font-family: var(--font-primary);
}

.tagline {
    font-size: 0.9rem;
    color: var(--light-text);
    margin: 0.25rem 0 0 0;
    font-family: var(--font-secondary);
}

/* Navigation Base */
.nav {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

.nav-link {
    color: var(--text-color);
    text-decoration: none;
    font-weight: var(--font-weight-bold, 700);
    transition: color 0.3s ease;
    font-family: var(--font-secondary);
    text-transform: var(--menu-transform, uppercase);
    font-size: var(--menu-size, 12px);
    letter-spacing: var(--letter-spacing-wide, 0.05em);
}

.nav-link:hover {
    color: var(--color-primary, var(--accent-color));
}

/* Header Actions */
.header-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.search-input {
    padding: 0.5rem 1rem;
    border: 1px solid rgba(0,0,0,0.2);
    border-radius: 20px;
    font-family: var(--font-secondary);
}

.btn-subscribe {
    padding: 0.5rem 1.5rem;
    background: var(--accent-color);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 600;
    font-family: var(--font-secondary);
}

/* Header Style Variations */
.header-centered .container {
    flex-direction: column;
    text-align: center;
}

.header-stacked .container {
    flex-direction: column;
}

.header-minimal .tagline {
    display: none;
}

.header-floating {
    position: absolute;
    background: transparent;
    backdrop-filter: blur(10px);
}

.header-compact {
    padding: 0.5rem 0;
}

/* Offcanvas Menu (Mobile) */
.nav-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    z-index: var(--z-header, 100);
}

.hamburger {
    display: block;
    width: 25px;
    height: 2px;
    background: var(--text-color, #333);
    position: relative;
    transition: var(--transition-base, 250ms ease-in-out);
}

.hamburger::before,
.hamburger::after {
    content: '';
    display: block;
    width: 25px;
    height: 2px;
    background: var(--text-color, #333);
    position: absolute;
    transition: var(--transition-base, 250ms ease-in-out);
}

.hamburger::before { top: -8px; }
.hamburger::after { bottom: -8px; }

/* Offcanvas Panel */
.offcanvas {
    position: fixed;
    top: 0;
    right: -100%;
    width: 300px;
    height: 100vh;
    background: var(--card-bg, #fff);
    box-shadow: -2px 0 10px rgba(0,0,0,0.1);
    z-index: var(--z-offcanvas, 200);
    transition: right var(--transition-base, 300ms ease-in-out);
    padding: 2rem;
    overflow-y: auto;
}

.offcanvas.active {
    right: 0;
}

.offcanvas-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: calc(var(--z-offcanvas, 200) - 1);
    opacity: 0;
    visibility: hidden;
    transition: var(--transition-base, 300ms ease-in-out);
}

.offcanvas-overlay.active {
    opacity: 1;
    visibility: visible;
}

.offcanvas .nav {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
}

.offcanvas .nav-link {
    width: 100%;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--color-border, #eee);
    text-transform: var(--menu-transform, uppercase);
    font-size: var(--menu-size, 12px);
    font-weight: var(--font-weight-bold, 700);
}

.offcanvas-close {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text-color, #333);
}

/* Responsive */
@media (max-width: 768px) {
    .nav-toggle {
        display: block;
    }
    
    .header .nav {
        display: none;
    }
    
    .header .container {
        flex-wrap: wrap;
        justify-content: space-between;
    }
    
    .header-branding {
        flex: 1;
    }
    
    .header-actions {
        display: flex;
        gap: 0.5rem;
    }
}

@media (min-width: 769px) {
    .offcanvas,
    .offcanvas-overlay {
        display: none;
    }
}

/* Offcanvas JavaScript - Agregar al final del HTML */
/*
<script>
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.querySelector('.nav-toggle');
    const offcanvas = document.querySelector('.offcanvas');
    const overlay = document.querySelector('.offcanvas-overlay');
    const closeBtn = document.querySelector('.offcanvas-close');
    
    if (toggle && offcanvas && overlay) {
        toggle.addEventListener('click', () => {
            offcanvas.classList.add('active');
            overlay.classList.add('active');
        });
        
        const close = () => {
            offcanvas.classList.remove('active');
            overlay.classList.remove('active');
        };
        
        if (closeBtn) closeBtn.addEventListener('click', close);
        overlay.addEventListener('click', close);
    }
});
</script>
*/
"""


if __name__ == "__main__":
    # Ejemplo de uso
    generator = HeaderGenerator()
    
    # Generar configuración aleatoria
    config = generator.generar_configuracion_aleatoria()
    print("Configuración generada:")
    print(f"  Header Style: {config['header_style']}")
    print(f"  Nav Style: {config['nav_style']}")
    print(f"  Sticky: {config['sticky']}")
    print(f"  Elementos Extra: {', '.join(config['elementos_extra']) if config['elementos_extra'] else 'Ninguno'}")
    
    # Generar header
    categorias = ["Inicio", "Política", "Tecnología", "Deportes", "Entretenimiento"]
    header_html = generator.generar_header(
        site_name="El Diario Digital",
        tagline="Tu fuente de noticias confiable",
        categorias=categorias,
        header_style=config['header_style'],
        nav_style=config['nav_style'],
        elementos_extra=config['elementos_extra'],
        sticky=config['sticky']
    )
    
    print("\nHeader HTML generado:")
    print(header_html)
