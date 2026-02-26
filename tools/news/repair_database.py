#!/usr/bin/env python3
import subprocess
import json
import os
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

def run_wrangler_json(command, target):
    cmd = ["wrangler", "d1", "execute", "news_db", target, "--command=" + command, "--config=src/wrangler.toml", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout)
        return data[0].get('results', []) if isinstance(data, list) else data.get('results', [])
    except:
        return []

def clean_content_aggressive(text):
    if not text: return ""
    text = re.sub(r'<h[1-3]>.*?</h[1-3]>', '', text, flags=re.DOTALL | re.I)
    bad_p_patterns = [
        r'<p>.*?abc\.es.*?</p>', r'<p>.*?Defensora del Lector.*?</p>',
        r'<p>.*?Teatro.*?Madrid.*?</p>', r'<p>.*?Entradas.*?Madrid.*?</p>',
        r'<p>.*?Auditorio Nacional.*?</p>', r'<p>.*?exclusiva para suscriptores.*?</p>',
        r'<p>.*?kits de herramientas.*?</p>', r'<p>.*?[A-Z][a-z]+ [A-Z][a-z]+.*?\..*?\(.*?, EE\.UU\.\)</p>',
        r'<p>.*?EUROPA PRESS.*?</p>', r'EUROPA PRESS', r'<p>.*?twitter\.com.*?</p>',
        r'<p>.*?pic\.\s*twitter.*?</p>', r'<p>.*?normas de convivencia.*?</p>',
        r'<p>.*?\[email\s*protected\].*?</p>', r'<p>.*?O elegí una de nuestras ilustraciones.*?</p>'
    ]
    for pattern in bad_p_patterns: text = re.sub(pattern, '', text, flags=re.DOTALL | re.I)
    text = re.sub(r'<p>\s*[‌\s]*\s*</p>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def repair():
    target = "--remote" if "--remote" in sys.argv else "--local"
    print(f"🔧 Generando archivo SQL masivo para {target}...")

    # 1. Obtener todos los datos de una vez
    articles = run_wrangler_json("SELECT ID, CONTENIDO, URL_IMAGEN FROM ARTICULOS_PARAFRASEADOS", target)
    if not articles:
        print("❌ Error al obtener artículos.")
        return

    sql_lines = []
    for art in articles:
        content = art.get('CONTENIDO', '') or ''
        new_content = clean_content_aggressive(content)
        
        img = art.get('URL_IMAGEN') or ''
        new_img = '/logo.png' if not img or 'jornada.com.mx' in img or 'sergio-mayer' in img else img
        
        if new_content != content or new_img != img:
            c_esc = new_content.replace("'", "''")
            i_esc = new_img.replace("'", "''")
            sql_lines.append(f"UPDATE ARTICULOS_PARAFRASEADOS SET CONTENIDO = '{c_esc}', URL_IMAGEN = '{i_esc}' WHERE ID = '{art['ID']}';")

    if sql_lines:
        sql_file = REPO_ROOT / "final_cleanup.sql"
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sql_lines))
        
        print(f"🚀 Inyectando {len(sql_lines)} actualizaciones en D1...")
        subprocess.run(f"wrangler d1 execute news_db {target} --file={sql_file} --config=src/wrangler.toml --yes", shell=True)
        if sql_file.exists(): sql_file.unlink()
        print("✅ Base de datos saneada completamente.")
    else:
        print("✨ No se encontraron artículos que requieran limpieza.")

if __name__ == "__main__":
    repair()
