#!/usr/bin/env python3
"""
Ingesta Masiva de Política Mexicana v3.1 (Inyección por lotes).
- Inyección en fragmentos para evitar errores de autenticación/timeout en D1.
- Distribución total: Cada noticia se publica en los 10 sitios de la red.
- Limpieza agresiva por Regex.
"""
import os
import sys
import uuid
import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.api.newsapi import fetch_newsapi
from utils.utils import _extract_full_text

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

def clean_content_regex(text):
    if not text: return ""
    text = re.sub(r'<h[1-3]>.*?</h[1-3]>', '', text, flags=re.DOTALL | re.I)
    noise_patterns = [
        r'Seguinos en Twitter.*?\n', r'Haz clic aquí.*?\n', r'Suscríbete aquí.*?\n',
        r'Y recuerda que.*?\n', r'Descarga la última.*?\n', r'¿Quiénes somos\?.*?Siguenos en:.*?\n',
        r'Medios asociados:.*?\n', r'Los mejores comentarios:.*?\n',
        r'Tecnología Videojuegos Entretenimiento.*?\n', r'twitter\.com/[a-zA-Z0-9_]+',
        r'pic\.twitter\.com/[a-zA-Z0-9_]+', r'\[email\s*protected\]'
    ]
    for p in noise_patterns: text = re.sub(p, '', text, flags=re.I)
    
    if '<p>' not in text:
        paragraphs = text.split('\n\n')
        text = "".join([f"<p>{p.strip()}</p>" for p in paragraphs if len(p.strip()) > 20])
    else:
        p_matches = re.findall(r'<p>(.*?)</p>', text, flags=re.DOTALL | re.I)
        text = "".join([f"<p>{m.strip()}</p>" for m in p_matches if len(m.strip()) > 20])

    text = text.replace('\n', ' ').replace('  ', ' ')
    return text.strip()

def run_bulk_ingest():
    is_remote = "--remote" in sys.argv
    target = "--remote" if is_remote else "--local"
    
    today = datetime.now()
    start_str = (today - timedelta(days=8)).strftime('%Y-%m-%d')
    
    print(f"🚀 Iniciando Ingesta Masiva de Política (Inyección por Lotes) ({target})...")
    raw_news = fetch_newsapi(query="política México", from_date=start_str, page_size=60, enrich=False, silent=True)
    
    processed_count = 0
    batch_sql = []
    
    for art in raw_news:
        if processed_count >= 30: break
        
        title = art.get('title', 'Sin Título')
        url = art.get('url')
        img_url = art.get('urlToImage') or '/logo.png'
        full_text = _extract_full_text(url) or art.get('description') or title
        clean_body = clean_content_regex(full_text)
        
        if len(clean_body.split()) < 250: continue

        orig_id = str(uuid.uuid4())
        slug = slugify(title)
        pub_date = art.get('publishedAt', datetime.now().isoformat())
        
        def esc(text): return "'" + str(text).replace("'", "''") + "'"

        # SQL para este artículo (Original + 10 Parafraseados + 10 Métricas)
        sql_chunk = []
        sql_chunk.append(f"INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, FECHA, CONTENIDO, CATEGORIA, LONGITUD, URL_IMAGEN) VALUES ({esc(orig_id)}, {esc(url)}, {esc(title)}, {esc(pub_date)}, {esc(full_text)}, 'POLITICA', {len(full_text)}, {esc(img_url)});")
        
        for site in SITIOS:
            para_id = str(uuid.uuid4())
            cat_label = "POLITICA NACIONAL" if processed_count % 2 == 0 else "POLITICA MEXICO"
            sql_chunk.append(f"INSERT INTO ARTICULOS_PARAFRASEADOS (ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, SLUG, DESCRIPCION_PARAFRASEADA, CONTENIDO, SITIO_DESTINO, CATEGORIA, FECHA_PUBLICACION, AUTOR, VERIFICACION, DESTACADO, URL_IMAGEN) VALUES ({esc(para_id)}, {esc(orig_id)}, {esc(title)}, {esc(slug + '-' + site)}, {esc(title)}, {esc(clean_body)}, {esc(site)}, {esc(cat_label)}, {esc(pub_date)}, 'Redacción', 'Verificado', 1, {esc(img_url)});")
            sql_chunk.append(f"INSERT INTO METRICAS_CONTENIDO (ID_ARTICULO_PARAFRASEADO, VISTAS) VALUES ({esc(para_id)}, 0);")
        
        batch_sql.append("\n".join(sql_chunk))
        processed_count += 1

        # Inyectar cada 5 noticias (evita archivos SQL gigantes)
        if len(batch_sql) >= 5:
            inject_batch(batch_sql, target)
            batch_sql = []

    if batch_sql:
        inject_batch(batch_sql, target)

    print(f"✨ Proceso completado. {processed_count} noticias publicadas exitosamente.")

def inject_batch(batch, target):
    sql_file = REPO_ROOT / f"batch_{uuid.uuid4().hex[:8]}.sql"
    with open(sql_file, "w", encoding="utf-8") as f:
        f.write("\n".join(batch))
    
    print(f"📦 Inyectando lote de noticias en D1...")
    subprocess.run(f"wrangler d1 execute news_db {target} --file={sql_file} --config=src/wrangler.toml --yes", shell=True)
    if sql_file.exists(): sql_file.unlink()

if __name__ == "__main__":
    run_bulk_ingest()
