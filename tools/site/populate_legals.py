import os
import sys
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

def get_sites():
    cmd = ["wrangler", "d1", "execute", "news_db", "--local", "--config=src/wrangler.toml", "--command", "SELECT ID, NOMBRE, SLUG, DOMINIO FROM SITIOS", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        output = json.loads(result.stdout)
        return output[0].get("results", [])
    return []

def generate_legals():
    sites = get_sites()
    if not sites:
        print("❌ No se encontraron sitios.")
        return

    sql_commands = []
    for s in sites:
        name, slug = s['NOMBRE'], s['SLUG']
        email_l = f"legal@{slug}.com"
        
        term = f"<h2>Términos de Uso - {name}</h2><p>Última actualización: 12 de Febrero, 2026</p><h3>Introducción</h3><p>Estos términos rigen el uso del sitio {name}. Al acceder, acepta estar sujeto a las leyes de México.</p><h3>Uso Aceptable</h3><p>Usted acepta usar este sitio solo para fines legales.</p><h3>Contacto</h3><p>Email: {email_l}</p>"
        priv = f"<h2>Política de Privacidad - {name}</h2><p>Última actualización: 12 de Febrero, 2026</p><h3>Datos</h3><p>En {name} protegemos su privacidad. No vendemos información a terceros.</p>"

        def esc(t): return t.replace("'", "''")
        sql_commands.append(f"INSERT OR REPLACE INTO LEGALES (ID_SITIO, TERMINOS_CONDICIONES, POLITICA_PRIVACIDAD, CONTACTO_EMAIL) VALUES ('{s['ID']}', '{esc(term)}', '{esc(priv)}', '{email_l}');")

    sql_file = REPO_ROOT / "pop_legals.sql"
    with open(sql_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_commands))
    
    subprocess.run(f"wrangler d1 execute news_db --local --file={sql_file} --config=src/wrangler.toml", shell=True)
    sql_file.unlink()
    print("✅ Legales inyectados.")

if __name__ == "__main__":
    generate_legals()
