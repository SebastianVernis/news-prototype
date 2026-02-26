#!/usr/bin/env python3
"""
Fix article headers - simpler approach
"""

import os
import re

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')

for slug in os.listdir(SITES_DIR):
    site_dir = os.path.join(SITES_DIR, slug)
    articulo_dir = os.path.join(site_dir, 'articulo')
    
    if not os.path.exists(articulo_dir):
        continue
    
    for filename in os.listdir(articulo_dir):
        if not filename.endswith('.html'):
            continue
        
        file_path = os.path.join(articulo_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace logo-icon div with img tag
        # Pattern: <div class="logo-icon"><i class="fas fa-XXX"></i></div>
        pattern = r'<div class="logo-icon"><i class="fas fa-[a-z-]+"></i></div>'
        replacement = '<img src="../logo.png" alt="logo" style="height:50px;width:auto;margin-right:15px;object-fit:contain;">'
        
        content = re.sub(pattern, replacement, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ {slug}: artículos actualizados")

print("\n✅ Todos los artículos con logo")
