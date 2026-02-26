#!/usr/bin/env python3
"""
Remove all tags/labels from articles
"""

import os
import re

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../'))
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
        
        # Remove entire article-tags section
        tags_pattern = r'<div class="article-tags">.*?</div>'
        content = re.sub(tags_pattern, '', content, flags=re.DOTALL)
        
        # Remove badge-paraphrased if exists
        badge_pattern = r"<span class='badge-paraphrased'>.*?</span>"
        content = re.sub(badge_pattern, '', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ {slug}: etiquetas eliminadas")

print("\n✅ Todas las etiquetas eliminadas de los artículos")
