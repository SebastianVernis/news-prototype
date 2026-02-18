#!/usr/bin/env python3
"""
Generador de Páginas de Secciones por Categoría
Crea páginas HTML para cada categoría de noticias
"""

from typing import Dict, List
from pathlib import Path


class SectionGenerator:
    """Genera páginas de sección por categoría"""
    
    def __init__(self):
        pass
    
    def generar_pagina_categoria(
        self,
        categoria_id: str,
        categoria_nombre: str,
        articles: List[Dict],
        site_metadata: Dict,
        color_palette: Dict,
        output_path: str
    ) -> str:
        """
        Genera página HTML para una categoría
        
        Args:
            categoria_id: ID de la categoría
            categoria_nombre: Nombre de la categoría
            articles: Artículos de esta categoría
            site_metadata: Metadata del sitio
            color_palette: Paleta de colores
            output_path: Path del archivo de salida
            
        Returns:
            Path del archivo generado
        """
        site_name = site_metadata.get('site_name', 'Noticias')
        site_url = site_metadata.get('site_url', 'https://ejemplo.com')
        
        # Colores
        primary_color = color_palette.get('primary', '#667eea')
        secondary_color = color_palette.get('secondary', '#764ba2')
        
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{categoria_nombre} - Noticias y análisis de {site_name}">
    <meta name="keywords" content="{categoria_nombre.lower()}, política méxico, noticias">
    
    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{categoria_nombre} - {site_name}">
    <meta property="og:description" content="Noticias de {categoria_nombre} en {site_name}">
    <meta property="og:url" content="{site_url}/categoria/{categoria_id}.html">
    
    <title>{categoria_nombre} - {site_name}</title>
    <link rel="stylesheet" href="../style.css">
    
    <style>
        /* Estilos específicos de categoría que complementan style.css */
        .header {{
            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .site-name {{
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .breadcrumb {{
            font-size: 0.9rem;
            opacity: 0.9;
        }}
        
        .breadcrumb a {{
            color: white;
            text-decoration: none;
        }}
        
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        
        .category-header {{
            background: white;
            padding: 2rem 1rem;
            margin: 2rem auto;
            max-width: 1200px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .category-title {{
            font-size: 2.5rem;
            color: {primary_color};
            margin-bottom: 0.5rem;
        }}
        
        .category-description {{
            color: #6c757d;
            font-size: 1.1rem;
        }}
        
        .article-count {{
            display: inline-block;
            background: {primary_color};
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-top: 1rem;
        }}
        
        .articles-grid {{
            max-width: 1200px;
            margin: 0 auto 3rem;
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
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            text-decoration: none;
            color: inherit;
            display: block;
        }}
        
        .article-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        
        .article-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
        }}
        
        .article-content {{
            padding: 1.5rem;
        }}
        
        .article-category {{
            display: inline-block;
            background: {primary_color}20;
            color: {primary_color};
            padding: 0.25rem 0.75rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.75rem;
        }}
        
        .article-title {{
            font-size: 1.25rem;
            font-weight: bold;
            margin-bottom: 0.75rem;
            color: #2c3e50;
            line-height: 1.4;
        }}
        
        .article-description {{
            color: #6c757d;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }}
        
        .article-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
            color: #95a5a6;
            padding-top: 1rem;
            border-top: 1px solid #ecf0f1;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 2rem 1rem;
            text-align: center;
            margin-top: 4rem;
        }}
        
        @media (max-width: 768px) {{
            .articles-grid {{
                grid-template-columns: 1fr;
            }}
            
            .category-title {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <div class="site-name">{site_name}</div>
            <div class="breadcrumb">
                <a href="../index.html">Inicio</a> › <span>{categoria_nombre}</span>
            </div>
        </div>
    </header>
    
    <div class="category-header">
        <h1 class="category-title">{categoria_nombre}</h1>
        <p class="category-description">Noticias y análisis político de {categoria_nombre.lower()}</p>
        <span class="article-count">{len(articles)} artículos</span>
    </div>
    
    <div class="articles-grid">
'''
        
        # Agregar artículos
        for idx, article in enumerate(articles, 1):
            title = article.get('title', 'Sin título')
            description = article.get('description', '')[:200]
            image_url = article.get('image_url', article.get('ai_image_path', ''))
            author = article.get('author', 'Redacción')
            published = article.get('published_at', '')[:10]
            
            if not image_url or not image_url.startswith('http'):
                image_url = 'https://via.placeholder.com/400x200/667eea/ffffff?text=Noticia'
            
            html += f'''
        <a href="../article_{idx}.html" class="article-card">
            <img src="{image_url}" alt="{title}" class="article-image" loading="lazy">
            <div class="article-content">
                <span class="article-category">{categoria_nombre}</span>
                <h2 class="article-title">{title[:120]}</h2>
                <p class="article-description">{description}</p>
                <div class="article-meta">
                    <span>👤 {author}</span>
                    <span>📅 {published}</span>
                </div>
            </div>
        </a>
'''
        
        html += '''
    </div>
    
    <footer class="footer">
        <p>&copy; 2026 ''' + site_name + '''. Todos los derechos reservados.</p>
        <p style="margin-top: 0.5rem; font-size: 0.9rem; opacity: 0.8;">
            <a href="../feed_''' + categoria_id + '''.xml" style="color: white;">📡 RSS de esta categoría</a>
        </p>
    </footer>
</body>
</html>'''
        
        # Guardar archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
    
    def generar_index_categorias(
        self,
        categorias_con_articulos: Dict[str, List[Dict]],
        site_metadata: Dict,
        color_palette: Dict,
        output_path: str
    ) -> str:
        """
        Genera página índice con todas las categorías
        
        Args:
            categorias_con_articulos: Dict con categoria_id -> lista de artículos
            site_metadata: Metadata del sitio
            color_palette: Paleta de colores
            output_path: Path del archivo de salida
            
        Returns:
            Path del archivo generado
        """
        from categorizer import NewsCategorizador
        categorizador = NewsCategorizador()
        
        site_name = site_metadata.get('site_name', 'Noticias')
        primary_color = color_palette.get('primary', '#667eea')
        secondary_color = color_palette.get('secondary', '#764ba2')
        
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Categorías - {site_name}</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Estilos específicos del índice de categorías */
        .header {{
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            text-align: center;
            padding: 3rem 1rem;
        }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .categories-grid {{
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 1rem;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
        }}
        .category-card {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            text-decoration: none;
            color: inherit;
            transition: all 0.3s ease;
            border-left: 4px solid {primary_color};
        }}
        .category-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }}
        .category-name {{
            font-size: 1.5rem;
            font-weight: bold;
            color: {primary_color};
            margin-bottom: 0.5rem;
        }}
        .category-desc {{
            color: #6c757d;
            font-size: 0.95rem;
            margin-bottom: 1rem;
        }}
        .category-count {{
            display: inline-block;
            background: {primary_color}20;
            color: {primary_color};
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <header class="header">
        <h1>📑 Categorías de Noticias</h1>
        <p>Explora noticias por tema</p>
    </header>
    
    <div class="categories-grid">
'''
        
        for cat_id, cat_articles in sorted(categorias_con_articulos.items(), key=lambda x: len(x[1]), reverse=True):
            cat_data = categorizador.CATEGORIAS.get(cat_id, {})
            cat_nombre = cat_data.get('nombre', cat_id.replace('-', ' ').title())
            cat_desc = cat_data.get('descripcion', '')
            count = len(cat_articles)
            
            html += f'''
        <a href="categoria/{cat_id}.html" class="category-card">
            <div class="category-name">{cat_nombre}</div>
            <p class="category-desc">{cat_desc}</p>
            <span class="category-count">{count} artículo{"s" if count != 1 else ""}</span>
        </a>
'''
        
        html += '''
    </div>
</body>
</html>'''
        
        # Guardar
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path


def main():
    """Test del generador de secciones"""
    import json
    import glob
    from categorizer import NewsCategorizador
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          📑 GENERADOR DE PÁGINAS POR CATEGORÍA                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Cargar artículos categorizados
    json_files = glob.glob('noticias_categorizadas*.json')
    if not json_files:
        print("❌ No hay artículos categorizados")
        print("💡 Ejecuta: python3 core/scripts/categorizer.py")
        return
    
    with open(sorted(json_files)[-1], 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Agrupar por categoría
    categorizador = NewsCategorizador()
    grouped = categorizador.agrupar_por_categoria(articles)
    
    # Metadata
    site_metadata = {
        'site_name': 'Política México Hoy',
        'site_url': 'https://politica-mexico.com'
    }
    
    color_palette = {
        'primary': '#667eea',
        'secondary': '#764ba2'
    }
    
    # Crear directorio
    import os
    os.makedirs('categoria', exist_ok=True)
    
    # Generar páginas
    generator = SectionGenerator()
    
    print(f"\n{'='*70}")
    print("📄 GENERANDO PÁGINAS DE CATEGORÍAS")
    print(f"{'='*70}\n")
    
    for cat_id, cat_articles in grouped.items():
        cat_data = categorizador.CATEGORIAS.get(cat_id, {})
        cat_nombre = cat_data.get('nombre', cat_id)
        
        output_file = f'categoria/{cat_id}.html'
        generator.generar_pagina_categoria(
            cat_id,
            cat_nombre,
            cat_articles,
            site_metadata,
            color_palette,
            output_file
        )
        
        print(f"  ✅ {cat_nombre}: {output_file} ({len(cat_articles)} artículos)")
    
    # Generar índice
    print(f"\n{'='*70}")
    print("📑 GENERANDO ÍNDICE DE CATEGORÍAS")
    print(f"{'='*70}\n")
    
    index_path = generator.generar_index_categorias(
        grouped,
        site_metadata,
        color_palette,
        'categorias.html'
    )
    
    print(f"  ✅ Índice: {index_path}")
    
    print(f"\n{'='*70}")
    print("✅ GENERACIÓN COMPLETADA")
    print(f"{'='*70}")
    print(f"\n💡 Abre categorias.html en tu navegador para ver el índice")


if __name__ == '__main__':
    main()
