#!/usr/bin/env python3
"""
Script auxiliar para servir sitios generados
Puede usarse standalone o desde el menú principal
"""

import sys
import subprocess
import argparse
from pathlib import Path

def listar_sitios():
    """Lista todos los sitios disponibles"""
    site_dir = Path('generated_sites')
    if not site_dir.exists():
        print("❌ No hay sitios generados")
        return []
    
    sites = sorted([d for d in site_dir.iterdir() if d.is_dir() and d.name.startswith('site_')])
    return sites

def servir_sitio(site_path: Path, port: int):
    """Sirve un sitio en el puerto especificado"""
    print(f"🌐 Sirviendo {site_path.name} en http://localhost:{port}")
    print(f"Presiona Ctrl+C para detener\n")
    
    try:
        subprocess.run(['python3', '-m', 'http.server', str(port)], cwd=site_path)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")

def servir_todos(sites: list, port_base: int = 8000):
    """Sirve todos los sitios en puertos secuenciales"""
    print(f"🌍 Iniciando servidores para {len(sites)} sitios...\n")
    
    processes = []
    for idx, site in enumerate(sites):
        port = port_base + idx
        print(f"  🌐 {site.name}: http://localhost:{port}")
        
        proc = subprocess.Popen(
            ['python3', '-m', 'http.server', str(port)],
            cwd=site,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        processes.append(proc)
    
    print(f"\n✅ {len(sites)} servidores iniciados en segundo plano")
    print(f"\n⚠️  Para detener todos los servidores:")
    print(f"   pkill -f 'http.server'")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Servir sitios generados')
    parser.add_argument('--site', type=str, help='Nombre del sitio (ej: site_1)')
    parser.add_argument('--port', type=int, default=8000, help='Puerto (default: 8000)')
    parser.add_argument('--all', action='store_true', help='Servir todos los sitios')
    parser.add_argument('--list', action='store_true', help='Listar sitios disponibles')
    
    args = parser.parse_args()
    
    sites = listar_sitios()
    
    if not sites:
        print("❌ No hay sitios generados")
        print("\nGenera un sitio primero:")
        print("  python scripts/master_orchestrator.py")
        sys.exit(1)
    
    if args.list:
        print(f"📋 Sitios disponibles: {len(sites)}\n")
        for idx, site in enumerate(sites, 1):
            html_count = len(list(site.glob('*.html')))
            images_count = len(list(site.glob('images/*.jpg')))
            size = sum(f.stat().st_size for f in site.rglob('*') if f.is_file()) / (1024 * 1024)
            print(f"  {idx}. {site.name}")
            print(f"     Páginas: {html_count} HTML, {images_count} imágenes")
            print(f"     Tamaño: {size:.2f} MB")
            print(f"     Puerto sugerido: {8000 + idx - 1}")
            print()
        return
    
    if args.all:
        servir_todos(sites, args.port)
        return
    
    if args.site:
        site_path = Path('generated_sites') / args.site
        if not site_path.exists():
            print(f"❌ {args.site} no existe")
            print(f"\nSitios disponibles:")
            for site in sites:
                print(f"  - {site.name}")
            sys.exit(1)
        
        servir_sitio(site_path, args.port)
    else:
        # Default: servir site_1
        site_1 = Path('generated_sites/site_1')
        if site_1.exists():
            servir_sitio(site_1, args.port)
        else:
            print("❌ site_1 no existe")
            print(f"\nSitios disponibles:")
            for site in sites:
                print(f"  - {site.name}")
            sys.exit(1)

if __name__ == '__main__':
    main()
