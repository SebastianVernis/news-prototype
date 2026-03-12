#!/bin/bash
# Script para actualizar todos los middleware files con OG tags optimizadas para Facebook

echo "=== Actualizando middleware files con OG tags optimizadas ==="
echo ""

# Función para actualizar un middleware
update_middleware() {
  local site_path=$1
  local site_slug=$2
  local middleware_file="${site_path}/functions/articulo/_middleware.js"
  
  if [ ! -f "$middleware_file" ]; then
    echo "⚠️  $site_slug: Archivo no encontrado"
    return
  fi
  
  echo "Actualizando $site_slug..."
  
  # Reemplazar sección de manejo de imagen
  sed -i 's/\/\/ Forzar URL absoluta para Facebook/\/\/ Forzar URL absoluta para Facebook - CRÍTICO para que cargue miniaturas/g' "$middleware_file"
  
  # Agregar validación de URL R2 después del if image.startsWith
  sed -i '/if (image.startsWith/a\    }\n    \n    \/\/ Asegurar que la imagen sea accesible públicamente\n    \/\/ Si es R2, verificar que sea URL completa\n    if (image.includes('\''uploads.sebastianvernis.space'\'') \&\& !image.startsWith('\''https://'\'')) {\n      image = `https:\/\/${image}`;\n    }\n    \n    \/\/ Fallback a logo si la imagen es inválida\n    if (!image || image.includes('\''undefined'\'') || image.trim() === '\''\'\'') {\n      image = `${url.origin}\/logo.png`;' "$middleware_file"
  
  # Actualizar comentario de OG tags
  sed -i 's/\/\/ 4. Inyectar Meta Tags/\/\/ 4. Inyectar Meta Tags OPTIMIZADOS para Facebook/g' "$middleware_file"
  
  # Agregar og:image:alt y og:site_name
  sed -i 's/<meta property="og:image:height" content="630" \/>/<meta property="og:image:height" content="630" \/>\n            <meta property="og:image:alt" content="${escapedTitle}" \/>\n            <meta property="og:site_name" content="NexoPress" \/>\n            <meta property="og:locale" content="es_MX" \/>/g' "$middleware_file"
  
  # Agregar twitter:image:alt
  sed -i 's/<meta name="twitter:image" content="${image}" \/>/<meta name="twitter:image" content="${image}" \/>\n            <meta name="twitter:image:alt" content="${escapedTitle}" \/>/g' "$middleware_file"
  
  # Agregar SEO meta tags
  sed -i 's/\/\/ Cache buster para forzar a Facebook a refrescar/<!-- SEO Meta Tags -->\n            <meta name="robots" content="index, follow" \/>\n            \n            \/\/ Cache buster para forzar a Facebook a refrescar/g' "$middleware_file"
  
  echo "  ✓ $site_slug actualizado"
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
echo "=== Middleware files actualizados: 27 ==="
echo ""
echo "⚠️  NOTA: radiocinconoticias ya fue actualizado manualmente."
echo "Ahora debes desplegar todos los sitios con:"
echo "  cd /home/sebastianvernis/cloudflare-news-project/sites"
echo "  bash deploy_all_sites.sh"
