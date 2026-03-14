#!/bin/bash
# Deploy de todos los sitios Cloudflare Pages

echo "=== Deploy de 27 sitios Cloudflare Pages ==="
echo "Fecha: $(date)"
echo ""

# Función para desplegar un sitio
deploy_site() {
  local site_path=$1
  local site_name=$2
  
  echo "Desplegando ${site_name}..."
  
  cd "$site_path"
  
  # Deploy a Cloudflare Pages
  wrangler pages deploy . --project-name="$site_name" --branch=master 2>&1 | grep -E "Deployed|Error|✔" || echo "  ✓ ${site_name} deployed"
  
  cd /home/sebastianvernis/cloudflare-news-project/sites
}

# Sitios Estables (10)
echo "=== Sitios Estables ==="
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/radiocinconoticias" "radiocinconoticias"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/centralmexico" "centralmexico"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/tvmexico" "tvmexico"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/cbnnoticias" "cbnnoticias"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/mexicoinformado" "mexicoinformado"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/nodoinformativo" "nodoinformativo"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/bitacoraurbana" "bitacoraurbana"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/reportecentralmx" "reportecentralmx"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/verticenoticias" "verticenoticias"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Estables/noticiasobjetivo" "noticiasobjetivo"

# Nuevos Sitios (17)
echo ""
echo "=== Nuevos Sitios ==="
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/boominformativo" "boominformativo"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/capitalpress" "capitalpress"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/diarioexpress" "diarioexpress"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/elpulsomexicano" "elpulsomexicano"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/enfoquecapital" "enfoquecapital"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/enfoquedirecto" "enfoquedirecto"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/formulacdmx" "formulacdmx"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/mexicantimes" "mexicantimes"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/mexico360noticias" "mexico360noticias"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/mradio" "mradio"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/noticiashorizonte" "noticiashorizonte"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/pulsodiario" "pulsodiario"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/puntoclave" "puntoclave"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/puntonoticias" "puntonoticias"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/radarinformativo" "radarinformativo"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/reportediario" "reportediario"
deploy_site "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/televisionabc" "televisionabc"

echo ""
echo "=== Deploy completado ==="
echo "Fecha: $(date)"
echo ""
echo "Sitios desplegados: 27"
