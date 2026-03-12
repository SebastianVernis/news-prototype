#!/bin/bash
# Fix new sites - Remove duplicate article loading script

cd /home/sebastianvernis/cloudflare-news-project/sites/Nuevos

for site in boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  echo "Fixing $site..."
  
  # Remove the duplicate script from index.html (keep only preloader script)
  sed -i '/\/\/ Article Loading/,/})();/d' $site/index.html
  
  echo "✓ Fixed $site"
done

echo "Done!"
