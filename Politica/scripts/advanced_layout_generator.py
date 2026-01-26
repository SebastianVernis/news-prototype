#!/usr/bin/env python3
"""
Generador de Layout Avanzado para Sitios de Noticias
- Header: Branding izquierda + Menu deslizable derecha
- Carrusel de titulares animado
- Grid destacados + Sidebar miniaturas
- Footer completo con redes sociales
"""

from typing import List, Dict


class AdvancedLayoutGenerator:
    """Genera layouts avanzados profesionales"""
    
    LAYOUTS = {
        "layout-1": "Header horizontal + Carrusel + Destacados izq + Sidebar der",
        "layout-2": "Header horizontal + Carrusel + Sidebar izq + Destacados der",
        "layout-3": "Header vertical + Carrusel destacados + Titulares izq + Miniaturas der",
        "layout-4": "Header centrado + Grid destacados 3 col + Sidebar bottom",
        "layout-5": "Header con categorías dropdown + Destacados full + Miniaturas grid",
        "layout-6": "Header minimal + Carrusel grande + Lista compacta",
        "layout-7": "Header con search + Destacados masonry + Sidebar sticky",
        "layout-8": "Header magazine + Hero destacado + Grid 2 col",
        "layout-9": "Header news-style + Carrusel + 3 columnas balanceadas",
        "layout-10": "Header boxed + Destacados cards + Timeline lateral"
    }
    
    def generar_header(
        self,
        site_name: str,
        logo_path: str,
        categorias: List[Dict],
        colores: Dict
    ) -> str:
        """
        Genera header profesional con branding y menú deslizable
        
        Args:
            site_name: Nombre del sitio
            logo_path: Path al logo
            categorias: Lista de categorías para el menú
            colores: Paleta de colores
            
        Returns:
            HTML del header
        """
        primary = colores.get('primary', '#667eea')
        secondary = colores.get('secondary', '#764ba2')
        
        # Generar items del menú
        menu_items = []
        for cat in categorias:
            cat_id = cat.get('id', '')
            cat_name = cat.get('nombre', '')
            menu_items.append(f'<a href="categoria/{cat_id}.html" class="menu-item">{cat_name}</a>')
        
        header_html = f'''
    <header class="main-header">
        <div class="header-container">
            <!-- Branding (Izquierda) -->
            <div class="branding">
                <a href="index.html" class="logo-link">
                    <img src="{logo_path}" alt="{site_name}" class="logo">
                    <span class="site-title">{site_name}</span>
                </a>
            </div>
            
            <!-- Menu Toggle (Móvil) -->
            <button class="menu-toggle" id="menuToggle" aria-label="Abrir menú">
                <span></span>
                <span></span>
                <span></span>
            </button>
            
            <!-- Navegación (Derecha) -->
            <nav class="main-nav" id="mainNav">
                <div class="nav-header">
                    <span class="nav-title">Categorías</span>
                    <button class="nav-close" id="navClose">&times;</button>
                </div>
                
                <div class="nav-content">
                    <a href="index.html" class="menu-item">🏠 Inicio</a>
                    <a href="categorias.html" class="menu-item">📑 Todas las Categorías</a>
                    
                    <div class="menu-divider"></div>
                    <span class="menu-label">Por Categoría</span>
                    
                    {chr(10).join(menu_items)}
                    
                    <div class="menu-divider"></div>
                    <a href="feed.xml" class="menu-item">📡 RSS Feed</a>
                </div>
                
                <!-- Redes Sociales en el menú -->
                <div class="nav-social">
                    <a href="#" class="social-icon" aria-label="Facebook">
                        <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                        </svg>
                    </a>
                    <a href="#" class="social-icon" aria-label="Twitter">
                        <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                        </svg>
                    </a>
                    <a href="#" class="social-icon" aria-label="WhatsApp">
                        <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                        </svg>
                    </a>
                </div>
            </nav>
            
            <!-- Overlay para menú móvil -->
            <div class="nav-overlay" id="navOverlay"></div>
        </div>
    </header>
    
    <style>
        .main-header {{
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        
        .header-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        /* Branding */
        .branding {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .logo-link {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: inherit;
        }}
        
        .logo {{
            height: 50px;
            width: auto;
        }}
        
        .site-title {{
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, {primary}, {secondary});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Menu Toggle (Móvil) */
        .menu-toggle {{
            display: none;
            flex-direction: column;
            gap: 4px;
            background: none;
            border: none;
            cursor: pointer;
            padding: 0.5rem;
        }}
        
        .menu-toggle span {{
            width: 25px;
            height: 3px;
            background: {primary};
            border-radius: 2px;
            transition: all 0.3s ease;
        }}
        
        .menu-toggle.active span:nth-child(1) {{
            transform: rotate(45deg) translateY(8px);
        }}
        
        .menu-toggle.active span:nth-child(2) {{
            opacity: 0;
        }}
        
        .menu-toggle.active span:nth-child(3) {{
            transform: rotate(-45deg) translateY(-8px);
        }}
        
        /* Navegación */
        .main-nav {{
            display: flex;
            align-items: center;
        }}
        
        .nav-header {{
            display: none;
        }}
        
        .nav-content {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}
        
        .menu-item {{
            padding: 0.75rem 1.25rem;
            text-decoration: none;
            color: #2c3e50;
            font-weight: 600;
            font-size: 0.95rem;
            border-radius: 6px;
            transition: all 0.3s ease;
            white-space: nowrap;
        }}
        
        .menu-item:hover {{
            background: {primary}15;
            color: {primary};
        }}
        
        .menu-divider {{
            width: 1px;
            height: 20px;
            background: #e0e0e0;
            margin: 0 0.5rem;
        }}
        
        .menu-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            color: #95a5a6;
            font-weight: 700;
            letter-spacing: 1px;
            padding: 0 0.5rem;
        }}
        
        .nav-social {{
            display: flex;
            gap: 0.75rem;
            padding-left: 1rem;
            border-left: 1px solid #e0e0e0;
        }}
        
        .social-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: {primary}10;
            color: {primary};
            transition: all 0.3s ease;
        }}
        
        .social-icon:hover {{
            background: {primary};
            color: white;
            transform: translateY(-2px);
        }}
        
        .nav-overlay {{
            display: none;
        }}
        
        .nav-close {{
            display: none;
        }}
        
        /* Responsive */
        @media (max-width: 1024px) {{
            .menu-toggle {{
                display: flex;
            }}
            
            .main-nav {{
                position: fixed;
                top: 0;
                right: -320px;
                width: 320px;
                height: 100vh;
                background: white;
                box-shadow: -2px 0 10px rgba(0,0,0,0.1);
                transition: right 0.3s ease;
                flex-direction: column;
                align-items: stretch;
                overflow-y: auto;
                z-index: 1001;
            }}
            
            .main-nav.active {{
                right: 0;
            }}
            
            .nav-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1.5rem;
                border-bottom: 1px solid #e0e0e0;
            }}
            
            .nav-title {{
                font-size: 1.25rem;
                font-weight: 700;
                color: {primary};
            }}
            
            .nav-close {{
                display: block;
                background: none;
                border: none;
                font-size: 2rem;
                color: #2c3e50;
                cursor: pointer;
                line-height: 1;
            }}
            
            .nav-content {{
                flex-direction: column;
                align-items: stretch;
                gap: 0;
                padding: 1rem;
            }}
            
            .menu-item {{
                padding: 1rem 1.25rem;
                border-radius: 0;
                border-bottom: 1px solid #f0f0f0;
            }}
            
            .menu-divider {{
                width: 100%;
                height: 1px;
                margin: 0.5rem 0;
            }}
            
            .menu-label {{
                padding: 1rem 1.25rem;
                display: block;
            }}
            
            .nav-social {{
                border-left: none;
                border-top: 1px solid #e0e0e0;
                padding: 1.5rem 1.25rem;
                margin-top: 1rem;
            }}
            
            .nav-overlay {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                z-index: 1000;
            }}
            
            .nav-overlay.active {{
                display: block;
            }}
        }}
    </style>
    
    <script>
        // Menu toggle functionality
        document.addEventListener('DOMContentLoaded', function() {{
            const menuToggle = document.getElementById('menuToggle');
            const navClose = document.getElementById('navClose');
            const mainNav = document.getElementById('mainNav');
            const navOverlay = document.getElementById('navOverlay');
            
            function openMenu() {{
                mainNav.classList.add('active');
                navOverlay.classList.add('active');
                menuToggle.classList.add('active');
                document.body.style.overflow = 'hidden';
            }}
            
            function closeMenu() {{
                mainNav.classList.remove('active');
                navOverlay.classList.remove('active');
                menuToggle.classList.remove('active');
                document.body.style.overflow = '';
            }}
            
            if (menuToggle) menuToggle.addEventListener('click', openMenu);
            if (navClose) navClose.addEventListener('click', closeMenu);
            if (navOverlay) navOverlay.addEventListener('click', closeMenu);
        }});
    </script>
'''
        
        return header_html
    
    def generar_carrusel_titulares(
        self,
        articles: List[Dict],
        colores: Dict
    ) -> str:
        """
        Genera carrusel animado de titulares
        
        Args:
            articles: Lista de artículos para el carrusel
            colores: Paleta de colores
            
        Returns:
            HTML del carrusel
        """
        primary = colores.get('primary', '#667eea')
        
        # Tomar últimos 10 artículos para el carrusel
        carousel_articles = articles[-10:] if len(articles) > 10 else articles
        
        slides_html = []
        for idx, article in enumerate(carousel_articles):
            article_idx = article.get('_display_index', idx + 1)
            slides_html.append(f'''
                <div class="ticker-item">
                    <span class="ticker-badge">{article.get('category_name', 'Noticias')}</span>
                    <a href="article_{article_idx}.html" class="ticker-link">
                        {article.get('title', 'Sin título')[:120]}
                    </a>
                </div>
''')
        
        carousel_html = f'''
    <div class="news-ticker">
        <div class="ticker-label">🔴 ÚLTIMAS NOTICIAS</div>
        <div class="ticker-content">
            <div class="ticker-track" id="tickerTrack">
                {chr(10).join(slides_html * 2)}
            </div>
        </div>
    </div>
    
    <style>
        .news-ticker {{
            background: {primary};
            color: white;
            padding: 0.75rem 0;
            overflow: hidden;
            position: relative;
        }}
        
        .ticker-label {{
            position: absolute;
            left: 2rem;
            top: 50%;
            transform: translateY(-50%);
            font-weight: 700;
            font-size: 0.85rem;
            background: rgba(0,0,0,0.3);
            padding: 0.5rem 1rem;
            border-radius: 4px;
            z-index: 1;
        }}
        
        .ticker-content {{
            margin-left: 200px;
            overflow: hidden;
        }}
        
        .ticker-track {{
            display: flex;
            gap: 3rem;
            animation: scroll 60s linear infinite;
            will-change: transform;
        }}
        
        .ticker-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            white-space: nowrap;
        }}
        
        .ticker-badge {{
            background: rgba(255,255,255,0.2);
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        .ticker-link {{
            color: white;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .ticker-link:hover {{
            text-decoration: underline;
        }}
        
        @keyframes scroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        
        .ticker-track:hover {{
            animation-play-state: paused;
        }}
        
        @media (max-width: 768px) {{
            .ticker-label {{
                position: static;
                transform: none;
                display: inline-block;
                margin-bottom: 0.5rem;
            }}
            
            .ticker-content {{
                margin-left: 1rem;
            }}
        }}
    </style>
'''
        
        return carousel_html
    
    def generar_grid_destacados_con_sidebar(
        self,
        featured_articles: List[Dict],
        sidebar_articles: List[Dict],
        colores: Dict
    ) -> str:
        """
        Genera grid de destacados (izquierda) + sidebar miniaturas (derecha)
        
        Args:
            featured_articles: Artículos destacados (principales)
            sidebar_articles: Artículos para sidebar (placeholders)
            colores: Paleta de colores
            
        Returns:
            HTML del layout principal
        """
        primary = colores.get('primary', '#667eea')
        secondary = colores.get('secondary', '#764ba2')
        
        # Grid de destacados (3 primeros)
        featured_html = []
        for idx, article in enumerate(featured_articles[:3], 1):
            article_idx = article.get('_display_index', idx)
            image_url = article.get('local_image_path', article.get('image_url', 'https://via.placeholder.com/800x400'))
            
            featured_html.append(f'''
                <article class="featured-article">
                    <a href="article_{article_idx}.html" class="featured-link">
                        <div class="featured-image-container">
                            <img src="{image_url}" alt="{article['title']}" class="featured-image">
                            <span class="featured-badge">⭐ Destacado</span>
                        </div>
                        <div class="featured-body">
                            <span class="featured-category">{article.get('category_name', 'Noticias')}</span>
                            <h2 class="featured-title">{article['title']}</h2>
                            <p class="featured-excerpt">{article.get('description', '')[:200]}...</p>
                            <div class="featured-meta">
                                <span>👤 {article.get('author', 'Redacción')}</span>
                                <span>📅 {article.get('published_at', '')[:10]}</span>
                                <span>📖 Lectura completa</span>
                            </div>
                        </div>
                    </a>
                </article>
''')
        
        # Sidebar miniaturas
        sidebar_html = []
        for idx, article in enumerate(sidebar_articles[:8], 1):
            article_idx = article.get('_display_index', idx + len(featured_articles))
            image_url = article.get('local_image_path', article.get('image_url', 'https://via.placeholder.com/150x100'))
            
            sidebar_html.append(f'''
                <article class="sidebar-item">
                    <a href="article_{article_idx}.html" class="sidebar-link">
                        <img src="{image_url}" alt="{article['title']}" class="sidebar-image">
                        <div class="sidebar-content">
                            <span class="sidebar-category">{article.get('category_name', 'Noticias')}</span>
                            <h4 class="sidebar-title">{article['title'][:80]}</h4>
                        </div>
                    </a>
                </article>
''')
        
        layout_html = f'''
    <div class="main-layout">
        <div class="layout-container">
            <!-- Grid Destacados (Izquierda) -->
            <main class="featured-grid">
                <h2 class="section-title">⭐ Artículos Destacados</h2>
                {chr(10).join(featured_html)}
            </main>
            
            <!-- Sidebar Miniaturas (Derecha) -->
            <aside class="sidebar">
                <h3 class="sidebar-title-header">📰 Más Noticias</h3>
                {chr(10).join(sidebar_html)}
            </aside>
        </div>
    </div>
    
    <style>
        .main-layout {{
            background: #f5f7fa;
            padding: 2rem 0;
        }}
        
        .layout-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 1fr 350px;
            gap: 2rem;
        }}
        
        /* Featured Grid */
        .featured-grid {{
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }}
        
        .section-title {{
            font-size: 2rem;
            color: #2c3e50;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid {primary};
        }}
        
        .featured-article {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .featured-article:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            border-color: {primary};
        }}
        
        .featured-link {{
            text-decoration: none;
            color: inherit;
            display: block;
        }}
        
        .featured-image-container {{
            position: relative;
            height: 400px;
            overflow: hidden;
        }}
        
        .featured-image {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .featured-article:hover .featured-image {{
            transform: scale(1.05);
        }}
        
        .featured-badge {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: linear-gradient(135deg, {primary}, {secondary});
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
        
        .featured-body {{
            padding: 2rem;
        }}
        
        .featured-category {{
            display: inline-block;
            background: {primary}20;
            color: {primary};
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 1rem;
        }}
        
        .featured-title {{
            font-size: 2rem;
            line-height: 1.3;
            margin-bottom: 1rem;
            color: #2c3e50;
        }}
        
        .featured-excerpt {{
            color: #6c757d;
            line-height: 1.7;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }}
        
        .featured-meta {{
            display: flex;
            gap: 1.5rem;
            font-size: 0.9rem;
            color: #95a5a6;
            padding-top: 1rem;
            border-top: 1px solid #ecf0f1;
            flex-wrap: wrap;
        }}
        
        /* Sidebar */
        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        .sidebar-title-header {{
            font-size: 1.5rem;
            color: #2c3e50;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid {primary};
        }}
        
        .sidebar-item {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: all 0.3s ease;
        }}
        
        .sidebar-item:hover {{
            box-shadow: 0 4px 15px rgba(0,0,0,0.12);
            transform: translateX(5px);
        }}
        
        .sidebar-link {{
            display: flex;
            gap: 1rem;
            text-decoration: none;
            color: inherit;
        }}
        
        .sidebar-image {{
            width: 100px;
            height: 80px;
            object-fit: cover;
            flex-shrink: 0;
        }}
        
        .sidebar-content {{
            padding: 0.75rem 0.75rem 0.75rem 0;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .sidebar-category {{
            display: inline-block;
            background: {primary}15;
            color: {primary};
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            align-self: flex-start;
        }}
        
        .sidebar-title {{
            font-size: 0.95rem;
            line-height: 1.4;
            color: #2c3e50;
            font-weight: 600;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        @media (max-width: 1024px) {{
            .layout-container {{
                grid-template-columns: 1fr;
            }}
            
            .sidebar {{
                order: -1;
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 1rem;
            }}
            
            .sidebar-title-header {{
                grid-column: 1 / -1;
            }}
        }}
    </style>
'''
        
        return layout_html
    
    def generar_footer_completo(
        self,
        site_name: str,
        categorias: List[Dict],
        colores: Dict
    ) -> str:
        """
        Genera footer completo con redes sociales y links
        
        Args:
            site_name: Nombre del sitio
            categorias: Lista de categorías
            colores: Paleta de colores
            
        Returns:
            HTML del footer
        """
        primary = colores.get('primary', '#667eea')
        secondary = colores.get('secondary', '#764ba2')
        
        # Columnas de categorías
        cat_links = []
        for cat in categorias[:8]:  # Máximo 8 categorías en footer
            cat_id = cat.get('id', '')
            cat_name = cat.get('nombre', '')
            cat_links.append(f'<a href="categoria/{cat_id}.html">{cat_name}</a>')
        
        footer_html = f'''
    <footer class="main-footer">
        <div class="footer-container">
            <!-- Columna 1: Sobre el sitio -->
            <div class="footer-column">
                <h3 class="footer-title">{site_name}</h3>
                <p class="footer-description">
                    Tu fuente confiable de noticias políticas de México. 
                    Información veraz, análisis profundo y cobertura completa.
                </p>
                <div class="footer-social">
                    <a href="#" class="footer-social-icon facebook" aria-label="Facebook">
                        <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                        </svg>
                    </a>
                    <a href="#" class="footer-social-icon twitter" aria-label="Twitter">
                        <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                        </svg>
                    </a>
                    <a href="#" class="footer-social-icon instagram" aria-label="Instagram">
                        <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/>
                        </svg>
                    </a>
                    <a href="#" class="footer-social-icon youtube" aria-label="YouTube">
                        <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                        </svg>
                    </a>
                </div>
            </div>
            
            <!-- Columna 2: Categorías -->
            <div class="footer-column">
                <h3 class="footer-title">Categorías</h3>
                <div class="footer-links">
                    {chr(10).join(cat_links)}
                </div>
            </div>
            
            <!-- Columna 3: Enlaces -->
            <div class="footer-column">
                <h3 class="footer-title">Información</h3>
                <div class="footer-links">
                    <a href="about.html">Acerca de</a>
                    <a href="contact.html">Contacto</a>
                    <a href="privacy.html">Privacidad</a>
                    <a href="feed.xml">RSS Feed</a>
                </div>
            </div>
            
            <!-- Columna 4: Newsletter -->
            <div class="footer-column">
                <h3 class="footer-title">Suscríbete</h3>
                <p class="footer-newsletter-text">Recibe las últimas noticias en tu correo</p>
                <form class="newsletter-form">
                    <input type="email" placeholder="tu@email.com" class="newsletter-input">
                    <button type="submit" class="newsletter-button">Suscribir</button>
                </form>
            </div>
        </div>
        
        <!-- Copyright -->
        <div class="footer-bottom">
            <div class="footer-container">
                <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
                <p class="footer-credits">Diseñado con ❤️ para informar con calidad</p>
            </div>
        </div>
    </footer>
    
    <style>
        .main-footer {{
            background: #2c3e50;
            color: white;
            padding: 3rem 0 0;
            margin-top: 4rem;
        }}
        
        .footer-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }}
        
        .footer-column {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .footer-title {{
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: white;
        }}
        
        .footer-description {{
            color: #bdc3c7;
            line-height: 1.6;
            font-size: 0.95rem;
        }}
        
        .footer-social {{
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }}
        
        .footer-social-icon {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: rgba(255,255,255,0.1);
            color: white;
            transition: all 0.3s ease;
        }}
        
        .footer-social-icon:hover {{
            background: {primary};
            transform: translateY(-3px);
        }}
        
        .footer-links {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }}
        
        .footer-links a {{
            color: #bdc3c7;
            text-decoration: none;
            transition: color 0.3s ease;
            font-size: 0.95rem;
        }}
        
        .footer-links a:hover {{
            color: white;
            padding-left: 0.5rem;
        }}
        
        .footer-newsletter-text {{
            color: #bdc3c7;
            font-size: 0.9rem;
        }}
        
        .newsletter-form {{
            display: flex;
            gap: 0.5rem;
            margin-top: 0.5rem;
        }}
        
        .newsletter-input {{
            flex: 1;
            padding: 0.75rem;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 0.9rem;
        }}
        
        .newsletter-input::placeholder {{
            color: rgba(255,255,255,0.5);
        }}
        
        .newsletter-button {{
            padding: 0.75rem 1.5rem;
            background: {primary};
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .newsletter-button:hover {{
            background: {secondary};
            transform: translateY(-2px);
        }}
        
        .footer-bottom {{
            margin-top: 3rem;
            padding: 1.5rem 0;
            border-top: 1px solid rgba(255,255,255,0.1);
            text-align: center;
        }}
        
        .footer-bottom p {{
            color: #bdc3c7;
            font-size: 0.9rem;
            margin: 0.25rem 0;
        }}
        
        .footer-credits {{
            font-size: 0.85rem !important;
            opacity: 0.7;
        }}
    </style>
'''
        
        return footer_html
    
    def generar_index_completo(
        self,
        site_metadata: Dict,
        featured_articles: List[Dict],
        all_articles: List[Dict],
        categorias: List[Dict],
        logo_path: str = 'assets/logo.svg'
    ) -> str:
        """
        Genera index.html completo con layout profesional
        
        Args:
            site_metadata: Metadata del sitio
            featured_articles: Artículos destacados (Blackbox Pro)
            all_articles: Todos los artículos
            categorias: Lista de categorías
            logo_path: Path al logo
            
        Returns:
            HTML completo del index
        """
        colores = {
            'primary': site_metadata.get('color_primario', '#667eea'),
            'secondary': site_metadata.get('color_secundario', '#764ba2')
        }
        
        # Generar componentes
        header = self.generar_header(
            site_metadata['nombre'],
            logo_path,
            categorias,
            colores
        )
        
        carousel = self.generar_carrusel_titulares(all_articles, colores)
        
        # Separar featured y sidebar
        sidebar_articles = [a for a in all_articles if not a.get('is_featured', False)]
        
        main_grid = self.generar_grid_destacados_con_sidebar(
            featured_articles,
            sidebar_articles,
            colores
        )
        
        footer = self.generar_footer_completo(
            site_metadata['nombre'],
            categorias,
            colores
        )
        
        # Ensamblar todo
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_metadata['nombre']} - {site_metadata.get('tagline', 'Noticias Políticas')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
        }}
    </style>
</head>
<body>
{header}
{carousel}
{main_grid}
{footer}
</body>
</html>'''
        
        return html


def main():
    """Demo del layout avanzado"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          🎨 GENERADOR DE LAYOUT AVANZADO                            ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Datos de ejemplo
    site_metadata = {
        'nombre': 'Política México Hoy',
        'tagline': 'Análisis profundo de la actualidad',
        'color_primario': '#667eea',
        'color_secundario': '#764ba2'
    }
    
    categorias = [
        {'id': 'política-nacional', 'nombre': 'Política Nacional'},
        {'id': 'economía', 'nombre': 'Economía'},
        {'id': 'seguridad', 'nombre': 'Seguridad'},
    ]
    
    featured = [
        {
            'title': 'Artículo Destacado 1',
            'description': 'Análisis completo del tema',
            'category_name': 'Política',
            '_display_index': 1,
            'is_featured': True
        }
    ]
    
    all_articles = featured + [
        {
            'title': f'Artículo {i}',
            'category_name': 'Noticias',
            '_display_index': i
        } for i in range(2, 10)
    ]
    
    # Generar
    generator = AdvancedLayoutGenerator()
    html = generator.generar_index_completo(
        site_metadata,
        featured,
        all_articles,
        categorias
    )
    
    # Guardar
    with open('layout/layout_avanzado_demo.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("✅ Layout avanzado generado: layout/layout_avanzado_demo.html")
    print("\n💡 Abre el archivo en tu navegador para ver:")
    print("   • Header con branding + menú deslizable")
    print("   • Carrusel de titulares animado")
    print("   • Grid de destacados + Sidebar miniaturas")
    print("   • Footer completo con redes sociales")


if __name__ == '__main__':
    main()
