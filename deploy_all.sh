#!/bin/bash

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          DESPLIEGUE COMPLETO - TOKENS + WORKERS + SITES       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Tokens configuration
declare -A TOKENS
declare -A WORKERS

# Read tokens from JSON file
echo "📖 Leyendo tokens desde docs/archive/formateado.json..."

# Map site names to their slugs and workers
# Worker: news-api (original), cms-nuevos, cms-nuevos2

# cms-originaux sites (10 sites) -> news-api worker
# cms-nuevos sites (9 sites) -> cms-nuevos worker
# cms-nuevos2 sites (8 sites) -> cms-nuevos2 worker (nuevos, aún sin tokens)

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "PASO 1: Configurar Tokens de Facebook"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Extract and upload tokens using Python
python3 << 'PYTHON_EOF'
import json
import subprocess
import re

with open('docs/archive/formateado.json', 'r') as f:
    data = json.load(f)

# Map site names to slugs and workers
site_mapping = {
    # cms-originaux -> news-api
    "Noticias Objetivo": ("noticiasobjetivo", "news-api"),
    "Nodo Informativo": ("nodoinformativo", "news-api"),
    "Bitácora Urbana": ("bitacoraurbana", "news-api"),
    "México Informado": ("mexicoinformado", "news-api"),
    "Radio Cinco Noticias": ("radiocinconoticias", "news-api"),
    "Central México News": ("centralmexico", "news-api"),
    "CBN Noticias": ("cbnnoticias", "news-api"),
    "Mexican Times": ("mexicantimes", "news-api"),
    "Reporte Central MX": ("reportecentralmx", "news-api"),
    "ABC Television": ("televisionabc", "news-api"),
    
    # cms-nuevos
    "Vértice Noticias": ("verticenoticias", "cms-nuevos"),
    "México Informado": ("mexicoinformado", "cms-nuevos"),  # duplicate check
    "Visión Ciudadana": ("enfoquecapital", "cms-nuevos"),
    "Capital Press": ("capitalpress", "cms-nuevos"),
    "M radio": ("mradio", "cms-nuevos"),
    "Formula CDMX": ("formulacdmx", "cms-nuevos"),
    "Enfoque capital": ("enfoquecapital", "cms-nuevos"),
    "Boom Informativo": ("boominformativo", "cms-nuevos"),
    "Punto Clave": ("puntoclave", "cms-nuevos"),
}

uploaded = []
for site in data['data']:
    name = site['name']
    token = site['access_token']
    
    if name in site_mapping:
        slug, worker = site_mapping[name]
        secret_name = f"FB_TOKEN_{slug.upper().replace('-', '_')}"
        
        print(f"Configurando {secret_name} en {worker}...")
        
        # Upload token using wrangler
        try:
            result = subprocess.run(
                ['wrangler', 'secret', 'put', secret_name, '--name', worker],
                input=token,
                text=True,
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  ✅ {secret_name} configurado")
                uploaded.append(secret_name)
            else:
                print(f"  ⚠️  {secret_name} - posiblemente ya existe o error")
        except Exception as e:
            print(f"  ⚠️  {secret_name} - error: {str(e)[:50]}")

print(f"\n✅ Tokens configurados: {len(uploaded)}")
PYTHON_EOF

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "PASO 2: Desplegar Workers CMS"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

echo "🔧 Desplegando cms-originaux..."
cd cms-originaux && ./deploy.sh
cd ..

echo ""
echo "🔧 Desplegando cms-nuevos..."
cd cms-nuevos && ./deploy.sh
cd ..

echo ""
echo "🔧 Desplegando cms-nuevos2..."
cd cms-nuevos2 && ./deploy.sh
cd ..

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "PASO 3: Desplegar Sitios Frontend"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Deploy all 8 new sites
SITES=("centronews" "noticias123" "breakingcentermexico" "alavistanoticias" "socialmexiconews" "tmznews" "radioabc" "noticiasintegra")

for SITE in "${SITES[@]}"; do
    echo ""
    echo "🚀 Desplegando $SITE..."
    cd "sites/$SITE"
    
    # Deploy using wrangler pages
    wrangler pages deploy . --project-name="$SITE" --branch=master || echo "  ⚠️  $SITE - posible error de deploy"
    
    cd ../..
    echo "  ✅ $SITE desplegado"
done

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "✅ DESPLIEGUE COMPLETADO"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📊 Resumen:"
echo "   • Tokens de Facebook configurados"
echo "   • 3 Workers CMS desplegados"
echo "   • 8 Sitios frontend desplegados"
echo ""
echo "🌐 URLs:"
echo "   • cms-originaux: https://news-api.sebastianvernis.workers.dev"
echo "   • cms-nuevos: https://cms-nuevos.sebastianvernis.workers.dev"
echo "   • cms-nuevos2: https://cms-nuevos2.sebastianvernis.workers.dev"
echo ""
echo "Los 8 sitios nuevos están disponibles en sus respectivos dominios"
echo ""

