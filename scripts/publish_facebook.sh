#!/bin/bash
# Publicar 2 artículos por sitio en Facebook

TOKEN="17f616e5c86c4988d2f6a6955ba9a98bc3c7ddda4c3557286ba3b80f8aa76291"
BASE_URL="https://news-api.sebastianvernis.workers.dev/api"

echo "================================================================================"
echo "PUBLICANDO 2 ARTÍCULOS POR SITIO EN FACEBOOK"
echo "================================================================================"
echo ""

# Sitios Estables (10)
echo "=== SITIOS ESTABLES (10) ==="
for sitio in radiocinconoticias centralmexico tvmexico cbnnoticias mexicoinformado nodoinformativo bitacoraurbana reportecentralmx verticenoticias noticiasobjetivo; do
  echo ""
  echo "📌 $sitio:"
  
  for i in 1 2; do
    RESULT=$(curl -s -X POST "$BASE_URL/facebook/force-publish/$sitio" -H "Authorization: Bearer $TOKEN")
    
    if echo "$RESULT" | grep -q '"success":true'; then
      POST_ID=$(echo "$RESULT" | grep -o '"fb_post_id":"[^"]*"' | cut -d'"' -f4 | cut -c1-20)
      echo "   ✅ Artículo $i: $POST_ID..."
    else
      ERROR=$(echo "$RESULT" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
      echo "   ⚠️ Artículo $i: $ERROR"
    fi
    sleep 3
  done
done

echo ""
echo ""
echo "=== NUEVOS SITIOS (17) ==="
for sitio in boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  echo ""
  echo "📌 $sitio:"
  
  for i in 1 2; do
    RESULT=$(curl -s -X POST "$BASE_URL/facebook/force-publish/$sitio" -H "Authorization: Bearer $TOKEN")
    
    if echo "$RESULT" | grep -q '"success":true'; then
      POST_ID=$(echo "$RESULT" | grep -o '"fb_post_id":"[^"]*"' | cut -d'"' -f4 | cut -c1-20)
      echo "   ✅ Artículo $i: $POST_ID..."
    else
      ERROR=$(echo "$RESULT" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
      echo "   ⚠️ Artículo $i: $ERROR"
    fi
    sleep 3
  done
done

echo ""
echo "================================================================================"
echo "PUBLICACIÓN COMPLETADA"
echo "================================================================================"
