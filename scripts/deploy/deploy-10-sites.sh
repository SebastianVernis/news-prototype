#!/bin/bash

# Script de despliegue de los 10 sitios de noticias
# Usa sudo para evitar problemas de permisos

set -e

echo "🚀 INICIANDO DESPLIEGUE DE 10 SITIOS DE NOTICIAS"
echo "=================================================="
echo ""

# Lista de sitios con sus nombres de proyecto
declare -a SITES=(
    "site1.html:noticiasobjetivo"
    "site2.html:mexicoinformado"
    "site3.html:bitacoraurbana"
    "site4.html:nodoinformativo"
    "site5.html:cbnnoticias"
    "site6.html:radiocinconoticias"
    "site7.html:centralmexico"
    "site8.html:reportecentralmx"
    "site9.html:tvmexico"
    "site10.html:verticenoticias"
)

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITES_DIR="${SITES_DIR:-$ROOT_DIR/sites}"
TEMPLATES_DIR="$SITES_DIR/templates"
ASSETS_DIR="${NEWS_ASSETS_DIR:-$ROOT_DIR/assets}"

# Función para desplegar un sitio individual
deploy_site() {
    local site_file=$1
    local project_name=$2
    
    echo "📦 Desplegando: $project_name"
    echo "   Archivo: $site_file"
    
    # Crear directorio temporal
    TEMP_DIR=$(mktemp -d)
    
    # Copiar archivo HTML como index.html
    cp "$SITES_DIR/$site_file" "$TEMP_DIR/index.html"
    
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
/assets/images/*.jpg
  Content-Type: image/jpeg
/assets/images/*.png
  Content-Type: image/png
EOF
    
    # Crear _routes.json
    cat > "$TEMP_DIR/_routes.json" << EOF
{
  "version": 1,
  "include": ["/*"],
  "exclude": []
}
EOF
    
    # Desplegar con wrangler usando sudo
    cd "$TEMP_DIR"
    sudo -E wrangler pages deploy . --project-name="$project_name" --commit-dirty=true
    
    # Limpiar directorio temporal
    rm -rf "$TEMP_DIR"
    
    echo "   ✅ Desplegado: https://$project_name.pages.dev"
    echo ""
}

# Verificar autenticación
echo "🔐 Verificando autenticación con Cloudflare..."
sudo -E wrangler whoami
echo ""

# Desplegar cada sitio
DEPLOYED_COUNT=0
FAILED_COUNT=0

for site_config in "${SITES[@]}"; do
    IFS=':' read -r site_file project_name <<< "$site_config"
    
    if [ -f "$SITES_DIR/$site_file" ]; then
        if deploy_site "$site_file" "$project_name"; then
            ((DEPLOYED_COUNT++))
        else
            ((FAILED_COUNT++))
            echo "   ❌ Error desplegando $project_name"
        fi
    else
        echo "⚠️  Archivo no encontrado: $SITES_DIR/$site_file"
        ((FAILED_COUNT++))
    fi
done

# Resumen final
echo ""
echo "=================================================="
echo "📊 RESUMEN DEL DESPLIEGUE"
echo "=================================================="
echo "✅ Sitios desplegados: $DEPLOYED_COUNT/10"
echo "❌ Errores: $FAILED_COUNT/10"
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
echo "=================================================="
