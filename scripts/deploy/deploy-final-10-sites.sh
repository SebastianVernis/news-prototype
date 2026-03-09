#!/bin/bash

# Set your Cloudflare API token before running:
# export CLOUDFLARE_API_TOKEN="your_token_here"
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "❌ Error: CLOUDFLARE_API_TOKEN not set"
    echo "   Run: export CLOUDFLARE_API_TOKEN=\"your_token_here\""
    exit 1
fi

echo "🚀 DESPLIEGUE DE 10 SITIOS DE NOTICIAS"
echo "======================================="
echo ""

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITES_DIR="${SITES_DIR:-$ROOT_DIR/sites}"

deploy_site() {
    local site_num=$1
    local project_name=$2
    local site_file="$SITES_DIR/site${site_num}.html"
    
    echo "📦 Desplegando: $project_name (sitio $site_num)"
    
    # Crear directorio temporal
    TEMP_DIR="/tmp/wrangler-deploy-$site_num"
    rm -rf "$TEMP_DIR"
    mkdir -p "$TEMP_DIR"
    
    # Copiar archivo HTML
    cp "$site_file" "$TEMP_DIR/index.html"
    
    # Crear _routes.json
    echo '{"version":1,"include":["/*"],"exclude":[]}' > "$TEMP_DIR/_routes.json"
    
    # Desplegar
    wrangler pages deploy "$TEMP_DIR" --project-name="$project_name" --branch=master 2>&1 | tail -10
    
    # Limpiar
    rm -rf "$TEMP_DIR"
    
    echo ""
}

# Desplegar los 10 sitios
deploy_site 1 "noticiasobjetivo"
deploy_site 2 "mexicoinformado"
deploy_site 3 "bitacoraurbana"
deploy_site 4 "nodoinformativo"
deploy_site 5 "radiocinconoticias"
deploy_site 6 "mexicoinformado"
deploy_site 7 "noticiasobjetivo"
deploy_site 8 "cbnnoticias"
deploy_site 9 "centralmexico"
deploy_site 10 "tvmexico"

echo "======================================="
echo "✅ DESPLIEGUE COMPLETADO"
echo "======================================="
echo ""
echo "🌐 SITIOS DESPLEGADOS:"
echo "   1. https://noticiasobjetivo.pages.dev"
echo "   2. https://mexicoinformado.pages.dev"
echo "   3. https://bitacoraurbana.pages.dev"
echo "   4. https://nodoinformativo.pages.dev"
echo "   5. https://radiocinconoticias.pages.dev"
echo "   6. https://mexicoinformado.pages.dev"
echo "   7. https://noticiasobjetivo.pages.dev"
echo "   8. https://cbnnoticias.pages.dev"
echo "   9. https://centralmexico.pages.dev"
echo "   10. https://tvmexico.pages.dev"
echo ""
