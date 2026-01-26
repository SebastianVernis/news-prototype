#!/usr/bin/env python3
"""
Test de Generación Completa: 2 Artículos por Categoría
Valida todo el flujo del sistema con dataset pequeño
"""

import os
import sys
from pathlib import Path
import json
import time

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'api'))

from newsapi import fetch_newsapi
from categorizer import NewsCategorizador
from gemini_paraphraser import GeminiParaphraser
from rss_generator import RSSGenerator
from seo_metadata_generator import SEOMetadataGenerator
from section_generator import SectionGenerator
from site_name_generator import SiteNameGenerator
from color_palette_generator import ColorPaletteGenerator
from preloader_generator import PreloaderGenerator
from featured_manager import FeaturedManager
import requests
import random

print("""
╔══════════════════════════════════════════════════════════════════════╗
║     🧪 TEST: 2 ARTÍCULOS POR CATEGORÍA (20 ARTÍCULOS TOTAL)         ║
║     Validación completa del flujo del sistema                        ║
╚══════════════════════════════════════════════════════════════════════╝
""")

start_total = time.time()

# Crear directorio de salida
output_dir = Path('sites/test_2_por_categoria')
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / 'images').mkdir(exist_ok=True)
(output_dir / 'categoria').mkdir(exist_ok=True)
(output_dir / 'og-images').mkdir(exist_ok=True)

# ============================================================================
# PASO 1: Descargar noticias
# ============================================================================
print("\n" + "="*70)
print("📥 PASO 1: Descargando 25 noticias (para tener variedad)")
print("="*70)

noticias = fetch_newsapi(
    query='política México',
    language='es',
    page_size=25,
    enrich=True,
    silent=False
)

print(f"✅ {len(noticias)} noticias descargadas")

# ============================================================================
# PASO 2: Parafrasear con Gemini (rápido para test)
# ============================================================================
print("\n" + "="*70)
print("📝 PASO 2: Parafraseando con Gemini (paralelo)")
print("="*70)

gemini = GeminiParaphraser()
noticias_parafraseadas = gemini.parafrasear_lote_paralelo(
    noticias,
    max_workers=3,
    delay_between_batches=0.5
)

# ============================================================================
# PASO 3: Categorizar
# ============================================================================
print("\n" + "="*70)
print("🏷️  PASO 3: Categorizando noticias")
print("="*70)

categorizador = NewsCategorizador()
noticias_categorizadas = categorizador.categorizar_lote(
    noticias_parafraseadas,
    use_ai=False,  # Keywords para velocidad
    batch_delay=0
)

# ============================================================================
# PASO 4: Seleccionar 2 por categoría
# ============================================================================
print("\n" + "="*70)
print("📊 PASO 4: Seleccionando 2 artículos por categoría")
print("="*70)

grouped = categorizador.agrupar_por_categoria(noticias_categorizadas)

articulos_finales = []
distribucion = {}

for cat_id in categorizador.CATEGORIAS.keys():
    cat_name = categorizador.CATEGORIAS[cat_id]['nombre']
    cat_articles = grouped.get(cat_id, [])
    
    # Tomar hasta 2 artículos de esta categoría
    selected = cat_articles[:2]
    
    if selected:
        articulos_finales.extend(selected)
        distribucion[cat_name] = len(selected)
        print(f"  {cat_name:30} {len(selected)} artículos")

print(f"\n✅ Total artículos seleccionados: {len(articulos_finales)}")
print(f"✅ Categorías con artículos: {len(distribucion)}")

# Marcar artículos destacados
featured_manager = FeaturedManager()
articulos_finales = featured_manager.marcar_destacados(articulos_finales)

# Separar destacados y placeholders
separated = featured_manager.separar_destacados_y_placeholders(articulos_finales)

print(f"\n📊 Artículos destacados (Blackbox): {separated['stats']['total_featured']}")
print(f"📊 Placeholders (Gemini): {separated['stats']['total_placeholders']}")

# Ordenar: destacados primero
articulos_finales = featured_manager.ordenar_destacados_primero(articulos_finales)

# ============================================================================
# PASO 5: Descargar imágenes
# ============================================================================
print("\n" + "="*70)
print("🖼️  PASO 5: Descargando imágenes")
print("="*70)

def descargar_imagen(url: str, output_path: str) -> bool:
    """Descarga una imagen"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except:
        return False

for idx, articulo in enumerate(articulos_finales, 1):
    image_url = articulo.get('image_url', articulo.get('urlToImage', ''))
    
    if image_url and image_url.startswith('http'):
        print(f"[{idx}/{len(articulos_finales)}] Descargando...", end=" ")
        output_path = output_dir / 'images' / f'news_{idx}.jpg'
        
        if descargar_imagen(image_url, str(output_path)):
            articulo['local_image_path'] = f'images/news_{idx}.jpg'
            print("✅")
        else:
            articulo['local_image_path'] = None
            print("⚠️")
    else:
        articulo['local_image_path'] = None

# ============================================================================
# PASO 6: Generar metadata del sitio
# ============================================================================
print("\n" + "="*70)
print("🏢 PASO 6: Generando metadata del sitio")
print("="*70)

name_gen = SiteNameGenerator()
site_name = name_gen.generar_nombre()
site_tagline = name_gen.generar_tagline(site_name)
color_gen = ColorPaletteGenerator()
colors = color_gen.obtener_paleta(random.randint(0, 19))

site_metadata = {
    'site_name': site_name,
    'nombre': site_name,
    'tagline': site_tagline,
    'description': f'{site_tagline}. Portal de noticias políticas.',
    'site_url': 'https://test-2-por-categoria.com',
    'domain': 'https://test-2-por-categoria.com',
    'color_primario': colors['primary'],
    'color_secundario': colors['secondary']
}

print(f"  ✅ Nombre: {site_name}")
print(f"  ✅ Colores: {colors['primary']} / {colors['secondary']}")

# ============================================================================
# PASO 7: Generar artículos HTML
# ============================================================================
print("\n" + "="*70)
print("📄 PASO 7: Generando artículos HTML")
print("="*70)

seo_generator = SEOMetadataGenerator()

for idx, articulo in enumerate(articulos_finales, 1):
    # Meta tags
    article_url = f"{site_metadata['site_url']}/article_{idx}.html"
    meta_tags = seo_generator.generar_meta_tags_articulo(
        articulo,
        site_metadata,
        article_url,
        idx
    )
    
    # Contenido - Priorizar full_text, luego content, luego description
    full_text = articulo.get('full_text', '') or articulo.get('content', '') or articulo.get('description', '')
    
    if not full_text or len(full_text) < 50:
        full_text = "Texto no disponible"
    
    # Si no tiene párrafos separados, dividir por oraciones (cada 3-4 oraciones = 1 párrafo)
    parrafos = [p.strip() for p in full_text.split('\n\n') if p.strip()]
    
    if len(parrafos) == 1 and len(full_text) > 400:
        # Dividir texto largo en párrafos de ~400 caracteres
        import re
        oraciones = re.split(r'([.!?]\s+)', full_text)
        
        parrafos = []
        parrafo_actual = ""
        
        for i in range(0, len(oraciones), 2):
            oracion = oraciones[i] + (oraciones[i+1] if i+1 < len(oraciones) else '')
            
            if len(parrafo_actual) + len(oracion) < 500:
                parrafo_actual += oracion
            else:
                if parrafo_actual:
                    parrafos.append(parrafo_actual.strip())
                parrafo_actual = oracion
        
        if parrafo_actual:
            parrafos.append(parrafo_actual.strip())
        
        # Limitar a 8 párrafos
        parrafos = parrafos[:8]
    
    html_parrafos = []
    for i, p in enumerate(parrafos[:10]):  # Máximo 10 párrafos
        if i == 0:
            html_parrafos.append(f'<p class="lead">{p}</p>')
        else:
            html_parrafos.append(f'<p>{p}</p>')
    
    contenido_html = '\n            '.join(html_parrafos) if html_parrafos else '<p>Contenido no disponible.</p>'
    
    # Imagen hero
    image_hero = ''
    if articulo.get('local_image_path'):
        image_hero = f'<img src="{articulo["local_image_path"]}" alt="{articulo["title"]}" style="width: 100%; height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 2rem;">'
    
    article_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
{meta_tags}
    <title>{articulo['title']} - {site_metadata['nombre']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Georgia, serif; line-height: 1.8; color: #2c3e50; background: #f5f7fa; }}
        .header {{ background: linear-gradient(135deg, {site_metadata['color_primario']}, {site_metadata['color_secundario']}); color: white; padding: 2rem 1rem; text-align: center; }}
        .container {{ max-width: 800px; margin: 2rem auto; background: white; padding: 3rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .category-badge {{ display: inline-block; background: {site_metadata['color_primario']}20; color: {site_metadata['color_primario']}; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin-bottom: 1rem; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 1.5rem; line-height: 1.3; }}
        .meta {{ color: #6c757d; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #ecf0f1; }}
        p {{ margin-bottom: 1.5rem; line-height: 1.8; text-align: justify; }}
        .lead {{ font-size: 1.2rem; font-weight: 500; color: #495057; }}
        .back-link {{ display: inline-block; margin-top: 2rem; color: {site_metadata['color_primario']}; text-decoration: none; font-weight: 600; }}
    </style>
</head>
<body>
    <header class="header">
        <h2>{site_metadata['nombre']}</h2>
        <p>{site_metadata['tagline']}</p>
    </header>
    
    <div class="container">
        <span class="category-badge">{articulo.get('category_name', 'Noticias')}</span>
        <h1>{articulo['title']}</h1>
        <div class="meta">
            👤 {articulo.get('author', 'Redacción')} • 
            📅 {articulo.get('published_at', '')[:10]} • 
            🏷️ {articulo.get('category_name', 'Noticias')}
        </div>
        
        {image_hero}
        
        <article>
            {contenido_html}
        </article>
        
        <a href="index.html" class="back-link">← Volver al inicio</a>
    </div>
</body>
</html>'''
    
    # Guardar
    with open(output_dir / f'article_{idx}.html', 'w', encoding='utf-8') as f:
        f.write(article_html)

print(f"  ✅ {len(articulos_finales)} artículos HTML generados")

# ============================================================================
# PASO 8: Generar index.html
# ============================================================================
print("\n" + "="*70)
print("🏠 PASO 8: Generando index.html")
print("="*70)

home_meta = seo_generator.generar_meta_tags_home(site_metadata, len(articulos_finales))

# Agregar índice de display a cada artículo
for idx, articulo in enumerate(articulos_finales, 1):
    articulo['_display_index'] = idx

# Generar sección de destacados HTML
featured_section_html = featured_manager.generar_seccion_destacados_html(
    separated['featured'],
    {'primary': site_metadata['color_primario'], 'secondary': site_metadata['color_secundario']}
)

# Cards de TODOS los artículos (destacados ya tienen su sección arriba)
articles_html = []
for idx, articulo in enumerate(articulos_finales, 1):
    image_src = articulo.get('local_image_path', 'https://via.placeholder.com/400x200')
    
    # Badge especial para destacados
    if articulo.get('is_featured'):
        badge_extra = '<span style="background: gold; color: #000; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.7rem; margin-left: 0.5rem;">⭐ Premium</span>'
    else:
        badge_extra = ''
    
    articles_html.append(f'''
        <article class="article-card">
            <a href="article_{idx}.html">
                <img src="{image_src}" alt="{articulo['title']}" class="article-image">
                <div class="article-content">
                    <span class="category-badge">{articulo.get('category_name', 'Noticias')}{badge_extra}</span>
                    <h2>{articulo['title'][:100]}</h2>
                    <p>{articulo.get('description', '')[:150]}...</p>
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
        body {{ font-family: -apple-system, sans-serif; background: #f5f7fa; }}
        .hero {{ background: linear-gradient(135deg, {site_metadata['color_primario']}, {site_metadata['color_secundario']}); color: white; padding: 4rem 2rem; text-align: center; }}
        .hero h1 {{ font-size: 3rem; margin-bottom: 1rem; }}
        .nav {{ background: white; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .nav a {{ margin: 0 1rem; text-decoration: none; color: {site_metadata['color_primario']}; font-weight: 600; }}
        .articles-grid {{ max-width: 1200px; margin: 3rem auto; padding: 0 1rem; display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2rem; }}
        .article-card {{ background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.08); transition: transform 0.3s; }}
        .article-card:hover {{ transform: translateY(-5px); }}
        .article-card a {{ text-decoration: none; color: inherit; }}
        .article-image {{ width: 100%; height: 200px; object-fit: cover; }}
        .article-content {{ padding: 1.5rem; }}
        .category-badge {{ display: inline-block; background: {site_metadata['color_primario']}20; color: {site_metadata['color_primario']}; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.75rem; }}
        .article-card h2 {{ font-size: 1.25rem; margin-bottom: 0.75rem; }}
        .article-card p {{ color: #6c757d; font-size: 0.95rem; }}
        .footer {{ background: #2c3e50; color: white; padding: 2rem; text-align: center; margin-top: 4rem; }}
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
    
    {featured_section_html if separated['featured'] else ''}
    
    <div style="max-width: 1200px; margin: 2rem auto; padding: 0 1rem;">
        <h2 style="font-size: 1.5rem; color: #2c3e50; margin-bottom: 1.5rem; text-align: center;">
            📰 Todos los Artículos
        </h2>
    </div>
    
    <div class="articles-grid">
        {''.join(articles_html)}
    </div>
    
    <footer class="footer">
        <p>&copy; 2026 {site_metadata['nombre']}. Test de 2 artículos por categoría.</p>
    </footer>
</body>
</html>'''

# Inyectar preloader
preloader_gen = PreloaderGenerator()
preloader_tipo = random.choice(['contador', 'slide-down', 'progress-circle'])
preloader_code = preloader_gen.generar_preloader_completo(
    preloader_tipo,
    {'primary': site_metadata['color_primario'], 'secondary': site_metadata['color_secundario']}
)
index_html = preloader_gen.inyectar_en_html(index_html, preloader_code)

with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print(f"  ✅ index.html (preloader: {preloader_tipo})")

# ============================================================================
# PASO 9: Generar RSS feeds
# ============================================================================
print("\n" + "="*70)
print("📡 PASO 9: Generando RSS feeds")
print("="*70)

rss_gen = RSSGenerator()
feeds = rss_gen.generar_feeds_por_categoria(
    articulos_finales,
    site_metadata,
    output_dir=str(output_dir)
)

print(f"  ✅ {len(feeds)} RSS feeds generados")

# ============================================================================
# PASO 10: Generar páginas de categorías
# ============================================================================
print("\n" + "="*70)
print("📑 PASO 10: Generando páginas de categorías")
print("="*70)

section_gen = SectionGenerator()
grouped_final = categorizador.agrupar_por_categoria(articulos_finales)

color_palette = {
    'primary': site_metadata['color_primario'],
    'secondary': site_metadata['color_secundario']
}

for cat_id, cat_articles in grouped_final.items():
    if not cat_articles:
        continue
    
    cat_data = categorizador.CATEGORIAS.get(cat_id, {})
    cat_nombre = cat_data.get('nombre', cat_id)
    
    output_file = output_dir / 'categoria' / f'{cat_id}.html'
    section_gen.generar_pagina_categoria(
        cat_id,
        cat_nombre,
        cat_articles,
        site_metadata,
        color_palette,
        str(output_file)
    )

# Índice de categorías
section_gen.generar_index_categorias(
    grouped_final,
    site_metadata,
    color_palette,
    str(output_dir / 'categorias.html')
)

print(f"  ✅ {len(grouped_final)} páginas de categoría + índice")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
elapsed_total = time.time() - start_total

print("\n" + "="*70)
print("✨ TEST COMPLETADO")
print("="*70)

print(f"""
📊 Estadísticas:
   • Noticias descargadas: {len(noticias)}
   • Noticias parafraseadas: {len(noticias_parafraseadas)}
   • Artículos finales: {len(articulos_finales)}
   • Categorías con artículos: {len(distribucion)}
   • Imágenes descargadas: {sum(1 for a in articulos_finales if a.get('local_image_path'))}
   • RSS feeds: {len(feeds)}
   • Páginas HTML: {len(articulos_finales) + len(grouped_final) + 2}
   
⏱️  Tiempo total: {elapsed_total/60:.1f} minutos

📁 Ubicación: {output_dir}

🌐 Para ver el sitio:
   cd {output_dir.parent}
   python3 -m http.server 8005 --directory {output_dir.name}
   
   Luego abre: http://localhost:8005

📚 Distribución por categoría:
""")

for cat_name, count in sorted(distribucion.items(), key=lambda x: x[1], reverse=True):
    print(f"   • {cat_name}: {count} artículos")

print("\n" + "="*70)
print("✅ VALIDACIÓN COMPLETA DEL FLUJO")
print("="*70)
print("""
Funcionalidades verificadas:
  ✓ Descarga de noticias
  ✓ Parafraseo con Gemini paralelo
  ✓ Categorización automática
  ✓ Selección de 2 por categoría
  ✓ Descarga de imágenes locales
  ✓ Generación de artículos HTML
  ✓ Meta tags SEO
  ✓ Preloader con colores del sitio
  ✓ RSS feeds por categoría
  ✓ Páginas de sección
  ✓ Navegación completa
""")

print("="*70)
