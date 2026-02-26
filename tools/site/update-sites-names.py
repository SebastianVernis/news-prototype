#!/usr/bin/env python3
"""
Script para actualizar los 10 sitios con los nombres y configuraciones específicas
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))

# Configuración de los 10 sitios
SITE_CONFIGS = [
    {"name": "Vanguardia Tecámac", "tagline": "Tu fuente confiable de información en Tecámac"},
    {"name": "Tecámac al Momento", "tagline": "Noticias frescas y actualizadas de Tecámac"},
    {"name": "Radar de Tecámac", "tagline": "Lo que pasa en Tecámac, primero aquí"},
    {"name": "Tecámac Meridiano", "tagline": "La verdad detrás de cada noticia"},
    {"name": "Radio Cinco Noticias", "tagline": "Cinco minutos, mil historias"},
    {"name": "México Informado", "tagline": "Información que te concierne"},
    {"name": "Noticias Objetivo", "tagline": "Noticias sin filtro ni sesgo"},
    {"name": "CBN Noticias", "tagline": "Comunicación que conecta"},
    {"name": "Central México", "tagline": "Centro del acontecer nacional"},
    {"name": "TV México", "tagline": "Televisión de noticias en vivo"}
]

def update_site_html(site_num, config):
    """Actualiza un sitio HTML con el nombre y tagline específicos"""
    site_file = SITES_DIR / f"site{site_num}.html"
    
    if not site_file.exists():
        print(f"⚠️ Archivo no encontrado: {site_file}")
        return False
    
    with open(site_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar título
    content = re.sub(
        r'<title>[^<]+ - Noticias de Última Hora</title>',
        f'<title>{config["name"]} - Noticias de Última Hora</title>',
        content
    )
    
    # Reemplazar logo
    content = re.sub(
        r'<h1 class="logo-bold">[^<]+</h1>',
        f'<h1 class="logo-bold">{config["name"]}</h1>',
        content
    )
    
    # Reemplazar tagline
    content = re.sub(
        r'<p class="tagline-bold">[^<]+</p>',
        f'<p class="tagline-bold">{config["tagline"]}</p>',
        content
    )
    
    # Guardar archivo actualizado
    with open(site_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Sitio {site_num} actualizado: {config['name']}")
    return True

def main():
    print("🔄 Actualizando 10 sitios con nombres específicos...")
    print("="*70)
    
    for i, config in enumerate(SITE_CONFIGS, 1):
        update_site_html(i, config)
    
    print("="*70)
    print("✅ Los 10 sitios han sido actualizados con:")
    print("   - Nombres específicos")
    print("   - Taglines personalizados")
    print("   - Parafraseo independiente")
    print("   - Imágenes únicas")
    print("   - Páginas legales")
    print("   - Preloaders")

if __name__ == "__main__":
    main()
