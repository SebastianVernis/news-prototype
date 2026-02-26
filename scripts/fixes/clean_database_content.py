#!/usr/bin/env python3
import os
import re
import subprocess
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WRANGLER_CONFIG = REPO_ROOT / "src" / "wrangler.toml"

def clean_text(text):
    if not text: return ""
    # 1. Eliminar bloques HTML estructurales
    text = re.sub(r'<(header|h1|figure|aside|img|figcaption|footer|nav)[^>]*>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<(header|h1|figure|aside|img|figcaption|footer|nav)[^>]*>', '', text, flags=re.IGNORECASE)
    
    # 2. Eliminar frases de marcas de agua, links y autores específicos
    bad_patterns = [
        r'¿Quién era.*?en este artículo',
        r'Todo sobre.*?MINUTO A MINUTO',
        r'Lee también:.*',
        r'Sigue leyendo:.*',
        r'También te puede interesar:.*',
        r'Foto:.*',
        r'Imagen:.*',
        r'Créditos:.*',
        r'Redacción /.*',
        r'Suscríbete a nuestro.*?$',
        r'Síguenos en.*?$',
        r'Este artículo ha sido optimizado para el sitio .*?\.',
        r'Contenido detallado parafraseado por IA .*?\.',
    ]
    for p in bad_patterns:
        text = re.sub(p, '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # 3. Eliminar firmas de autor al inicio o final
    text = re.sub(r'^Por\s+.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\nPor\s+.*$', '', text, flags=re.IGNORECASE)
    
    # 4. Normalizar espacios
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_json(text):
    match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
    if match:
        return match.group(0)
    return None

def process_database(remote=False):
    target = "--remote" if remote else "--local"
    print(f"🧹 Limpieza incremental D1 ({target})...")
    
    # Obtener IDs primero
    cmd_ids = f"wrangler d1 execute news_db {target} --command=\"SELECT ID FROM ARTICULOS_PARAFRASEADOS;\" --config={WRANGLER_CONFIG} --format=json"
    res = subprocess.run(cmd_ids, shell=True, capture_output=True, text=True)
    json_str = extract_json(res.stdout)
    
    if not json_str:
        print("❌ No se pudo extraer JSON de IDs.")
        return
        
    data = json.loads(json_str)
    # Wrangler envuelve en un array de un objeto con 'results'
    results = data[0]['results'] if 'results' in data[0] else data
    ids = [r['ID'] for r in results if 'ID' in r]
    
    print(f"✅ Encontrados {len(ids)} artículos. Procesando...")
    
    chunk_size = 25
    for i in range(0, len(ids), chunk_size):
        chunk_ids = ids[i:i+chunk_size]
        ids_str = ",".join([f"'{id_val}'" for id_val in chunk_ids])
        
        cmd_chunk = f"wrangler d1 execute news_db {target} --command=\"SELECT ID, CONTENIDO FROM ARTICULOS_PARAFRASEADOS WHERE ID IN ({ids_str});\" --config={WRANGLER_CONFIG} --format=json"
        res_chunk = subprocess.run(cmd_chunk, shell=True, capture_output=True, text=True)
        json_chunk_str = extract_json(res_chunk.stdout)
        
        if not json_chunk_str: continue
        
        chunk_data = json.loads(json_chunk_str)
        articles = chunk_data[0]['results'] if 'results' in chunk_data[0] else chunk_data
        
        updates = []
        for art in articles:
            original = art.get('CONTENIDO', '')
            if not original: continue
            clean = clean_text(original)
            if clean != original:
                safe_content = clean.replace("'", "''")
                art_id = art['ID']
                updates.append(f"UPDATE ARTICULOS_PARAFRASEADOS SET CONTENIDO = '{safe_content}' WHERE ID = '{art_id}';")
        
        if updates:
            with open("tmp_clean.sql", "w") as f: f.write("\n".join(updates))
            subprocess.run(f"wrangler d1 execute news_db {target} --file=tmp_clean.sql --config={WRANGLER_CONFIG} --yes", shell=True)
            print(f"   ✨ Bloque {i//chunk_size + 1} procesado ({len(updates)} cambios)")

    if os.path.exists("tmp_clean.sql"): os.remove("tmp_clean.sql")
    print("🎉 ¡Limpieza completa!")

if __name__ == "__main__":
    process_database("--remote" in sys.argv)
