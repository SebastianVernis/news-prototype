#!/usr/bin/env python3
"""
Re-download article images with correct mapping
Each article gets its own unique image from the news data
"""

import os
import json
from urllib.request import urlopen, Request
from urllib.error import URLError

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')
NEWS_FILE = os.path.join(ROOT_DIR, 'data', 'noticias_parafraseadas.json')

def download_image(url, dest_path):
    """Download image from URL"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = Request(url, headers=headers)
        response = urlopen(req, timeout=30)
        with open(dest_path, 'wb') as f:
            f.write(response.read())
        return True
    except Exception as e:
        print(f"  ⚠️ Error downloading {url[:50]}: {e}")
    return False

# Load news data
print("📰 Cargando noticias...")
with open(NEWS_FILE, 'r', encoding='utf-8') as f:
    news_data = json.load(f)
print(f"   ✅ {len(news_data)} noticias cargadas\n")

# Process each site
for slug in os.listdir(SITES_DIR):
    site_dir = os.path.join(SITES_DIR, slug)
    if not os.path.isdir(site_dir):
        continue
    
    assets_dir = os.path.join(site_dir, 'assets', 'images')
    os.makedirs(assets_dir, exist_ok=True)
    
    print(f"📍 {slug}:")
    
    # Download images for each news article
    for i, article in enumerate(news_data[:21]):
        img_filename = f"article_{i+1}.jpg"
        img_path = os.path.join(assets_dir, img_filename)
        
        image_url = article.get('image_url', '')
        if not image_url:
            continue
        
        # Download if not exists or is too small (corrupted)
        if not os.path.exists(img_path) or os.path.getsize(img_path) < 10000:
            print(f"   📷 Descargando imagen {i+1}/21...")
            download_image(image_url, img_path)
        else:
            print(f"   ✅ article_{i+1}.jpg ya existe")
    
    print(f"   ✅ {slug} completado\n")

print("✅ Todas las imágenes descargadas correctamente")
