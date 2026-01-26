#!/usr/bin/env python3
"""
Generador de 2 Sitios Premium Completos
Con TODAS las características implementadas:
- Layouts avanzados con carrusel
- Headers/Footers completos
- Sidebars collapsibles
- TyC, PdP, Documentación completa
- Máximo de artículos de la data disponible
- Imágenes verificadas y descargadas
- Sistema paralelo completo
"""

import os
import sys
from pathlib import Path
import json
import time
import random
import re

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'api'))

from paraphrase import NewsParaphraser
from gemini_paraphraser import GeminiParaphraser
from categorizer import NewsCategorizador
from rss_generator import RSSGenerator
from seo_metadata_generator import SEOMetadataGenerator
from section_generator import SectionGenerator
from preloader_generator import PreloaderGenerator
from featured_manager import FeaturedManager
from enhanced_components import EnhancedComponents
from advanced_layout_generator import AdvancedLayoutGenerator
from legal_pages_generator import LegalPagesGenerator
from color_palette_generator import ColorPaletteGenerator
from global_styles import GlobalStyles
import requests

print("""
╔══════════════════════════════════════════════════════════════════════╗
║     🏆 GENERADOR DE 2 SITIOS PREMIUM COMPLETOS                      ║
║     Con carrusel, layouts avanzados y máximo contenido              ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# Configuración de los 2 sitios
sitios_config = [
    {
        'nombre': 'Política México Hoy',
        'tagline': 'Análisis Profundo de la Actualidad Nacional',
        'layout_tipo': 'classic',  # Con carrusel arriba, destacados izq, sidebar der
        'usa_sidebar': False,
        'color_index': 0
    },
    {
        'nombre': 'El Observador Político',
        'tagline': 'Información Veraz y Análisis Independiente',
        'layout_tipo': 'magazine',  # Sidebar izquierdo, carrusel destacados
        'usa_sidebar': True,
        'sidebar_pos': 'left',
        'color_index': 5
    }
]

# Inicializar componentes
paraphraser_blackbox = NewsParaphraser()
paraphraser_gemini = GeminiParaphraser()
categorizador = NewsCategorizador()
rss_gen = RSSGenerator()
seo_gen = SEOMetadataGenerator()
section_gen = SectionGenerator()
preloader_gen = PreloaderGenerator()
featured_mgr = FeaturedManager()
components = EnhancedComponents()
adv_layout = AdvancedLayoutGenerator()
legal_gen = LegalPagesGenerator()
color_gen = ColorPaletteGenerator()
global_styles = GlobalStyles()

# ============================================================================
# CARGAR DATOS EXISTENTES
# ============================================================================
print("\n" + "="*70)
print("📂 Cargando datos existentes")
print("="*70)

import glob

# Buscar el archivo más reciente de noticias
json_files = sorted(glob.glob('newsapi_*.json'))
if not json_files:
    print("❌ No hay datos descargados. Ejecuta primero la descarga de noticias.")
    sys.exit(1)

latest_file = json_files[-1]
print(f"Cargando: {latest_file}")

with open(latest_file, 'r', encoding='utf-8') as f:
    todas_noticias = json.load(f)

print(f"✅ {len(todas_noticias)} noticias disponibles")

# Dividir noticias entre los 2 sitios
mitad = len(todas_noticias) // 2
noticias_sitio_1 = todas_noticias[:mitad]
noticias_sitio_2 = todas_noticias[mitad:]

print(f"  Sitio 1: {len(noticias_sitio_1)} noticias")
print(f"  Sitio 2: {len(noticias_sitio_2)} noticias")

start_total = time.time()

# ============================================================================
# GENERAR LOS 2 SITIOS
# ============================================================================

for site_num, (config, noticias_sitio) in enumerate(zip(sitios_config, [noticias_sitio_1, noticias_sitio_2]), 1):
    print("\n" + "="*70)
    print(f"🏗️  GENERANDO SITIO {site_num}/2: {config['nombre']}")
    print("="*70)
    
    site_start = time.time()
    
    # Crear directorio
    site_dir = Path(f'sites/premium_site_{site_num}')
    site_dir.mkdir(parents=True, exist_ok=True)
    (site_dir / 'images').mkdir(exist_ok=True)
    (site_dir / 'categoria').mkdir(exist_ok=True)
    (site_dir / 'assets').mkdir(exist_ok=True)
    
    # Tomar máximo de artículos (limitar para no exceder)
    max_articulos = min(len(noticias_sitio), 50)  # Máximo 50 por sitio
    noticias_sitio = noticias_sitio[:max_articulos]
    
    print(f"📰 Procesando {len(noticias_sitio)} artículos")
    
    # PASO 1: Parafrasear destacados (primeros 5 con Blackbox Pro)
    print(f"\n📝 Parafraseando 5 artículos destacados (Blackbox Pro)...")
    
    destacados = []
    for i, noticia in enumerate(noticias_sitio[:5], 1):
        print(f"  [{i}/5] {noticia.get('title', '')[:50]}...", end=" ", flush=True)
        
        try:
            style = ['formal y objetivo', 'técnico y detallado', 'analítico y crítico'][i % 3]
            resultado = paraphraser_blackbox.paraphrase_article(noticia, style=style)
            resultado['paraphrase_method'] = 'blackbox-pro'
            resultado['author'] = resultado.get('author') or legal_gen.generar_autor_aleatorio()
            destacados.append(resultado)
            print("✅")
        except Exception as e:
            print(f"❌ {e}")
            noticia['paraphrase_method'] = 'original'
            destacados.append(noticia)
    
    # PASO 2: Parafrasear placeholders (resto con Gemini paralelo)
    print(f"\n🚀 Parafraseando {len(noticias_sitio[5:])} placeholders (Gemini)...")
    
    placeholders = paraphraser_gemini.parafrasear_lote_paralelo(
        noticias_sitio[5:],
        max_workers=3,
        delay_between_batches=0.5
    )
    
    # Agregar autores a placeholders
    for p in placeholders:
        if not p.get('author'):
            p['author'] = legal_gen.generar_autor_aleatorio()
    
    # Combinar
    todos_articulos = destacados + placeholders
    
    # PASO 3: Categorizar
    print(f"\n🏷️  Categorizando {len(todos_articulos)} artículos...")
    
    todos_articulos_cat = categorizador.categorizar_lote(
        todos_articulos,
        use_ai=False,
        batch_delay=0
    )
    
    # PASO 4: Marcar destacados
    todos_articulos_cat = featured_mgr.marcar_destacados(todos_articulos_cat)
    todos_articulos_cat = featured_mgr.ordenar_destacados_primero(todos_articulos_cat)
    separated = featured_mgr.separar_destacados_y_placeholders(todos_articulos_cat)
    
    print(f"  ⭐ Destacados: {separated['stats']['total_featured']}")
    print(f"  📄 Placeholders: {separated['stats']['total_placeholders']}")
    
    # PASO 5: Descargar y verificar imágenes
    print(f"\n🖼️  Descargando y verificando imágenes...")
    
    def descargar_imagen_verificada(url: str, output_path: str) -> bool:
        """Descarga y verifica que la imagen sea válida"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=15, stream=True)
            response.raise_for_status()
            
            # Verificar que sea una imagen
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type.lower():
                return False
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            
            # Verificar tamaño mínimo (evitar imágenes rotas)
            if Path(output_path).stat().st_size < 1024:  # Menos de 1KB
                Path(output_path).unlink()
                return False
            
            return True
        except:
            return False
    
    imagenes_ok = 0
    for idx, articulo in enumerate(todos_articulos_cat, 1):
        articulo['_display_index'] = idx  # Agregar índice
        
        image_url = articulo.get('image_url', articulo.get('urlToImage', ''))
        
        if image_url and image_url.startswith('http'):
            output_path = site_dir / 'images' / f'news_{idx}.jpg'
            
            if descargar_imagen_verificada(image_url, str(output_path)):
                articulo['local_image_path'] = f'images/news_{idx}.jpg'
                imagenes_ok += 1
            else:
                articulo['local_image_path'] = None
        else:
            articulo['local_image_path'] = None
    
    print(f"  ✅ {imagenes_ok}/{len(todos_articulos_cat)} imágenes válidas")
    
    # PASO 6: Metadata del sitio
    print(f"\n🏢 Configurando sitio...")
    
    colors = color_gen.obtener_paleta(config['color_index'])
    
    site_metadata = {
        'nombre': config['nombre'],
        'site_name': config['nombre'],
        'tagline': config['tagline'],
        'description': f"{config['tagline']}. Portal de noticias políticas con análisis profundo.",
        'site_url': f'https://{config["nombre"].lower().replace(" ", "")}.com',
        'domain': f'https://{config["nombre"].lower().replace(" ", "")}.com',
        'color_primario': colors['primary'],
        'color_secundario': colors['secondary']
    }
    
    print(f"  Nombre: {config['nombre']}")
    print(f"  Tagline: {config['tagline']}")
    print(f"  Colores: {colors['primary']} / {colors['secondary']}")
    
    # PASO 7: Generar artículos HTML
    print(f"\n📄 Generando {len(todos_articulos_cat)} artículos HTML...")
    
    for idx, articulo in enumerate(todos_articulos_cat, 1):
        # Meta tags SEO
        article_url = f"{site_metadata['site_url']}/article_{idx}.html"
        meta_tags = seo_gen.generar_meta_tags_articulo(articulo, site_metadata, article_url, idx)
        
        # Procesar contenido
        full_text = articulo.get('full_text', '') or articulo.get('content', '') or articulo.get('description', '')
        
        if not full_text or len(full_text) < 50:
            full_text = articulo.get('description', 'Contenido en desarrollo')
        
        # División inteligente de párrafos
        parrafos = [p.strip() for p in full_text.split('\n\n') if p.strip()]
        
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
            
            parrafos = parrafos[:10]
        
        html_parrafos = []
        for i, p in enumerate(parrafos[:12]):
            if i == 0:
                html_parrafos.append(f'<p class="lead">{p}</p>')
            else:
                html_parrafos.append(f'<p>{p}</p>')
        
        contenido_html = '\n            '.join(html_parrafos)
        
        # Badge destacado
        badge_destacado = ''
        if articulo.get('is_featured'):
            badge_destacado = '<span class="featured-badge-article">⭐ Artículo Destacado - Calidad Premium</span>'
        
        # Imagen hero
        image_hero = ''
        if articulo.get('local_image_path'):
            image_hero = f'''
            <div class="article-image-container">
                <img src="{articulo['local_image_path']}" alt="{articulo['title']}" class="article-hero-image">
            </div>'''
        
        # Generar HTML del artículo
        article_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
{meta_tags}
    <title>{articulo['title']} - {site_metadata['nombre']}</title>
{global_styles.get_complete_global_styles()}
    <style>
        body {{ font-family: Georgia, 'Times New Roman', serif; line-height: 1.9; color: #2c3e50; background: #f8f9fa; }}
        .article-header {{ background: linear-gradient(135deg, {site_metadata['color_primario']}, {site_metadata['color_secundario']}); color: white; padding: 3rem 2rem; text-align: center; }}
        .article-header h2 {{ font-size: 2.5rem; margin-bottom: 0.75rem; font-weight: 800; }}
        .article-header p {{ font-size: 1.2rem; opacity: 0.95; }}
        .article-container {{ max-width: 900px; margin: 3rem auto; background: white; padding: 4rem; border-radius: 16px; box-shadow: 0 8px 40px rgba(0,0,0,0.08); }}
        .article-badges {{ margin-bottom: 1.5rem; }}
        .category-badge {{ background: {site_metadata['color_primario']}20; color: {site_metadata['color_primario']}; padding: 0.6rem 1.2rem; border-radius: 24px; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
        .featured-badge-article {{ background: linear-gradient(135deg, #ffd700, #ffed4e); color: #000; padding: 0.6rem 1.2rem; border-radius: 24px; font-size: 0.9rem; font-weight: 800; margin-left: 1rem; box-shadow: 0 2px 10px rgba(255,215,0,0.3); }}
        h1 {{ font-size: 3rem; margin: 1.5rem 0; line-height: 1.3; color: #1a202c; font-weight: 800; }}
        .article-meta {{ color: #718096; margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 3px solid #e2e8f0; font-size: 1rem; display: flex; gap: 1.5rem; flex-wrap: wrap; }}
        .article-image-container {{ margin: 2rem 0; }}
        .article-hero-image {{ width: 100%; height: auto; max-height: 600px; object-fit: cover; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
        article {{ margin: 2rem 0; }}
        p {{ margin-bottom: 1.8rem; line-height: 2; text-align: justify; font-size: 1.1rem; color: #2d3748; }}
        .lead {{ font-size: 1.35rem; font-weight: 500; color: #1a202c; line-height: 1.9; background: #f7fafc; padding: 1.5rem; border-left: 4px solid {site_metadata['color_primario']}; border-radius: 8px; }}
        .share-section {{ margin: 3rem 0; padding: 2rem; background: linear-gradient(135deg, {site_metadata['color_primario']}10, {site_metadata['color_secundario']}10); border-radius: 12px; text-align: center; }}
        .share-title {{ font-size: 1.3rem; font-weight: 700; color: #2c3e50; margin-bottom: 1.5rem; }}
        .share-buttons {{ display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }}
        .share-btn {{ padding: 0.75rem 1.5rem; background: white; color: #2c3e50; border-radius: 8px; font-weight: 600; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: all 0.3s; border: 2px solid transparent; }}
        .share-btn:hover {{ border-color: {site_metadata['color_primario']}; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
        .back-link {{ display: inline-block; margin-top: 3rem; padding: 1rem 2rem; background: {site_metadata['color_primario']}; color: white; border-radius: 8px; font-weight: 600; transition: all 0.3s; }}
        .back-link:hover {{ background: {site_metadata['color_secundario']}; transform: translateY(-2px); }}
        .related-articles {{ margin: 3rem 0; padding: 2rem; background: #f8f9fa; border-radius: 12px; }}
        .related-title {{ font-size: 1.5rem; font-weight: 700; margin-bottom: 1.5rem; color: #2c3e50; }}
    </style>
</head>
<body>
    <header class="article-header">
        <h2>{site_metadata['nombre']}</h2>
        <p>{site_metadata['tagline']}</p>
    </header>
    
    <div class="article-container">
        <div class="article-badges">
            <span class="category-badge">{articulo.get('category_name', 'Noticias')}</span>
            {badge_destacado}
        </div>
        
        <h1>{articulo['title']}</h1>
        
        <div class="article-meta">
            <span>✍️ {articulo.get('author', 'Redacción')}</span>
            <span>📅 {articulo.get('published_at', '')[:10]}</span>
            <span>🏷️ {articulo.get('category_name', 'Noticias')}</span>
            <span>📖 {len(parrafos)} {'párrafo' if len(parrafos) == 1 else 'párrafos'}</span>
        </div>
        
        {image_hero}
        
        <article>
            {contenido_html}
        </article>
        
        <div class="share-section">
            <h3 class="share-title">Compartir este artículo</h3>
            <div class="share-buttons">
                <a href="#" class="share-btn">📘 Facebook</a>
                <a href="#" class="share-btn">🐦 Twitter</a>
                <a href="#" class="share-btn">💼 LinkedIn</a>
                <a href="#" class="share-btn">📱 WhatsApp</a>
                <a href="#" class="share-btn">✉️ Email</a>
            </div>
        </div>
        
        <div style="text-align: center;">
            <a href="index.html" class="back-link">← Volver al Inicio</a>
        </div>
    </div>
</body>
</html>'''
        
        with open(site_dir / f'article_{idx}.html', 'w', encoding='utf-8') as f:
            f.write(article_html)
    
    print(f"  ✅ Artículos generados")
    
    # PASO 8: Generar INDEX con LAYOUT AVANZADO
    print(f"\n🎨 Generando index.html con layout avanzado...")
    
    # Preparar categorías
    categorias_lista = [
        {'id': cat_id, 'nombre': categorizador.CATEGORIAS[cat_id]['nombre']}
        for cat_id in categorizador.CATEGORIAS.keys()
    ]
    
    # Generar con AdvancedLayoutGenerator
    if config['usa_sidebar']:
        # Layout con sidebar collapsible
        sidebar = components.sidebar_iconos_collapsible(
            site_metadata,
            categorias_lista,
            site_metadata,
            config.get('sidebar_pos', 'left')
        )
        
        # Carrusel de destacados
        carousel = adv_layout.generar_carrusel_titulares(todos_articulos_cat, site_metadata)
        
        # Grid
        main_grid = adv_layout.generar_grid_destacados_con_sidebar(
            separated['featured'],
            separated['placeholders'],
            site_metadata
        )
        
        footer = components.footer_completo_profesional(site_metadata, categorias_lista)
        
        content_class = f'content-with-sidebar-{config.get("sidebar_pos", "left")}'
        
        index_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_metadata['nombre']} - {site_metadata['tagline']}</title>
{global_styles.get_complete_global_styles()}
</head>
<body>
{sidebar}
<div class="{content_class}">
{carousel}
{main_grid}
{footer}
</div>
</body>
</html>'''
    
    else:
        # Layout tradicional con header
        header = components.header_completo_horizontal(site_metadata, categorias_lista)
        carousel = adv_layout.generar_carrusel_titulares(todos_articulos_cat, site_metadata)
        main_grid = adv_layout.generar_grid_destacados_con_sidebar(
            separated['featured'],
            separated['placeholders'],
            site_metadata
        )
        footer = components.footer_completo_profesional(site_metadata, categorias_lista)
        
        index_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_metadata['nombre']} - {site_metadata['tagline']}</title>
{global_styles.get_complete_global_styles()}
</head>
<body>
{header}
{carousel}
{main_grid}
{footer}
</body>
</html>'''
    
    # Inyectar preloader
    preloader_tipo = random.choice(['contador', 'progress-circle', 'slide-down'])
    preloader_code = preloader_gen.generar_preloader_completo(
        preloader_tipo,
        site_metadata
    )
    index_html = preloader_gen.inyectar_en_html(index_html, preloader_code)
    
    with open(site_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"  ✅ index.html (layout: {config['layout_tipo']}, preloader: {preloader_tipo})")
    
    # PASO 9: RSS Feeds
    print(f"\n📡 Generando RSS feeds...")
    
    feeds = rss_gen.generar_feeds_por_categoria(
        todos_articulos_cat,
        site_metadata,
        output_dir=str(site_dir)
    )
    
    print(f"  ✅ {len(feeds)} RSS feeds")
    
    # PASO 10: Páginas de categorías
    print(f"\n📑 Generando páginas de categorías...")
    
    grouped = categorizador.agrupar_por_categoria(todos_articulos_cat)
    
    for cat_id, cat_articles in grouped.items():
        if not cat_articles:
            continue
        
        cat_data = categorizador.CATEGORIAS.get(cat_id, {})
        cat_nombre = cat_data.get('nombre', cat_id)
        
        section_gen.generar_pagina_categoria(
            cat_id,
            cat_nombre,
            cat_articles,
            site_metadata,
            site_metadata,
            str(site_dir / 'categoria' / f'{cat_id}.html')
        )
    
    section_gen.generar_index_categorias(
        grouped,
        site_metadata,
        site_metadata,
        str(site_dir / 'categorias.html')
    )
    
    print(f"  ✅ {len(grouped)} categorías")
    
    # PASO 11: Páginas legales
    print(f"\n📄 Generando páginas legales...")
    
    # Términos y Condiciones
    tyc = legal_gen.generar_terminos_condiciones(
        site_metadata['nombre'],
        site_metadata['domain']
    )
    with open(site_dir / 'terminos.html', 'w', encoding='utf-8') as f:
        f.write(tyc)
    
    # Política de Privacidad
    pdp = legal_gen.generar_politica_privacidad(
        site_metadata['nombre'],
        site_metadata['domain']
    )
    with open(site_dir / 'privacidad.html', 'w', encoding='utf-8') as f:
        f.write(pdp)
    
    # Acerca de
    about = legal_gen.generar_acerca_de(
        site_metadata['nombre'],
        site_metadata['tagline'],
        site_metadata['domain']
    )
    with open(site_dir / 'acerca.html', 'w', encoding='utf-8') as f:
        f.write(about)
    
    # Contacto
    contact = legal_gen.generar_contacto(site_metadata['nombre'])
    with open(site_dir / 'contacto.html', 'w', encoding='utf-8') as f:
        f.write(contact)
    
    print(f"  ✅ TyC, PdP, Acerca, Contacto")
    
    # PASO 12: Guardar estadísticas
    stats = {
        'site_number': site_num,
        'site_name': config['nombre'],
        'tagline': config['tagline'],
        'layout_type': config['layout_tipo'],
        'usa_sidebar': config.get('usa_sidebar', False),
        'preloader': preloader_tipo,
        'colores': {'primary': colors['primary'], 'secondary': colors['secondary']},
        'total_articulos': len(todos_articulos_cat),
        'destacados': separated['stats']['total_featured'],
        'placeholders': separated['stats']['total_placeholders'],
        'imagenes_validas': imagenes_ok,
        'rss_feeds': len(feeds),
        'categorias_activas': len(grouped),
        'tiempo_generacion': time.time() - site_start
    }
    
    with open(site_dir / 'site_info.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    elapsed = time.time() - site_start
    
    print(f"\n{'='*70}")
    print(f"✅ SITIO {site_num} COMPLETADO")
    print(f"{'='*70}")
    print(f"  📁 Directorio: {site_dir}")
    print(f"  🌐 Nombre: {config['nombre']}")
    print(f"  🎨 Layout: {config['layout_tipo']}")
    print(f"  📰 Artículos: {len(todos_articulos_cat)} ({separated['stats']['total_featured']} destacados)")
    print(f"  🖼️  Imágenes: {imagenes_ok}/{len(todos_articulos_cat)}")
    print(f"  📡 RSS: {len(feeds)} feeds")
    print(f"  ⏱️  Tiempo: {elapsed/60:.1f} minutos")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
elapsed_total = time.time() - start_total

print("\n" + "="*70)
print("🎉 GENERACIÓN DE 2 SITIOS PREMIUM COMPLETADA")
print("="*70)
print(f"""
⏱️  Tiempo total: {elapsed_total/60:.1f} minutos

📁 Sitios generados:
   • sites/premium_site_1/
   • sites/premium_site_2/

🌐 Para servir:
   Terminal 1: python3 -m http.server 9001 --directory sites/premium_site_1
   Terminal 2: python3 -m http.server 9002 --directory sites/premium_site_2
   
   URLs:
   → http://localhost:9001 (Política México Hoy)
   → http://localhost:9002 (El Observador Político)

📊 Características de cada sitio:
   ✅ Carrusel de titulares animado
   ✅ Grid de destacados con imágenes
   ✅ Sidebar con miniaturas
   ✅ Headers completos con categorías
   ✅ Footers con TyC, PdP, newsletter
   ✅ Términos y Condiciones
   ✅ Política de Privacidad
   ✅ Página Acerca de
   ✅ Página de Contacto
   ✅ Preloader animado
   ✅ RSS feeds completos
   ✅ Meta tags SEO
   ✅ Scrollbars ocultas
   ✅ Imágenes verificadas

🎨 NOMBRES PARA LOGOS:

   SITIO 1: Política México Hoy
   → Logo sugerido: Iniciales "PMH" o escudo mexicano estilizado
   
   SITIO 2: El Observador Político  
   → Logo sugerido: Iniciales "OP" o ojo estilizado (observador)

""")

print("="*70)
print("✨ TODO IMPLEMENTADO CON CARRUSEL Y COMPONENTES COMPLETOS")
print("="*70)
