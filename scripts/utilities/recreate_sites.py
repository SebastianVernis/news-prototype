#!/usr/bin/env python3
"""
Recrea los index.html de los 9 sitios con contenido limpio y dinámico.
"""

import os
import re

SITES = [
    ('cbnnoticias', 'CBN Noticias', 'Noticias con credibilidad', '#003366'),
    ('centralmexico', 'Central México', 'El pulso de la nación', '#004a99'),
    ('mexicoinformado', 'México Informado', 'Información que importa', '#1a472a'),
    ('nodoinformativo', 'Nodo Informativo', 'Conectando con la verdad', '#2c3e50'),
    ('noticiasobjetivo', 'Noticias Objetivo', 'La verdad sin filtros', '#8B0000'),
    ('radiocinconoticias', 'Radio Cinco Noticias', 'La voz de la información', '#FF6B00'),
    ('reportecentralmx', 'Reporte Central MX', 'Reporte verificado', '#4A0E4E'),
    ('tvmexico', 'TV México', 'Noticias en vivo', '#C41E3A'),
    ('verticenoticias', 'Vértice Noticias', 'El ángulo correcto', '#1B5E20'),
]

def extract_original_structure(site_dir):
    """Extrae la estructura original del sitio para preservar el diseño."""
    path = os.path.join(site_dir, 'index.html')
    if not os.path.exists(path):
        return None, None, None
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer header (desde <header hasta </header>)
    header_match = re.search(r'(<header[\s\S]*?</header>)', content, re.IGNORECASE)
    header = header_match.group(1) if header_match else ''
    
    # Extraer footer (desde <footer hasta </footer>)
    footer_match = re.search(r'(<footer[\s\S]*?</footer>)', content, re.IGNORECASE)
    footer = footer_match.group(1) if footer_match else ''
    
    # Extraer breaking news si existe
    breaking_match = re.search(r'(<section class="breaking-news"[\s\S]*?</section>)', content, re.IGNORECASE)
    breaking = breaking_match.group(1) if breaking_match else ''
    
    return header, footer, breaking

def create_clean_index(site_slug, site_name, site_tagline, preloader_color):
    site_dir = os.path.join('sites', site_slug)
    
    # Extraer estructura original
    header, footer, breaking = extract_original_structure(site_dir)
    
    # Si no hay header/footer, usar valores por defecto
    if not header:
        header = f'''<header class="header">
   <div class="container header-container">
    <div class="logo-section">
     <img alt="{site_slug}" class="site-logo" src="logo.png" style="height:60px;width:auto;object-fit:contain;"/>
     <div style="display:none;">
      <h1 class="site-title">{site_name}</h1>
      <p class="tagline">{site_tagline}</p>
     </div>
    </div>
    <nav class="main-nav">
     <a class="nav-link active" href="index.html">Inicio</a>
     <a class="nav-link" href="categoria/nacional.html">Nacional</a>
     <a class="nav-link" href="categoria/politica.html">Política</a>
     <a class="nav-link" href="categoria/economia.html">Economía</a>
     <a class="nav-link" href="categoria/deportes.html">Deportes</a>
    </nav>
   </div>
  </header>'''
    
    if not footer:
        footer = f'''<footer class="footer">
   <div class="container">
    <div class="footer-grid cols-3">
     <div class="footer-column">
      <div class="footer-logo"><img alt="{site_name}" src="logo.png" style="height:40px;width:auto;object-fit:contain;"/><h3>{site_name}</h3></div>
      <p class="footer-about">{site_tagline}. Información veraz y oportuna.</p>
      <div class="social-links">
       <a class="social-link" href="#"><i class="fab fa-facebook-f"></i></a>
       <a class="social-link" href="#"><i class="fab fa-twitter"></i></a>
       <a class="social-link" href="#"><i class="fab fa-instagram"></i></a>
       <a class="social-link" href="#"><i class="fab fa-youtube"></i></a>
      </div>
     </div>
     <div class="footer-column">
      <h4>Secciones</h4>
      <ul class="footer-links">
       <li><a href="categoria/nacional.html">Nacional</a></li>
       <li><a href="categoria/politica.html">Política</a></li>
       <li><a href="categoria/economia.html">Economía</a></li>
       <li><a href="categoria/deportes.html">Deportes</a></li>
      </ul>
     </div>
     <div class="footer-column">
      <h4>Información</h4>
      <ul class="footer-links">
       <li><a href="acerca-de.html">Acerca de</a></li>
       <li><a href="contacto.html">Contacto</a></li>
       <li><a href="privacidad.html">Privacidad</a></li>
       <li><a href="terminos.html">Términos</a></li>
      </ul>
     </div>
    </div>
    <div class="footer-bottom">
     <p>© 2026 {site_name}. Todos los derechos reservados.</p>
     <p class="disclaimer">Este sitio publica contenidos con fines informativos. Las opiniones expresadas pertenecen a sus autores.</p>
    </div>
   </div>
  </footer>'''
    
    if not breaking:
        breaking = f'''<section class="breaking-news">
    <div class="breaking-label">ÚLTIMA HORA</div>
    <div class="breaking-ticker">
        <marquee behavior="scroll" direction="left" onmouseout="this.start();" onmouseover="this.stop();">
            <span class="ticker-item">Bienvenido a {site_name} - Información verificada las 24 horas</span>
            <span class="ticker-item">•</span>
            <span class="ticker-item">Síguenos en redes sociales para más actualizaciones</span>
        </marquee>
    </div>
</section>'''
    
    # Crear el HTML limpio
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>{site_name} - {site_tagline}</title>
    <meta content="{site_tagline}. Noticias de México y el mundo." name="description"/>
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

{header}

{breaking}

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

{footer}

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
        const section = document.getElementById('news-section');
        if (!container) return;
        
        if (!articles.length) {{
            section.style.display = 'none';
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
    
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', loadArticles);
    }} else {{
        loadArticles();
    }}
}})();
</script>

</body>
</html>'''
    
    # Guardar el archivo limpio
    path = os.path.join(site_dir, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'  [OK] Recreado: {site_slug}')

def main():
    print('=' * 60)
    print('Recreando sitios con contenido limpio')
    print('=' * 60)
    
    for site_slug, site_name, site_tagline, preloader_color in SITES:
        site_dir = os.path.join('sites', site_slug)
        if not os.path.isdir(site_dir):
            print(f'  [SKIP] No existe: {site_slug}')
            continue
        
        try:
            create_clean_index(site_slug, site_name, site_tagline, preloader_color)
        except Exception as e:
            print(f'  [ERROR] {site_slug}: {e}')
    
    print('\n' + '=' * 60)
    print('¡Recreación completada!')
    print('=' * 60)

if __name__ == '__main__':
    main()
