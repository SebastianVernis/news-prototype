#!/usr/bin/env python3
"""
Fix image paths in all sites:
- Add logos to index.html headers
- Copy article images to assets folder
- Update article HTML to use local images
"""

import os
import re
import shutil
import json
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from urllib.error import URLError

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')
LOGOS_DIR = os.path.join(ROOT_DIR, 'assets', 'logos')
NEWS_FILE = os.path.join(ROOT_DIR, 'data', 'noticias_parafraseadas.json')

# Logo mapping
LOGO_MAP = {
    'radiocinconoticias': 'LOGO_RADIO_CINCO.png',
    'centralmexico': 'LOGO_CENTRAL_MEXICO.png',
    'tvmexico': 'LOGO_TV_MEXICO.png',
    'cbnnoticias': 'LOGO_CBN.png',
    'mexicoinformado': 'LOGO_MEXICO_INFORMADO.png',
    'nodoinformativo': 'LOGO_NODO_INFORMATIVO.png',
    'bitacoraurbana': 'LOGO_BITACORA_URBANA.png',
    'reportecentralmx': 'LOGO_REPORTE_CENTRAL.png',
    'verticenoticias': 'LOGO_VERTICE_NOTICIAS.png',
    'noticiasobjetivo': 'LOGO_NOTICIAS_OBJETIVO.png'
}

# Icon mapping
ICON_MAP = {
    'radiocinconoticias': 'fa-broadcast-tower',
    'centralmexico': 'fa-newspaper',
    'tvmexico': 'fa-tv',
    'cbnnoticias': 'fa-globe',
    'mexicoinformado': 'fa-check-circle',
    'nodoinformativo': 'fa-network-wired',
    'bitacoraurbana': 'fa-city',
    'reportecentralmx': 'fa-file-alt',
    'verticenoticias': 'fa-crosshairs',
    'noticiasobjetivo': 'fa-bullseye'
}

def load_news():
    """Load news data"""
    with open(NEWS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def download_image(url, dest_path):
    """Download image from URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = Request(url, headers=headers)
        response = urlopen(req, timeout=30)
        with open(dest_path, 'wb') as f:
            f.write(response.read())
        return True
    except Exception as e:
        print(f"      ⚠️  Error downloading {url}: {e}")
    return False

def fix_index_html(site_slug, site_dir):
    """Fix index.html to show logo image"""
    index_path = os.path.join(site_dir, 'index.html')
    if not os.path.exists(index_path):
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace logo icon with logo image
    old_logo_section = '''<div class="logo-section">
                <div class="logo-icon"><i class="fas '''
    
    icon_class = ICON_MAP.get(site_slug, 'fa-newspaper')
    new_logo_section = f'''<div class="logo-section">
                <img src="logo.png" alt="{site_slug}" class="site-logo" style="height:50px;width:auto;margin-right:15px;">
                <div>
                    <h1 class="site-title">'''
    
    # Check if already has image logo
    if '<img src="logo.png"' not in content:
        content = content.replace(old_logo_section, new_logo_section)
        
        # Also need to close the div properly
        content = content.replace(
            '''<div class="logo-section">
                <img src="logo.png" alt="''' + site_slug + '''" class="site-logo" style="height:50px;width:auto;margin-right:15px;">
                <div>
                    <h1 class="site-title">''',
            '''<div class="logo-section">
                <img src="logo.png" alt="''' + site_slug + '''" class="site-logo" style="height:50px;width:auto;margin-right:15px;">
                <div>
                    <h1 class="site-title">'''
        )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ index.html actualizado")

def fix_article_images(site_slug, site_dir, news_data):
    """Fix article images - download and update HTML"""
    articulo_dir = os.path.join(site_dir, 'articulo')
    assets_images_dir = os.path.join(site_dir, 'assets', 'images')
    
    os.makedirs(assets_images_dir, exist_ok=True)
    
    # Process each article file
    for i, article in enumerate(news_data[:21]):
        # Get image URL
        image_url = article.get('image_url', '')
        if not image_url:
            continue
        
        # Generate image filename
        img_filename = f"article_{i+1}.jpg"
        img_path = os.path.join(assets_images_dir, img_filename)
        img_relative_path = f"../assets/images/{img_filename}"
        
        # Download image if not exists
        if not os.path.exists(img_path):
            print(f"      📷 Descargando imagen {i+1}/21...")
            download_image(image_url, img_path)
        
        # Update article HTML files
        for filename in os.listdir(articulo_dir):
            if not filename.endswith('.html'):
                continue
            
            file_path = os.path.join(articulo_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if this article matches
            article_title = article.get('title', '')[:50]
            if article_title.lower() in content.lower() or f'article_{i+1}' in filename.lower():
                # Replace image src
                if image_url in content:
                    content = content.replace(image_url, img_relative_path)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"      ✅ {filename} actualizado")
                break

def fix_admin_logo(site_slug, site_dir):
    """Fix admin panel logo"""
    admin_dir = os.path.join(site_dir, 'admin')
    
    for filename in ['index.html', 'login.html']:
        file_path = os.path.join(admin_dir, filename)
        if not os.path.exists(file_path):
            continue
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add logo image after sidebar-header opens
        if '<img src="../logo.png"' not in content:
            content = content.replace(
                '<div class="sidebar-header">',
                '<div class="sidebar-header">\n                <img src="../logo.png" alt="Logo" style="height:40px;width:auto;margin-right:10px;">'
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ admin/{filename} actualizado")

def add_css_for_logo(site_dir):
    """Add CSS for logo styling"""
    style_path = os.path.join(site_dir, 'style.css')
    if not os.path.exists(style_path):
        return
    
    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add logo styling if not exists
    if '.site-logo' not in content:
        # Find :root and add after it
        if '.logo-section' in content:
            content = content.replace(
                '.logo-section {',
                '.site-logo { height: 50px; width: auto; object-fit: contain; }\n.logo-section {'
            )
        else:
            # Add to end of file
            content += '\n\n.site-logo { height: 50px; width: auto; object-fit: contain; }\n'
        
        with open(style_path, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    print("🔧 Corrigiendo rutas de imágenes...\n")
    
    # Load news data
    print("📰 Cargando datos de noticias...")
    news_data = load_news()
    print(f"   ✅ {len(news_data)} noticias cargadas\n")
    
    # Process each site
    for slug in LOGO_MAP.keys():
        site_dir = os.path.join(SITES_DIR, slug)
        if not os.path.exists(site_dir):
            print(f"⚠️  Sitio no encontrado: {slug}")
            continue
        
        print(f"\n{'='*50}")
        print(f"📍 {slug}")
        print(f"{'='*50}")
        
        # 1. Fix index.html logo
        print("   🖼️  Actualizando logo en index.html...")
        fix_index_html(slug, site_dir)
        
        # 2. Add CSS for logo
        print("   🎨 Agregando CSS para logo...")
        add_css_for_logo(site_dir)
        
        # 3. Fix admin panel logo
        print("   🔧 Actualizando admin panel...")
        fix_admin_logo(slug, site_dir)
        
        # 4. Download and fix article images
        print("   📷 Procesando imágenes de artículos...")
        fix_article_images(slug, site_dir, news_data)
        
        print(f"   ✅ {slug} completado")
    
    print(f"\n{'='*50}")
    print("✅ ¡Imágenes corregidas exitosamente!")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
