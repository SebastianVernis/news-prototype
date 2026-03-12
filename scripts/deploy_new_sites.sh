#!/bin/bash
# Script para desplegar los 17 nuevos sitios a Cloudflare Pages
# Uso: ./deploy_new_sites.sh

set -e

cd /home/sebastianvernis/cloudflare-news-project/sites/Nuevos

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

for site in "${SITES[@]}"; do
  echo "----------------------------------------"
  echo "Desplegando: $site"
  echo "----------------------------------------"
  cd "$site"
  
  # Deploy a Cloudflare Pages
  wrangler pages deploy . --project-name="$site" --branch=main
  
  echo "✅ $site desplegado exitosamente"
  echo ""
  
  cd ..
done

echo "=========================================="
echo "✅ Todos los sitios fueron desplegados!"
echo "=========================================="
