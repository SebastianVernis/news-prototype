#!/usr/bin/env python3
"""
Generador de Layouts CSS Independientes
Genera estilos de layout estructurales que pueden combinarse con cualquier paleta y fuente
"""

import random
from typing import Dict, List


class LayoutCSSGenerator:
    """Genera estilos CSS de layout independientes"""
    
    # Definiciones de layouts estructurales (profesionales primero)
    LAYOUTS = [
        # 1. Radio M Professional (Basado en análisis real)
        {
            "nombre": "radio_m_professional",
            "descripcion": "Estilo profesional Radio M",
            "container_width": "1070px",
            "grid_template": "2fr 300px",
            "gap": "20px",
            "card_style": "professional",
            "sidebar_position": "right",
            "header_height": "65px",
            "featured_layout": "hero_split",
            "news_per_row": 3
        },
        # 2. Milenio Style
        {
            "nombre": "milenio_style",
            "descripcion": "Estilo Milenio profesional",
            "container_width": "1070px",
            "grid_template": "repeat(3, 1fr)",
            "gap": "20px",
            "card_style": "professional",
            "sidebar_position": "none",
            "header_height": "65px",
            "featured_layout": "grid_featured",
            "news_per_row": 3
        },
        # 3. Classic Grid
        {
            "nombre": "classic_grid",
            "descripcion": "Grid clásico 2 columnas con sidebar",
            "container_width": "1200px",
            "grid_template": "2fr 1fr",
            "gap": "30px",
            "card_style": "professional",
            "sidebar_position": "right",
            "header_height": "80px",
            "featured_layout": "split_60_40",
            "news_per_row": 2
        },
        # 4. Magazine Style
        {
            "nombre": "magazine_style",
            "descripcion": "Estilo revista con grid masonry",
            "container_width": "1400px",
            "grid_template": "1fr 1fr 1fr",
            "gap": "25px",
            "card_style": "professional",
            "sidebar_position": "none",
            "header_height": "100px",
            "featured_layout": "hero_full",
            "news_per_row": 3
        },
        # 3. Minimal Clean
        {
            "nombre": "minimal_clean",
            "descripcion": "Minimalista con mucho espacio",
            "container_width": "1000px",
            "grid_template": "1fr",
            "gap": "50px",
            "card_style": "borderless",
            "sidebar_position": "none",
            "header_height": "60px",
            "featured_layout": "minimal_hero",
            "news_per_row": 1
        },
        # 4. Compact Dense
        {
            "nombre": "compact_dense",
            "descripcion": "Compacto y denso de información",
            "container_width": "1600px",
            "grid_template": "repeat(4, 1fr)",
            "gap": "15px",
            "card_style": "compact",
            "sidebar_position": "right",
            "header_height": "50px",
            "featured_layout": "grid_featured",
            "news_per_row": 4
        },
        # 5. Wide Screen
        {
            "nombre": "wide_screen",
            "descripcion": "Pantalla ancha moderna",
            "container_width": "1800px",
            "grid_template": "repeat(3, 1fr)",
            "gap": "40px",
            "card_style": "elevated",
            "sidebar_position": "left",
            "header_height": "90px",
            "featured_layout": "hero_split",
            "news_per_row": 3
        },
        # 6. Mobile First
        {
            "nombre": "mobile_first",
            "descripcion": "Optimizado para móvil primero",
            "container_width": "100%",
            "grid_template": "1fr",
            "gap": "20px",
            "card_style": "card",
            "sidebar_position": "none",
            "header_height": "70px",
            "featured_layout": "stacked",
            "news_per_row": 1
        },
        # 7. Newspaper Classic
        {
            "nombre": "newspaper_classic",
            "descripcion": "Periódico clásico multi-columna",
            "container_width": "1300px",
            "grid_template": "1fr 1fr 1fr 1fr",
            "gap": "20px",
            "card_style": "bordered",
            "sidebar_position": "right",
            "header_height": "120px",
            "featured_layout": "big_small_grid",
            "news_per_row": 4
        },
        # 8. Asymmetric Modern
        {
            "nombre": "asymmetric_modern",
            "descripcion": "Asimétrico moderno",
            "container_width": "1400px",
            "grid_template": "3fr 2fr",
            "gap": "35px",
            "card_style": "shadow",
            "sidebar_position": "right",
            "header_height": "85px",
            "featured_layout": "hero_split",
            "news_per_row": 2
        },
        # 9. Card Focused
        {
            "nombre": "card_focused",
            "descripcion": "Centrado en tarjetas",
            "container_width": "1200px",
            "grid_template": "repeat(3, 1fr)",
            "gap": "30px",
            "card_style": "card_rounded",
            "sidebar_position": "none",
            "header_height": "75px",
            "featured_layout": "carousel",
            "news_per_row": 3
        },
        # 10. Split View
        {
            "nombre": "split_view",
            "descripcion": "Vista dividida 50/50",
            "container_width": "100%",
            "grid_template": "1fr 1fr",
            "gap": "0px",
            "card_style": "borderless",
            "sidebar_position": "none",
            "header_height": "80px",
            "featured_layout": "diagonal_split",
            "news_per_row": 2
        },
        # 11. Timeline Vertical
        {
            "nombre": "timeline_vertical",
            "descripcion": "Línea de tiempo vertical",
            "container_width": "900px",
            "grid_template": "1fr",
            "gap": "40px",
            "card_style": "timeline",
            "sidebar_position": "none",
            "header_height": "70px",
            "featured_layout": "stacked",
            "news_per_row": 1
        },
        # 12. Portfolio Grid
        {
            "nombre": "portfolio_grid",
            "descripcion": "Grid estilo portafolio",
            "container_width": "1500px",
            "grid_template": "repeat(auto-fit, minmax(350px, 1fr))",
            "gap": "30px",
            "card_style": "overlay",
            "sidebar_position": "none",
            "header_height": "90px",
            "featured_layout": "grid_featured",
            "news_per_row": 3
        },
        # 13. Boxed Container
        {
            "nombre": "boxed_container",
            "descripcion": "Contenedor en caja centrada",
            "container_width": "1100px",
            "grid_template": "2fr 1fr",
            "gap": "25px",
            "card_style": "boxed",
            "sidebar_position": "right",
            "header_height": "80px",
            "featured_layout": "hero_full",
            "news_per_row": 2
        },
        # 14. Full Width Bleed
        {
            "nombre": "full_width_bleed",
            "descripcion": "Ancho completo sin márgenes",
            "container_width": "100%",
            "grid_template": "repeat(4, 1fr)",
            "gap": "0px",
            "card_style": "bleed",
            "sidebar_position": "none",
            "header_height": "100px",
            "featured_layout": "full_height_hero",
            "news_per_row": 4
        },
        # 15. Sidebar Left Focus
        {
            "nombre": "sidebar_left_focus",
            "descripcion": "Sidebar izquierda destacada",
            "container_width": "1300px",
            "grid_template": "1fr 3fr",
            "gap": "30px",
            "card_style": "standard",
            "sidebar_position": "left",
            "header_height": "80px",
            "featured_layout": "hero_split",
            "news_per_row": 2
        },
        # 16. Masonry Dynamic
        {
            "nombre": "masonry_dynamic",
            "descripcion": "Masonry dinámico pinterest-style",
            "container_width": "1400px",
            "grid_template": "repeat(3, 1fr)",
            "gap": "20px",
            "card_style": "masonry",
            "sidebar_position": "none",
            "header_height": "75px",
            "featured_layout": "magazine_spread",
            "news_per_row": 3
        },
        # 17. Two Sidebar
        {
            "nombre": "two_sidebar",
            "descripcion": "Dos sidebars laterales",
            "container_width": "1600px",
            "grid_template": "1fr 3fr 1fr",
            "gap": "25px",
            "card_style": "standard",
            "sidebar_position": "both",
            "header_height": "85px",
            "featured_layout": "hero_full",
            "news_per_row": 1
        },
        # 18. Floating Cards
        {
            "nombre": "floating_cards",
            "descripcion": "Tarjetas flotantes con sombras",
            "container_width": "1300px",
            "grid_template": "repeat(3, 1fr)",
            "gap": "35px",
            "card_style": "floating",
            "sidebar_position": "none",
            "header_height": "80px",
            "featured_layout": "overlay_cards",
            "news_per_row": 3
        },
        # 19. Compact Sidebar
        {
            "nombre": "compact_sidebar",
            "descripcion": "Sidebar compacto y eficiente",
            "container_width": "1200px",
            "grid_template": "3fr 1fr",
            "gap": "20px",
            "card_style": "compact",
            "sidebar_position": "right",
            "header_height": "65px",
            "featured_layout": "featured_3col",
            "news_per_row": 3
        },
        # 20. Editorial Large
        {
            "nombre": "editorial_large",
            "descripcion": "Editorial grande y espacioso",
            "container_width": "1500px",
            "grid_template": "1fr 1fr",
            "gap": "50px",
            "card_style": "editorial",
            "sidebar_position": "none",
            "header_height": "110px",
            "featured_layout": "parallax",
            "news_per_row": 2
        }
    ]
    
    def __init__(self):
        """Inicializa el generador"""
        self.layouts_disponibles = self.LAYOUTS.copy()
    
    def obtener_layout(self, index: int = None) -> Dict[str, any]:
        """
        Obtiene un layout por índice o aleatorio
        
        Args:
            index: Índice del layout (0-19), None para aleatorio
            
        Returns:
            dict: Configuración del layout
        """
        if index is not None:
            return self.LAYOUTS[index % len(self.LAYOUTS)]
        return random.choice(self.LAYOUTS)
    
    def obtener_todos_los_layouts(self) -> List[Dict[str, any]]:
        """
        Obtiene todos los layouts disponibles
        
        Returns:
            list: Lista de todos los layouts
        """
        return self.LAYOUTS.copy()
    
    def generar_css_layout(self, layout: Dict[str, any]) -> str:
        """
        Genera CSS completo para un layout
        
        Args:
            layout: Configuración del layout
            
        Returns:
            str: CSS del layout
        """
        css = f"""/* Layout: {layout['nombre']} - {layout['descripcion']} */

/* Container - Modern CSS approach with clamp() for fluid sizing */
.container {{
    max-width: {layout['container_width']};
    margin: 0 auto;
    padding: 0 clamp(1rem, 5vw, 2rem);
    width: 100%;
}}

/* Header - Flexible height with modern flexbox */
.header {{
    min-height: {layout['header_height']};
    display: flex;
    align-items: center;
}}

/* News Grid - Using CSS Grid best practices with auto-fit */
.news-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(1rem, 3vw, {layout['gap']});
    margin: clamp(1.5rem, 5vw, 2.5rem) 0;
}}

/* Card Styles - {layout['card_style']} */
"""
        
        # Estilos específicos de tarjeta
        card_styles = self._get_card_styles(layout['card_style'])
        css += card_styles
        
        # Estilos de sidebar
        if layout['sidebar_position'] != 'none':
            css += self._get_sidebar_styles(layout['sidebar_position'])
        
        # Media queries responsivas
        css += self._get_responsive_styles(layout)
        
        return css
    
    def _get_card_styles(self, card_style: str) -> str:
        """Genera estilos específicos de tarjetas"""
        styles = {
            "professional": """.news-card {
    background: var(--card-bg, #fff);
    border-radius: var(--radius-box, 6px);
    overflow: hidden;
    box-shadow: var(--shadow-sm, 0 1px 3px rgba(0,0,0,0.1));
    transition: var(--transition-base, all 250ms ease-in-out);
    height: 100%;
    display: flex;
    flex-direction: column;
}

.news-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md, 0 4px 6px rgba(0,0,0,0.1));
}

.card-image-wrapper {
    position: relative;
    overflow: hidden;
}

.card-image {
    width: 100%;
    height: 240px;
    object-fit: cover;
    transition: transform var(--transition-slow, 350ms ease-in-out);
}

.news-card:hover .card-image {
    transform: scale(1.05);
}

.category-badge {
    position: absolute;
    top: var(--gap-sm, 10px);
    left: var(--gap-sm, 10px);
    background: var(--color-primary, #B10B1F);
    color: white;
    padding: var(--badge-padding-y, 5px) var(--badge-padding-x, 12px);
    border-radius: var(--radius-button, 10px);
    font-size: var(--badge-font-size, 12px);
    font-weight: var(--badge-font-weight, 700);
    text-transform: uppercase;
    letter-spacing: var(--letter-spacing-wide, 0.05em);
    z-index: 2;
}

.card-content {
    padding: var(--padding-md, 15px) var(--padding-lg, 25px);
    flex: 1;
    display: flex;
    flex-direction: column;
}

.card-title {
    margin: 0 0 var(--gap-sm, 10px) 0;
    font-family: var(--font-heading, 'Bebas Neue', sans-serif);
    font-size: var(--font-size-xl, 22px);
    line-height: var(--line-height-tight, 1.2);
    font-weight: var(--heading-weight, 700);
}

.card-link {
    color: var(--text-color, #202124);
    text-decoration: none;
    transition: color var(--transition-fast, 150ms ease-in-out);
}

.card-link:hover {
    color: var(--color-primary, #B10B1F);
}

.card-excerpt {
    margin: 0 0 var(--gap-md, 20px) 0;
    font-family: var(--font-body, 'Poppins', sans-serif);
    font-size: var(--font-size-base, 14px);
    line-height: var(--line-height-relaxed, 1.7);
    color: var(--color-text, #202124);
    flex: 1;
}

.card-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--gap-sm, 10px);
    padding-top: var(--gap-sm, 10px);
    border-top: 1px solid var(--color-border, #EFEFEF);
    font-size: var(--font-size-sm, 12px);
    color: var(--color-text-light, #999);
    font-family: var(--font-body, 'Poppins', sans-serif);
}

.meta-author,
.meta-date {
    font-weight: var(--font-weight-medium, 500);
}
""",
            "standard": """.news-card {
    background: var(--card-bg);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s;
}
.news-card:hover {
    transform: translateY(-5px);
}
""",
            "elevated": """.news-card {
    background: var(--card-bg);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transition: all 0.3s;
}
.news-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
}
""",
            "borderless": """.news-card {
    background: transparent;
    border: none;
    overflow: visible;
}
.card-content {
    padding: 20px 0;
    border-bottom: 1px solid rgba(0,0,0,0.1);
}
""",
            "compact": """.news-card {
    background: var(--card-bg);
    border-radius: 4px;
    overflow: hidden;
    font-size: 0.9em;
}
.card-content {
    padding: 15px;
}
""",
            "card": """.news-card {
    background: var(--card-bg);
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
""",
            "bordered": """.news-card {
    background: var(--card-bg);
    border: 2px solid var(--primary-color);
    border-radius: 5px;
    overflow: hidden;
}
""",
            "shadow": """.news-card {
    background: var(--card-bg);
    border-radius: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.12);
    overflow: hidden;
}
""",
            "card_rounded": """.news-card {
    background: var(--card-bg);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
}
""",
            "timeline": """.news-card {
    position: relative;
    padding-left: 40px;
    border-left: 3px solid var(--primary-color);
}
.news-card::before {
    content: '';
    position: absolute;
    left: -8px;
    top: 0;
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: var(--primary-color);
}
""",
            "overlay": """.news-card {
    position: relative;
    overflow: hidden;
    border-radius: 10px;
}
.card-content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 20px;
    background: linear-gradient(transparent, rgba(0,0,0,0.8));
    color: white;
}
""",
            "boxed": """.news-card {
    background: var(--card-bg);
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 6px;
    padding: 20px;
}
""",
            "bleed": """.news-card {
    background: var(--card-bg);
    border-radius: 0;
    border-right: 1px solid rgba(0,0,0,0.05);
}
""",
            "masonry": """.news-card {
    background: var(--card-bg);
    border-radius: 8px;
    overflow: hidden;
    break-inside: avoid;
    margin-bottom: 20px;
}
""",
            "floating": """.news-card {
    background: var(--card-bg);
    border-radius: 12px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    transition: all 0.4s;
}
.news-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 50px rgba(0,0,0,0.15);
}
""",
            "editorial": """.news-card {
    background: var(--card-bg);
    border-radius: 0;
    padding: 40px;
}
.card-title {
    font-size: 2em;
    line-height: 1.2;
}
"""
        }
        
        return styles.get(card_style, styles["standard"])
    
    def _get_sidebar_styles(self, position: str) -> str:
        """Genera estilos de sidebar"""
        if position == "right":
            return """\n/* Sidebar Right */
.sidebar {
    position: sticky;
    top: 20px;
    height: fit-content;
}
"""
        elif position == "left":
            return """\n/* Sidebar Left */
.sidebar {
    position: sticky;
    top: 20px;
    height: fit-content;
    order: -1;
}
"""
        elif position == "both":
            return """\n/* Sidebars Both */
.sidebar-left, .sidebar-right {
    position: sticky;
    top: 20px;
    height: fit-content;
}
"""
        return ""
    
    def _get_responsive_styles(self, layout: Dict[str, any]) -> str:
        """Genera media queries responsivas usando mejores prácticas"""
        # Usar auto-fit para grids más inteligentes según Context7
        return f"""
/* Responsive Design - Modern CSS Grid Approach */
/* Mobile First: Base styles for small screens */
@media (max-width: 640px) {{
    .container {{
        padding: 0 15px;
    }}
    .news-grid {{
        grid-template-columns: 1fr;
        gap: 1rem;
    }}
    .header {{
        height: auto;
        min-height: 60px;
    }}
    .sidebar {{
        position: relative;
        top: 0;
    }}
}}

/* Tablet: 641px - 1024px */
@media (min-width: 641px) and (max-width: 1024px) {{
    .news-grid {{
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }}
}}

/* Desktop: 1025px - 1440px */
@media (min-width: 1025px) and (max-width: 1440px) {{
    .news-grid {{
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
    }}
}}

/* Large Desktop: 1441px+ */
@media (min-width: 1441px) {{
    .news-grid {{
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 2.5rem;
    }}
}}
"""
    
    def generar_archivo_layout(self, layout: Dict[str, any], output_path: str):
        """
        Genera un archivo CSS con un layout específico
        
        Args:
            layout: Configuración del layout
            output_path: Ruta del archivo de salida
        """
        css = self.generar_css_layout(layout)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(css)
    
    def generar_todos_los_layouts_css(self, output_dir: str):
        """
        Genera archivos CSS para todos los layouts
        
        Args:
            output_dir: Directorio de salida
        """
        from pathlib import Path
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for i, layout in enumerate(self.LAYOUTS, 1):
            filename = f"layout_{i:02d}_{layout['nombre']}.css"
            output_path = f"{output_dir}/{filename}"
            self.generar_archivo_layout(layout, output_path)
            print(f"✅ Generado layout {i}: {layout['nombre']}")
    
    def obtener_info_layouts(self) -> str:
        """
        Genera información legible de todos los layouts
        
        Returns:
            str: Descripción de todos los layouts
        """
        info = "📐 Layouts Estructurales Disponibles\n"
        info += "=" * 70 + "\n\n"
        
        for i, layout in enumerate(self.LAYOUTS, 1):
            info += f"{i:2d}. {layout['nombre']:25s} - {layout['descripcion']}\n"
            info += f"    Grid: {layout['grid_template']:30s}  Sidebar: {layout['sidebar_position']}\n"
        
        return info


def main():
    """Función de prueba"""
    print("📐 Generador de Layouts CSS")
    print("=" * 70)
    
    generator = LayoutCSSGenerator()
    
    # Mostrar información de layouts
    print(generator.obtener_info_layouts())
    
    # Ejemplo de generación de CSS
    print("\n📝 Ejemplo de CSS generado para un layout:\n")
    layout = generator.obtener_layout(0)
    print(generator.generar_css_layout(layout)[:500] + "...\n")
    
    # Generar todos los layouts
    output_dir = "../templates/css/layouts"
    print(f"\n💾 Generando archivos CSS en {output_dir}...\n")
    generator.generar_todos_los_layouts_css(output_dir)
    
    print(f"\n✅ Se generaron {len(generator.LAYOUTS)} archivos de layouts")
    print(f"📂 Ubicación: {output_dir}/")


if __name__ == "__main__":
    main()
