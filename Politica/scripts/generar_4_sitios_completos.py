#!/usr/bin/env python3
"""
Generador de 4 Sitios Completos
Con todas las características implementadas:
- Categorización, RSS, SEO, Preloaders
- Layouts diferentes
- Artículos destacados (Blackbox Pro) + Placeholders (Gemini)
- Imágenes descargadas localmente
- Headers/Sidebars completos, Footers completos
"""

import os
import sys
from pathlib import Path
import json
import time
import random

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'api'))

from newsapi import fetch_newsapi
from paraphrase import NewsParaphraser
from gemini_paraphraser import GeminiParaphraser
from categorizer import NewsCategorizador
from rss_generator import RSSGenerator
from seo_metadata_generator import SEOMetadataGenerator
from section_generator import SectionGenerator
from site_name_generator import SiteNameGenerator
from color_palette_generator import ColorPaletteGenerator
from preloader_generator import PreloaderGenerator
from featured_manager import FeaturedManager
from enhanced_components import EnhancedComponents
import requests
import re

print("""
╔══════════════════════════════════════════════════════════════════════╗
║     🚀 GENERADOR DE 4 SITIOS COMPLETOS DE PRODUCCIÓN                ║
║     Con todas las características implementadas                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# Inicializar componentes
paraphraser_blackbox = NewsParaphraser()  # Para destacados
paraphraser_gemini = GeminiParaphraser()  # Para placeholders
categorizador = NewsCategorizador()
rss_gen = RSSGenerator()
seo_gen = SEOMetadataGenerator()
section_gen = SectionGenerator()
name_gen = SiteNameGenerator()
color_gen = ColorPaletteGenerator()
preloader_gen = PreloaderGenerator()
featured_mgr = FeaturedManager()
components = EnhancedComponents()

# Layouts a usar para cada sitio
layouts_config = [
    {'numero': 1, 'usa_sidebar': False, 'sidebar_pos': None},
    {'numero': 2, 'usa_sidebar': True, 'sidebar_pos': 'left'},
    {'numero': 3, 'usa_sidebar': False, 'sidebar_pos': None},
    {'numero': 4, 'usa_sidebar': True, 'sidebar_pos': 'right'},
]

start_total = time.time()

# ============================================================================
# DESCARGAR NOTICIAS (una sola vez para los 4 sitios)
# ============================================================================
print("\n" + "="*70)
print("📥 Descargando noticias del día")
print("="*70)

noticias = fetch_newsapi(
    query='política México',
    language='es',
    page_size=100,  # Suficientes para 4 sitios
    enrich=True,
    silent=False
)

print(f"✅ {len(noticias)} noticias descargadas")

# ============================================================================
# GENERAR 4 SITIOS
# ============================================================================

for site_num, layout_config in enumerate(layouts_config, 1):
    print("\n" + "="*70)
    print(f"🏗️  GENERANDO SITIO {site_num}/4")
    print("="*70)
    
    site_start = time.time()
    
    # Directorio del sitio
    site_dir = Path(f'sites/site_{site_num}')
    site_dir.mkdir(parents=True, exist_ok=True)
    (site_dir / 'images').mkdir(exist_ok=True)
    (site_dir / 'categoria').mkdir(exist_ok=True)
    (site_dir / 'og-images').mkdir(exist_ok=True)
    (site_dir / 'assets').mkdir(exist_ok=True)
    
    # Tomar subset de noticias para este sitio
    start_idx = (site_num - 1) * 20
    end_idx = start_idx + 20
    noticias_sitio = noticias[start_idx:end_idx]
    
    if len(noticias_sitio) < 5:
        print(f"⚠️  No hay suficientes noticias para sitio {site_num}, saltando...")
        continue
    
    print(f"📰 Procesando {len(noticias_sitio)} noticias para este sitio")
    
    # PASO 1: Parafrasear artículos destacados (primeros 3 con Blackbox Pro)
    print(f"\n📝 Parafraseando 3 artículos destacados (Blackbox Pro)...")
    
    destacados = []
    for i, noticia in enumerate(noticias_sitio[:3], 1):
        print(f"  [{i}/3] {noticia.get('title', '')[:50]}...", end=" ", flush=True)
        
        style = ['formal y objetivo', 'casual y cercano', 'técnico y detallado'][i % 3]
        resultado = paraphraser_blackbox.paraphrase_article(noticia, style=style)
        resultado['paraphrase_method'] = 'blackbox-pro'
        destacados.append(resultado)
        
        print("✅")
    
    # PASO 2: Parafrasear placeholders (resto con Gemini paralelo)
    print(f"\n🚀 Parafraseando {len(noticias_sitio[3:])} placeholders (Gemini paralelo)...")
    
    placeholders = paraphraser_gemini.parafrasear_lote_paralelo(
        noticias_sitio[3:],
        max_workers=3,
        delay_between_batches=0.5
    )
    
    # Combinar todos
    todos_articulos = destacados + placeholders
    
    # PASO 3: Categorizar
    print(f"\n🏷️  Categorizando {len(todos_articulos)} artículos...")
    
    todos_articulos_cat = categorizador.categorizar_lote(
        todos_articulos,
        use_ai=False,  # Keywords para velocidad
        batch_delay=0
    )
    
    # PASO 4: Marcar destacados y ordenar
    todos_articulos_cat = featured_mgr.marcar_destacados(todos_articulos_cat)
    todos_articulos_cat = featured_mgr.ordenar_destacados_primero(todos_articulos_cat)
    separated = featured_mgr.separar_destacados_y_placeholders(todos_articulos_cat)
    
    print(f"  ⭐ Destacados: {separated['stats']['total_featured']}")
    print(f"  📄 Placeholders: {separated['stats']['total_placeholders']}")
    
    # PASO 5: Descargar imágenes
    print(f"\n🖼️  Descargando imágenes...")
    
    def descargar_imagen_segura(url: str, output_path: str) -> bool:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=15, stream=True)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            return True
        except:
            return False
    
    imagenes_descargadas = 0
    for idx, articulo in enumerate(todos_articulos_cat, 1):
        image_url = articulo.get('image_url', articulo.get('urlToImage', ''))
        
        if image_url and image_url.startswith('http'):
            output_path = site_dir / 'images' / f'news_{idx}.jpg'
            
            if descargar_imagen_segura(image_url, str(output_path)):
                articulo['local_image_path'] = f'images/news_{idx}.jpg'
                imagenes_descargadas += 1
            else:
                articulo['local_image_path'] = None
        else:
            articulo['local_image_path'] = None
    
    print(f"  ✅ {imagenes_descargadas}/{len(todos_articulos_cat)} imágenes descargadas")
    
    # PASO 6: Metadata del sitio
    print(f"\n🏢 Generando metadata del sitio...")
    
    site_name = name_gen.generar_nombre()
    site_tagline = name_gen.generar_tagline(site_name)
    colors = color_gen.obtener_paleta(site_num - 1)
    
    site_metadata = {
        'nombre': site_name,
        'site_name': site_name,
        'tagline': site_tagline,
        'description': f'{site_tagline}. Portal de noticias políticas de México.',
        'site_url': f'https://sitio-{site_num}.com',
        'domain': f'https://sitio-{site_num}.com',
        'color_primario': colors['primary'],
        'color_secundario': colors['secondary']
    }
    
    print(f"  Nombre: {site_name}")
    print(f"  Colores: {colors['primary']} / {colors['secondary']}")
    
    # PASO 7: Generar artículos HTML
    print(f"\n📄 Generando {len(todos_articulos_cat)} artículos HTML...")
    
    # Agregar índice de display
    for idx, articulo in enumerate(todos_articulos_cat, 1):
        articulo['_display_index'] = idx
    
    for idx, articulo in enumerate(todos_articulos_cat, 1):
        # Meta tags
        article_url = f"{site_metadata['site_url']}/article_{idx}.html"
        meta_tags = seo_gen.generar_meta_tags_articulo(articulo, site_metadata, article_url, idx)
        
        # Contenido con división de párrafos
        full_text = articulo.get('full_text', '') or articulo.get('content', '') or articulo.get('description', '')
        
        if not full_text or len(full_text) < 50:
            full_text = articulo.get('description', 'Contenido no disponible')
        
        # Dividir en párrafos
        parrafos = [p.strip() for p in full_text.split('\n\n') if p.strip()]
        
        # Si solo hay 1 párrafo largo, dividir inteligentemente
        if len(parrafos) == 1 and len(full_text) > 400:
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
            
            parrafos = parrafos[:8]
        
        html_parrafos = []
        for i, p in enumerate(parrafos[:10]):
            if i == 0:
                html_parrafos.append(f'<p class="lead">{p}</p>')
            else:
                html_parrafos.append(f'<p>{p}</p>')
        
        contenido_html = '\n            '.join(html_parrafos) if html_parrafos else '<p>Contenido no disponible.</p>'
        
        # Imagen hero
        image_hero = ''
        if articulo.get('local_image_path'):
            image_hero = f'<img src="../{articulo["local_image_path"]}" alt="{articulo["title"]}" class="article-hero-image">'
        
        # Badge de destacado
        badge_destacado = ''
        if articulo.get('is_featured'):
            badge_destacado = '<span class="featured-badge-article">⭐ Artículo Destacado</span>'
        
        article_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
{meta_tags}
    <title>{articulo['title']} - {site_metadata['nombre']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Georgia, 'Times New Roman', serif; line-height: 1.8; color: #2c3e50; background: #f5f7fa; }}
        .header {{ background: linear-gradient(135deg, {site_metadata['color_primario']}, {site_metadata['color_secundario']}); color: white; padding: 2rem 1rem; text-align: center; }}
        .header h2 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .header p {{ opacity: 0.95; }}
        .container {{ max-width: 900px; margin: 2rem auto; background: white; padding: 3rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .category-badge {{ display: inline-block; background: {site_metadata['color_primario']}20; color: {site_metadata['color_primario']}; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; margin-bottom: 1rem; }}
        .featured-badge-article {{ display: inline-block; background: gold; color: #000; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 700; margin-left: 0.5rem; }}
        h1 {{ font-size: 2.5rem; margin-bottom: 1.5rem; line-height: 1.3; color: #1a202c; }}
        .meta {{ color: #6c757d; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #ecf0f1; font-size: 0.95rem; }}
        .article-hero-image {{ width: 100%; height: 450px; object-fit: cover; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        p {{ margin-bottom: 1.5rem; line-height: 1.9; text-align: justify; }}
        .lead {{ font-size: 1.25rem; font-weight: 500; color: #374151; line-height: 1.8; }}
        .back-link {{ display: inline-block; margin-top: 2rem; color: {site_metadata['color_primario']}; text-decoration: none; font-weight: 600; padding: 0.75rem 1.5rem; border: 2px solid {site_metadata['color_primario']}; border-radius: 6px; transition: all 0.3s; }}
        .back-link:hover {{ background: {site_metadata['color_primario']}; color: white; }}
        .share-buttons {{ margin: 2rem 0; padding: 1.5rem; background: #f8f9fa; border-radius: 8px; text-align: center; }}
        .share-btn {{ display: inline-block; margin: 0 0.5rem; padding: 0.5rem 1rem; background: {site_metadata['color_primario']}; color: white; border-radius: 6px; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <header class="header">
        <h2>{site_metadata['nombre']}</h2>
        <p>{site_metadata['tagline']}</p>
    </header>
    
    <div class="container">
        <div>
            <span class="category-badge">{articulo.get('category_name', 'Noticias')}</span>
            {badge_destacado}
        </div>
        
        <h1>{articulo['title']}</h1>
        
        <div class="meta">
            👤 {articulo.get('author', 'Redacción')} • 
            📅 {articulo.get('published_at', '')[:10]} • 
            🏷️ {articulo.get('category_name', 'Noticias')} •
            📖 {len(parrafos)} párrafos
        </div>
        
        {image_hero}
        
        <article>
            {contenido_html}
        </article>
        
        <div class="share-buttons">
            <p style="margin-bottom: 1rem; font-weight: 600; color: #2c3e50;">Compartir este artículo:</p>
            <a href="#" class="share-btn">📘 Facebook</a>
            <a href="#" class="share-btn">🐦 Twitter</a>
            <a href="#" class="share-btn">💼 LinkedIn</a>
            <a href="#" class="share-btn">📱 WhatsApp</a>
        </div>
        
        <a href="index.html" class="back-link">← Volver al inicio</a>
    </div>
</body>
</html>'''
        
        # Guardar
        with open(site_dir / f'article_{idx}.html', 'w', encoding='utf-8') as f:
            f.write(article_html)
    
    print(f"  ✅ Artículos HTML generados")
    
    # PASO 8: Generar index.html
    print(f"\n🏠 Generando index.html...")
    
    home_meta = seo_gen.generar_meta_tags_home(site_metadata, len(todos_articulos_cat))
    
    # Preparar datos para componentes
    categorias_lista = [
        {'id': cat_id, 'nombre': categorizador.CATEGORIAS[cat_id]['nombre']}
        for cat_id in categorizador.CATEGORIAS.keys()
    ]
    
    # Generar header o sidebar según configuración
    if layout_config['usa_sidebar']:
        header_html = components.sidebar_iconos_collapsible(
            site_metadata,
            categorias_lista,
            site_metadata,
            layout_config['sidebar_pos']
        )
        content_class = f'content-with-sidebar-{layout_config["sidebar_pos"]}'
    else:
        header_html = components.header_completo_horizontal(
            site_metadata,
            categorias_lista
        )
        content_class = ''
    
    # Footer
    footer_html = components.footer_completo_profesional(site_metadata, categorias_lista)
    
    # Cards de artículos
    articles_cards = []
    for idx, articulo in enumerate(todos_articulos_cat, 1):
        image_src = articulo.get('local_image_path', 'https://via.placeholder.com/400x300')
        
        badge_premium = ''
        if articulo.get('is_featured'):
            badge_premium = '<span style="background: gold; color: #000; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.7rem; margin-left: 0.5rem;">⭐ Premium</span>'
        
        articles_cards.append(f'''
        <article class="article-card">
            <a href="article_{idx}.html">
                <img src="{image_src}" alt="{articulo['title']}" class="card-image" loading="lazy">
                <div class="card-content">
                    <span class="card-category">{articulo.get('category_name', 'Noticias')}{badge_premium}</span>
                    <h2 class="card-title">{articulo['title'][:120]}</h2>
                    <p class="card-excerpt">{articulo.get('description', '')[:150]}...</p>
                    <div class="card-meta">
                        <span>📅 {articulo.get('published_at', '')[:10]}</span>
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
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f7fa; }}
        
        .hero {{ background: linear-gradient(135deg, {site_metadata['color_primario']}, {site_metadata['color_secundario']}); color: white; padding: 4rem 2rem; text-align: center; }}
        .hero h1 {{ font-size: 3.5rem; margin-bottom: 1rem; font-weight: 800; }}
        .hero p {{ font-size: 1.3rem; opacity: 0.95; }}
        
        .articles-section {{ max-width: 1400px; margin: 3rem auto; padding: 0 2rem; }}
        .section-title {{ font-size: 2rem; color: #2c3e50; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 3px solid {site_metadata['color_primario']}; }}
        
        .articles-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 2rem; }}
        .article-card {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); transition: all 0.3s; }}
        .article-card:hover {{ transform: translateY(-8px); box-shadow: 0 8px 30px rgba(0,0,0,0.15); }}
        .article-card a {{ text-decoration: none; color: inherit; display: block; }}
        .card-image {{ width: 100%; height: 220px; object-fit: cover; }}
        .card-content {{ padding: 1.5rem; }}
        .card-category {{ display: inline-block; background: {site_metadata['color_primario']}20; color: {site_metadata['color_primario']}; padding: 0.4rem 0.9rem; border-radius: 16px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 1rem; }}
        .card-title {{ font-size: 1.35rem; font-weight: 700; margin-bottom: 0.75rem; line-height: 1.4; color: #1a202c; }}
        .card-excerpt {{ color: #6c757d; line-height: 1.7; margin-bottom: 1rem; font-size: 0.95rem; }}
        .card-meta {{ font-size: 0.85rem; color: #95a5a6; padding-top: 1rem; border-top: 1px solid #ecf0f1; }}
        
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 2.5rem; }}
            .articles-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
{header_html}

<div class="{content_class}">
    <div class="hero">
        <h1>{site_metadata['nombre']}</h1>
        <p>{site_metadata['tagline']}</p>
    </div>
    
    <div class="articles-section">
        <h2 class="section-title">📰 Últimas Noticias</h2>
        <div class="articles-grid">
            {''.join(articles_cards)}
        </div>
    </div>
    
{footer_html}
</div>
</body>
</html>'''
    
    # Inyectar preloader
    preloader_tipo = random.choice(['contador', 'slide-down', 'progress-circle', 'fade', 'wave-animation'])
    preloader_code = preloader_gen.generar_preloader_completo(
        preloader_tipo,
        {'primary': site_metadata['color_primario'], 'secondary': site_metadata['color_secundario']}
    )
    index_html = preloader_gen.inyectar_en_html(index_html, preloader_code)
    
    with open(site_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"  ✅ index.html (preloader: {preloader_tipo})")
    
    # PASO 9: RSS feeds
    print(f"\n📡 Generando RSS feeds...")
    
    feeds = rss_gen.generar_feeds_por_categoria(
        todos_articulos_cat,
        site_metadata,
        output_dir=str(site_dir)
    )
    
    print(f"  ✅ {len(feeds)} RSS feeds generados")
    
    # PASO 10: Páginas de categorías
    print(f"\n📑 Generando páginas de categorías...")
    
    grouped = categorizador.agrupar_por_categoria(todos_articulos_cat)
    color_palette = {
        'primary': site_metadata['color_primario'],
        'secondary': site_metadata['color_secundario']
    }
    
    for cat_id, cat_articles in grouped.items():
        if not cat_articles:
            continue
        
        cat_data = categorizador.CATEGORIAS.get(cat_id, {})
        cat_nombre = cat_data.get('nombre', cat_id)
        
        output_file = site_dir / 'categoria' / f'{cat_id}.html'
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
        grouped,
        site_metadata,
        color_palette,
        str(site_dir / 'categorias.html')
    )
    
    print(f"  ✅ {len(grouped)} páginas de categoría + índice")
    
    # PASO 11: Guardar estadísticas
    stats = {
        'site_number': site_num,
        'site_name': site_name,
        'layout': layout_config['numero'],
        'usa_sidebar': layout_config['usa_sidebar'],
        'preloader': preloader_tipo,
        'total_articulos': len(todos_articulos_cat),
        'destacados': separated['stats']['total_featured'],
        'placeholders': separated['stats']['total_placeholders'],
        'imagenes_descargadas': imagenes_descargadas,
        'rss_feeds': len(feeds),
        'categorias_activas': len(grouped),
        'tiempo_generacion': time.time() - site_start
    }
    
    with open(site_dir / 'site_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    site_elapsed = time.time() - site_start
    
    print(f"\n{'='*70}")
    print(f"✅ SITIO {site_num} COMPLETADO")
    print(f"{'='*70}")
    print(f"  Nombre: {site_name}")
    print(f"  Layout: {layout_config['numero']} ({'Sidebar ' + layout_config['sidebar_pos'] if layout_config['usa_sidebar'] else 'Header tradicional'})")
    print(f"  Artículos: {len(todos_articulos_cat)} ({separated['stats']['total_featured']} destacados)")
    print(f"  Imágenes: {imagenes_descargadas}")
    print(f"  Tiempo: {site_elapsed/60:.1f} minutos")
    print(f"  Directorio: {site_dir}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
elapsed_total = time.time() - start_total

print("\n" + "="*70)
print("🎉 GENERACIÓN DE 4 SITIOS COMPLETADA")
print("="*70)
print(f"""
⏱️  Tiempo total: {elapsed_total/60:.1f} minutos

📁 Sitios generados en: sites/

🌐 Para servir los sitios:
   cd sites
   
   Sitio 1: python3 -m http.server 9001 --directory site_1
   Sitio 2: python3 -m http.server 9002 --directory site_2
   Sitio 3: python3 -m http.server 9003 --directory site_3
   Sitio 4: python3 -m http.server 9004 --directory site_4

📊 Características de cada sitio:
   • 20 artículos (3 destacados Blackbox Pro + 17 placeholders Gemini)
   • Categorización automática
   • Imágenes descargadas localmente
   • RSS feeds completos
   • Meta tags SEO
   • Preloader animado
   • Headers/Sidebars completos
   • Footers con TyC y PdP
   • Diseño responsive

✅ TODO IMPLEMENTADO Y FUNCIONANDO
""")

print("="*70)
