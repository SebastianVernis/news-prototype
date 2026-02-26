#!/usr/bin/env python3
"""
Fix article thumbnail images in all index.html files
Replace placehold.co URLs with local assets/images/
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
    
    # Find all img tags with placehold.co in card contexts
    # Pattern for news-card images
    patterns_to_fix = [
        # Pattern 1: placehold.co in card-image-wrapper
        (r'<img src="https://placehold\.co/400x250/[^"]*"', r'<img src="assets/images/article_{}.jpg"'),
        # Pattern 2: placehold.co in card-mini
        (r'<img src="https://placehold\.co/150x100/[^"]*"', r'<img src="assets/images/article_{}.jpg"'),
        # Pattern 3: placehold.co in card-hero
        (r'<img src="https://placehold\.co/800x500/[^"]*"', r'<img src="assets/images/article_1.jpg"'),
    ]
    
    # Replace with actual article images
    # We'll assign article_1.jpg through article_6.jpg to the cards
    
    # Fix news cards (usually 6 cards in grid)
    card_count = 0
    def replace_card_image(match):
        global card_count
        card_count += 1
        img_num = ((card_count - 1) % 21) + 1  # Cycle through 1-21
        return f'<img src="assets/images/article_{img_num}.jpg"'
    
    # Replace placehold.co images in news-card contexts
    content = re.sub(
        r'(<div class="card-image-wrapper">[\s\n]*<img) src="https://placehold\.co/[^"]*"',
        replace_card_image,
        content
    )
    
    # Fix mini cards
    mini_count = 0
    def replace_mini_image(match):
        global mini_count
        mini_count += 1
        img_num = (mini_count % 21) + 1
        return f'<img src="assets/images/article_{img_num}.jpg"'
    
    content = re.sub(
        r'(<article class="card-mini"[^>]*>[\s\n]*<img) src="https://placehold\.co/[^"]*"',
        replace_mini_image,
        content
    )
    
    # Fix hero card
    content = re.sub(
        r'(<article class="card-hero"[^>]*>[\s\n]*<img) src="https://placehold\.co/[^"]*"',
        r'\1 src="assets/images/article_1.jpg"',
        content
    )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {slug}: miniaturas actualizadas")

print("\n✅ Todas las miniaturas corregidas")
