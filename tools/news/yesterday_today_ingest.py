#!/usr/bin/env python3
"""
Ingesta de noticias de AYER y HOY con IA Premium.
- Parafraseo completo con Gemini 1.5 Flash.
- Categorización inteligente por IA.
- Gestión de Imágenes y Slugs.
"""
import os
import sys
import uuid
import json
import re
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
from tools.news.llm_client import chat

SITIOS = [
    "noticiasobjetivo", "mexicoinformado", "bitacoraurbana", "nodoinformativo",
    "cbnnoticias", "radiocinconoticias", "centralmexico", "reportecentralmx",
    "tvmexico", "verticenoticias"
]

CATEGORIAS_VALIDAS = ["NACIONAL", "POLITICA", "ECONOMIA", "DEPORTES", "TECNOLOGIA", "INTERNACIONAL", "CIENCIA", "ENTRETENIMIENTO", "CULTURA"]

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

def get_ai_category(title, content):
    prompt = f"""Clasifica esta noticia en UNA sola de estas categorías: {", ".join(CATEGORIAS_VALIDAS)}.
Responde SOLO con el nombre de la categoría en MAYÚSCULAS.

Título: {title}
Contenido: {content[:500]}..."""
    try:
        cat = chat("gemini", "gemini-1.5-flash", [{"role": "user", "content": prompt}], temperature=0.3).strip().upper()
        if cat in CATEGORIAS_VALIDAS:
            return cat
    except:
        pass
    return "NACIONAL"

def run_ingest():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    
    is_remote = "--remote" in sys.argv
    target = "--remote" if is_remote else "--local"
    
    print(f"🌟 Iniciando Ingesta Premium ({target})...")
    
    # Descargar noticias
    news_yesterday = fetch_newsapi(query="México", from_date=yesterday_str, to_date=yesterday_str, page_size=10, enrich=False, silent=True)
    news_today = fetch_newsapi(query="México", from_date=today_str, to_date=today_str, page_size=10, enrich=False, silent=True)
    all_raw_news = news_yesterday + news_today
    
    if len(all_raw_news) < 20:
        extra = fetch_newsapi(query="México noticias", page_size=20 - len(all_raw_news), enrich=False, silent=True)
        all_raw_news.extend(extra)

    paraphraser = NewsParaphraser()
    sql_commands = []
    
    for i, art in enumerate(all_raw_news):
        site = SITIOS[i % len(SITIOS)]
        print(f"📝 [{i+1}/{len(all_raw_news)}] Procesando para: {site}...")
        
        url = art.get('url')
        img_url = art.get('urlToImage') or ''
        full_text = _extract_full_text(url) or art.get('description') or art.get('title')
        art['full_text'] = full_text
        pub_date = art.get('publishedAt', datetime.now().isoformat())
        
        try:
            # 1. Parafraseo
            para_art = paraphraser.paraphrase_article(art)
            
            # 2. Categoría por IA
            cat = get_ai_category(para_art['title'], para_art['full_text'])
            
            # 3. Datos y IDs
            orig_id = str(uuid.uuid4())
            para_id = str(uuid.uuid4())
            slug = slugify(para_art['title'])
            autor = f"Redacción {site}"
            
            def esc(text):
                return "'" + str(text).replace("'", "''") + "'"

            # SQL Original
            sql_commands.append(f"INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, FECHA, CONTENIDO, CATEGORIA, LONGITUD, URL_IMAGEN) VALUES ({esc(orig_id)}, {esc(url)}, {esc(art['title'])}, {esc(pub_date)}, {esc(full_text)}, {esc(cat)}, {len(full_text)}, {esc(img_url)});")
            
            # SQL Parafraseado (Incluyendo URL_IMAGEN y SLUG)
            sql_commands.append(f"INSERT INTO ARTICULOS_PARAFRASEADOS (ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, CONTENIDO, SITIO_DESTINO, CATEGORIA, FECHA_PUBLICACION, AUTOR, VERIFICACION, DESTACADO, URL_IMAGEN, SLUG) VALUES ({esc(para_id)}, {esc(orig_id)}, {esc(para_art['title'])}, {esc(para_art['description'])}, {esc(para_art['full_text'])}, {esc(site)}, {esc(cat)}, {esc(pub_date)}, {esc(autor)}, 'IA Arcee-AI', 1, {esc(img_url)}, {esc(slug)});")
            
            # Métricas
            sql_commands.append(f"INSERT INTO METRICAS_CONTENIDO (ID_ARTICULO_PARAFRASEADO, VISTAS) VALUES ({esc(para_id)}, 0);")
            
        except Exception as e:
            print(f"❌ Error en {i+1}: {e}")

    if sql_commands:
        sql_file = REPO_ROOT / "premium_ingest.sql"
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sql_commands))
        
        import subprocess
        print(f"🚀 Ejecutando SQL en D1 [{target}]...")
        try:
            subprocess.run(f"wrangler d1 execute news_db {target} --file={sql_file} --config=src/wrangler.toml --yes", shell=True, check=True)
            print(f"✅ ¡Éxito! Noticias con imágenes y categorías inteligentes publicadas.")
        except Exception as e:
            print(f"❌ Error SQL: {e}")
        finally:
            if sql_file.exists(): sql_file.unlink()
    else:
        print("❌ No hay noticias para publicar.")

if __name__ == "__main__":
    run_ingest()
