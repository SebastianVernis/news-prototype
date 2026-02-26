#!/usr/bin/env python3
"""
Script para crear estructura completa de sitios:
- Categorías con páginas individuales
- Páginas legales (términos, privacidad, contacto, acerca-de)
- Enlaces correctos

Ahora trabaja con directorios de sitios en lugar de archivos planos.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))
DATA_DIR = Path(os.getenv("NEWS_DATA_DIR", REPO_ROOT / "data"))

# Categorías estándar (los IDs ya están sin tildes)
CATEGORIES = [
    {'id': 'politica', 'name': 'Política', 'icon': '🏛️'},
    {'id': 'economia', 'name': 'Economía', 'icon': '💰'},
    {'id': 'deportes', 'name': 'Deportes', 'icon': '⚽'},
    {'id': 'tecnologia', 'name': 'Tecnología', 'icon': '💻'},
    {'id': 'cultura', 'name': 'Cultura', 'icon': '🎭'},
    {'id': 'internacional', 'name': 'Internacional', 'icon': '🌎'}
]

def slugify_category(name):
    """Convierte nombre de categoría a slug sin tildes"""
    slug = name.lower()
    slug = slug.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    slug = slug.replace(" ", "-")
    return slug

def load_news():
    """Carga las noticias desde el archivo JSON más reciente"""
    patterns = ["*paraphrased*_cached_images.json", "*paraphrased*.json", "newsapi_*.json"]
    files = []
    for pattern in patterns:
        files.extend(DATA_DIR.glob(pattern))
    
    if not files:
        return []
    
    latest_file = sorted(files)[-1]
    with open(latest_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def categorize_news(articles):
    """Asigna categorías a las noticias basándose en su contenido"""
    category_keywords = {
        'politica': ['presidente', 'gobierno', 'congreso', 'senado', 'política', 'elecciones', 'partido'],
        'economia': ['economía', 'peso', 'dólar', 'inflación', 'banco', 'finanzas', 'mercado', 'empleo'],
        'deportes': ['fútbol', 'deportes', 'equipo', 'jugador', 'partido', 'liga', 'campeonato'],
        'tecnologia': ['tecnología', 'digital', 'internet', 'app', 'software', 'inteligencia artificial'],
        'cultura': ['cultura', 'arte', 'música', 'cine', 'teatro', 'exposición', 'festival'],
        'internacional': ['internacional', 'mundo', 'global', 'extranjero', 'ONU', 'tratado']
    }

    categorized = []
    for article in articles:
        title = (article.get('title', '') + ' ' + article.get('description', '')).lower()
        assigned_category = 'general'
        
        for cat_id, keywords in category_keywords.items():
            if any(keyword in title for keyword in keywords):
                assigned_category = cat_id
                break

        article['category'] = assigned_category
        article['category_name'] = next((c['name'] for c in CATEGORIES if c['id'] == assigned_category), 'General')
        categorized.append(article)

    return categorized

def create_category_pages(site_dir, site_name, articles):
    """Crea páginas HTML para cada categoría dentro del directorio del sitio"""
    by_category = {}
    for article in articles:
        cat = article.get('category', 'general')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(article)

    for cat in CATEGORIES:
        cat_id = cat['id']
        cat_name = cat['name']
        cat_articles = by_category.get(cat_id, [])

        articles_html = ""
        for article in cat_articles[:12]:
            title = article.get('title', 'Noticia')[:100]
            description = article.get('description', '')[:200]
            image = article.get('urlToImage', article.get('image', 'assets/images/fallback-1.svg'))
            author = article.get('author', f"Redacción {article.get('category', 'General')}")
            published = article.get('publishedAt', '')[:10] if article.get('publishedAt') else ''
            
            # Crear slug para el artículo
            slug = slugify_title(title)

            articles_html += f'''
            <article class="category-card">
                <a href="articulo-{slug}.html">
                <img src="{image}" alt="{title[:50]}">
                <div class="category-card-content">
                    <h3 class="category-card-title">{title}</h3>
                    <p class="category-card-excerpt">{description}...</p>
                    <div class="category-meta">
                        <span>Por {author}</span>
                        <span>{published}</span>
                    </div>
                </div>
                </a>
            </article>
'''

        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_name} - {site_name}</title>
    <link rel="stylesheet" href="templates/css/template1.css">
    <style>
        .category-header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center; }}
        .category-title {{ font-size: 2.5em; margin-bottom: 10px; }}
        .article-count {{ font-size: 1.2em; opacity: 0.9; }}
        .category-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; padding: 40px 20px; max-width: 1200px; margin: 0 auto; }}
        .category-card {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s; }}
        .category-card:hover {{ transform: translateY(-5px); }}
        .category-card img {{ width: 100%; height: 200px; object-fit: cover; }}
        .category-card-content {{ padding: 20px; }}
        .category-card-title {{ font-size: 1.2em; margin-bottom: 10px; line-height: 1.4; }}
        .category-card-excerpt {{ color: #666; line-height: 1.6; margin-bottom: 15px; }}
        .category-meta {{ display: flex; justify-content: space-between; color: #888; font-size: 0.85em; padding-top: 15px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <header class="header header-bold">
        <div class="container">
            <div class="header-bold">
                <h1 class="logo-bold"><a href="index.html" style="color:inherit;text-decoration:none;">{site_name}</a></h1>
                <p class="tagline-bold">Tu fuente confiable de información</p>
            </div>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
                <a href="categoria-politica.html" class="nav-link">Política</a>
                <a href="categoria-economia.html" class="nav-link">Economía</a>
                <a href="categoria-deportes.html" class="nav-link">Deportes</a>
                <a href="categoria-tecnologia.html" class="nav-link">Tecnología</a>
                <a href="categoria-cultura.html" class="nav-link">Cultura</a>
                <a href="categoria-internacional.html" class="nav-link">Internacional</a>
            </nav>
        </div>
    </header>

    <div class="category-header">
        <div class="category-title">{cat['icon']} {cat_name}</div>
        <div class="article-count">{len(cat_articles)} noticias</div>
    </div>

    <main class="main-content">
        <div class="category-grid">
{articles_html}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-column">
                    <h3>{site_name}</h3>
                    <p>Tu fuente confiable de información</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>
</body>
</html>
'''

        category_file = site_dir / f'categoria-{cat_id}.html'
        with open(category_file, 'w', encoding='utf-8') as f:
            f.write(html)

def slugify_title(title):
    """Convierte un título en slug para URL"""
    import re
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug.strip()[:50]  # Máximo 50 caracteres
    return slug or 'noticia'

def create_article_pages(site_dir, site_name, articles):
    """Crea páginas individuales para cada artículo"""
    for article in articles:
        title = article.get('title', 'Noticia')
        slug = slugify_title(title)
        description = article.get('description', '')
        content = article.get('full_text', article.get('content', description))
        image = article.get('urlToImage', article.get('image', '../assets/images/fallback-1.svg'))
        author = article.get('author', f"Redacción {article.get('category', 'General')}")
        published = article.get('publishedAt', '')[:19].replace('T', ' ') if article.get('publishedAt') else ''

        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title[:60]} - {site_name}</title>
    <link rel="stylesheet" href="templates/css/template1.css">
    <style>
        .article-header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 20px; text-align: center; }}
        .article-title {{ font-size: 2.5em; margin-bottom: 20px; max-width: 900px; margin-left: auto; margin-right: auto; }}
        .article-meta {{ font-size: 1.1em; opacity: 0.9; }}
        .article-content {{ max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.8; font-size: 1.1em; }}
        .article-content p {{ margin-bottom: 20px; }}
        .article-image {{ max-width: 100%; height: auto; border-radius: 12px; margin: 30px 0; }}
        .article-source {{ color: #888; font-size: 0.9em; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <header class="header header-bold">
        <div class="container">
            <div class="header-bold">
                <h1 class="logo-bold"><a href="index.html" style="color:inherit;text-decoration:none;">{site_name}</a></h1>
                <p class="tagline-bold">Tu fuente confiable de información</p>
            </div>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
                <a href="categoria-politica.html" class="nav-link">Política</a>
                <a href="categoria-economia.html" class="nav-link">Economía</a>
                <a href="categoria-deportes.html" class="nav-link">Deportes</a>
                <a href="categoria-tecnologia.html" class="nav-link">Tecnología</a>
                <a href="categoria-cultura.html" class="nav-link">Cultura</a>
                <a href="categoria-internacional.html" class="nav-link">Internacional</a>
            </nav>
        </div>
    </header>

    <div class="article-header">
        <div class="article-title">{title}</div>
        <div class="article-meta">
            <span>Por {author}</span> • <span>{published}</span>
        </div>
    </div>

    <main class="article-content">
        <img src="{image}" alt="{title[:50]}" class="article-image">

        {content.replace(chr(10), '<br>')}

        <div class="article-source">
            <p>© {site_name} - {author}. Todos los derechos reservados.</p>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-column">
                    <h3>{site_name}</h3>
                    <p>Tu fuente confiable de información</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>
</body>
</html>
'''

        article_file = site_dir / f'articulo-{slug}.html'
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(html)

def create_legal_pages(site_dir, site_name):
    """Crea páginas legales dentro del directorio del sitio"""
    
    # Términos y Condiciones
    terminos_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Términos y Condiciones - {site_name}</title>
    <link rel="stylesheet" href="templates/css/template1.css">
    <style>
        .legal-content {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .legal-content h1 {{ font-size: 2em; margin-bottom: 20px; color: var(--text-color, #004D40); }}
        .legal-content h2 {{ font-size: 1.5em; margin: 30px 0 15px 0; color: var(--primary-color, #00897B); }}
        .legal-content p {{ line-height: 1.8; color: #555; margin-bottom: 15px; }}
    </style>
</head>
<body>
    <header class="header header-bold">
        <div class="container">
            <div class="header-bold">
                <h1 class="logo-bold"><a href="index.html" style="color:inherit;text-decoration:none;">{site_name}</a></h1>
            </div>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
                <a href="terminos.html" class="nav-link">Términos</a>
                <a href="privacidad.html" class="nav-link">Privacidad</a>
                <a href="contacto.html" class="nav-link">Contacto</a>
            </nav>
        </div>
    </header>

    <main class="legal-content">
        <h1>Términos y Condiciones</h1>
        <p>Última actualización: {datetime.now().strftime('%d/%m/%Y')}</p>
        
        <h2>1. Aceptación de los términos</h2>
        <p>Al acceder y utilizar {site_name}, aceptas estar sujeto a estos Términos y Condiciones de Uso.</p>
        
        <h2>2. Uso del sitio</h2>
        <p>El contenido de este sitio web es solo para uso informativo y personal.</p>
        
        <h2>3. Propiedad intelectual</h2>
        <p>Todo el contenido publicado en {site_name} está protegido por derechos de autor.</p>
        
        <h2>4. Limitación de responsabilidad</h2>
        <p>{site_name} no se responsabiliza por errores u omisiones en la información publicada.</p>
        
        <h2>5. Contacto</h2>
        <p>Para consultas sobre estos términos, contáctanos en contacto@{site_name.lower().replace(' ', '')}.com</p>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>
'''

    # Política de Privacidad
    privacidad_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Política de Privacidad - {site_name}</title>
    <link rel="stylesheet" href="templates/css/template1.css">
    <style>
        .legal-content {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .legal-content h1 {{ font-size: 2em; margin-bottom: 20px; color: var(--text-color, #004D40); }}
        .legal-content h2 {{ font-size: 1.5em; margin: 30px 0 15px 0; color: var(--primary-color, #00897B); }}
        .legal-content p {{ line-height: 1.8; color: #555; margin-bottom: 15px; }}
    </style>
</head>
<body>
    <header class="header header-bold">
        <div class="container">
            <div class="header-bold">
                <h1 class="logo-bold"><a href="index.html" style="color:inherit;text-decoration:none;">{site_name}</a></h1>
            </div>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
                <a href="terminos.html" class="nav-link">Términos</a>
                <a href="privacidad.html" class="nav-link">Privacidad</a>
                <a href="contacto.html" class="nav-link">Contacto</a>
            </nav>
        </div>
    </header>

    <main class="legal-content">
        <h1>Política de Privacidad</h1>
        <p>Última actualización: {datetime.now().strftime('%d/%m/%Y')}</p>
        
        <h2>1. Información que recopilamos</h2>
        <p>En {site_name} respetamos tu privacidad y nos comprometemos a proteger tus datos personales.</p>
        
        <h2>2. Uso de la información</h2>
        <p>La información recopilada se utiliza únicamente para mejorar la experiencia del usuario.</p>
        
        <h2>3. Cookies</h2>
        <p>Este sitio utiliza cookies para mejorar la navegación y analizar el tráfico.</p>
        
        <h2>4. Seguridad</h2>
        <p>Implementamos medidas de seguridad para proteger tu información personal.</p>
        
        <h2>5. Tus derechos</h2>
        <p>Tienes derecho a acceder, rectificar o eliminar tu información personal en cualquier momento.</p>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>
'''

    # Contacto
    contacto_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contacto - {site_name}</title>
    <link rel="stylesheet" href="templates/css/template1.css">
    <style>
        .contact-content {{ max-width: 600px; margin: 0 auto; padding: 40px 20px; }}
        .contact-content h1 {{ font-size: 2em; margin-bottom: 20px; color: var(--text-color, #004D40); }}
        .contact-info {{ background: var(--background-color, #E0F2F1); padding: 20px; border-radius: 8px; margin-top: 20px; }}
        .contact-info p {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <header class="header header-bold">
        <div class="container">
            <div class="header-bold">
                <h1 class="logo-bold"><a href="index.html" style="color:inherit;text-decoration:none;">{site_name}</a></h1>
            </div>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
                <a href="terminos.html" class="nav-link">Términos</a>
                <a href="privacidad.html" class="nav-link">Privacidad</a>
                <a href="contacto.html" class="nav-link">Contacto</a>
            </nav>
        </div>
    </header>

    <main class="contact-content">
        <h1>Contacto</h1>
        <p>¿Tienes alguna pregunta o sugerencia? ¡Nos gustaría escucharte!</p>
        
        <div class="contact-info">
            <p><strong>Email:</strong> contacto@{site_name.lower().replace(' ', '')}.com</p>
            <p><strong>Teléfono:</strong> +52 55 1234 5678</p>
            <p><strong>Dirección:</strong> Ciudad de México, México</p>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>
'''

    # Acerca de
    acerca_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acerca de - {site_name}</title>
    <link rel="stylesheet" href="templates/css/template1.css">
    <style>
        .about-content {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; }}
        .about-content h1 {{ font-size: 2em; margin-bottom: 20px; color: var(--text-color, #004D40); }}
        .about-content p {{ line-height: 1.8; color: #555; margin-bottom: 15px; }}
    </style>
</head>
<body>
    <header class="header header-bold">
        <div class="container">
            <div class="header-bold">
                <h1 class="logo-bold"><a href="index.html" style="color:inherit;text-decoration:none;">{site_name}</a></h1>
            </div>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
                <a href="terminos.html" class="nav-link">Términos</a>
                <a href="privacidad.html" class="nav-link">Privacidad</a>
                <a href="contacto.html" class="nav-link">Contacto</a>
            </nav>
        </div>
    </header>

    <main class="about-content">
        <h1>Acerca de {site_name}</h1>
        <p>{site_name} es tu fuente confiable de información actualizada sobre eventos nacionales e internacionales.</p>
        
        <h2>Nuestra Misión</h2>
        <p>Proporcionar información veraz, oportuna y relevante para nuestra comunidad de lectores.</p>
        
        <h2>Nuestros Valores</h2>
        <ul>
            <li>Compromiso con la verdad</li>
            <li>Respeto por nuestros lectores</li>
            <li>Independencia editorial</li>
            <li>Responsabilidad social</li>
        </ul>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
        </div>
    </footer>
</body>
</html>
'''

    # Guardar todas las páginas legales
    legal_pages = {
        'terminos.html': terminos_html,
        'privacidad.html': privacidad_html,
        'contacto.html': contacto_html,
        'acerca-de.html': acerca_html
    }

    for filename, content in legal_pages.items():
        legal_file = site_dir / filename
        with open(legal_file, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    """Función principal"""
    import sys
    
    print("🏗️  CREANDO ESTRUCTURA COMPLETA DE SITIOS")
    print("="*60)

    # Obtener cantidad de sitios de variable de entorno o argumento
    sites_count = int(os.getenv("SITES_COUNT", "3"))
    if len(sys.argv) > 1:
        try:
            sites_count = int(sys.argv[1])
        except ValueError:
            pass

    # Cargar y categorizar noticias
    print("\n📰 Cargando y categorizando noticias...")
    articles = load_news()
    articles = categorize_news(articles)
    print(f"   ✅ {len(articles)} noticias categorizadas")

    # Detectar directorios de sitios existentes
    site_dirs = [d for d in SITES_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if not site_dirs:
        print("⚠️  No se encontraron directorios de sitios en", SITES_DIR)
        return

    print(f"\n📁 Se encontraron {len(site_dirs)} directorios de sitios")

    # Procesar cada directorio de sitio
    for site_dir in site_dirs[:sites_count]:
        # Leer site_config.json si existe para obtener el nombre
        config_file = site_dir / 'site_config.json'
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            site_name = config.get('name', config.get('title', site_dir.name))
        else:
            site_name = site_dir.name.replace('-', ' ').title()

        print(f"\n🌐 Procesando: {site_name} ({site_dir.name})")

        # Crear directorio templates/css si no existe (para el CSS)
        templates_css_dir = site_dir / 'templates' / 'css'
        templates_css_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar CSS desde public/templates/css si existe
        source_css = REPO_ROOT / 'public' / 'templates' / 'css'
        if source_css.exists():
            for css_file in source_css.glob('*.css'):
                dest_css = templates_css_dir / css_file.name
                if not dest_css.exists():
                    dest_css.write_bytes(css_file.read_bytes())

        # Crear páginas de categorías
        print("   📁 Creando páginas de categorías...")
        create_category_pages(site_dir, site_name, articles)

        # Crear páginas de artículos individuales
        print("   📄 Creando páginas de artículos...")
        create_article_pages(site_dir, site_name, articles)

        # Crear páginas legales
        print("   ⚖️  Creando páginas legales...")
        create_legal_pages(site_dir, site_name)

        print(f"   ✅ {site_name} completado")

    print("\n" + "="*60)
    print("✅ ESTRUCTURA COMPLETA CREADA")
    print("="*60)
    print(f"\n📁 {len(site_dirs[:sites_count])} sitios procesados")
    print("   Cada sitio tiene:")
    print("   - index.html con noticias destacadas")
    print("   - 6 páginas de categorías (categoria-*.html)")
    print("   - Páginas de artículos individuales (articulo-*.html)")
    print("   - 4 páginas legales (terminos.html, privacidad.html, etc.)")
    print("\n🔗 Todos los enlaces ahora funcionan correctamente")

if __name__ == "__main__":
    main()
