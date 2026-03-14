#!/bin/bash
# Actualizar middleware files con WEB_PUBLICADO tracking

echo "=== Actualizando middleware files para WEB_PUBLICADO ==="
echo "Fecha: $(date)"
echo ""

# Función para actualizar un middleware
update_middleware() {
  local site_path=$1
  local site_slug=$2
  local template_file="/home/sebastianvernis/cloudflare-news-project/sites/middleware_template.js"
  local output_file="${site_path}/functions/articulo/_middleware.js"
  
  echo "Actualizando ${site_slug}..."
  
  # Reemplazar placeholder con el slug real
  sed "s/SITE_SLUG_PLACEHOLDER/${site_slug}/g" "$template_file" > "$output_file"
  
  echo "  ✓ ${site_slug} actualizado"
}

# Sitios Estables (10)
echo "=== Sitios Estables ==="
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/radiocinconoticias" "radiocinconoticias"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/centralmexico" "centralmexico"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/tvmexico" "tvmexico"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/cbnnoticias" "cbnnoticias"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/mexicoinformado" "mexicoinformado"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/nodoinformativo" "nodoinformativo"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/bitacoraurbana" "bitacoraurbana"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/reportecentralmx" "reportecentralmx"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/verticenoticias" "verticenoticias"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Estables/noticiasobjetivo" "noticiasobjetivo"

# Nuevos Sitios (17)
echo ""
echo "=== Nuevos Sitios ==="
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/boominformativo" "boominformativo"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/capitalpress" "capitalpress"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/diarioexpress" "diarioexpress"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/elpulsomexicano" "elpulsomexicano"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/enfoquecapital" "enfoquecapital"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/enfoquedirecto" "enfoquedirecto"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/formulacdmx" "formulacdmx"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/mexicantimes" "mexicantimes"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/mexico360noticias" "mexico360noticias"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/mradio" "mradio"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/noticiashorizonte" "noticiashorizonte"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/pulsodiario" "pulsodiario"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/puntoclave" "puntoclave"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/puntonoticias" "puntonoticias"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/radarinformativo" "radarinformativo"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/reportediario" "reportediario"
update_middleware "/home/sebastianvernis/cloudflare-news-project/sites/Nuevos/televisionabc" "televisionabc"

echo ""
echo "=== Todos los middleware files actualizados ==="
echo "Fecha: $(date)"

# Limpiar template
rm -f /home/sebastianvernis/cloudflare-news-project/sites/middleware_template.js

echo ""
echo "Archivos actualizados: 27"
