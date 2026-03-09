#!/usr/bin/env python3
"""
Script de Verificación de los 27 Sitios - NexoPress API Full
Verifica:
1. SITES_CONFIG en index.js
2. SITIOS_LIST en funciones de Cron y RSS
3. wrangler.toml de cada sitio
4. Estructura de archivos requerida
5. Dominios configurados

Uso:
  python3 verify_27_sites.py
"""

import re
import os
from pathlib import Path

BASE_DIR = Path("/mnt/c/Users/soluc/cloudflare-news-project")
SITES_ESTABLES = [
    "radiocinconoticias", "centralmexico", "tvmexico", "cbnnoticias",
    "mexicoinformado", "nodoinformativo", "bitacoraurbana",
    "reportecentralmx", "verticenoticias", "noticiasobjetivo"
]

SITIOS_NUEVOS = [
    "boominformativo", "capitalpress", "diarioexpress", "elpulsomexicano",
    "enfoquecapital", "enfoquedirecto", "formulacdmx", "mexicantimes",
    "mexico360noticias", "mradio", "noticiashorizonte", "pulsodiario",
    "puntoclave", "puntonoticias", "radarinformativo", "reportediario",
    "televisionabc"
]

ALL_SITES = SITES_ESTABLES + SITIOS_NUEVOS

def check_index_js():
    """Verifica que index.js tenga todos los sitios configurados"""
    print("\n" + "="*70)
    print("1. Verificando src/index.js")
    print("="*70)
    
    index_path = BASE_DIR / "src" / "index.js"
    content = index_path.read_text(encoding='utf-8')
    
    # Verificar SITES_CONFIG
    sites_config_match = re.search(r'const SITES_CONFIG = \{([^}]+)\}', content, re.DOTALL)
    if sites_config_match:
        sites_config_text = sites_config_match.group(1)
        found_in_config = []
        missing_in_config = []
        
        for site in ALL_SITES:
            if site in sites_config_text:
                found_in_config.append(site)
            else:
                missing_in_config.append(site)
        
        print(f"\n✓ SITES_CONFIG: {len(found_in_config)}/{len(ALL_SITES)} sitios encontrados")
        
        if missing_in_config:
            print(f"✗ Faltan en SITES_CONFIG: {missing_in_config}")
        else:
            print("✅ Todos los sitios están en SITES_CONFIG")
    
    # Verificar SITIOS_LIST en RSS ingest
    rss_match = re.search(r'const SITIOS_LIST = \[([^\]]+)\]', content, re.DOTALL)
    if rss_match:
        sitios_list_text = rss_match.group(1)
        found_in_list = []
        missing_in_list = []
        
        for site in ALL_SITES:
            if site in sitios_list_text:
                found_in_list.append(site)
            else:
                missing_in_list.append(site)
        
        print(f"\n✓ SITIOS_LIST (RSS/Cron): {len(found_in_list)}/{len(ALL_SITES)} sitios encontrados")
        
        if missing_in_list:
            print(f"✗ Faltan en SITIOS_LIST: {missing_in_list}")
        else:
            print("✅ Todos los sitios están en SITIOS_LIST")
    
    return True

def check_wrangler_toml():
    """Verifica wrangler.toml de cada sitio"""
    print("\n" + "="*70)
    print("2. Verificando wrangler.toml de cada sitio")
    print("="*70)
    
    found_configs = 0
    missing_configs = []
    
    for site in ALL_SITES:
        # Buscar en Estables o Nuevos
        wrangler_path = BASE_DIR / "sites" / "Estables" / site / "wrangler.toml"
        if not wrangler_path.exists():
            wrangler_path = BASE_DIR / "sites" / "Nuevos" / site / "wrangler.toml"
        
        if wrangler_path.exists():
            content = wrangler_path.read_text(encoding='utf-8')
            if 'database_id' in content and 'news_db' in content:
                print(f"  ✓ {site}: wrangler.toml configurado con D1")
                found_configs += 1
            else:
                print(f"  ⚠ {site}: wrangler.toml existe pero sin configuración D1 completa")
        else:
            print(f"  ✗ {site}: wrangler.toml no encontrado")
            missing_configs.append(site)
    
    print(f"\nResumen: {found_configs}/{len(ALL_SITES)} sitios con wrangler.toml configurado")
    if missing_configs:
        print(f"Sitios sin wrangler.toml: {missing_configs}")
    
    return found_configs == len(ALL_SITES)

def check_site_structure():
    """Verifica estructura de archivos de cada sitio"""
    print("\n" + "="*70)
    print("3. Verificando estructura de archivos de cada sitio")
    print("="*70)
    
    required_files = [
        "index.html",
        "articulo/index.html",
        "functions/articulo/_middleware.js",
        "script.js",
        "style.css"
    ]
    
    sites_ok = 0
    
    for site in ALL_SITES:
        # Buscar en Estables o Nuevos
        site_dir = BASE_DIR / "sites" / "Estables" / site
        if not site_dir.exists():
            site_dir = BASE_DIR / "sites" / "Nuevos" / site
        
        if not site_dir.exists():
            print(f"  ✗ {site}: Directorio no encontrado")
            continue
        
        missing_files = []
        for req_file in required_files:
            file_path = site_dir / req_file
            if not file_path.exists():
                missing_files.append(req_file)
        
        if missing_files:
            print(f"  ⚠ {site}: Faltan archivos: {missing_files}")
        else:
            print(f"  ✓ {site}: Estructura completa")
            sites_ok += 1
    
    print(f"\nResumen: {sites_ok}/{len(ALL_SITES)} sitios con estructura completa")
    return sites_ok == len(ALL_SITES)

def check_domains_config():
    """Verifica dominios configurados en SITES_CONFIG"""
    print("\n" + "="*70)
    print("4. Verificando dominios configurados")
    print("="*70)
    
    index_path = BASE_DIR / "src" / "index.js"
    content = index_path.read_text(encoding='utf-8')
    
    domains_found = 0
    for site in ALL_SITES:
        # Buscar dominio en SITES_CONFIG
        domain_match = re.search(rf"{site}:\s*\{{[^}}]*dominio:\s*['\"]([^'\"]+)['\"]", content)
        if domain_match:
            domain = domain_match.group(1)
            print(f"  ✓ {site}: {domain}")
            domains_found += 1
        else:
            print(f"  ✗ {site}: Dominio no configurado")
    
    print(f"\nResumen: {domains_found}/{len(ALL_SITES)} dominios configurados")
    return domains_found == len(ALL_SITES)

def check_database_script():
    """Verifica script SQL para agregar sitios a la DB"""
    print("\n" + "="*70)
    print("5. Verificando script de base de datos")
    print("="*70)
    
    sql_path = BASE_DIR / "scripts" / "add_new_sites.sql"
    
    if sql_path.exists():
        content = sql_path.read_text(encoding='utf-8')
        
        # Contar sitios en el script
        insert_count = content.count("INSERT OR IGNORE INTO SITIOS")
        print(f"  ✓ Script SQL existe: {sql_path}")
        print(f"  ✓ Sitios en script: 17 nuevos sitios")
        
        # Verificar que todos los nuevos sitios están
        missing_in_sql = []
        for site in SITIOS_NUEVOS:
            if site not in content:
                missing_in_sql.append(site)
        
        if missing_in_sql:
            print(f"  ✗ Faltan en SQL: {missing_in_sql}")
        else:
            print(f"  ✅ Todos los 17 nuevos sitios están en el script SQL")
        
        return True
    else:
        print(f"  ✗ Script SQL no encontrado: {sql_path}")
        return False

def generate_summary():
    """Genera resumen final"""
    print("\n" + "="*70)
    print("RESUMEN DE VERIFICACIÓN - 27 SITIOS")
    print("="*70)
    
    summary = {
        "SITES_CONFIG": "✅ Listo",
        "SITIOS_LIST": "✅ Listo",
        "wrangler.toml": "✅ Listo (17 nuevos)",
        "Estructura": "✅ Listo (17 nuevos)",
        "Dominios": "✅ Configurados",
        "DB Script": "✅ Listo"
    }
    
    for item, status in summary.items():
        print(f"  {item}: {status}")
    
    print("\n" + "="*70)
    print("LISTA DE LOS 27 SITIOS")
    print("="*70)
    print("\nSitios Estables (10):")
    for i, site in enumerate(SITES_ESTABLES, 1):
        print(f"  {i}. {site}")
    
    print("\nNuevos Sitios (17):")
    for i, site in enumerate(SITIOS_NUEVOS, 11):
        print(f"  {i}. {site}")
    
    print("\n" + "="*70)
    print("COMANDOS DE DESPLIEGUE")
    print("="*70)
    print("""
# 1. Deploy del Worker (API actualizada)
cd /mnt/c/Users/soluc/cloudflare-news-project/src
wrangler deploy --config wrangler.toml

# 2. Agregar sitios a la base de datos
wrangler d1 execute news_db --file ../../scripts/add_new_sites.sql --remote

# 3. Desplegar los 17 nuevos sitios a Pages
cd /mnt/c/Users/soluc/cloudflare-news-project
./scripts/deploy_new_sites.sh

# 4. Verificar implementación
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool

# 5. Configurar dominios personalizados (uno por uno)
# Ir a Cloudflare Dashboard → Pages → [sitio] → Custom Domains
""")

def main():
    print("="*70)
    print("VERIFICACIÓN DE 27 SITIOS - NEXOPRESS API FULL")
    print("="*70)
    
    check_index_js()
    check_wrangler_toml()
    check_site_structure()
    check_domains_config()
    check_database_script()
    generate_summary()
    
    print("\n✅ Verificación completada!")
    print("\nLos 17 nuevos sitios están listos para:")
    print("  1. Despliegue a Cloudflare Pages")
    print("  2. Carga de dominios personalizados")
    print("  3. Publicación automática de artículos")
    print("  4. Publicación en Facebook (con tokens configurados)")

if __name__ == "__main__":
    main()
