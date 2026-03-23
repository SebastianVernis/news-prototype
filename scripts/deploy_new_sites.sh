#!/bin/bash
# Uso: ./deploy_new_sites.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SITES_DIR="$ROOT_DIR/sites"

# Lista de sitios nuevos
SITES=(
  "boominformativo"
  "capitalpress"
  "diarioexpress"
  "elpulsomexicano"
  "enfoquecapital"
  "enfoquedirecto"
  "formulacdmx"
  "mexicantimes"
  "mexico360noticias"
  "mradio"
  "noticiashorizonte"
  "pulsodiario"
  "puntoclave"
  "puntonoticias"
  "radarinformativo"
  "reportediario"
  "televisionabc"
)

echo "=========================================="
echo "Despliegue de 17 Nuevos Sitios"
echo "=========================================="
echo ""

if [ ! -d "$SITES_DIR" ]; then
  echo "❌ No existe el directorio de sitios: $SITES_DIR"
  exit 1
fi

for site in "${SITES[@]}"; do
  echo "----------------------------------------"
  echo "Desplegando: $site"
  echo "----------------------------------------"

  SITE_DIR="$SITES_DIR/$site"
  if [ ! -d "$SITE_DIR" ]; then
    echo "⚠️  Directorio no encontrado, se omite: $SITE_DIR"
    echo ""
    continue
  fi
  
  # Deploy a Cloudflare Pages
  (cd "$SITE_DIR" && wrangler pages deploy . --project-name="$site" --branch=main)
  
  echo "✅ $site desplegado exitosamente"
  echo ""
done

echo "=========================================="
echo "✅ Todos los sitios fueron desplegados!"
echo "=========================================="
