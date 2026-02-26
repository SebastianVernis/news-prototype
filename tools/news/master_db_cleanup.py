#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import re
import ftfy
import time
from pathlib import Path
from dotenv import load_dotenv

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

load_dotenv()
if os.path.exists(REPO_ROOT / ".dev.vars"):
    load_dotenv(REPO_ROOT / ".dev.vars")

# Category Mapping
CATEGORY_MAP = {
    "NACIONAL": "NACIONAL",
    "Nacional": "NACIONAL",
    "nacional": "NACIONAL",
    "POLITICA": "POLITICA",
    "politica": "POLITICA",
    "Política": "POLITICA",
    "cultura": "CULTURA",
    "Cultura": "CULTURA",
    "deportes": "DEPORTES",
    "Deportes": "DEPORTES",
    "economia": "ECONOMIA",
    "Economia": "ECONOMIA",
    "Economía": "ECONOMIA",
    "internacional": "INTERNACIONAL",
    "Internacional": "INTERNACIONAL",
    "tecnologia": "TECNOLOGIA",
    "Tecnologia": "TECNOLOGIA",
    "Tecnología": "TECNOLOGIA",
}

def run_query(query, json_mode=True):
    cmd = ["wrangler", "d1", "execute", "news_db", "--remote", "--command", query]
    if json_mode: cmd.append("--json")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    if not json_mode:
        return result.stdout
    try:
        data = json.loads(result.stdout)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get('results', [])
        return []
    except: return []

def aggressive_clean(text):
    if not text: return ""
    text = ftfy.fix_text(text)
    text = re.sub(r'Revista Proceso\s*[-–—]\s*Todos los derechos reservados\s*[-–—]\s*202\d', '', text, flags=re.IGNORECASE)
    text = text.replace("Derechos Reservados", "").replace("©", "")
    text = re.sub(r'^[A-ZÁÉÍÓÚÑ\s,\.]+(?:,\s*[A-Za-z\s\.]+,)?\s*\(.*?\)\s*[\.\-—–]*\s*', '', text)
    text = re.sub(r'^[A-ZÁÉÍÓÚÑ\s,\.]+\s*[\-—–]{1,2}\s*', '', text)
    if len(text) > 10:
        prefix = text[:60]
        prefix = re.sub(r'\(apro\)\s*[\.\-—–]*\s*', '', prefix)
        text = prefix + text[60:]
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def cleanup_duplicates():
    print("🔍 Checking for duplicates (Titles & Descriptions on same sites)...")
    # 1. Duplicates by Title on same site
    dupes_title = run_query("SELECT TITULO_PARAFRASEADO, SITIO_DESTINO, COUNT(*) as cnt FROM ARTICULOS_PARAFRASEADOS GROUP BY TITULO_PARAFRASEADO, SITIO_DESTINO HAVING cnt > 1;")
    
    # 2. Duplicates by Description on same site
    dupes_desc = run_query("SELECT DESCRIPCION_PARAFRASEADA, SITIO_DESTINO, COUNT(*) as cnt FROM ARTICULOS_PARAFRASEADOS WHERE DESCRIPCION_PARAFRASEADA != '' GROUP BY DESCRIPCION_PARAFRASEADA, SITIO_DESTINO HAVING cnt > 1;")
    
    deleted = 0
    for d in dupes_title:
        title = d['TITULO_PARAFRASEADO'].replace("'", "''")
        site = d['SITIO_DESTINO']
        entries = run_query(f"SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE TITULO_PARAFRASEADO = '{title}' AND SITIO_DESTINO = '{site}' ORDER BY rowid DESC;")
        if len(entries) > 1:
            to_delete = [e['ID'] for e in entries[1:]]
            ids_str = "','".join(to_delete)
            run_query(f"DELETE FROM ARTICULOS_PARAFRASEADOS WHERE ID IN ('{ids_str}');", json_mode=False)
            deleted += len(to_delete)

    for d in dupes_desc:
        desc = d['DESCRIPCION_PARAFRASEADA'].replace("'", "''")
        site = d['SITIO_DESTINO']
        entries = run_query(f"SELECT ID FROM ARTICULOS_PARAFRASEADOS WHERE DESCRIPCION_PARAFRASEADA = '{desc}' AND SITIO_DESTINO = '{site}' ORDER BY rowid DESC;")
        if len(entries) > 1:
            to_delete = [e['ID'] for e in entries[1:]]
            ids_str = "','".join(to_delete)
            run_query(f"DELETE FROM ARTICULOS_PARAFRASEADOS WHERE ID IN ('{ids_str}');", json_mode=False)
            deleted += len(to_delete)
            
    print(f"✅ Removed {deleted} duplicate articles.")

def clean_all_articles():
    print("🧹 Cleaning articles (titles, content, descriptions, authors, categories)...")
    articles = run_query("SELECT ID, TITULO_PARAFRASEADO, CONTENIDO, DESCRIPCION_PARAFRASEADA, CATEGORIA, SITIO_DESTINO FROM ARTICULOS_PARAFRASEADOS;")
    
    cleaned_count = 0
    for art in articles:
        art_id = art['ID']
        site = art['SITIO_DESTINO'] or "mexicoinformado"
        new_title = aggressive_clean(art['TITULO_PARAFRASEADO'])
        new_content = aggressive_clean(art['CONTENIDO'])
        new_desc = aggressive_clean(art.get('DESCRIPCION_PARAFRASEADA', ''))
        new_author = f"Redacción {site}"
        raw_cat = art.get('CATEGORIA', 'NACIONAL')
        new_cat = CATEGORY_MAP.get(raw_cat, raw_cat.upper())
        
        t_sql = new_title.replace("'", "''")
        c_sql = new_content.replace("'", "''")
        d_sql = new_desc.replace("'", "''")
        
        query = f"UPDATE ARTICULOS_PARAFRASEADOS SET TITULO_PARAFRASEADO = '{t_sql}', CONTENIDO = '{c_sql}', DESCRIPCION_PARAFRASEADA = '{d_sql}', AUTOR = '{new_author}', CATEGORIA = '{new_cat}' WHERE ID = '{art_id}';"
        run_query(query, json_mode=False)
        cleaned_count += 1
        if cleaned_count % 50 == 0:
            print(f"   Processed {cleaned_count} articles...")

    print(f"✨ Successfully cleaned {cleaned_count} articles.")

if __name__ == "__main__":
    cleanup_duplicates()
    clean_all_articles()
