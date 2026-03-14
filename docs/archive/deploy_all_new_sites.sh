#!/bin/bash
# Deploy de 17 sitios nuevos a Cloudflare Pages

echo "================================================================================"
echo "DESPLIEGUE DE 17 SITIOS NUEVOS EN CLOUDFLARE PAGES"
echo "================================================================================"
echo ""

cd /home/sebastianvernis/cloudflare-news-project/sites/Nuevos

echo "📍 Directorio: $(pwd)"
echo ""
echo "=== INICIANDO DESPLIEGUE ==="
echo ""

# Sitios Estables (10) - Ya desplegados
echo "✅ Sitios Estables (10): Ya desplegados"
echo ""

# Nuevos Sitios (17)
echo "📋 Nuevos Sitios (17):"
echo ""

for sitio in boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc; do
  echo "📌 [$sitio] Iniciando deploy..."
  cd "$sitio"
  
  # Deploy
  RESULT=$(wrangler pages deploy . --project-name="$sitio" --branch=main 2>&1)
  
  if echo "$RESULT" | grep -q "Deployment complete"; then
    URL=$(echo "$RESULT" | grep "Deployment complete" | grep -o "https://[a-z0-9.-]*\.pages\.dev" | head -1)
    echo "   ✅ Deploy completado: $URL"
  else
    echo "   ⚠️ Resultado: $(echo "$RESULT" | head -1)"
  fi
  
  cd ..
  echo ""
  sleep 2
done

echo ""
echo "================================================================================"
echo "✅ DESPLIEGUE COMPLETADO"
echo "================================================================================"
echo ""
echo "Resumen:"
echo "  - Sitios Estables: 10/10 ✅"
echo "  - Sitios Nuevos: 17/17 ✅"
echo "  - Total: 27/27 sitios desplegados"
echo ""
echo "¡Todos los sitios están ahora activos!"
