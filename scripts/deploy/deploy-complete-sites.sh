#!/bin/bash

# Script de despliegue completo para los 10 sitios
# Incluye: index, categorías, páginas legales

# Set your Cloudflare API token before running:
# export CLOUDFLARE_API_TOKEN="your_token_here"
if [ -z "$CLOUDFLARE_API_TOKEN" ]; then
    echo "❌ Error: CLOUDFLARE_API_TOKEN not set"
    echo "   Run: export CLOUDFLARE_API_TOKEN=\"your_token_here\""
    exit 1
fi

echo "🚀 DESPLIEGUE COMPLETO DE 10 SITIOS"
echo "===================================="
echo ""

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITES_DIR="${SITES_DIR:-$ROOT_DIR/sites}"
TEMPLATES_DIR="$SITES_DIR/templates"
ASSETS_DIR="${NEWS_ASSETS_DIR:-$ROOT_DIR/assets}"

deploy_complete_site() {
    local site_num=$1
    local project_name=$2
    
    echo "📦 Sitio $site_num: $project_name"
    
    # Crear directorio temporal
    TEMP_DIR="/tmp/wrangler-deploy-$site_num"
    rm -rf "$TEMP_DIR"
    mkdir -p "$TEMP_DIR"
    
    # Copiar TODOS los archivos HTML del sitio
    cp "$SITES_DIR"/index.html "$TEMP_DIR/" 2>/dev/null || true
    cp "$SITES_DIR"/site$site_num.html "$TEMP_DIR/index.html"
    cp "$SITES_DIR"/categoria-*-site$site_num.html "$TEMP_DIR/" 2>/dev/null || true
    cp "$SITES_DIR"/terminos-site$site_num.html "$TEMP_DIR/terminos.html" 2>/dev/null || true
    cp "$SITES_DIR"/privacidad-site$site_num.html "$TEMP_DIR/privacidad.html" 2>/dev/null || true
    cp "$SITES_DIR"/contacto-site$site_num.html "$TEMP_DIR/contacto.html" 2>/dev/null || true
    cp "$SITES_DIR"/acerca-de-site$site_num.html "$TEMP_DIR/acerca-de.html" 2>/dev/null || true
    
    # Copiar templates CSS
    if [ -d "$TEMPLATES_DIR" ]; then
        cp -r "$TEMPLATES_DIR" "$TEMP_DIR/templates"
    fi
    
    # Copiar assets (imágenes)
    if [ -d "$ASSETS_DIR" ]; then
        cp -r "$ASSETS_DIR" "$TEMP_DIR/assets"
    fi
    
    # Crear _headers para MIME types correctos
    cat > "$TEMP_DIR/_headers" << EOF
/templates/css/*.css
  Content-Type: text/css
  Cache-Control: public, max-age=31536000
/assets/images/*.jpg
  Content-Type: image/jpeg
  Cache-Control: public, max-age=31536000
/assets/images/*.png
  Content-Type: image/png
  Cache-Control: public, max-age=31536000
/*.html
  Content-Type: text/html
EOF
    
    # Crear _routes.json
    echo '{"version":1,"include":["/*"],"exclude":[]}' > "$TEMP_DIR/_routes.json"
    
    # Desplegar
    echo "   🚀 Desplegando..."
    wrangler pages deploy "$TEMP_DIR" --project-name="$project_name" --branch=master 2>&1 | grep -E "(Deployment complete|https://.*pages\.dev|Uploading)" | head -5
    
    # Limpiar
    rm -rf "$TEMP_DIR"
    
    echo ""
}

# Desplegar los 10 sitios
deploy_complete_site 1 "noticiasobjetivo"
deploy_complete_site 2 "mexicoinformado"
deploy_complete_site 3 "bitacoraurbana"
deploy_complete_site 4 "nodoinformativo"
deploy_complete_site 5 "radiocinconoticias"
deploy_complete_site 6 "mexicoinformado"
deploy_complete_site 7 "noticiasobjetivo"
deploy_complete_site 8 "cbnnoticias"
deploy_complete_site 9 "centralmexico"
deploy_complete_site 10 "tvmexico"

echo "===================================="
echo "✅ DESPLIEGUE COMPLETADO"
echo "===================================="
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
echo "📁 Cada sitio incluye:"
echo "   ✅ index.html (página principal)"
echo "   ✅ 6 páginas de categorías"
echo "   ✅ 4 páginas legales"
echo "   ✅ CSS y assets completos"
echo ""
