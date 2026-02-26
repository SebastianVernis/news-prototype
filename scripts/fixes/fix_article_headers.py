#!/usr/bin/env python3
"""
Fix article headers to show logo instead of icon
"""

import os
import re

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')

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

SITE_NAMES = {
    'radiocinconoticias': 'Radio Cinco Noticias',
    'centralmexico': 'Central México',
    'tvmexico': 'TV México',
    'cbnnoticias': 'CBN Noticias',
    'mexicoinformado': 'México Informado',
    'nodoinformativo': 'Nodo Informativo',
    'bitacoraurbana': 'Bitácora Urbana',
    'reportecentralmx': 'Reporte Central MX',
    'verticenoticias': 'Vértice Noticias',
    'noticiasobjetivo': 'Noticias Objetivo'
}

for slug, icon in ICON_MAP.items():
    site_dir = os.path.join(SITES_DIR, slug)
    articulo_dir = os.path.join(site_dir, 'articulo')
    
    if not os.path.exists(articulo_dir):
        continue
    
    site_name = SITE_NAMES[slug]
    
    for filename in os.listdir(articulo_dir):
        if not filename.endswith('.html'):
            continue
        
        file_path = os.path.join(articulo_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix logo section in article header
        old_logo = f'''<div class="logo-section">
                <div class="logo-icon">
                    <i class="fas {icon}"></i>
                </div>
                <div>
                    <h1 class="site-title">{site_name}</h1>'''
        
        new_logo = f'''<div class="logo-section">
                <img src="../logo.png" alt="{slug}" class="site-logo" style="height:50px;width:auto;margin-right:15px;object-fit:contain;">
                <div>
                    <h1 class="site-title">{site_name}</h1>'''
        
        if old_logo in content:
            content = content.replace(old_logo, new_logo)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    print(f"✅ {slug}: artículos corregidos")

print("\n✅ Todos los artículos con logo corregido")
