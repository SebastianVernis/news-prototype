#!/bin/bash

# Set your Cloudflare API token before running:
# export CLOUDFLARE_API_TOKEN="your_token_here"
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "❌ Error: CLOUDFLARE_API_TOKEN not set"
    echo "   Run: export CLOUDFLARE_API_TOKEN=\"your_token_here\""
    exit 1
fi

echo "🚀 CREACIÓN Y DESPLIEGUE DE 10 SITIOS DE NOTICIAS"
echo "=================================================="
echo ""

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITES_DIR="${SITES_DIR:-$ROOT_DIR/sites}"

create_and_deploy_site() {
    local site_num=$1
    local project_name=$2
    local site_file="$SITES_DIR/site${site_num}.html"
    
    echo "📦 Sitio $site_num: $project_name"
    
    # Crear directorio temporal
    TEMP_DIR="/tmp/wrangler-deploy-$site_num"
    rm -rf "$TEMP_DIR"
    mkdir -p "$TEMP_DIR"
    
    # Copiar archivo HTML
    cp "$site_file" "$TEMP_DIR/index.html"
    
    # Crear _routes.json
    echo '{"version":1,"include":["/*"],"exclude":[]}' > "$TEMP_DIR/_routes.json"
    
    # Intentar crear el proyecto primero
    echo "   📁 Creando proyecto..."
    wrangler pages project create "$project_name" --production-branch=main 2>&1 | grep -E "(success|Created|already)" || true

    # Desplegar
    echo "   🚀 Desplegando..."
    wrangler pages deploy "$TEMP_DIR" --project-name="$project_name" --branch=master 2>&1 | tail -5
    
    # Limpiar
    rm -rf "$TEMP_DIR"
    
    echo ""
}

# Crear y desplegar los 10 sitios
create_and_deploy_site 1 "noticiasobjetivo"
create_and_deploy_site 2 "mexicoinformado"
create_and_deploy_site 3 "bitacoraurbana"
create_and_deploy_site 4 "nodoinformativo"
create_and_deploy_site 5 "radiocinconoticias"
create_and_deploy_site 6 "mexicoinformado"
create_and_deploy_site 7 "noticiasobjetivo"
create_and_deploy_site 8 "cbnnoticias"
create_and_deploy_site 9 "centralmexico"
create_and_deploy_site 10 "tvmexico"

echo "=================================================="
echo "✅ PROCESO COMPLETADO"
echo "=================================================="
echo ""
echo "🌐 URLs DE LOS SITIOS:"
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
