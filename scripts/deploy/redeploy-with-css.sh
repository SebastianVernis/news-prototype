#!/bin/bash

export CLOUDFLARE_API_TOKEN="2yB_LyzS8ykeKIUv6720ogmi13dBVc5DLzjfdZJZ"

echo "🚀 RE-DESPLIEGUE DE 10 SITIOS CON CSS Y ASSETS"
echo "================================================"
echo ""

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITES_DIR="${SITES_DIR:-$ROOT_DIR/sites}"
TEMPLATES_DIR="$SITES_DIR/templates"
ASSETS_DIR="${NEWS_ASSETS_DIR:-$ROOT_DIR/assets}"

deploy_site_with_assets() {
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
    
    # Copiar templates CSS
    if [ -d "$TEMPLATES_DIR" ]; then
        cp -r "$TEMPLATES_DIR" "$TEMP_DIR/templates"
        echo "   ✅ CSS copiado"
    else
        echo "   ⚠️ Templates no encontrados"
    fi
    
    # Copiar assets (imágenes)
    if [ -d "$ASSETS_DIR" ]; then
        cp -r "$ASSETS_DIR" "$TEMP_DIR/assets"
        echo "   ✅ Assets copiados"
    else
        echo "   ⚠️ Assets no encontrados"
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
EOF
    
    # Crear _routes.json
    echo '{"version":1,"include":["/*"],"exclude":[]}' > "$TEMP_DIR/_routes.json"
    
    # Desplegar
    echo "   🚀 Desplegando..."
    sudo CLOUDFLARE_API_TOKEN="2yB_LyzS8ykeKIUv6720ogmi13dBVc5DLzjfdZJZ" wrangler pages deploy "$TEMP_DIR" --project-name="$project_name" --branch=main 2>&1 | grep -E "(Deployment complete|https://.*pages\.dev)"
    
    # Limpiar
    rm -rf "$TEMP_DIR"
    
    echo ""
}

# Re-desplegar los 10 sitios con CSS y assets
deploy_site_with_assets 1 "noticiasobjetivo"
deploy_site_with_assets 2 "mexicoinformado"
deploy_site_with_assets 3 "bitacoraurbana"
deploy_site_with_assets 4 "nodoinformativo"
deploy_site_with_assets 5 "radiocinconoticias"
deploy_site_with_assets 6 "mexicoinformado"
deploy_site_with_assets 7 "noticiasobjetivo"
deploy_site_with_assets 8 "cbnnoticias"
deploy_site_with_assets 9 "centralmexico"
deploy_site_with_assets 10 "tvmexico"

echo "================================================"
echo "✅ RE-DESPLIEGUE COMPLETADO CON CSS Y ASSETS"
echo "================================================"
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
