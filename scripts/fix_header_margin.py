#!/usr/bin/env python3
"""
Script para remover el margin-top del header en sitios con ticker en bottom
"""

import os
import re

SITES_DIR = "/mnt/c/Users/soluc/cloudflare-news-project/sites/Nuevos"

# Sitios a actualizar (todos los nuevos sitios)
SITES = [
    "boominformativo",
    "capitalpress",
    "diarioexpress",
    "elpulsomexicano",
    "enfoquecapital",
    "enfoquedirecto",
    "formulacdmx",
    "mexicantimes",
    "mexico360noticias",
    "mradio",
    "noticiashorizonte",
    "pulsodiario",
    "puntoclave",
    "puntonoticias",
    "radarinformativo",
    "reportediario",
    "televisionabc",
]

def update_components(site_name):
    file_path = os.path.join(SITES_DIR, site_name, "components.js")
    
    if not os.path.exists(file_path):
        print(f"❌ {site_name}: No existe components.js")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si tiene ticker en bottom
    has_bottom_ticker = 'position:fixed;bottom:0' in content
    
    if not has_bottom_ticker:
        print(f"⏭️  {site_name}: No tiene ticker en bottom")
        return False
    
    # Reemplazar margin-top:40px por margin-top:0 en el header
    # Patrón 1: header style="margin-top:40px
    pattern1 = r'(<header[^>]*style="[^"]*)margin-top:40px'
    replacement1 = r'\1margin-top:0'
    
    # Patrón 2: header style="margin-top:35px (algunos sitios)
    pattern2 = r'(<header[^>]*style="[^"]*)margin-top:35px'
    replacement2 = r'\1margin-top:0'
    
    # Patrón 3: position:sticky;top:40px -> position:sticky;top:0
    pattern3 = r'position:sticky;top:40px'
    replacement3 = r'position:sticky;top:0'
    
    original = content
    content = re.sub(pattern1, replacement1, content)
    content = re.sub(pattern2, replacement2, content)
    content = re.sub(pattern3, replacement3, content)
    
    if content == original:
        print(f"⏭️  {site_name}: No se encontraron cambios necesarios")
        return False
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {site_name}: Actualizado")
    return True

def main():
    print("="*60)
    print("Remover margin-top del header - Sitios con ticker en bottom")
    print("="*60)
    print()
    
    updated = 0
    skipped = 0
    
    for site in SITES:
        if update_components(site):
            updated += 1
        else:
            skipped += 1
    
    print()
    print("="*60)
    print(f"✅ Actualizados: {updated}")
    print(f"⏭️  Saltados: {skipped}")
    print("="*60)

if __name__ == "__main__":
    main()
