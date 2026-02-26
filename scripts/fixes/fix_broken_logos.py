#!/usr/bin/env python3
"""
Fix broken logo HTML in all sites
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

for slug, icon in ICON_MAP.items():
    index_path = os.path.join(SITES_DIR, slug, 'index.html')
    if not os.path.exists(index_path):
        continue
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix broken logo sections - multiple patterns
    
    # Pattern 1: Remove leftover icon text
    broken_patterns = [
        f'<h1 class="site-title">{icon}"></i></h1>',
        f'<h1 class="site-title">{icon}"></i></div>',
        f'{icon}"></i>',
        f'<h1 class="site-title">{icon}',
    ]
    
    for pattern in broken_patterns:
        content = content.replace(pattern, '')
    
    # Fix logo section completely
    correct_logo = f'''<div class="logo-section">
                <img src="logo.png" alt="{slug}" class="site-logo" style="height:50px;width:auto;margin-right:15px;object-fit:contain;">
                <div>
                    <h1 class="site-title">{slug.replace('-', ' ').replace('_', ' ').title()}</h1>'''
    
    # Find and replace any broken logo-section
    if '<div class="logo-section">' in content:
        # Extract everything from logo-section to the end of site-title
        pattern = r'<div class="logo-section">.*?</h1>'
        content = re.sub(pattern, correct_logo, content, flags=re.DOTALL)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {slug}: logo corregido")

print("\n✅ Todos los logos corregidos")
