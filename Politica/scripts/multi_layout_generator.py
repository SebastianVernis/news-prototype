#!/usr/bin/env python3
"""
Generador de 10 Layouts Diferentes
Crea variaciones visuales ricas con componentes intercambiables
"""

from pathlib import Path
from typing import List, Dict
import random


class MultiLayoutGenerator:
    """Genera 10 layouts diferentes para sitios de noticias"""
    
    def __init__(self):
        self.layouts_config = {
            1: {
                "nombre": "Classic News",
                "header": "horizontal-left",
                "ticker": True,
                "main": "destacados-left-sidebar-right",
                "footer": "4-columns"
            },
            2: {
                "nombre": "Modern Flip",
                "header": "horizontal-center",
                "ticker": True,
                "main": "sidebar-left-destacados-right",
                "footer": "3-columns"
            },
            3: {
                "nombre": "Magazine Style",
                "header": "vertical-left",
                "ticker": False,
                "main": "carousel-destacados-top-split-bottom",
                "footer": "2-columns-wide"
            },
            4: {
                "nombre": "Grid Master",
                "header": "horizontal-center-logo",
                "ticker": True,
                "main": "destacados-3col-sidebar-bottom",
                "footer": "minimal"
            },
            5: {
                "nombre": "Premium Portal",
                "header": "horizontal-dropdown",
                "ticker": False,
                "main": "destacados-full-miniatures-grid",
                "footer": "newsletter-focus"
            },
            6: {
                "nombre": "Minimalist",
                "header": "minimal-sticky",
                "ticker": False,
                "main": "carousel-large-compact-list",
                "footer": "simple"
            },
            7: {
                "nombre": "Masonry News",
                "header": "horizontal-search",
                "ticker": True,
                "main": "destacados-masonry-sidebar-sticky",
                "footer": "4-columns"
            },
            8: {
                "nombre": "Hero Focus",
                "header": "magazine-style",
                "ticker": False,
                "main": "hero-destacado-grid-2col",
                "footer": "split"
            },
            9: {
                "nombre": "Balanced 3-Col",
                "header": "news-style-top",
                "ticker": True,
                "main": "carousel-3col-balanced",
                "footer": "3-columns"
            },
            10: {
                "nombre": "Timeline Portal",
                "header": "boxed-brand",
                "ticker": False,
                "main": "destacados-cards-timeline-sidebar",
                "footer": "magazine"
            }
        }
    
    def generar_layout(
        self,
        layout_number: int,
        site_metadata: Dict,
        featured_articles: List[Dict],
        all_articles: List[Dict],
        categorias: List[Dict]
    ) -> str:
        """
        Genera un layout específico
        
        Args:
            layout_number: Número de layout (1-10)
            site_metadata: Metadata del sitio
            featured_articles: Artículos destacados
            all_articles: Todos los artículos
            categorias: Lista de categorías
            
        Returns:
            HTML completo
        """
        config = self.layouts_config.get(layout_number, self.layouts_config[1])
        
        primary = site_metadata.get('color_primario', '#667eea')
        secondary = site_metadata.get('color_secundario', '#764ba2')
        
        # Generar componentes según configuración
        header = self._generar_header_variante(config['header'], site_metadata, categorias, primary, secondary)
        ticker = self._generar_ticker_variante(all_articles, primary) if config['ticker'] else ''
        main_content = self._generar_main_variante(config['main'], featured_articles, all_articles, primary, secondary)
        footer = self._generar_footer_variante(config['footer'], site_metadata, categorias, primary, secondary)
        
        # Ensamblar
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_metadata['nombre']} - Layout {layout_number}: {config['nombre']}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', -apple-system, sans-serif; line-height: 1.6; color: #2c3e50; }}
        a {{ text-decoration: none; color: inherit; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <!-- Layout {layout_number}: {config['nombre']} -->
    {header}
    {ticker}
    {main_content}
    {footer}
</body>
</html>'''
        
        return html
    
    def _generar_header_variante(self, tipo: str, site_metadata: Dict, categorias: List[Dict], primary: str, secondary: str) -> str:
        """Genera diferentes variantes de header"""
        
        site_name = site_metadata['nombre']
        
        if tipo == "horizontal-left":
            return f'''<header style="background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000;">
    <div style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, {primary}, {secondary}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{site_name}</div>
    <nav style="display: flex; gap: 1.5rem;">
        <a href="index.html" style="padding: 0.5rem 1rem; font-weight: 600; color: #2c3e50;">Inicio</a>
        <a href="categorias.html" style="padding: 0.5rem 1rem; font-weight: 600; color: #2c3e50;">Categorías</a>
        <a href="feed.xml" style="padding: 0.5rem 1rem; font-weight: 600; color: {primary};">RSS</a>
    </nav>
</header>'''
        
        elif tipo == "horizontal-center":
            return f'''<header style="background: linear-gradient(135deg, {primary}, {secondary}); color: white; padding: 2rem; text-align: center;">
    <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">{site_name}</h1>
    <nav style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
        <a href="index.html" style="color: white; font-weight: 600;">Inicio</a>
        <a href="categorias.html" style="color: white; font-weight: 600;">Categorías</a>
        <a href="feed.xml" style="color: white; font-weight: 600;">RSS</a>
    </nav>
</header>'''
        
        elif tipo == "vertical-left":
            return f'''<header style="position: fixed; left: 0; top: 0; width: 250px; height: 100vh; background: {primary}; color: white; padding: 2rem 1rem; overflow-y: auto; z-index: 1000;">
    <h2 style="font-size: 1.5rem; margin-bottom: 2rem; text-align: center;">{site_name}</h2>
    <nav style="display: flex; flex-direction: column; gap: 1rem;">
        <a href="index.html" style="color: white; padding: 0.75rem; background: rgba(255,255,255,0.1); border-radius: 6px;">🏠 Inicio</a>
        <a href="categorias.html" style="color: white; padding: 0.75rem; background: rgba(255,255,255,0.1); border-radius: 6px;">📑 Categorías</a>
        <div style="border-top: 1px solid rgba(255,255,255,0.2); margin: 1rem 0;"></div>
        {chr(10).join([f'<a href="categoria/{cat.get("id", "")}.html" style="color: white; padding: 0.5rem; font-size: 0.9rem;">{cat.get("nombre", "")}</a>' for cat in categorias[:6]])}
    </nav>
</header>
<div style="margin-left: 250px;"><!-- Content wrapper for vertical header --></div>'''
        
        else:  # default
            return f'''<header style="background: white; padding: 1.5rem 2rem; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <div style="max-width: 1400px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center;">
        <h1 style="font-size: 2rem; color: {primary};">{site_name}</h1>
        <nav style="display: flex; gap: 1.5rem;">
            <a href="index.html" style="color: #2c3e50; font-weight: 600;">Inicio</a>
            <a href="categorias.html" style="color: #2c3e50; font-weight: 600;">Categorías</a>
        </nav>
    </div>
</header>'''
    
    def _generar_ticker_variante(self, articles: List[Dict], primary: str) -> str:
        """Genera ticker de noticias"""
        items = []
        for a in articles[-8:]:
            items.append(f'<span style="margin: 0 3rem;">🔴 {a.get("title", "")[:80]}</span>')
        
        return f'''<div style="background: {primary}; color: white; padding: 0.75rem 2rem; overflow: hidden;">
    <div style="display: flex; animation: scroll 40s linear infinite; white-space: nowrap;">
        {chr(10).join(items * 2)}
    </div>
</div>
<style>
@keyframes scroll {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-50%); }} }}
</style>'''
    
    def _generar_main_variante(self, tipo: str, featured: List[Dict], all_articles: List[Dict], primary: str, secondary: str) -> str:
        """Genera diferentes layouts principales"""
        
        if tipo == "destacados-left-sidebar-right":
            # Layout 1: Destacados izquierda, sidebar derecha
            featured_html = self._crear_cards_destacados(featured[:3], primary, "large")
            sidebar_html = self._crear_miniaturas(all_articles[3:11], primary, "compact")
            
            return f'''<main style="max-width: 1400px; margin: 2rem auto; padding: 0 2rem; display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
    <div>{featured_html}</div>
    <aside>{sidebar_html}</aside>
</main>'''
        
        elif tipo == "sidebar-left-destacados-right":
            # Layout 2: Invertido
            featured_html = self._crear_cards_destacados(featured[:3], primary, "large")
            sidebar_html = self._crear_miniaturas(all_articles[3:11], primary, "compact")
            
            return f'''<main style="max-width: 1400px; margin: 2rem auto; padding: 0 2rem; display: grid; grid-template-columns: 1fr 2fr; gap: 2rem;">
    <aside>{sidebar_html}</aside>
    <div>{featured_html}</div>
</main>'''
        
        elif tipo == "carousel-destacados-top-split-bottom":
            # Layout 3: Carrusel destacados arriba, split abajo
            carousel_html = self._crear_carrusel_destacados(featured[:5], primary)
            titulares_html = self._crear_lista_titulares(all_articles[5:13], primary)
            miniaturas_html = self._crear_miniaturas(all_articles[13:21], primary, "grid")
            
            return f'''<main style="max-width: 1400px; margin: 2rem auto; padding: 0 2rem;">
    {carousel_html}
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem;">
        <div>{titulares_html}</div>
        <div>{miniaturas_html}</div>
    </div>
</main>'''
        
        elif tipo == "destacados-3col-sidebar-bottom":
            # Layout 4: Grid 3 columnas + sidebar abajo
            featured_html = self._crear_cards_destacados(featured[:6], primary, "medium-3col")
            sidebar_html = self._crear_miniaturas(all_articles[6:14], primary, "horizontal-scroll")
            
            return f'''<main style="max-width: 1400px; margin: 2rem auto; padding: 0 2rem;">
    {featured_html}
    <div style="margin-top: 2rem;">{sidebar_html}</div>
</main>'''
        
        elif tipo == "destacados-full-miniatures-grid":
            # Layout 5: Destacados full width + miniaturas en grid
            featured_html = self._crear_cards_destacados(featured[:4], primary, "full-width")
            miniaturas_html = self._crear_miniaturas(all_articles[4:16], primary, "grid-4col")
            
            return f'''<main style="max-width: 1400px; margin: 2rem auto; padding: 0 2rem;">
    {featured_html}
    <div style="margin-top: 3rem;">{miniaturas_html}</div>
</main>'''
        
        else:  # Default
            return self._generar_main_variante("destacados-left-sidebar-right", featured, all_articles, primary, secondary)
    
    def _crear_cards_destacados(self, articles: List[Dict], primary: str, style: str) -> str:
        """Crea cards de destacados según estilo"""
        
        if not articles:
            return "<p>No hay artículos destacados</p>"
        
        cards = []
        for idx, article in enumerate(articles, 1):
            article_idx = article.get('_display_index', idx)
            image = article.get('local_image_path', 'https://via.placeholder.com/800x500')
            
            if style == "large":
                cards.append(f'''
<article style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin-bottom: 2rem; border: 2px solid {primary};">
    <img src="{image}" style="width: 100%; height: 400px; object-fit: cover;">
    <div style="padding: 2rem;">
        <span style="background: {primary}20; color: {primary}; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">⭐ DESTACADO</span>
        <h2 style="font-size: 2rem; margin: 1rem 0; line-height: 1.3;"><a href="article_{article_idx}.html">{article.get('title', '')}</a></h2>
        <p style="color: #6c757d; font-size: 1.05rem; line-height: 1.7;">{article.get('description', '')[:200]}...</p>
    </div>
</article>''')
            
            elif style == "medium-3col":
                cards.append(f'''
<article style="background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 15px rgba(0,0,0,0.08);">
    <img src="{image}" style="width: 100%; height: 200px; object-fit: cover;">
    <div style="padding: 1.5rem;">
        <h3 style="font-size: 1.25rem; margin-bottom: 0.75rem;"><a href="article_{article_idx}.html">{article.get('title', '')[:80]}</a></h3>
    </div>
</article>''')
            
            else:  # full-width
                cards.append(f'''
<article style="background: white; border-radius: 10px; padding: 2rem; box-shadow: 0 3px 15px rgba(0,0,0,0.08); margin-bottom: 1.5rem;">
    <div style="display: grid; grid-template-columns: 300px 1fr; gap: 2rem;">
        <img src="{image}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px;">
        <div>
            <span style="color: {primary}; font-weight: 700; text-transform: uppercase; font-size: 0.85rem;">⭐ Destacado</span>
            <h2 style="font-size: 1.75rem; margin: 0.5rem 0;"><a href="article_{article_idx}.html">{article.get('title', '')}</a></h2>
            <p style="color: #6c757d;">{article.get('description', '')[:150]}...</p>
        </div>
    </div>
</article>''')
        
        if style == "medium-3col":
            return f'<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">{chr(10).join(cards)}</div>'
        else:
            return chr(10).join(cards)
    
    def _crear_miniaturas(self, articles: List[Dict], primary: str, style: str) -> str:
        """Crea miniaturas según estilo"""
        
        if not articles:
            return ""
        
        items = []
        for idx, article in enumerate(articles, 1):
            article_idx = article.get('_display_index', idx + 10)
            image = article.get('local_image_path', 'https://via.placeholder.com/150x100')
            
            items.append(f'''
<article style="background: white; border-radius: 6px; padding: 0.75rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); display: flex; gap: 1rem; margin-bottom: 1rem;">
    <img src="{image}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px; flex-shrink: 0;">
    <div>
        <h4 style="font-size: 0.9rem; line-height: 1.4; margin-bottom: 0.25rem;"><a href="article_{article_idx}.html">{article.get('title', '')[:70]}</a></h4>
        <span style="font-size: 0.75rem; color: #95a5a6;">{article.get('category_name', 'Noticias')}</span>
    </div>
</article>''')
        
        if style == "grid-4col":
            return f'<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">{chr(10).join(items)}</div>'
        elif style == "horizontal-scroll":
            return f'<div style="display: flex; gap: 1rem; overflow-x: auto; padding-bottom: 1rem;">{chr(10).join(items)}</div>'
        else:
            return f'<div><h3 style="margin-bottom: 1rem; color: #2c3e50;">📰 Más Noticias</h3>{chr(10).join(items)}</div>'
    
    def _crear_carrusel_destacados(self, articles: List[Dict], primary: str) -> str:
        """Crea carrusel de destacados grande"""
        
        if not articles:
            return ""
        
        slides = []
        for idx, article in enumerate(articles):
            article_idx = article.get('_display_index', idx + 1)
            image = article.get('local_image_path', 'https://via.placeholder.com/1200x600')
            
            slides.append(f'''
<div class="carousel-slide" style="min-width: 100%; position: relative;">
    <img src="{image}" style="width: 100%; height: 500px; object-fit: cover; border-radius: 12px;">
    <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.8)); padding: 3rem 2rem; color: white;">
        <h2 style="font-size: 2.5rem; margin-bottom: 0.5rem;"><a href="article_{article_idx}.html" style="color: white;">{article.get('title', '')}</a></h2>
        <p style="font-size: 1.1rem; opacity: 0.9;">{article.get('description', '')[:150]}...</p>
    </div>
</div>''')
        
        return f'''
<div style="overflow: hidden; border-radius: 12px; margin-bottom: 2rem;">
    <div style="display: flex; transition: transform 0.5s ease;" id="carouselTrack">
        {chr(10).join(slides)}
    </div>
</div>
<script>
let currentSlide = 0;
const totalSlides = {len(slides)};
setInterval(() => {{
    currentSlide = (currentSlide + 1) % totalSlides;
    document.getElementById('carouselTrack').style.transform = `translateX(-${{currentSlide * 100}}%)`;
}}, 5000);
</script>'''
    
    def _crear_lista_titulares(self, articles: List[Dict], primary: str) -> str:
        """Crea lista de titulares"""
        
        items = []
        for idx, article in enumerate(articles, 1):
            article_idx = article.get('_display_index', idx + 20)
            items.append(f'''
<div style="padding: 1rem; border-bottom: 1px solid #ecf0f1;">
    <a href="article_{article_idx}.html" style="font-weight: 600; color: #2c3e50; display: block; margin-bottom: 0.25rem;">{article.get('title', '')[:100]}</a>
    <span style="font-size: 0.85rem; color: #95a5a6;">{article.get('category_name', 'Noticias')}</span>
</div>''')
        
        return f'<div style="background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.06);"><h3 style="padding: 1.5rem 1rem; background: {primary}; color: white; border-radius: 8px 8px 0 0;">📋 Últimas Noticias</h3>{chr(10).join(items)}</div>'
    
    def _generar_footer_variante(self, tipo: str, site_metadata: Dict, categorias: List[Dict], primary: str, secondary: str) -> str:
        """Genera diferentes variantes de footer"""
        
        site_name = site_metadata['nombre']
        
        if tipo == "4-columns":
            return f'''<footer style="background: #2c3e50; color: white; padding: 3rem 2rem; margin-top: 4rem;">
    <div style="max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem;">
        <div>
            <h3 style="margin-bottom: 1rem;">{site_name}</h3>
            <p style="color: #bdc3c7; font-size: 0.9rem;">Portal de noticias políticas</p>
            <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                <a href="#" style="width: 40px; height: 40px; background: {primary}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;">F</a>
                <a href="#" style="width: 40px; height: 40px; background: {primary}; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white;">T</a>
            </div>
        </div>
        <div>
            <h4 style="margin-bottom: 1rem;">Categorías</h4>
            {chr(10).join([f'<a href="categoria/{cat.get("id", "")}.html" style="display: block; color: #bdc3c7; margin-bottom: 0.5rem;">{cat.get("nombre", "")}</a>' for cat in categorias[:5]])}
        </div>
        <div>
            <h4 style="margin-bottom: 1rem;">Información</h4>
            <a href="about.html" style="display: block; color: #bdc3c7; margin-bottom: 0.5rem;">Acerca de</a>
            <a href="contact.html" style="display: block; color: #bdc3c7; margin-bottom: 0.5rem;">Contacto</a>
        </div>
        <div>
            <h4 style="margin-bottom: 1rem;">RSS</h4>
            <a href="feed.xml" style="display: block; color: {primary}; font-weight: 600;">📡 Suscribirse</a>
        </div>
    </div>
    <div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1); color: #bdc3c7;">&copy; 2026 {site_name}</div>
</footer>'''
        
        else:  # minimal
            return f'''<footer style="background: #34495e; color: white; padding: 2rem; text-align: center; margin-top: 4rem;">
    <p>&copy; 2026 {site_name} - <a href="feed.xml" style="color: {primary};">RSS</a></p>
</footer>'''
    
    def generar_todos_los_layouts(
        self,
        site_metadata: Dict,
        featured_articles: List[Dict],
        all_articles: List[Dict],
        categorias: List[Dict]
    ) -> Dict[int, str]:
        """
        Genera los 10 layouts
        
        Returns:
            Dict con número -> HTML
        """
        layouts = {}
        
        for layout_num in range(1, 11):
            html = self.generar_layout(
                layout_num,
                site_metadata,
                featured_articles,
                all_articles,
                categorias
            )
            layouts[layout_num] = html
        
        return layouts


def main():
    """Genera los 10 layouts y crea galería"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║        🎨 GENERADOR DE 10 LAYOUTS PROFESIONALES                     ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Datos de ejemplo
    site_metadata = {
        'nombre': 'Política México',
        'tagline': 'Noticias y Análisis',
        'color_primario': '#667eea',
        'color_secundario': '#764ba2'
    }
    
    categorias = [
        {'id': 'politica', 'nombre': 'Política'},
        {'id': 'economia', 'nombre': 'Economía'},
        {'id': 'seguridad', 'nombre': 'Seguridad'},
        {'id': 'internacional', 'nombre': 'Internacional'},
        {'id': 'analisis', 'nombre': 'Análisis'},
    ]
    
    # Artículos de ejemplo
    featured = []
    for i in range(1, 6):
        featured.append({
            'title': f'Artículo Destacado {i}: Análisis profundo de tema importante',
            'description': 'Este es un artículo con parafraseo completo de alta calidad usando Blackbox Pro. Contiene análisis profundo y múltiples párrafos bien estructurados.',
            'category_name': random.choice(['Política', 'Economía', 'Seguridad']),
            'author': 'Redacción',
            'published_at': '2026-01-20',
            '_display_index': i,
            'is_featured': True,
            'local_image_path': f'https://via.placeholder.com/800x500/667eea/ffffff?text=Destacado+{i}'
        })
    
    all_articles = featured.copy()
    for i in range(6, 26):
        all_articles.append({
            'title': f'Noticia {i}: Título del artículo placeholder',
            'description': 'Artículo con parafraseo rápido de Gemini.',
            'category_name': random.choice(['Política', 'Economía', 'Seguridad']),
            '_display_index': i,
            'is_featured': False,
            'local_image_path': f'https://via.placeholder.com/400x300/764ba2/ffffff?text=Articulo+{i}'
        })
    
    # Generar todos
    generator = MultiLayoutGenerator()
    
    print("\nGenerando 10 layouts...\n")
    
    for i in range(1, 11):
        config = generator.layouts_config[i]
        html = generator.generar_layout(i, site_metadata, featured, all_articles, categorias)
        
        filename = f'layout_{i}_{config["nombre"].lower().replace(" ", "_")}.html'
        filepath = f'layout/{filename}'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✅ Layout {i}: {config['nombre']:20} → {filepath}")
    
    # Crear galería de layouts
    galeria_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galería de 10 Layouts Profesionales</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #f5f7fa; padding: 2rem; }
        .header { text-align: center; margin-bottom: 3rem; }
        .header h1 { font-size: 2.5rem; color: #2c3e50; margin-bottom: 0.5rem; }
        .gallery { max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 2rem; }
        .layout-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); transition: transform 0.3s; }
        .layout-card:hover { transform: translateY(-5px); box-shadow: 0 8px 30px rgba(0,0,0,0.15); }
        .layout-preview { width: 100%; height: 250px; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem; font-weight: 800; }
        .layout-info { padding: 1.5rem; }
        .layout-name { font-size: 1.5rem; font-weight: 700; color: #2c3e50; margin-bottom: 0.5rem; }
        .layout-description { color: #6c757d; font-size: 0.95rem; margin-bottom: 1rem; line-height: 1.6; }
        .layout-features { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
        .feature-tag { background: #ecf0f1; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; color: #2c3e50; }
        .view-button { display: block; width: 100%; padding: 0.75rem; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; text-align: center; }
        .view-button:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 Galería de 10 Layouts Profesionales</h1>
        <p style="color: #6c757d; font-size: 1.1rem;">Explora diferentes diseños para sitios de noticias</p>
    </div>
    
    <div class="gallery">
'''
    
    for i in range(1, 11):
        config = generator.layouts_config[i]
        filename = f'layout_{i}_{config["nombre"].lower().replace(" ", "_")}.html'
        
        features = []
        if config['ticker']:
            features.append('Carrusel')
        features.append('Header ' + config['header'].split('-')[0])
        features.append('Footer ' + config['footer'].split('-')[0])
        
        galeria_html += f'''
        <div class="layout-card">
            <div class="layout-preview">{i}</div>
            <div class="layout-info">
                <h2 class="layout-name">Layout {i}: {config['nombre']}</h2>
                <p class="layout-description">{config['main']}</p>
                <div class="layout-features">
                    {chr(10).join([f'<span class="feature-tag">{f}</span>' for f in features])}
                </div>
                <a href="{filename}" target="_blank" class="view-button">Ver Layout Completo</a>
            </div>
        </div>
'''
    
    galeria_html += '''
    </div>
</body>
</html>'''
    
    with open('layout/layouts_gallery.html', 'w', encoding='utf-8') as f:
        f.write(galeria_html)
    
    print("\n" + "="*70)
    print("✅ 10 Layouts generados")
    print("="*70)
    print("\n🌐 Galería disponible en:")
    print("   http://localhost:8006/layout/layouts_gallery.html")
    print("\n💡 Desde ahí puedes ver cada layout individualmente")


if __name__ == '__main__':
    main()
