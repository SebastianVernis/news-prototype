#!/usr/bin/env python3
"""
Fix article authors to "Redacción {Categoria}"
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
        
        # Find category badge
        category_match = re.search(r'<span class="article-category-badge cat-([a-z]+)">', content)
        if category_match:
            category = category_match.group(1)
            category_name = category.capitalize()
            
            # Special cases
            if category == 'nacional':
                category_name = 'Nacional'
            elif category == 'politica':
                category_name = 'Política'
            elif category == 'economia':
                category_name = 'Economía'
            elif category == 'deportes':
                category_name = 'Deportes'
            elif category == 'cultura':
                category_name = 'Cultura'
            elif category == 'tecnologia':
                category_name = 'Tecnología'
            
            # Replace author
            old_author_pattern = r'<span class="author"><i class="far fa-user"></i> Por [^<]+</span>'
            new_author = f'<span class="author"><i class="far fa-user"></i> Por Redacción {category_name}</span>'
            
            content = re.sub(old_author_pattern, new_author, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ {filename}: Redacción {category_name}")
    
    print(f"✅ {slug}: autores actualizados")

print("\n✅ Todos los autores actualizados a 'Redacción {Categoría}'")
