#!/usr/bin/env python3
"""
Script para corregir las rutas de los enlaces en los 10 sitios
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))

def fix_site_links(site_num):
    """Corrige los enlaces de un sitio específico"""
    site_file = SITES_DIR / f'site{site_num}.html'
    
    if not site_file.exists():
        print(f"⚠️ Archivo no encontrado: {site_file}")
        return False
    
    with open(site_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Corregir enlaces de navegación
    content = re.sub(r'href="#inicio"', 'href="index.html"', content)
    content = re.sub(r'href="#política"', 'href="categoria/politica.html"', content)
    content = re.sub(r'href="#tecnología"', 'href="categoria/tecnologia.html"', content)
    content = re.sub(r'href="#deportes"', 'href="categoria/deportes.html"', content)
    content = re.sub(r'href="#entretenimiento"', 'href="categoria/entretenimiento.html"', content)
    content = re.sub(r'href="#negocios"', 'href="categoria/negocios.html"', content)
    content = re.sub(r'href="#mundial"', 'href="categoria/mundial.html"', content)
    
    # Corregir enlaces de artículos
    content = re.sub(r'href="article-(\d+)\.html"', 'href="articulo/\g<1>.html"', content)
    
    # Corregir enlaces del footer
    content = re.sub(r'href="terminos\.html"', 'href="terminos.html"', content)
    content = re.sub(r'href="privacidad\.html"', 'href="privacidad.html"', content)
    content = re.sub(r'href="contacto\.html"', 'href="contacto.html"', content)
    content = re.sub(r'href="acerca-de\.html"', 'href="acerca-de.html"', content)
    
    # Corregir rutas de CSS y assets
    content = re.sub(r'href="\.\./templates/css/', 'href="templates/css/', content)
    content = re.sub(r'src="\.\./templates/css/', 'src="templates/css/', content)
    content = re.sub(r'href="templates/css/', 'href="templates/css/', content)
    content = re.sub(r'src="assets/', 'src="assets/', content)
    content = re.sub(r'href="assets/', 'href="assets/', content)
    
    # Guardar archivo actualizado
    with open(site_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Sitio {site_num} actualizado")
    return True

def main():
    print("🔗 Corrigiendo rutas de enlaces en los 10 sitios...")
    print("="*60)
    
    for i in range(1, 11):
        fix_site_links(i)
    
    print("="*60)
    print("✅ Rutas de enlaces corregidas en los 10 sitios")

if __name__ == "__main__":
    main()
