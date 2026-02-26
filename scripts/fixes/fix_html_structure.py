#!/usr/bin/env python3
"""
Fix broken article tags in index.html files
"""

import os
import re

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')

for slug in os.listdir(SITES_DIR):
    site_dir = os.path.join(SITES_DIR, slug)
    if not os.path.isdir(site_dir):
        continue
    
    index_path = os.path.join(site_dir, 'index.html')
    if not os.path.exists(index_path):
        continue
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix card-mini - add opening tag before img
    content = re.sub(
        r'(<aside class="side-col left">[\s\n]*)(<img src="assets/images/)',
        r'\1<article class="card-mini" data-article="1">\2',
        content
    )
    
    # Add article tags for subsequent mini cards
    content = re.sub(
        r'(</article>[\s\n]*)(<img src="assets/images/article_[2-9]\.jpg")',
        r'\1<article class="card-mini" data-article="2">\2',
        content
    )
    
    # Fix news cards - ensure proper structure
    content = re.sub(
        r'(<article class="news-card">[\s\n]*)(<div class="card-image-wrapper">[\s\n]*)(<img src="assets/images/)',
        r'\1\2\3',
        content
    )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {slug}: estructura HTML corregida")

print("\n✅ Estructura HTML corregida en todos los sitios")
