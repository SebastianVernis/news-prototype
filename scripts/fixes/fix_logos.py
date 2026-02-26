#!/usr/bin/env python3
"""
Fix logos in all index.html files
"""

import os

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
        print(f"❌ {slug}: index.html no encontrado")
        continue
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the logo section
    old_logo = f'''<div class="logo-section">
                <div class="logo-icon">
                    <i class="fas {icon}"></i>
                </div>
                <div>'''
    
    new_logo = f'''<div class="logo-section">
                <img src="logo.png" alt="{slug}" class="site-logo" style="height:50px;width:auto;margin-right:15px;object-fit:contain;">
                <div>'''
    
    if old_logo in content:
        content = content.replace(old_logo, new_logo)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {slug}: logo actualizado")
    else:
        # Try alternative pattern
        if '<img src="logo.png"' not in content:
            # Find and replace simpler pattern
            old_simple = f'<div class="logo-icon"><i class="fas {icon}"></i></div>'
            new_simple = '<img src="logo.png" alt="' + slug + '" class="site-logo" style="height:50px;width:auto;margin-right:15px;object-fit:contain;">'
            
            if old_simple in content:
                content = content.replace(old_simple, new_simple)
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {slug}: logo actualizado (patrón simple)")
            else:
                print(f"⚠️  {slug}: no se encontró el patrón del logo")
        else:
            print(f"✅ {slug}: ya tiene logo")

print("\n✅ Logos corregidos en todos los index.html")
