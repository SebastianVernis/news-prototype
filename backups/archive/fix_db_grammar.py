#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

# Add repo root to sys.path for imports
REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))

# Load Environment Variables
load_dotenv()
if os.path.exists(REPO_ROOT / ".dev.vars"):
    load_dotenv(REPO_ROOT / ".dev.vars")

# Import LLM client
from tools.news.llm_client import chat

# Configuration
PARAPHRASE_PROVIDER = "openrouter"
PARAPHRASE_MODEL = "google/gemini-2.0-flash-001"

def proofread_text(text, role="contenido"):
    if not text or len(text) < 10:
        return text
    
    prompt = f"""
    Actúa como un corrector de estilo profesional para un periódico de prestigio.
    Tu tarea es corregir errores de ORTOGRAFÍA, PUNTUACIÓN y GRAMÁTICA en el siguiente {role} en español.
    
    REGLAS ESTRICTAS:
    1. NO cambies el estilo, el tono o el significado original.
    2. NO resumas, NO acortes y NO trunques el texto. Debe tener la misma longitud aproximada.
    3. Mantén el formato original (párrafos).
    4. Si el texto ya es correcto, devuélvelo exactamente igual.
    5. NO añadidas comentarios, notas o introducciones. Devuelve SOLO el texto corregido.
    
    TEXTO A CORREGIR:
    {text}
    """
    
    try:
        messages = [{"role": "user", "content": prompt}]
        corrected = chat(PARAPHRASE_PROVIDER, PARAPHRASE_MODEL, messages, temperature=0.1)
        return corrected.strip()
    except Exception as e:
        print(f"⚠️ Error en IA: {e}")
        return text

def run_query(query):
    cmd = ["wrangler", "d1", "execute", "news_db", "--remote", "--command", query, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing query: {result.stderr}")
        return []
    try:
        data = json.loads(result.stdout)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get('results', [])
        return []
    except:
        return []

def update_article(table, art_id, title, content):
    title_sql = title.replace("'", "''")
    content_sql = content.replace("'", "''")
    
    title_col = "TITULO_PARAFRASEADO" if table == "ARTICULOS_PARAFRASEADOS" else "TITULO"
    if table == "REVISION_CONTENIDO": title_col = "TITULO_PROPUESTO"
    
    content_col = "CONTENIDO"
    if table == "REVISION_CONTENIDO": content_col = "CONTENIDO_PROPUESTO"

    query = f"UPDATE {table} SET {title_col} = '{title_sql}', {content_col} = '{content_sql}' WHERE ID = '{art_id}';"
    
    cmd = ["wrangler", "d1", "execute", "news_db", "--remote", "--command", query]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def process_table(table, limit=10):
    print(f"\n--- Corrigiendo ortografía y gramática en: {table} (Límite: {limit}) ---")
    
    title_col = "TITULO_PARAFRASEADO" if table == "ARTICULOS_PARAFRASEADOS" else "TITULO"
    if table == "REVISION_CONTENIDO": title_col = "TITULO_PROPUESTO"
    
    content_col = "CONTENIDO"
    if table == "REVISION_CONTENIDO": content_col = "CONTENIDO_PROPUESTO"

    articles = run_query(f"SELECT ID, {title_col}, {content_col} FROM {table} ORDER BY rowid DESC LIMIT {limit} OFFSET 10;")
    
    for art in articles:
        art_id = art['ID']
        title = art.get(title_col, "")
        content = art.get(content_col, "")
        
        print(f"📖 Procesando: {title[:50]}...")
        
        # Corregir Título
        fixed_title = proofread_text(title, "título")
        # Corregir Contenido
        fixed_content = proofread_text(content, "contenido")
        
        if fixed_title != title or fixed_content != content:
            print(f"✅ Cambios detectados, actualizando DB...")
            update_article(table, art_id, fixed_title, fixed_content)
            time.sleep(1) # Pequeña pausa entre actualizaciones
        else:
            print(f"✨ Ya estaba correcto.")

if __name__ == "__main__":
    # Procesar los 10 más recientes de la tabla principal
    process_table("ARTICULOS_PARAFRASEADOS", limit=10)
