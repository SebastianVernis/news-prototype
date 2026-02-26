#!/usr/bin/env python3
"""
RSS Ingest Premium: Fetch 10 news items via RSS, paraphrase with Gemini 2.0 Flash,
upload images to R2, and publish to the news network.
Optimized for rate limits and mandatory images.
"""
import os
import sys
import uuid
import json
import time
import requests
import feedparser
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

# Load Environment Variables
load_dotenv()
if os.path.exists(REPO_ROOT / ".dev.vars"):
    load_dotenv(REPO_ROOT / ".dev.vars")

# Configure OpenRouter for Paraphrasing
os.environ["PARAPHRASE_PROVIDER"] = "openrouter"
os.environ["PARAPHRASE_MODEL"] = "arcee-ai/trinity-large-preview:free"

# Import local tools
from tools.news.paraphrase import NewsParaphraser
from utils.utils import _extract_full_text

# Configuration
RSS_FEEDS = [
    "https://elpais.com/rss/mexico/portada.xml",
    "https://www.proceso.com.mx/rss/feed.html?id=12",
    "https://aristeguinoticias.com/feed/",
    "https://www.animalpolitico.com/feed/",
]

SITIOS = [
    "radiocinconoticias", "centralmexico", "tvmexico", "cbnnoticias", 
    "mexicoinformado", "nodoinformativo", "bitacoraurbana", 
    "reportecentralmx", "verticenoticias", "noticiasobjetivo"
]

# API Configuration
API_BASE_URL = "https://cms-api.sebastianvernis.space/api"
API_TOKEN = os.getenv("ADMIN_TOKEN", "passwordtemporal") 

def get_image_from_url(url):
    """Scrapes the og:image from the article URL if not in RSS"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            og_image = soup.find('meta', property='og:image')
            if og_image: return og_image.get('content')
            twitter_image = soup.find('meta', name='twitter:image')
            if twitter_image: return twitter_image.get('content')
    except: pass
    return None

def upload_image_to_r2(image_url):
    """Downloads an image and uploads it to our R2 via the API"""
    if not image_url or not image_url.startswith("http"):
        return None
    
    try:
        headers_img = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        img_res = requests.get(image_url, headers=headers_img, timeout=15)
        if img_res.status_code != 200: return None
        
        content_type = img_res.headers.get('Content-Type', 'image/jpeg')
        ext = ".jpg"
        if "png" in content_type: ext = ".png"
        elif "webp" in content_type: ext = ".webp"
        
        filename = f"rss_import_{uuid.uuid4()}{ext}"
        files = {'file': (filename, img_res.content, content_type)}
        headers = {'Authorization': f'Bearer {API_TOKEN}'}
        
        upload_res = requests.post(f"{API_BASE_URL}/upload", files=files, headers=headers, timeout=30)
        if upload_res.status_code == 200:
            return upload_res.json().get('url')
        return None
    except Exception as e:
        print(f"⚠️ Image upload error: {e}")
        return None

def clean_title(title):
    """Removes 'Name: ' prefixes from titles"""
    if ":" in title:
        parts = title.split(":", 1)
        if len(parts[0]) < 30:
            return parts[1].strip()
    return title.strip()

def run_rss_ingest():
    print(f"🚀 Starting RSS Ingest Premium (via OpenRouter) ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    
    paraphraser = NewsParaphraser()
    target_count = 10
    
    all_entries = []
    for feed_url in RSS_FEEDS:
        print(f"📡 Fetching feed: {feed_url}")
        try:
            feed = feedparser.parse(feed_url)
            all_entries.extend(feed.entries)
        except Exception as e:
            print(f"⚠️ Error fetching {feed_url}: {e}")
    
    all_entries.sort(key=lambda x: getattr(x, 'published_parsed', time.gmtime(0)), reverse=True)
    
    published_count = 0
    
    for entry in all_entries:
        if published_count >= target_count:
            break
            
        title = entry.get('title', '')
        url = entry.get('link', '')
        summary = entry.get('summary', '')
        
        # Enhanced Image Detection
        image_url = None
        if 'media_content' in entry and len(entry.media_content) > 0:
            image_url = entry.media_content[0].get('url')
        if not image_url:
            image_url = get_image_from_url(url)

        if not image_url: continue

        print(f"\n--- Article {published_count + 1}/{target_count} ---")
        print(f"📰 Original: {title}")
        
        # Extract full text
        full_text = _extract_full_text(url) or summary or title
        raw_art = {
            'title': title,
            'url': url,
            'description': summary,
            'full_text': full_text,
            'image_url': image_url
        }
        
        # --- Paraphrasing ---
        para_art = None
        try:
            if published_count > 0:
                print("⏳ Waiting 5s...")
                time.sleep(5)
            
            print(f"✨ Paraphrasing with OpenRouter ({os.getenv('PARAPHRASE_MODEL')})...")
            para_art = paraphraser.paraphrase_article(raw_art)
        except Exception as e:
            print(f"⚠️ AI Failure: {e}")
        
        if not para_art:
            print("❌ Skipping article due to AI failure.")
            continue
            
        try:
            clean_t = clean_title(para_art.get('title', title))
            if clean_t and clean_t[0].islower():
                clean_t = clean_t[0].upper() + clean_t[1:]
            
            print(f"🖼️  Uploading image...")
            final_image_url = upload_image_to_r2(image_url)
            
            if not final_image_url:
                print("⚠️  Image upload failed.")
                continue
            
            site = SITIOS[published_count % len(SITIOS)]
            payload = {
                "title": clean_t,
                "content": para_art.get('content', ''),
                "excerpt": para_art.get('excerpt', ''),
                "category": para_art.get('category', 'NACIONAL').upper(),
                "imageUrl": final_image_url,
                "site": site,
                "sites": [site],
                "featured": 1,
                "author": f"Redacción {site}"
            }
            
            print(f"📤 Publishing to {site}...")
            headers = {
                'Authorization': f'Bearer {API_TOKEN}',
                'Content-Type': 'application/json'
            }
            pub_res = requests.post(f"{API_BASE_URL}/articles", json=payload, headers=headers, timeout=30)
            
            if pub_res.status_code == 200:
                print(f"✅ Success: {clean_t}")
                published_count += 1
            else:
                print(f"❌ API Error: {pub_res.text}")
                
        except Exception as e:
            print(f"❌ Error in publication: {e}")
            continue

    print(f"\n✨ Ingest completed. {published_count}/{target_count} articles published.")

if __name__ == "__main__":
    run_rss_ingest()
