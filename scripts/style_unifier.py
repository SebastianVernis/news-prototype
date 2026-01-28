#!/usr/bin/env python3
"""
Unificador de Estilos CSS
Crea un archivo style.css base que puede ser usado por todas las páginas
del sitio para mantener consistencia visual.
"""

from pathlib import Path
from typing import Dict


class StyleUnifier:
    """Genera un archivo CSS base unificado para todo el sitio"""
    
    def __init__(self, primary_color: str = '#667eea', secondary_color: str = '#764ba2'):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
    
    def generate_base_css(self) -> str:
        """Genera el CSS base unificado"""
        
        css = f'''/* ========================================
   ESTILOS BASE UNIFICADOS
   Aplicables a: index, legal, artículos, categorías
   ======================================== */

/* Reset y base */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: #2c3e50;
    background: #f5f7fa;
}}

/* Header común */
.header {{
    background: linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%);
    color: white;
    padding: 2rem 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

.header-content {{
    max-width: 1200px;
    margin: 0 auto;
}}

.header .logo {{
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}}

.header .logo a {{
    color: white;
    text-decoration: none;
}}

.header .nav {{
    margin-top: 1rem;
}}

.header .nav-link {{
    color: white;
    text-decoration: none;
    margin-right: 1.5rem;
    opacity: 0.9;
    transition: opacity 0.3s;
}}

.header .nav-link:hover {{
    opacity: 1;
    text-decoration: underline;
}}

/* Contenedor principal */
.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}}

/* Páginas legales */
.legal-page {{
    padding: 3rem 1rem;
}}

.legal-content {{
    background: white;
    padding: 3rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    max-width: 900px;
    margin: 0 auto;
}}

.legal-content h1 {{
    color: {self.primary_color};
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.legal-content h2 {{
    color: #2c3e50;
    font-size: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}}

.legal-content h3 {{
    color: #34495e;
    font-size: 1.2rem;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}}

.legal-content p {{
    margin-bottom: 1rem;
    color: #555;
}}

.legal-content ul {{
    margin-bottom: 1rem;
    padding-left: 2rem;
}}

.legal-content li {{
    margin-bottom: 0.5rem;
}}

.last-updated {{
    color: #6c757d;
    font-size: 0.9rem;
    margin-bottom: 2rem;
}}

/* Footer */
.footer {{
    background: #2c3e50;
    color: white;
    padding: 2rem 1rem;
    margin-top: 3rem;
    text-align: center;
}}

.footer a {{
    color: white;
    text-decoration: none;
}}

.footer a:hover {{
    text-decoration: underline;
}}

/* Grid de artículos */
.articles-grid {{
    max-width: 1200px;
    margin: 0 auto 3rem;
    padding: 0 1rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 2rem;
}}

/* Cards de artículos */
.article-card {{
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-decoration: none;
    color: inherit;
    display: block;
}}

.article-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}}

.article-image {{
    width: 100%;
    height: 200px;
    object-fit: cover;
    background: linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%);
}}

.article-content {{
    padding: 1.5rem;
}}

.article-category {{
    display: inline-block;
    background: {self.primary_color}20;
    color: {self.primary_color};
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.75rem;
}}

.article-title {{
    font-size: 1.25rem;
    font-weight: bold;
    margin-bottom: 0.75rem;
    color: #2c3e50;
    line-height: 1.4;
}}

.article-description {{
    color: #6c757d;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1rem;
}}

.article-meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
    color: #6c757d;
}}

/* Header de categoría */
.category-header {{
    background: white;
    padding: 2rem 1rem;
    margin: 2rem auto;
    max-width: 1200px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}}

.category-title {{
    font-size: 2.5rem;
    color: {self.primary_color};
    margin-bottom: 0.5rem;
}}

.category-description {{
    color: #6c757d;
    font-size: 1.1rem;
}}

.article-count {{
    display: inline-block;
    background: {self.primary_color};
    color: white;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    margin-top: 1rem;
}}

/* Breadcrumb */
.breadcrumb {{
    font-size: 0.9rem;
    opacity: 0.9;
}}

.breadcrumb a {{
    color: white;
    text-decoration: none;
}}

.breadcrumb a:hover {{
    text-decoration: underline;
}}

/* Grid de categorías */
.categories-grid {{
    max-width: 1200px;
    margin: 3rem auto;
    padding: 0 1rem;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
}}

.category-card {{
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
    border-left: 4px solid {self.primary_color};
}}

.category-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}}

.category-name {{
    font-size: 1.5rem;
    font-weight: bold;
    color: {self.primary_color};
    margin-bottom: 0.5rem;
}}

.category-desc {{
    color: #6c757d;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}}

.category-count {{
    display: inline-block;
    background: {self.primary_color}20;
    color: {self.primary_color};
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
}}

/* Responsive */
@media (max-width: 768px) {{
    .articles-grid {{
        grid-template-columns: 1fr;
    }}
    
    .categories-grid {{
        grid-template-columns: 1fr;
    }}
    
    .legal-content {{
        padding: 2rem 1rem;
    }}
    
    .legal-content h1 {{
        font-size: 1.8rem;
    }}
    
    .category-title {{
        font-size: 1.8rem;
    }}
}}
'''
        return css
    
    def save_base_css(self, output_path: str = 'style.css') -> str:
        """
        Guarda el CSS base en un archivo.
        
        Args:
            output_path: Ruta del archivo de salida
            
        Returns:
            Ruta del archivo generado
        """
        css = self.generate_base_css()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(css)
        
        print(f"✅ CSS base unificado guardado en: {output_path}")
        return output_path


def main():
    """Demo del unificador de estilos"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          🎨 UNIFICADOR DE ESTILOS CSS                               ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    unifier = StyleUnifier(
        primary_color='#667eea',
        secondary_color='#764ba2'
    )
    
    output_file = unifier.save_base_css('style.css')
    
    print(f"\n📄 Archivo generado: {output_file}")
    print("\n💡 Este archivo debe ser copiado a cada directorio de sitio generado")
    print("   y las páginas HTML deben enlazarlo con: <link rel='stylesheet' href='style.css'>")


if __name__ == '__main__':
    main()