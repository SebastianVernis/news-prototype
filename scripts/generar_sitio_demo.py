#!/usr/bin/env python3
"""
Genera un sitio demo pequeño con todas las funcionalidades SEO
Versión rápida con solo 3 artículos
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'api'))

# Imports
from newsapi import fetch_newsapi
from paraphrase import NewsParaphraser
from categorizer import NewsCategorizador
from rss_generator import RSSGenerator
from seo_metadata_generator import SEOMetadataGenerator
from section_generator import SectionGenerator
from site_name_generator import SiteNameGenerator
from color_palette_generator import ColorPaletteGenerator
from legal_pages_generator import LegalPagesGenerator
from preloader_generator import PreloaderGenerator
import requests
import hashlib
import random

print("""
╔══════════════════════════════════════════════════════════════════════╗
║     🚀 GENERADOR DE SITIO DEMO CON SEO COMPLETO                     ║
║     (3 artículos para testing rápido)                                ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# Crear directorio de salida
output_dir = Path('sites/site_demo')
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / 'images').mkdir(exist_ok=True)
(output_dir / 'categoria').mkdir(exist_ok=True)
(output_dir / 'og-images').mkdir(exist_ok=True)

# ============================================================================
# PASO 1: Descargar 3 noticias
# ============================================================================
print("\n" + "="*70)
print("📥 PASO 1: Descargando 3 noticias")
print("="*70)

noticias = fetch_newsapi(
    query='política México',
    language='es',
    page_size=3,
    enrich=True,
    silent=False
)

print(f"✅ {len(noticias)} noticias descargadas")

# ============================================================================
# PASO 2: Parafrasear
# ============================================================================
print("\n" + "="*70)
print("📝 PASO 2: Parafraseando (con párrafos correctos)")
print("="*70)

paraphraser = NewsParaphraser()
noticias_parafraseadas = []

for idx, noticia in enumerate(noticias, 1):
    print(f"[{idx}/3] {noticia.get('title', '')[:50]}...", end=" ")
    resultado = paraphraser.paraphrase_article(noticia, style="formal y objetivo")
    resultado['author'] = resultado.get('author') or LegalPagesGenerator().generar_autor_aleatorio()
    noticias_parafraseadas.append(resultado)
    print("✅")

# ============================================================================
# PASO 3: Categorizar
# ============================================================================
print("\n" + "="*70)
print("🏷️  PASO 3: Categorizando")
print("="*70)

categorizador = NewsCategorizador()
noticias_categorizadas = categorizador.categorizar_lote(noticias_parafraseadas, use_ai=True)

# ============================================================================
# PASO 3.5: Descargar imágenes
# ============================================================================
print("\n" + "="*70)
print("🖼️  PASO 3.5: Descargando imágenes")
print("="*70)

def descargar_imagen(url: str, output_path: str, index: int) -> bool:
    """Descarga una imagen desde URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"    ⚠️  Error descargando: {e}")
        return False

for idx, noticia in enumerate(noticias_categorizadas, 1):
    image_url = noticia.get('image_url', noticia.get('urlToImage', ''))
    
    if image_url and image_url.startswith('http'):
        print(f"[{idx}/3] Descargando imagen...", end=" ")
        
        output_path = output_dir / 'images' / f'news_{idx}.jpg'
        
        if descargar_imagen(image_url, str(output_path), idx):
            noticia['local_image_path'] = f'images/news_{idx}.jpg'
            print(f"✅ news_{idx}.jpg")
        else:
            noticia['local_image_path'] = None
    else:
        noticia['local_image_path'] = None
        print(f"[{idx}/3] Sin imagen disponible")

# ============================================================================
# PASO 4: Generar metadata del sitio
# ============================================================================
print("\n" + "="*70)
print("🏢 PASO 4: Generando metadata del sitio")
print("="*70)

name_gen = SiteNameGenerator()
site_name = name_gen.generar_nombre()
site_tagline = name_gen.generar_tagline(site_name)
color_gen = ColorPaletteGenerator()
colors = color_gen.obtener_paleta(0)

site_metadata = {
    'site_name': site_name,
    'nombre': site_name,
    'tagline': site_tagline,
    'description': f'{site_tagline}. Portal de noticias políticas.',
    'site_url': 'https://ejemplo.com',
    'domain': 'https://ejemplo.com',
    'color_primario': colors['primary'],
    'color_secundario': colors['secondary']
}

print(f"  ✅ Nombre: {site_name}")
print(f"  ✅ Tagline: {site_tagline}")
print(f"  ✅ Colores: {colors['primary']} / {colors['secondary']}")

# ============================================================================
# PASO 5: Generar artículos HTML
# ============================================================================
print("\n" + "="*70)
print("📄 PASO 5: Generando artículos HTML")
print("="*70)

seo_generator = SEOMetadataGenerator()

for idx, noticia in enumerate(noticias_categorizadas, 1):
    # Generar meta tags
    article_url = f"{site_metadata['site_url']}/article_{idx}.html"
    meta_tags = seo_generator.generar_meta_tags_articulo(
        noticia,
        site_metadata,
        article_url,
        idx
    )
    
    # Formatear contenido
    full_text = noticia.get('full_text', '')
    parrafos = [p.strip() for p in full_text.split('\n\n') if p.strip()]
    
    html_parrafos = []
    for i, p in enumerate(parrafos):
        if i == 0:
            html_parrafos.append(f'<p class="lead" style="font-size: 1.2rem; font-weight: 500; color: #495057;">{p}</p>')
        else:
            html_parrafos.append(f'<p style="margin-bottom: 1.5rem; line-height: 1.8; text-align: justify;">{p}</p>')
    
    contenido_html = '\n'.join(html_parrafos)
    
    # Generar HTML del artículo
    article_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
{meta_tags}
    <title>{noticia['title']} - {site_metadata['nombre']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.8;
            color: #2c3e50;
            background: #f5f7fa;
        }}
        .header {{
            background: linear-gradient(135deg, {site_metadata['color_primario']}, {site_metadata['color_secundario']});
            color: white;
            padding: 2rem 1rem;
            text-align: center;
        }}
        .container {{
            max-width: 800px;
            margin: 2rem auto;
            background: white;
            padding: 3rem;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .category-badge {{
            display: inline-block;
            background: {site_metadata['color_primario']}20;
            color: {site_metadata['color_primario']};
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            line-height: 1.3;
        }}
        .meta {{
            color: #6c757d;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #ecf0f1;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 2rem;
            color: {site_metadata['color_primario']};
            text-decoration: none;
            font-weight: 600;
        }}
        .back-link:hover {{ text-decoration: underline; }}
        .article-image-hero {{
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 8px;
            margin-bottom: 2rem;
        }}
    </style>
</head>
<body>
    <header class="header">
        <h2>{site_metadata['nombre']}</h2>
        <p>{site_metadata['tagline']}</p>
    </header>
    
    <div class="container">
        <span class="category-badge">{noticia.get('category_name', 'Noticias')}</span>
        <h1>{noticia['title']}</h1>
        <div class="meta">
            👤 {noticia.get('author', 'Redacción')} • 
            📅 {noticia.get('published_at', '')[:10]} • 
            🏷️ {noticia.get('category_name', 'Noticias')}
        </div>
        
        {'<img src="' + noticia.get('local_image_path', '') + '" alt="' + noticia['title'] + '" class="article-image-hero">' if noticia.get('local_image_path') else ''}
        
        <article>
            {contenido_html}
        </article>
        
        <a href="index.html" class="back-link">← Volver al inicio</a>
    </div>
</body>
</html>'''
    
    # Guardar
    article_path = output_dir / f"article_{idx}.html"
    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(article_html)
    
    print(f"  ✅ article_{idx}.html")

# ============================================================================
# PASO 6: Generar índice HTML
# ============================================================================
print("\n" + "="*70)
print("🏠 PASO 6: Generando index.html")
print("="*70)

home_meta = seo_generator.generar_meta_tags_home(site_metadata, len(noticias_categorizadas))

# Cards de artículos
articles_html = []
for idx, noticia in enumerate(noticias_categorizadas, 1):
    # Usar imagen local si existe, sino placeholder
    if noticia.get('local_image_path'):
        image_src = noticia['local_image_path']
    else:
        image_src = 'https://via.placeholder.com/400x200/667eea/ffffff?text=Noticia'
    
    articles_html.append(f'''
        <article class="article-card">
            <a href="article_{idx}.html" style="text-decoration: none; color: inherit;">
                <img src="{image_src}" alt="{noticia['title']}" class="article-image">
                <div class="article-content">
                    <span class="category-badge">{noticia.get('category_name', 'Noticias')}</span>
                    <h2 class="article-title">{noticia['title']}</h2>
                    <p class="article-description">{noticia.get('description', '')[:150]}...</p>
                    <div class="article-meta">
                        <span>👤 {noticia.get('author', 'Redacción')}</span>
                        <span>📅 {noticia.get('published_at', '')[:10]}</span>
                    </div>
                </div>
            </a>
        </article>
''')

index_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
{home_meta}
    <title>{site_metadata['nombre']} - {site_metadata['tagline']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
        }}
        .hero {{
            background: linear-gradient(135deg, {site_metadata['color_primario']}, {site_metadata['color_secundario']});
            color: white;
            padding: 4rem 2rem;
            text-align: center;
        }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .hero p {{ font-size: 1.25rem; opacity: 0.95; }}
        .nav {{
            background: white;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .nav a {{
            margin: 0 1rem;
            text-decoration: none;
            color: {site_metadata['color_primario']};
            font-weight: 600;
        }}
        .nav a:hover {{ text-decoration: underline; }}
        .articles-grid {{
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 1rem;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }}
        .article-card {{
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            transition: transform 0.3s ease;
        }}
        .article-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        .article-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
        }}
        .article-content {{
            padding: 1.5rem;
        }}
        .category-badge {{
            display: inline-block;
            background: {site_metadata['color_primario']}20;
            color: {site_metadata['color_primario']};
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }}
        .article-title {{
            font-size: 1.25rem;
            font-weight: bold;
            margin-bottom: 0.75rem;
            color: #2c3e50;
        }}
        .article-description {{
            color: #6c757d;
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }}
        .article-meta {{
            font-size: 0.85rem;
            color: #95a5a6;
            padding-top: 1rem;
            border-top: 1px solid #ecf0f1;
        }}
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 2rem;
            text-align: center;
            margin-top: 4rem;
        }}
    </style>
</head>
<body>
    <header class="hero">
        <h1>{site_metadata['nombre']}</h1>
        <p>{site_metadata['tagline']}</p>
    </header>
    
    <nav class="nav">
        <a href="index.html">🏠 Inicio</a>
        <a href="categorias.html">📑 Categorías</a>
        <a href="feed.xml">📡 RSS</a>
    </nav>
    
    <div class="articles-grid">
        {''.join(articles_html)}
    </div>
    
    <footer class="footer">
        <p>&copy; 2026 {site_metadata['nombre']}. Todos los derechos reservados.</p>
        <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            <a href="feed.xml" style="color: white;">📡 Suscríbete al RSS</a> • 
            <a href="categorias.html" style="color: white;">📑 Ver Categorías</a>
        </p>
    </footer>
</body>
</html>'''

# Inyectar preloader en index.html
preloader_gen = PreloaderGenerator()
preloader_tipo = random.choice([
    'contador', 'fade', 'slide-down', 'circle-expand', 
    'bars-loading', 'dots-pulse', 'spinning-logo', 
    'wave-animation', 'glitch-effect', 'rotating-square',
    'progress-circle', 'bouncing-balls'
])

colores_preloader = {
    'primary': site_metadata['color_primario'],
    'secondary': site_metadata['color_secundario']
}

preloader_code = preloader_gen.generar_preloader_completo(preloader_tipo, colores_preloader)
index_html = preloader_gen.inyectar_en_html(index_html, preloader_code)

with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f"  ✅ index.html (con preloader: {preloader_tipo})")

# ============================================================================
# PASO 7: Generar RSS feeds
# ============================================================================
print("\n" + "="*70)
print("📡 PASO 7: Generando RSS feeds")
print("="*70)

rss_generator = RSSGenerator()
feeds = rss_generator.generar_feeds_por_categoria(
    noticias_categorizadas,
    site_metadata,
    output_dir=str(output_dir)
)

print(f"  ✅ {len(feeds)} feeds generados")

# ============================================================================
# PASO 8: Generar páginas de categorías
# ============================================================================
print("\n" + "="*70)
print("📑 PASO 8: Generando páginas de categorías")
print("="*70)

section_generator = SectionGenerator()
grouped = categorizador.agrupar_por_categoria(noticias_categorizadas)

color_palette = {
    'primary': site_metadata['color_primario'],
    'secondary': site_metadata['color_secundario']
}

for cat_id, cat_articles in grouped.items():
    cat_data = categorizador.CATEGORIAS.get(cat_id, {})
    cat_nombre = cat_data.get('nombre', cat_id)
    
    output_file = output_dir / 'categoria' / f"{cat_id}.html"
    section_generator.generar_pagina_categoria(
        cat_id,
        cat_nombre,
        cat_articles,
        site_metadata,
        color_palette,
        str(output_file)
    )

# Índice de categorías
index_path = section_generator.generar_index_categorias(
    grouped,
    site_metadata,
    color_palette,
    str(output_dir / 'categorias.html')
)

print(f"  ✅ {len(grouped)} páginas de categoría + índice")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*70)
print("✨ SITIO DEMO GENERADO")
print("="*70)
print(f"""
📊 Estadísticas:
   • Artículos: {len(noticias_categorizadas)}
   • Categorías: {len(grouped)}
   • RSS feeds: {len(feeds)}
   • Páginas HTML: {len(noticias_categorizadas) + len(grouped) + 2}

📁 Ubicación: {output_dir}

🌐 Archivos principales:
   • index.html (home)
   • article_1.html, article_2.html, article_3.html
   • categorias.html (índice)
   • categoria/*.html (páginas de sección)
   • feed.xml (RSS general)
   • feed_*.xml (RSS por categoría)

✅ Funcionalidades incluidas:
   ✓ Párrafos bien formateados (8-12 por artículo)
   ✓ Categorización automática con IA
   ✓ Meta tags SEO completos
   ✓ Open Graph y Twitter Cards
   ✓ JSON-LD structured data
   ✓ RSS feeds (general + por categoría)
   ✓ Páginas de sección por categoría
   ✓ Navegación completa
""")

print("="*70)
print("🚀 SERVIDOR HTTP")
print("="*70)
print(f"""
Para servir el sitio, ejecuta:

  python3 -m http.server 8003 --directory {output_dir}

Luego abre en tu navegador:
  http://localhost:8003

""")
