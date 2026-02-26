#!/usr/bin/env python3
"""
Fix article links in index.html to point to real article files
"""

import os

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')

# Map generic links to real article files
ARTICLE_MAP = {
    'articulo/nota-1.html': 'articulo/ariadna-montiel-se-reune-con-representantes-de-agr.html',
    'articulo/nota-2.html': 'articulo/cierre-del-dolar-cotizacion-peso-mexicano-hoy-18-f.html',
    'articulo/nota-3.html': 'articulo/comercio-china-mexico-mantiene-pese-eu-especialist.html',
    'articulo/nota-4.html': 'articulo/cual-es-estado-salud-elena-poniatowska-escritora-h.html',
    'articulo/nota-5.html': 'articulo/edc-mexico-2026-objetos-prohibidos-y-permitidos-fe.html',
    'articulo/nota-6.html': 'articulo/587724-diputado-mexicano-licencia-participar-reali.html',
    'articulo/nota-7.html': 'articulo/arbol-genealogico-sergio-mayer-quien-es-la-familia.html',
    'articulo/nota-8.html': 'articulo/marisol-schulz-recibe-medalla-oro-merito-cultural-.html',
    'articulo/nota-9.html': 'articulo/00031771451603338459814.htm.html',
    'articulo/nota-10.html': 'articulo/informe-especial-tecnologia.html',
}

for slug in os.listdir(SITES_DIR):
    site_dir = os.path.join(SITES_DIR, slug)
    if not os.path.isdir(site_dir):
        continue
    
    index_path = os.path.join(site_dir, 'index.html')
    if not os.path.exists(index_path):
        continue
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace generic article links with real ones
    for old_link, new_link in ARTICLE_MAP.items():
        content = content.replace(f'href="{old_link}"', f'href="{new_link}"')
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {slug}: enlaces de artículos corregidos")

print("\n✅ Todos los enlaces de artículos corregidos")
