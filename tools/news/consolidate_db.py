#!/usr/bin/env python3
import subprocess
import json
import sys
from pathlib import Path

def run_wrangler_json(command, target):
    cmd = ["wrangler", "d1", "execute", "news_db", target, "--command=" + command, "--config=src/wrangler.toml", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0: return None
    try:
        data = json.loads(result.stdout)
        return data[0].get('results', []) if isinstance(data, list) else data.get('results', [])
    except: return []

def consolidate():
    target = "--remote" if "--remote" in sys.argv else "--local"
    print(f"🔗 Consolidando artículos en {target}...")

    rows = run_wrangler_json("SELECT TITULO_PARAFRASEADO, GROUP_CONCAT(ID) as ids, GROUP_CONCAT(SITIO_DESTINO) as sitios FROM ARTICULOS_PARAFRASEADOS GROUP BY TITULO_PARAFRASEADO", target)
    
    if not rows:
        print("❌ No se pudieron obtener datos.")
        return

    print(f"📊 Encontrados {len(rows)} grupos únicos de noticias.")

    sql_commands = []
    for row in rows:
        ids = row['ids'].split(',')
        sitios_list = list(set([s.strip() for s in row['sitios'].split(',') if s.strip()]))
        sitios_str = ",".join(sitios_list)
        
        main_id = ids[0]
        other_ids = ids[1:]

        sql_commands.append(f"UPDATE ARTICULOS_PARAFRASEADOS SET SITIO_DESTINO = '{sitios_str}' WHERE ID = '{main_id}';")
        
        if other_ids:
            others_str = ",".join([f"'{oid}'" for oid in other_ids])
            sql_commands.append(f"DELETE FROM METRICAS_CONTENIDO WHERE ID_ARTICULO_PARAFRASEADO IN ({others_str}); DELETE FROM ARTICULOS_PARAFRASEADOS WHERE ID IN ({others_str});")

    if sql_commands:
        print(f"🚀 Ejecutando {len(sql_commands)} comandos de consolidación...")
        for i in range(0, len(sql_commands), 20):
            chunk = " ".join(sql_commands[i:i+20])
            subprocess.run(["wrangler", "d1", "execute", "news_db", target, "--command=" + chunk, "--config=src/wrangler.toml", "--yes"])
        
    print("✅ Consolidación terminada.")

if __name__ == "__main__":
    consolidate()
