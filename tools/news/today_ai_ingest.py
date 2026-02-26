#!/usr/bin/env python3
"""
Ingesta Premium: 10 noticias de HOY parafraseadas con IA.
Una noticia destacada para cada sitio.
"""
import os
import sys
import uuid
import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.api.newsapi import fetch_newsapi
from utils.utils import _extract_full_text
from tools.news.paraphrase import NewsParaphraser

SITIOS = [
    "radiocinconoticias", "centralmexico", "tvmexico", "cbnnoticias", 
    "mexicoinformado", "nodoinformativo", "bitacoraurbana", 
    "reportecentralmx", "verticenoticias"
]

def run_today_ingest():
    print(f"🌟 Buscando las 10 noticias más relevantes de hoy...")
    raw_news = fetch_newsapi(query="México hoy", page_size=10, enrich=False, silent=True)
    
    if len(raw_news) < 10:
        raw_news = fetch_newsapi(query="Actualidad", page_size=10, enrich=False, silent=True)[:10]

    paraphraser = NewsParaphraser()
    sql_commands = []
    now_iso = datetime.now().isoformat()

    for i, art in enumerate(raw_news):
        site = SITIOS[i % len(SITIOS)]
        print(f"📝 [{i+1}/10] Parafraseando para: {site}...")
        
        url = art.get('url')
        full_text = _extract_full_text(url) or art.get('description') or art.get('title')
        art['full_text'] = full_text
        
        try:
            para_art = paraphraser.paraphrase_article(art)
            orig_id = str(uuid.uuid4())
            para_id = str(uuid.uuid4())
            cat = "Nacional"
            autor = f"Redacción {site} {cat}"
            
            def esc(text):
                return "'" + str(text).replace("'", "''") + "'"

            sql_commands.append(f"INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, FECHA, CONTENIDO, CATEGORIA, LONGITUD) VALUES ({esc(orig_id)}, {esc(url)}, {esc(art['title'])}, {esc(now_iso)}, {esc(full_text)}, {esc(cat)}, {len(full_text)});")
            sql_commands.append(f"INSERT INTO ARTICULOS_PARAFRASEADOS (ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, CONTENIDO, SITIO_DESTINO, CATEGORIA, FECHA_PUBLICACION, AUTOR, VERIFICACION, DESTACADO) VALUES ({esc(para_id)}, {esc(orig_id)}, {esc(para_art['title'])}, {esc(para_art['description'])}, {esc(para_art['full_text'])}, {esc(site)}, {esc(cat)}, {esc(now_iso)}, {esc(autor)}, 'IA Arcee-AI', 1);")
            sql_commands.append(f"INSERT INTO METRICAS_CONTENIDO (ID_ARTICULO_PARAFRASEADO, VISTAS) VALUES ({esc(para_id)}, 0);")
        except Exception as e:
            print(f"❌ Error: {e}")

    if sql_commands:
        sql_file = REPO_ROOT / "today_premium.sql"
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sql_commands))
        import subprocess
        try:
            subprocess.run(f"wrangler d1 execute news_db --local --file={sql_file} --config=src/wrangler.toml", shell=True, check=True)
            print(f"✅ ¡Éxito! 10 noticias de hoy publicadas.")
        finally:
            if sql_file.exists(): sql_file.unlink()

if __name__ == "__main__":
    run_today_ingest()
