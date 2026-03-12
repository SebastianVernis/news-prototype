#!/bin/bash
# Actualizar middleware files con lógica WEB_PUBLICADO corregida

echo "=== Actualizando middleware files (WEB_PUBLICADO = 1 por defecto) ==="
echo ""

# Función para actualizar un middleware
update_middleware() {
  local site_path=$1
  local site_slug=$2
  local middleware_file="${site_path}/functions/articulo/_middleware.js"
  
  echo "Actualizando ${site_slug}..."
  
  # Reemplazar la lógica de WEB_PUBLICADO
  sed -i 's/SET WEB_PUBLICADO = 1, WEB_FECHA = datetime.*WHERE ID_PARAFRASEADO = ? AND WEB_PUBLICADO = 0/SET WEB_URL = ?, WEB_FECHA = CASE WHEN WEB_FECHA IS NULL THEN datetime('"'"'now'"'"') ELSE WEB_FECHA END\n      WHERE ID_PARAFRASEADO = ?/g' "$middleware_file"
  
  # Reemplazar el bind para que tenga 2 parámetros (url, article_id) en lugar de 3
  sed -i 's/).bind(url.href, article.para_id, siteSlug)/).bind(url.href, article.para_id)/g' "$middleware_file"
  
  # Actualizar comentario
  sed -i 's/Esto marca el artículo como publicado en este sitio específico/NOTA: WEB_PUBLICADO ya debería ser 1 por defecto al insertar/g' "$middleware_file"
  sed -i 's/Actualizar WEB_PUBLICADO = 1 con timestamp y URL/Actualizar WEB_URL (WEB_PUBLICADO ya debería ser 1)/g' "$middleware_file"
  sed -i 's/Silencioso: el artículo puede no estar en la tabla de este sitio aún/El artículo puede no estar en la tabla de este sitio aún/g' "$middleware_file"
  sed -i 's/Esto es normal para artículos antiguos antes de la migración/Esto es normal para artículos antiguos/g' "$middleware_file"
  sed -i 's/console.log(\[WEB_PUBLISH\] Article.*published to/console.log([WEB_PUBLISH] Article/g' "$middleware_file"
  sed -i 's/${siteSlug}$/accessed on ${siteSlug}/g' "$middleware_file"
  
  echo "  ✓ ${site_slug} actualizado"
}

# Sitios Estables (10)
echo "=== Sitios Estables ==="
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
echo "=== Middleware files actualizados: 26 ==="
