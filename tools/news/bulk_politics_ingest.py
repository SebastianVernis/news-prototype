#!/usr/bin/env python3
"""
Ingesta Histórica de Política Mexicana (7-8 días).
- Parafraseo con Gemini 2.0 Flash.
- Limpieza Agresiva (Solo Párrafos).
- Gestión de Imágenes y Slugs.
"""
import os
import sys
import uuid
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.api.newsapi import fetch_newsapi
from utils.utils import _extract_full_text

# Configure Gemini
os.environ["PARAPHRASE_PROVIDER"] = "gemini"
os.environ["PARAPHRASE_MODEL"] = "gemini-2.0-flash"

from tools.news.paraphrase import NewsParaphraser

SITIOS = [
    "noticiasobjetivo", "mexicoinformado", "bitacoraurbana", "nodoinformativo",
    "cbnnoticias", "radiocinconoticias", "centralmexico", "reportecentralmx",
    "tvmexico", "verticenoticias"
]

def slugify(text):
    text = text.lower()
    text = re.sub(r'[áàäâã]', 'a', text)
    text = re.sub(r'[éèëê]', 'e', text)
    text = re.sub(r'[íìïî]', 'i', text)
    text = re.sub(r'[óòöôõ]', 'o', text)
    text = re.sub(r'[úùüû]', 'u', text)
    text = re.sub(r'[ñ]', 'n', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text).strip('-')
    return text[:100]

def clean_content_aggressive(text):
    if not text: return ""
    text = re.sub(r'<h[1-3]>.*?</h[1-3]>', '', text, flags=re.DOTALL | re.I)
    bad_p_patterns = [
        r'<p>.*?twitter\.com.*?</p>',
        r'<p>.*?pic\.\s*twitter.*?</p>',
        r'<p>.*?normas de convivencia.*?</p>',
        r'<p>.*?\[email\s*protected\].*?</p>',
        r'<p>.*?confirmes tu identidad.*?</p>',
        r'<p>.*?vía WhatsApp.*?</p>',
        r'<p>.*?O elegí una de nuestras ilustraciones.*?</p>',
        r'<p>.*?Seguinos en Twitter.*?</p>',
        r'<p>.*?Periodista de.*?Ha publicado en.*?</p>'
    ]
    for pattern in bad_p_patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL | re.I)
    
    # Eliminar cualquier párrafo que sea puramente decorativo o corto con ruido
    text = re.sub(r'<p>\s*[‌\s]*\s*</p>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def run_bulk_ingest():
    is_remote = "--remote" in sys.argv
    target = "--remote" if is_remote else "--local"
    
    today = datetime.now()
    start_date = today - timedelta(days=8)
    start_str = start_date.strftime('%Y-%m-%d')
    
    print(f"🌟 Buscando noticias de POLITICA MÉXICO desde {start_str}...")
    
    raw_news = fetch_newsapi(query="política México", from_date=start_str, page_size=50, enrich=False, silent=True)
    print(f"📥 Se encontraron {len(raw_news)} noticias potenciales.")

    paraphraser = NewsParaphraser()
    sql_commands = []
    processed_count = 0
    
    for i, art in enumerate(raw_news):
        if processed_count >= 30: break
        
        site = SITIOS[processed_count % len(SITIOS)]
        print(f"📝 [{processed_count+1}/30] Procesando para: {site}...")
        
        url = art.get('url')
        img_url = art.get('urlToImage') or '/logo.png'
        full_text = _extract_full_text(url) or art.get('description') or art.get('title')
        art['full_text'] = full_text
        pub_date = art.get('publishedAt', datetime.now().isoformat())
        
        try:
            para_art = paraphraser.paraphrase_article(art)
            clean_body = clean_content_aggressive(para_art['full_text'])
            
            if len(clean_body.split()) < 300:
                print(f"   ⚠️ Saltado por longitud insuficiente ({len(clean_body.split())} palabras).")
                continue

            orig_id = str(uuid.uuid4())
            para_id = str(uuid.uuid4())
            slug = slugify(para_art['title'])
            cat = "POLITICA"
            autor = f"Redacción {site}"
            
            def esc(text):
                return "'" + str(text).replace("'", "''") + "'"

            sql_commands.append(f"INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, FECHA, CONTENIDO, CATEGORIA, LONGITUD, URL_IMAGEN) VALUES ({esc(orig_id)}, {esc(url)}, {esc(art['title'])}, {esc(pub_date)}, {esc(full_text)}, {esc(cat)}, {len(full_text)}, {esc(img_url)});")
            sql_commands.append(f"INSERT INTO ARTICULOS_PARAFRASEADOS (ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, CONTENIDO, SITIO_DESTINO, CATEGORIA, FECHA_PUBLICACION, AUTOR, VERIFICACION, DESTACADO, URL_IMAGEN, SLUG) VALUES ({esc(para_id)}, {esc(orig_id)}, {esc(para_art['title'])}, {esc(para_art['description'])}, {esc(clean_body)}, {esc(site)}, {esc(cat)}, {esc(pub_date)}, {esc(autor)}, 'IA Gemini 2.0', 1, {esc(img_url)}, {esc(slug)});")
            sql_commands.append(f"INSERT INTO METRICAS_CONTENIDO (ID_ARTICULO_PARAFRASEADO, VISTAS) VALUES ({esc(para_id)}, 0);")
            
            processed_count += 1
            time.sleep(2) # Pausa reducida para Gemini 2.0
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            time.sleep(2)

    if sql_commands:
        sql_file = REPO_ROOT / "bulk_politics_final.sql"
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sql_commands))
        
        print(f"🚀 Inyectando {processed_count} noticias en D1 [{target}]...")
        subprocess.run(f"wrangler d1 execute news_db {target} --file={sql_file} --config=src/wrangler.toml --yes", shell=True)
        if sql_file.exists(): sql_file.unlink()
    else:
        print("❌ No hay noticias para inyectar.")

if __name__ == "__main__":
    run_bulk_ingest()
