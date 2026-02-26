#!/usr/bin/env python3
"""
Ingesta Histórica Masiva para los 10 NUEVOS SITIOS.
~168 noticias (1 por hora / 7 días).
"""
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import random

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

# Nuevos Slugs de los 10 sitios
SITIOS = [
    "noticiasobjetivo", "mexicoinformado", "bitacoraurbana", "nodoinformativo",
    "cbnnoticias", "radiocinconoticias", "centralmexico", "reportecentralmx",
    "tvmexico", "verticenoticias"
]

CATEGORIAS = ["Nacional", "Política", "Economía", "Deportes", "Cultura"]

def run_bulk_ingest():
    print(f"🚀 Poblando historial para los 10 sitios nuevos...")
    
    sql_commands = []
    now = datetime.now()

    for i in range(168):
        fecha_simulada = now - timedelta(hours=i)
        fecha_iso = fecha_simulada.isoformat()
        
        site = SITIOS[i % len(SITIOS)]
        cat = random.choice(CATEGORIAS)
        
        orig_id = str(uuid.uuid4())
        para_id = str(uuid.uuid4())
        
        titulo = f"Noticia Importante en {cat} - {fecha_simulada.strftime('%d/%m %H:00')}"
        contenido = f"Contenido detallado parafraseado por IA sobre un evento de {cat} que afecta a México. Este artículo ha sido optimizado para el sitio {site}."
        
        def esc(text):
            return "'" + str(text).replace("'", "''") + "'"

        # Original
        sql_commands.append(f"INSERT INTO ARTICULOS_ORIGINALES (ID, URL, TITULO, FECHA, CONTENIDO, CATEGORIA, LONGITUD) VALUES ({esc(orig_id)}, 'https://fuente.test/{i}', {esc(titulo)}, {esc(fecha_iso)}, {esc(contenido)}, {esc(cat)}, {len(contenido)});")

        # Parafraseado (Directo a la tabla final para ver los sitios vivos)
        autor = f"Redacción {site} {cat}"
        sql_commands.append(f"INSERT INTO ARTICULOS_PARAFRASEADOS (ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, CONTENIDO, SITIO_DESTINO, CATEGORIA, FECHA_PUBLICACION, AUTOR, VERIFICACION, DESTACADO) VALUES ({esc(para_id)}, {esc(orig_id)}, {esc(titulo)}, {esc(contenido[:150])}, {esc(contenido)}, {esc(site)}, {esc(cat)}, {esc(fecha_iso)}, {esc(autor)}, 'Sistema Auto', {1 if i % 10 == 0 else 0});")

    sql_file = REPO_ROOT / "bulk_new_sites.sql"
    with open(sql_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_commands))
    
    import subprocess
    try:
        subprocess.run(f"wrangler d1 execute news_db --local --file={sql_file} --config=src/wrangler.toml", shell=True, check=True)
        print(f"✅ ¡Historial cargado con éxito para los 10 sitios!")
    finally:
        if sql_file.exists(): sql_file.unlink()

if __name__ == "__main__":
    run_bulk_ingest()
