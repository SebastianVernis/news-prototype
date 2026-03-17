#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import ftfy
from pathlib import Path

# Common mojibake replacements that ftfy might miss or that are very specific
MANUAL_FIXES = {
    "MĂ‰XICO": "MÉXICO",
    "M├®xico": "México",
    "M├ēXICO": "MÉXICO",
    "FiscalГӯa": "Fiscalía",
    "RepГәblica": "República",
    "investigaciĂłn": "investigación",
    "investigaciĂłn": "investigación",
    "investigaciĂłn": "investigación",
    "CibernĂ©tica": "Cibernética",
    "Ăł": "ó",
    "Ă©": "é",
    "Ă­": "í",
    "Ăº": "ú",
    "Ă±": "ñ",
    "Ă": "Á",
    "intent├│": "intentó",
    "Secretar√≠a": "Secretaría",
    "Protecci√≥n": "Protección",
    "Fiscal√≠a": "Fiscalía",
    "RepГәblica": "República",
    "aГұo": "año",
    "indГӯgena": "indígena",
    "MГүXICO": "MÉXICO",
    "├│": "ó",
    "├®": "é",
    "├í": "á",
    "├¡": "í",
    "├║": "ú",
    "├▒": "ñ",
    "√≠": "í",
    "√≥": "ó",
    "√°": "á",
    "√©": "é",
    "√∫": "ú",
    "√±": "ñ",
}

def aggressive_fix(text):
    if not text: return text
    
    # 1. Manual replacements first
    for broken, fixed in MANUAL_FIXES.items():
        text = text.replace(broken, fixed)
    
    # 2. Use ftfy
    text = ftfy.fix_text(text)
    
    # 3. Handle double UTF-8 if still present (aggressive)
    try:
        # If it contains characters that look like Latin-1 interpretation of UTF-8
        if any(c in text for c in "ÃÂ"):
            text = text.encode('latin-1').decode('utf-8')
    except:
        pass
        
    return text

def run_query(query):
    cmd = ["wrangler", "d1", "execute", "news_db", "--remote", "--command", query, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error executing query: {result.stderr}")
        return []
    try:
        # Wrangler D1 output is a bit messy in JSON mode sometimes
        data = json.loads(result.stdout)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get('results', [])
        return []
    except:
        return []

def update_article(table, art_id, title, content, excerpt):
    # Escape single quotes for SQL
    title_sql = title.replace("'", "''")
    content_sql = content.replace("'", "''")
    excerpt_sql = (excerpt or "").replace("'", "''")
    
    # Use different column names depending on table
    title_col = "TITULO_PARAFRASEADO" if table == "ARTICULOS_PARAFRASEADOS" else "TITULO"
    if table == "REVISION_CONTENIDO": title_col = "TITULO_PROPUESTO"
    
    content_col = "CONTENIDO"
    if table == "REVISION_CONTENIDO": content_col = "CONTENIDO_PROPUESTO"
    
    excerpt_col = "DESCRIPCION_PARAFRASEADA" if table == "ARTICULOS_PARAFRASEADOS" else "DESCRIPCION"
    if table == "REVISION_CONTENIDO": excerpt_col = "DESCRIPCION_PROPUESTA"

    query = f"UPDATE {table} SET {title_col} = '{title_sql}', {content_col} = '{content_sql}', {excerpt_col} = '{excerpt_sql}' WHERE ID = '{art_id}';"
    
    cmd = ["wrangler", "d1", "execute", "news_db", "--remote", "--command", query]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def fix_table(table):
    print(f"\n--- Fixing table: {table} ---")
    
    # Get columns
    title_col = "TITULO_PARAFRASEADO" if table == "ARTICULOS_PARAFRASEADOS" else "TITULO"
    if table == "REVISION_CONTENIDO": title_col = "TITULO_PROPUESTO"
    
    content_col = "CONTENIDO"
    if table == "REVISION_CONTENIDO": content_col = "CONTENIDO_PROPUESTO"
    
    excerpt_col = "DESCRIPCION_PARAFRASEADA" if table == "ARTICULOS_PARAFRASEADOS" else "DESCRIPCION"
    if table == "REVISION_CONTENIDO": excerpt_col = "DESCRIPCION_PROPUESTA"

    articles = run_query(f"SELECT ID, {title_col}, {content_col}, {excerpt_col} FROM {table} ORDER BY rowid DESC LIMIT 200;")
    print(f"Found {len(articles)} articles to check.")
    
    fixed_count = 0
    for art in articles:
        art_id = art['ID']
        title = art.get(title_col, "")
        content = art.get(content_col, "")
        excerpt = art.get(excerpt_col, "")
        
        fixed_title = aggressive_fix(title)
        fixed_content = aggressive_fix(content)
        fixed_excerpt = aggressive_fix(excerpt)
        
        if fixed_title != title or fixed_content != content or fixed_excerpt != excerpt:
            print(f"Fixing ID: {art_id} | {title[:40]}...")
            if update_article(table, art_id, fixed_title, fixed_content, fixed_excerpt):
                fixed_count += 1
            else:
                print(f"Failed to update {art_id}")
                
    print(f"Fixed {fixed_count} articles in {table}.")

if __name__ == "__main__":
    fix_table("ARTICULOS_PARAFRASEADOS")
    fix_table("ARTICULOS_CMS")
    fix_table("REVISION_CONTENIDO")
