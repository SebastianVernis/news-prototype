#!/bin/bash
# ==============================================
#   Script de Despliegue Rápido
#   Cloudflare News Project
# ==============================================

echo ""
echo "=============================================="
echo "   🚀 Despliegue de Sitios - Cloudflare Pages"
echo "=============================================="
echo ""

# Verificar wrangler
if ! command -v wrangler &> /dev/null; then
    echo "❌ wrangler no está instalado"
    echo "   Ejecuta: npm install -g wrangler"
    exit 1
fi

echo "✅ wrangler instalado: $(wrangler --version)"
echo ""

# Login check
echo "Verificando sesión..."
if ! wrangler whoami &> /dev/null; then
    echo "❌ Necesitas iniciar sesión"
    echo "   Ejecuta: wrangler login"
    exit 1
fi

echo "✅ Sesión activa"
echo ""

# Get root directory (project root)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Sitios
SITES=(
    "radiocinconoticias:Radio Cinco Noticias (Carousel)"
    "centralmexico:Central México (Grid 4)"
    "tvmexico:TV México (Classic)"
    "cbnnoticias:CBN Noticias (Horizontal)"
    "mexicoinformado:México Informado (Magazine)"
    "nodoinformativo:Nodo Informativo (Masonry)"
    "bitacoraurbana:Bitácora Urbana (Masonry)"
    "reportecentralmx:Reporte Central MX (Classic)"
    "verticenoticias:Vértice Noticias (Masonry)"
    "noticiasobjetivo:Noticias Objetivo (Carousel)"
)

echo "📦 Sitios disponibles:"
echo ""
for i in "${!SITES[@]}"; do
    num=$((i + 1))
    site_name="${SITES[$i]}"
    echo "   $num. ${site_name#*:}"
done
echo ""

# Seleccionar sitio
echo "Selecciona un sitio (1-10) o 'all' para todos:"
read -p "> " selection

if [ "$selection" == "all" ]; then
    # Desplegar todos
    for site_info in "${SITES[@]}"; do
        site="${site_info%%:*}"
        echo ""
        echo "=============================================="
        echo "📍 Desplegando: $site"
        echo "=============================================="
        wrangler pages deploy "$ROOT_DIR/sites/$site" --project-name="$site" --branch=main --commit-dirty=true
    done
else
    # Desplegar uno
    if [[ "$selection" =~ ^[0-9]+$ ]] && [ "$selection" -ge 1 ] && [ "$selection" -le "${#SITES[@]}" ]; then
        site_info="${SITES[$((selection-1))]}"
        site="${site_info%%:*}"
        
        echo ""
        echo "=============================================="
        echo "📍 Desplegando: $site"
        echo "=============================================="
        wrangler pages deploy "$ROOT_DIR/sites/$site" --project-name="$site" --branch=main --commit-dirty=true
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ ¡Despliegue exitoso!"
            echo "   URL: https://$site.pages.dev"
        fi
    else
        echo "❌ Opción inválida"
        exit 1
    fi
fi

echo ""
echo "=============================================="
echo "   ¡Despliegue completado!"
echo "=============================================="
echo ""
