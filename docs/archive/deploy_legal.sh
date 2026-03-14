#!/bin/bash
cd /home/sebastianvernis/cloudflare-news-project/sites/Nuevos

for site in boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  echo "Deploying $site..."
  wrangler pages deploy ./$site --project-name=$site --branch=main --commit-dirty=true 2>&1 | grep -E "Deployment complete|Error"
  echo "✓ $site"
done

echo "Done!"
