#!/usr/bin/env python3
"""
Fix category pages to use local images instead of placehold.co
"""

import os
import re

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')

for slug in os.listdir(SITES_DIR):
    site_dir = os.path.join(SITES_DIR, slug)
    categoria_dir = os.path.join(site_dir, 'categoria')
    
    if not os.path.exists(categoria_dir):
        continue
    
    for filename in os.listdir(categoria_dir):
        if not filename.endswith('.html'):
            continue
        
        file_path = os.path.join(categoria_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placehold.co images with local assets
        # Pattern 1: placehold.co/400x250
        content = re.sub(
            r'img src="https://placehold\.co/400x250/[^"]*"',
            'img src="../assets/images/article_1.jpg"',
            content
        )
        
        # Assign different images to different cards
        img_counter = [0]
        def replace_with_counter(match):
            img_counter[0] += 1
            img_num = ((img_counter[0] - 1) % 21) + 1
            return f'img src="../assets/images/article_{img_num}.jpg"'
        
        content = re.sub(
            r'img src="https://placehold\.co/400x250/[^"]*"',
            replace_with_counter,
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ {filename}: imágenes corregidas")
    
    print(f"✅ {slug}: categorías actualizadas")

print("\n✅ Todas las páginas de categoría con imágenes locales")
