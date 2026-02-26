#!/usr/bin/env python3
"""
Fix site titles in all index.html files
"""

import os

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')

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

for slug, name in SITE_NAMES.items():
    index_path = os.path.join(SITES_DIR, slug, 'index.html')
    if not os.path.exists(index_path):
        continue
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix title in logo section
    old_title = f'<h1 class="site-title">{slug.replace("-", " ").title()}</h1>'
    new_title = f'<h1 class="site-title">{name}</h1>'
    
    if old_title in content:
        content = content.replace(old_title, new_title)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {slug}: título corregido a '{name}'")
    else:
        # Try alternative - any site-title that has the slug
        import re
        pattern = r'<h1 class="site-title">[^<]+</h1>'
        replacement = f'<h1 class="site-title">{name}</h1>'
        content = re.sub(pattern, replacement, content, count=1)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {slug}: título corregido (regex)")

print("\n✅ Todos los títulos corregidos")
