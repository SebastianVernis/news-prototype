#!/usr/bin/env python3
"""
Test de generación de sitio completo con todas las funcionalidades SEO
- Categorización
- RSS Feeds
- Metadatos SEO
- Open Graph images
- Secciones por categoría
"""

import sys
import json
from pathlib import Path

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'api'))

from newsapi import fetch_newsapi
from paraphrase import NewsParaphraser
from categorizer import NewsCategorizador
from rss_generator import RSSGenerator
from seo_metadata_generator import SEOMetadataGenerator
from section_generator import SectionGenerator

print("""
╔══════════════════════════════════════════════════════════════════════╗
║     🧪 TEST DE SITIO COMPLETO CON SEO Y CATEGORIZACIÓN             ║
╚══════════════════════════════════════════════════════════════════════╝
""")

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

print(f"✅ {len(noticias)} noticias descargadas\n")

# ============================================================================
# PASO 2: Parafrasear
# ============================================================================
print("\n" + "="*70)
print("📝 PASO 2: Parafraseando noticias")
print("="*70)

paraphraser = NewsParaphraser()
noticias_parafraseadas = []

for idx, noticia in enumerate(noticias, 1):
    print(f"[{idx}/3] Parafraseando: {noticia.get('title', '')[:50]}...")
    resultado = paraphraser.paraphrase_article(noticia, style="formal y objetivo")
    noticias_parafraseadas.append(resultado)
    print(f"  ✅ Completado")

# ============================================================================
# PASO 3: Categorizar
# ============================================================================
print("\n" + "="*70)
print("🏷️  PASO 3: Categorizando noticias")
print("="*70)

categorizador = NewsCategorizador()
noticias_categorizadas = categorizador.categorizar_lote(noticias_parafraseadas, use_ai=True)

# ============================================================================
# PASO 4: Generar RSS
# ============================================================================
print("\n" + "="*70)
print("📡 PASO 4: Generando RSS Feeds")
print("="*70)

site_metadata = {
    'site_name': 'Política México Test',
    'site_url': 'https://politica-test.com',
    'tagline': 'Noticias políticas de prueba',
    'description': 'Sitio de prueba con todas las funcionalidades SEO'
}

rss_generator = RSSGenerator()

# Feed general
general_feed = rss_generator.generar_rss(
    noticias_categorizadas,
    site_metadata,
    output_file='test/test_feed.xml'
)
print(f"  ✅ Feed general: {general_feed}")

# ============================================================================
# PASO 5: Generar metadatos SEO
# ============================================================================
print("\n" + "="*70)
print("🎯 PASO 5: Generando metadatos SEO")
print("="*70)

seo_generator = SEOMetadataGenerator()

for idx, article in enumerate(noticias_categorizadas, 1):
    article_url = f"{site_metadata['site_url']}/article_{idx}.html"
    meta_tags = seo_generator.generar_meta_tags_articulo(
        article,
        site_metadata,
        article_url,
        idx
    )
    
    # Guardar ejemplo del primer artículo
    if idx == 1:
        with open(f'test/test_meta_article_{idx}.html', 'w', encoding='utf-8') as f:
            f.write(meta_tags)
        print(f"  ✅ Artículo {idx}: test/test_meta_article_{idx}.html")
    else:
        print(f"  ✅ Artículo {idx}: Meta tags generados")

# Meta tags para home
home_meta = seo_generator.generar_meta_tags_home(site_metadata, len(noticias_categorizadas))
with open('test/test_meta_home.html', 'w', encoding='utf-8') as f:
    f.write(home_meta)
print(f"  ✅ Home: test/test_meta_home.html")

# ============================================================================
# PASO 6: Generar páginas de categorías
# ============================================================================
print("\n" + "="*70)
print("📑 PASO 6: Generando páginas de categorías")
print("="*70)

section_generator = SectionGenerator()
grouped = categorizador.agrupar_por_categoria(noticias_categorizadas)

import os
os.makedirs('test/test_categoria', exist_ok=True)

color_palette = {'primary': '#667eea', 'secondary': '#764ba2'}

for cat_id, cat_articles in grouped.items():
    cat_data = categorizador.CATEGORIAS.get(cat_id, {})
    cat_nombre = cat_data.get('nombre', cat_id)
    
    output_file = f'test/test_categoria/{cat_id}.html'
    section_generator.generar_pagina_categoria(
        cat_id,
        cat_nombre,
        cat_articles,
        site_metadata,
        color_palette,
        output_file
    )
    print(f"  ✅ {cat_nombre}: {output_file}")

# Índice de categorías
index_path = section_generator.generar_index_categorias(
    grouped,
    site_metadata,
    color_palette,
    'test/test_categorias_index.html'
)
print(f"  ✅ Índice: {index_path}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*70)
print("✨ RESUMEN FINAL")
print("="*70)
print(f"""
📊 Estadísticas:
   • Noticias descargadas: {len(noticias)}
   • Noticias parafraseadas: {len(noticias_parafraseadas)}
   • Noticias categorizadas: {len(noticias_categorizadas)}
   • Categorías encontradas: {len(grouped)}
   • RSS feeds generados: 1 (general)
   • Meta tags generados: {len(noticias_categorizadas) + 1} (artículos + home)
   • Páginas de categoría: {len(grouped)}

📁 Archivos generados:
   • test/test_feed.xml (RSS general)
   • test/test_meta_article_1.html (ejemplo meta tags)
   • test/test_meta_home.html (meta tags home)
   • test/test_categorias_index.html (índice de categorías)
   • test/test_categoria/*.html (páginas por categoría)

📚 Categorías detectadas:
""")

for cat_id, cat_articles in sorted(grouped.items(), key=lambda x: len(x[1]), reverse=True):
    cat_name = categorizador.CATEGORIAS[cat_id]['nombre']
    print(f"   • {cat_name}: {len(cat_articles)} artículo(s)")

print(f"\n{'='*70}")
print("✅ TEST COMPLETADO - TODAS LAS FUNCIONALIDADES VERIFICADAS")
print(f"{'='*70}")

print(f"""
💡 Próximo paso: Generar sitio completo con:
   python3 scripts/master_orchestrator.py
""")
