#!/usr/bin/env python3
"""
Convierte los 9 sitios de HTML estático a carga dinámica pura.
Elimina los bloques con data-article y reemplaza con contenedores vacíos + render desde cero.
"""

import os
import re

SITES_DIR = 'sites'

SITES = [
    'cbnnoticias',
    'centralmexico', 
    'mexicoinformado',
    'nodoinformativo',
    'noticiasobjetivo',
    'radiocinconoticias',
    'reportecentralmx',
    'tvmexico',
    'verticenoticias',
]

def extract_header(site_dir):
    """Extrae el header del index.html existente."""
    path = os.path.join(site_dir, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer desde <!DOCTYPE hasta </header>
    match = re.search(r'(<!DOCTYPE html>.*?<body>.*?<header.*?</header>)', content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def extract_footer(site_dir):
    """Extrae el footer del index.html existente."""
    path = os.path.join(site_dir, 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer footer
    match = re.search(r'(<footer.*?</footer>.*?</body>.*?</html>)', content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def get_preloader_color(site_dir):
    """Obtiene el color del preloader del style.css."""
    style_path = os.path.join(site_dir, 'style.css')
    if not os.path.exists(style_path):
        return '#1a1a2e'
    
    with open(style_path, 'r', encoding='utf-8') as f:
        css = f.read()
    
    # Buscar --primary-color o --accent-color
    match = re.search(r'--(?:primary|accent)-color\s*:\s*(#[0-9a-fA-F]{3,6})', css)
    if match:
        return match.group(1)
    return '#1a1a2e'

def get_site_name(site_slug):
    """Obtiene el nombre del sitio."""
    names = {
        'cbnnoticias': 'CBN Noticias',
        'centralmexico': 'Central México',
        'mexicoinformado': 'México Informado',
        'nodoinformativo': 'Nodo Informativo',
        'noticiasobjetivo': 'Noticias Objetivo',
        'radiocinconoticias': 'Radio Cinco Noticias',
        'reportecentralmx': 'Reporte Central MX',
        'tvmexico': 'TV México',
        'verticenoticias': 'Vértice Noticias',
    }
    return names.get(site_slug, site_slug)

def create_dynamic_index(site_slug):
    """Crea un nuevo index.html con carga dinámica pura."""
    site_dir = os.path.join(SITES_DIR, site_slug)
    site_name = get_site_name(site_slug)
    preloader_color = get_preloader_color(site_dir)
    
    # Leer el index original para extraer header/footer
    original_path = os.path.join(site_dir, 'index.html')
    with open(original_path, 'r', encoding='utf-8') as f:
        original = f.read()
    
    # Extraer header (desde <!DOCTYPE hasta </header>)
    header_match = re.search(r'(<!DOCTYPE html>.*?<body>.*?<header.*?</header>)', original, re.DOTALL | re.IGNORECASE)
    header_html = header_match.group(1) if header_match else ''
    
    # Extraer footer (desde <footer hasta </html>)
    footer_match = re.search(r'(<footer.*?</footer>.*?</body>.*?</html>)', original, re.DOTALL | re.IGNORECASE)
    footer_html = footer_match.group(1) if footer_match else ''
    
    # Extraer breaking news si existe
    breaking_match = re.search(r'(<section class="breaking-news".*?</section>)', original, re.DOTALL | re.IGNORECASE)
    breaking_html = breaking_match.group(1) if breaking_match else ''
    
    # Crear el nuevo HTML con carga dinámica
    new_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>{site_name} - Noticias</title>
    <meta content="Noticias de México y el mundo." name="description"/>
    <link href="https://fonts.googleapis.com" rel="preconnect"/>
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;800&amp;family=Noto+Sans:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"/>
    <link href="style.css" rel="stylesheet"/>
</head>
<body>

<!-- Preloader -->
<div id="preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;background:{preloader_color};z-index:999999;display:flex;flex-direction:column;justify-content:center;align-items:center;">
    <div style="text-align:center;">
        <div style="margin-bottom:25px;animation:spin3D 2s ease-in-out infinite;">
            <img src="logo.png" alt="Logo" style="height:120px;width:auto;filter:brightness(0) invert(1);">
        </div>
        <div style="width:40px;height:40px;border:4px solid rgba(255,255,255,0.2);border-top:4px solid white;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 20px;"></div>
        <p style="font-family:Arial,sans-serif;color:white;font-weight:bold;letter-spacing:2px;text-transform:uppercase;font-size:0.9rem;">Cargando...</p>
    </div>
</div>
<style>
    @keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
    @keyframes spin3D {{
        0% {{ transform: rotateY(0deg) scale(1); }}
        50% {{ transform: rotateY(180deg) scale(1.1); }}
        100% {{ transform: rotateY(360deg) scale(1); }}
    }}
</style>
<script>
    window.addEventListener('load', function() {{
        setTimeout(function() {{
            var preloader = document.getElementById('preloader');
            if(preloader) {{
                preloader.style.transition = 'opacity 0.5s ease';
                preloader.style.opacity = '0';
                setTimeout(function() {{ preloader.style.display = 'none'; }}, 500);
            }}
        }}, 1500);
    }});
</script>

{header_html}

{breaking_html}

<main class="main-content">
    <div class="container">
        <!-- Sección destacada - carga dinámica -->
        <section class="featured-section">
            <div id="featured-container" data-api="/api/articles?site={site_slug}&limit=20">
                <div style="text-align:center;padding:40px;color:#666;">Cargando noticias...</div>
            </div>
        </section>
        
        <!-- Sección de noticias adicionales -->
        <section class="news-section" id="news-section">
            <h2 class="section-title">Más Noticias</h2>
            <div id="news-container" class="horizontal-list"></div>
        </section>
    </div>
</main>

{footer_html}

<script src="script.js"></script>
<script>
(function() {{
    const apiUrl = document.querySelector('#featured-container')?.dataset.api || '/api/articles?site={site_slug}&limit=20';
    
    async function loadArticles() {{
        try {{
            const res = await fetch(apiUrl);
            if (!res.ok) throw new Error('Network error');
            const {{articles}} = await res.json();
            if (!articles?.length) {{
                document.getElementById('featured-container').innerHTML = '<div style="text-align:center;padding:40px;color:#666;">No hay noticias disponibles.</div>';
                return;
            }}
            
            // Renderizar artículos
            renderFeatured(articles.slice(0, 4));
            renderNews(articles.slice(4));
        }} catch (e) {{
            console.error('Error loading articles:', e);
            document.getElementById('featured-container').innerHTML = '<div style="text-align:center;padding:40px;color:#666;">Error al cargar noticias.</div>';
        }}
    }}
    
    function renderFeatured(articles) {{
        const container = document.getElementById('featured-container');
        if (!container || !articles.length) return;
        
        // Hero horizontal (primer artículo)
        const hero = articles[0];
        const heroHtml = `
            <div class="hero-horizontal">
                <a href="articulo/index.html?slug=${{encodeURIComponent(hero.slug || '')}}">
                    <img src="${{hero.imageUrl || 'assets/images/article_placeholder.jpg'}}" alt="${{escHtml(hero.title || '')}}" loading="lazy" style="width:100%;aspect-ratio:16/9;object-fit:cover;">
                </a>
                <div class="hero-overlay">
                    <span class="category-badge cat-${{escHtml((hero.category || 'general').toLowerCase())}}">${{escHtml(hero.category || 'General')}}</span>
                    <h2 class="hero-title">
                        <a href="articulo/index.html?slug=${{encodeURIComponent(hero.slug || '')}}" style="color:inherit;text-decoration:none;">
                            ${{escHtml(hero.title || '')}}
                        </a>
                    </h2>
                    <p class="hero-excerpt">${{escHtml(hero.excerpt || '')}}</p>
                    <div class="hero-meta">
                        <span class="author"><i class="far fa-user"></i> ${{escHtml(hero.author || 'Redacción')}}</span>
                        <span class="date"><i class="far fa-calendar"></i> ${{hero.publishedAt ? new Date(hero.publishedAt).toLocaleDateString('es-MX') : ''}}</span>
                    </div>
                </div>
            </div>
        `;
        
        // Lista horizontal (artículos 2-4)
        let listHtml = '<div class="horizontal-list">';
        for (let i = 1; i < articles.length; i++) {{
            const a = articles[i];
            listHtml += `
                <article class="horizontal-card">
                    <a href="articulo/index.html?slug=${{encodeURIComponent(a.slug || '')}}">
                        <img src="${{a.imageUrl || 'assets/images/article_placeholder.jpg'}}" alt="${{escHtml(a.title || '')}}" loading="lazy">
                    </a>
                    <div class="horizontal-card-content">
                        <span class="category-badge cat-${{escHtml((a.category || 'general').toLowerCase())}}">${{escHtml(a.category || 'General')}}</span>
                        <h3><a href="articulo/index.html?slug=${{encodeURIComponent(a.slug || '')}}" style="color:inherit;text-decoration:none;">${{escHtml(a.title || '')}}</a></h3>
                        <p>${{escHtml(a.excerpt || '')}}</p>
                        <div class="card-meta">
                            <span class="timestamp"><i class="far fa-clock"></i> ${{a.publishedAt ? new Date(a.publishedAt).toLocaleDateString('es-MX') : ''}}</span>
                            <span class="author"><i class="far fa-user"></i> ${{escHtml(a.author || 'Redacción')}}</span>
                        </div>
                    </div>
                </article>
            `;
        }}
        listHtml += '</div>';
        
        container.innerHTML = heroHtml + listHtml;
    }}
    
    function renderNews(articles) {{
        const container = document.getElementById('news-container');
        if (!container || !articles.length) {{
            document.getElementById('news-section').style.display = 'none';
            return;
        }}
        
        let html = '';
        for (const a of articles) {{
            html += `
                <article class="horizontal-card">
                    <a href="articulo/index.html?slug=${{encodeURIComponent(a.slug || '')}}">
                        <img src="${{a.imageUrl || 'assets/images/article_placeholder.jpg'}}" alt="${{escHtml(a.title || '')}}" loading="lazy">
                    </a>
                    <div class="horizontal-card-content">
                        <span class="category-badge cat-${{escHtml((a.category || 'general').toLowerCase())}}">${{escHtml(a.category || 'General')}}</span>
                        <h3><a href="articulo/index.html?slug=${{encodeURIComponent(a.slug || '')}}" style="color:inherit;text-decoration:none;">${{escHtml(a.title || '')}}</a></h3>
                        <p>${{escHtml(a.excerpt || '')}}</p>
                        <div class="card-meta">
                            <span class="card-date">${{a.publishedAt ? new Date(a.publishedAt).toLocaleDateString('es-MX') : ''}}</span>
                        </div>
                    </div>
                </article>
            `;
        }}
        container.innerHTML = html;
    }}
    
    function escHtml(text) {{
        if (!text) return '';
        return String(text)
            .replace(/&/g, '&amp;')
            .replace(/</g, '<')
            .replace(/>/g, '>')
            .replace(/"/g, '"');
    }}
    
    // Cargar artículos al iniciar
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', loadArticles);
    }} else {{
        loadArticles();
    }}
}})();
</script>

</body>
</html>'''
    
    # Guardar el nuevo index.html
    with open(original_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f'  [OK] Convertido a dinámico: {site_slug}')

def main():
    print('=' * 60)
    print('Convirtiendo sitios a carga dinámica pura')
    print('=' * 60)
    
    for site_slug in SITES:
        site_dir = os.path.join(SITES_DIR, site_slug)
        if not os.path.isdir(site_dir):
            print(f'  [SKIP] No encontrado: {site_slug}')
            continue
        
        try:
            create_dynamic_index(site_slug)
        except Exception as e:
            print(f'  [ERROR] {site_slug}: {e}')
    
    print('\n' + '=' * 60)
    print('¡Conversión completada!')
    print('=' * 60)

if __name__ == '__main__':
    main()
