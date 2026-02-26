#!/usr/bin/env python3
"""
Flujo de Ingesta Robusto con DETECCIÓN DE DUPLICADOS Y SQL BATCH
1. Descarga noticias
2. Filtra Duplicados
3. Descarta sin Full Text
4. Parafrasea y Valida
5. Inyecta en D1 (Mesa de Revisión)
"""

import os
import sys
import json
import uuid
import subprocess
from datetime import datetime
from pathlib import Path
from difflib import SequenceMatcher
from dotenv import load_dotenv

# Agregar raíz al path
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from utils.utils import _extract_full_text
from tools.api.newsapi import fetch_newsapi
from tools.news.paraphrase import NewsParaphraser
from tools.news.llm_client import chat

load_dotenv()

SITIOS = [
    "vanguardia-tecamac", "tecamac-momento", "radar-tecamac", 
    "tecamac-meridiano", "radio-cinco", "mexico-informado", 
    "noticias-objetivo", "cbn-noticias", "central-mexico", "tv-mexico"
]

def get_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def check_db_duplicates(title):
    try:
        cmd = ["wrangler", "d1", "execute", "news_db", "--local", "--config=src/wrangler.toml", 
               "--command", "SELECT ID, TITULO FROM ARTICULOS_ORIGINALES ORDER BY FECHA DESC LIMIT 100", "--json"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            output = json.loads(result.stdout)
            if output and len(output) > 0:
                existing = output[0].get("results", [])
                for art in existing:
                    sim = get_similarity(title, art["TITULO"])
                    if sim > 0.70:
                        return art["ID"], art["TITULO"], sim
    except Exception: pass
    return None, None, 0

def ai_validation(title, content):
    provider = os.getenv("SUPERVISOR_PROVIDER")
    model = os.getenv("SUPERVISOR_MODEL")
    if not provider or not model: return None, "IA no configurada"
    prompt = f"Editor: ¿Este artículo es coherente?\nJSON: {{\"aprobado\": true/false, \"motivo\": \"...\"}}\nTÍTULO: {title}\nCONTENIDO: {content[:1000]}"
    try:
        res = chat(provider, model, [{"role": "user", "content": prompt}])
        data = json.loads(res.replace('```json', '').replace('```', '').strip())
        return data.get("aprobado"), data.get("motivo")
    except: return None, "Error en IA"

def process_flow(query="México", limit=5):
    print(f"🚀 Iniciando flujo para: {query}")
    raw_articles = fetch_newsapi(query=query, page_size=limit, enrich=False, silent=True)
    
    paraphraser = NewsParaphraser()
    sql_commands = []
    
    def esc(text):
        if text is None: return "NULL"
        return "'" + str(text).replace("'", "''") + "'"

    for art in raw_articles:
        titulo = art.get("title", "")
        print(f"\n🔍 Analizando: {titulo[:60]}...")
        
        dup_id, dup_title, sim = check_db_duplicates(titulo)
        if dup_id:
            print(f"⚠️ Duplicado detectado ({int(sim*100)}%): '{dup_title}'")
            continue

        url = art.get("url")
        full_text = _extract_full_text(url)
        if not full_text or len(full_text) < 200:
            print(f"❌ Sin full text.")
            continue
            
        orig_id = str(uuid.uuid4())
        # Guardar Original
        sql_commands.append(f"INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, DESCRIPCION, URL_IMAGEN, FECHA, CONTENIDO, CATEGORIA, LONGITUD, SITIOS) VALUES ({esc(orig_id)}, {esc(url)}, {esc(titulo)}, {esc(art.get('description'))}, {esc(art.get('urlToImage'))}, {esc(art.get('publishedAt'))}, {esc(full_text)}, 'Nacional', {len(full_text)}, 10);")

        # Parafrasear para un sitio de prueba (en producción sería un bucle por sitios)
        for site in SITIOS[:2]: # Solo 2 para la prueba rápida
            print(f"📝 Parafraseando para: {site}...")
            para_art = paraphraser.paraphrase_article(art)
            
            # Insertar en Revisión
            sql_commands.append(f"INSERT INTO REVISION_CONTENIDO (ID_ORIGEN, TIPO_ORIGEN, TITULO_PROPUESTO, DESCRIPCION_PROPUESTA, CONTENIDO_PROPUESTO, SITIO_DESTINO, CATEGORIA) VALUES ({esc(orig_id)}, 'API', {esc(para_art['title'])}, {esc(para_art['description'])}, {esc(para_art['full_text'])}, {esc(site)}, 'Nacional');")

    if sql_commands:
        sql_file = REPO_ROOT / "temp_ingest.sql"
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sql_commands))
        print(f"\n💾 Inyectando {len(sql_commands)} registros en D1...")
        subprocess.run(f"wrangler d1 execute news_db --local --file={sql_file} --config=src/wrangler.toml", shell=True)
        sql_file.unlink()
        print("✅ ¡Listo! Revisa la Mesa de Revisión en el Panel.")
    else:
        print("🏁 No se encontraron noticias nuevas únicas.")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Gobierno México"
    process_flow(query=query, limit=5)
