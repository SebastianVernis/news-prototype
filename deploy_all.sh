#!/bin/bash
set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       DESPLIEGUE COMPLETO - WORKERS + CMS + SITES            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "PASO 1: Desplegar Workers CMS + Admin UI"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

echo "🔧 Desplegando cms-originaux..."
cd cms-originaux && ./deploy.sh
cd ..

echo ""
echo "🔧 Desplegando cms-nuevos..."
cd cms-nuevos && ./deploy.sh
cd ..

echo ""
echo "🔧 Desplegando cms-nuevos2..."
cd cms-nuevos2 && ./deploy.sh
cd ..

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "PASO 2: Desplegar Sitios Frontend (35 sitios)"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

SITES=(
  "alavistanoticias"
  "bitacoraurbana"
  "boominformativo"
  "breakingcentermexico"
  "capitalpress"
  "cbnnoticias"
  "centralmexico"
  "centronews"
  "diarioexpress"
  "elpulsomexicano"
  "enfoquecapital"
  "enfoquedirecto"
  "formulacdmx"
  "mexicantimes"
  "mexico360noticias"
  "mexicoinformado"
  "mradio"
  "nodoinformativo"
  "noticias123"
  "noticiashorizonte"
  "noticiasintegra"
  "noticiasobjetivo"
  "pulsodiario"
  "puntoclave"
  "puntonoticias"
  "radarinformativo"
  "radioabc"
  "radiocinconoticias"
  "reportecentralmx"
  "reportediario"
  "socialmexiconews"
  "televisionabc"
  "tmznews"
  "tvmexico"
  "verticenoticias"
)

DEPLOYED=0
FAILED=0

for SITE in "${SITES[@]}"; do
  echo "🚀 Desplegando $SITE..."
  if cd "sites/$SITE" 2>/dev/null; then
    if wrangler pages deploy . --project-name="$SITE" --branch=main --commit-dirty=true 2>&1 | tail -1; then
      DEPLOYED=$((DEPLOYED + 1))
    else
      echo "  ⚠️  $SITE - error de deploy"
      FAILED=$((FAILED + 1))
    fi
    cd ../..
  else
    echo "  ⚠️  $SITE - directorio no encontrado"
    FAILED=$((FAILED + 1))
  fi
done

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "✅ DESPLIEGUE COMPLETADO"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📊 Resumen:"
echo "   • 3 Workers CMS desplegados (con Admin UI)"
echo "   • $DEPLOYED/$((DEPLOYED + FAILED)) sitios frontend desplegados"
if [ $FAILED -gt 0 ]; then
  echo "   • $FAILED sitios con errores"
fi
echo ""
echo "🌐 Workers:"
echo "   • cms-originaux: https://cms-originaux.sebastianvernis.workers.dev"
echo "   • cms-nuevos:    https://cms-nuevos.sebastianvernis.workers.dev"
echo "   • cms-nuevos2:   https://cms-nuevos2.sebastianvernis.workers.dev"
echo ""
echo "🖥️  Admin UIs:"
echo "   • https://cms-admin-originaux.pages.dev"
echo "   • https://cms-admin-nuevos.pages.dev"
echo "   • https://cms-admin-nuevos2.pages.dev"
