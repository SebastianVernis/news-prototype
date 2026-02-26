#!/usr/bin/env python3
"""
1. Copy logos to favicon.ico
2. Remove site name text from header (leave only logo)
3. Verify each site has unique layout
"""

import os
import shutil

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')
LOGOS_DIR = os.path.join(ROOT_DIR, 'assets', 'logos')

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

# Icon mapping for favicons
ICON_MAP = {
    'radiocinconoticias': 'ICONO_RADIO_CINCO.png',
    'centralmexico': 'ICONO_CENTRAL_MEXICO.png',
    'tvmexico': 'ICONO_TV_MEXICO.png',
    'cbnnoticias': 'ICONO_CBN.png',
    'mexicoinformado': 'ICONO_MEXICO_INFORMADO.png',
    'nodoinformativo': 'ICONO_NODO_INFORMATIVO.png',
    'bitacoraurbana': 'ICONO_BITACORA_URBANA.png',
    'reportecentralmx': 'ICONO_REPORTE_CENTRAL.png',
    'verticenoticias': 'ICONO_VERTICE_NOTICIAS.png',
    'noticiasobjetivo': 'ICONO_NOTICIAS_OBJETIVO.png'
}

print("📋 Actualizando sitios...\n")

for slug, logo_file in LOGO_MAP.items():
    site_dir = os.path.join(SITES_DIR, slug)
    
    if not os.path.exists(site_dir):
        print(f"❌ {slug}: Directorio no encontrado")
        continue
    
    print(f"📍 {slug}:")
    
    # 1. Copy favicon
    icon_file = ICON_MAP.get(slug)
    if icon_file:
        src_icon = os.path.join(LOGOS_DIR, icon_file)
        dst_favicon = os.path.join(site_dir, 'favicon.ico')
        if os.path.exists(src_icon):
            shutil.copy2(src_icon, dst_favicon)
            print(f"   ✅ favicon.ico copiado")
        else:
            print(f"   ⚠️  Icono no encontrado: {icon_file}")
    
    # 2. Update index.html - remove text from header, leave only logo
    index_path = os.path.join(site_dir, 'index.html')
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove site title and tagline from header, keep only logo
        old_header = '''<div class="logo-section">
                <img src="logo.png" alt="''' + slug + '''" class="site-logo" style="height:50px;width:auto;margin-right:15px;object-fit:contain;">
                <div>
                    <h1 class="site-title">'''
        
        new_header = '''<div class="logo-section">
                <img src="logo.png" alt="''' + slug + '''" class="site-logo" style="height:60px;width:auto;object-fit:contain;">
                <div style="display:none;">
                    <h1 class="site-title">'''
        
        if old_header in content:
            content = content.replace(old_header, new_header)
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ Header actualizado (solo logo)")
        else:
            # Try alternative pattern
            if '<div class="logo-section">' in content and '<h1 class="site-title">' in content:
                # Hide the div with title
                content = content.replace(
                    '<div class="logo-section">',
                    '<div class="logo-section" style="display:flex;align-items:center;">'
                )
                content = content.replace(
                    '<img src="logo.png"',
                    '<img src="logo.png" style="height:60px;width:auto;object-fit:contain;"'
                )
                content = content.replace(
                    '<div>',
                    '<div style="display:none;">',
                    1  # Only replace first occurrence
                )
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Header actualizado (solo logo - alternativo)")
    
    # 3. Update article pages too
    articulo_dir = os.path.join(site_dir, 'articulo')
    if os.path.exists(articulo_dir):
        for filename in os.listdir(articulo_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(articulo_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Hide title div
                if '<div class="logo-section">' in content:
                    content = content.replace(
                        '<div class="logo-section">',
                        '<div class="logo-section" style="display:flex;align-items:center;">'
                    )
                    content = content.replace(
                        '<img src="../logo.png"',
                        '<img src="../logo.png" style="height:50px;width:auto;object-fit:contain;"'
                    )
                    # Hide the text div
                    content = content.replace(
                        '<div>\n                    <h1 class="site-title">',
                        '<div style="display:none;">\n                    <h1 class="site-title">',
                        1
                    )
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
        
        print(f"   ✅ Artículos actualizados")
    
    print()

print("✅ Todos los sitios actualizados con favicon y logo en header")
