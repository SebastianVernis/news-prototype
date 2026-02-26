#!/bin/bash

# Script para desplegar los 10 sitios de noticias (principal + 9 adicionales)
# Con corrección para el problema de tipos MIME de CSS

set -e  # Salir si hay algún error

echo "🚀 Iniciando despliegue de 10 sitios de noticias..."

# Verificar que wrangler esté instalado
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI no está instalado. Instalando..."
    npm install -g wrangler
fi

# Verificar autenticación
echo "🔐 Verificando autenticación con Cloudflare..."
wrangler whoami

# Directorio de los sitios generados
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITES_DIR="${SITES_DIR:-$ROOT_DIR/sites}"

# Nombre base para los proyectos
BASE_PROJECT_NAME="noticias-hoy"

# Crear directorio temporal para cada despliegue
TEMP_DIR=$(mktemp -d)
echo "📁 Directorio temporal creado: $TEMP_DIR"

# Función para preparar y desplegar un sitio
deploy_site() {
    local site_num=$1
    local site_file="$SITES_DIR/site${site_num}.html"
    local project_name="${BASE_PROJECT_NAME}-${site_num}"
    
    echo "🌐 Desplegando sitio ${site_num}..."
    
    # Limpiar directorio temporal
    rm -rf "$TEMP_DIR"/*
    
    # Copiar el archivo HTML al directorio temporal
    cp "$site_file" "$TEMP_DIR/index.html"
    
    # Crear directorio para templates y copiar CSS
    mkdir -p "$TEMP_DIR/templates/css"
    TEMPLATES_SOURCE="${NEWS_TEMPLATES_DIR:-$ROOT_DIR/public/templates/css}"
    if [ -d "$TEMPLATES_SOURCE" ]; then
        cp -r "$TEMPLATES_SOURCE" "$TEMP_DIR/templates/"
    fi
    
    # Crear archivo _headers para especificar tipos MIME correctos
    cat > "$TEMP_DIR/_headers" << EOF
/templates/css/*.css
  Content-Type: text/css
EOF
    
    # Crear archivo _routes.json para manejar rutas
    cat > "$TEMP_DIR/_routes.json" << EOF
{
  "version": 1,
  "include": ["/api/*"],
  "exclude": ["/static/*", "/assets/*", "/favicon.ico", "/manifest.json", "/sitemap.xml", "/robots.txt", "/templates/*"]
}
EOF
    
    # Desplegar el sitio
    cd "$TEMP_DIR"
    wrangler pages deploy . --project-name="$project_name"
    
    echo "✅ Sitio ${site_num} desplegado como https://${project_name}.pages.dev"
}

# Desplegar el sitio principal primero
echo "🌐 Desplegando sitio principal..."
cd "$ROOT_DIR"
echo "📤 Desplegando noticias-hoy (sitio principal)..."
wrangler pages deploy ./public --project-name="noticias-hoy"
echo "✅ Sitio principal desplegado en https://noticias-hoy.pages.dev"

# Desplegar cada uno de los 9 sitios adicionales
for i in {1..9}; do
    deploy_site $i
    echo "---"
done

# Limpiar directorio temporal
rm -rf "$TEMP_DIR"

echo "🎉 ¡Todos los 10 sitios han sido desplegados exitosamente!"
echo ""
echo "Sitios disponibles en:"
echo "  - Principal: https://noticias-hoy.pages.dev"
for i in {1..9}; do
    echo "  - Sitio $i: https://${BASE_PROJECT_NAME}-${i}.pages.dev"
done

echo ""
echo "💡 Recuerda que todos los sitios comparten el mismo backend API:"
echo "   - https://noticias-hoy.pages.dev/api/articles"
echo "   - Esto permite gestión centralizada del contenido"
echo ""
echo "🔧 Se han agregado archivos _headers para corregir problemas de tipos MIME"
echo "   - CSS files will be served with correct Content-Type: text/css"
