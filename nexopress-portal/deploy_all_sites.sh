#!/bin/bash

echo "🚀 DESPLIEGUE MASIVO - TODOS LOS SITIOS FRONTEND"
echo "=================================================="
echo ""

cd /home/sebastianvernis/ProyectosActivos/cloudflare-news-project

# CMS Originaux - 10 sitios
SITES_ORIGINAUX=(
    "noticiasobjetivo"
    "mexicoinformado"
    "bitacoraurbana"
    "nodoinformativo"
    "cbnnoticias"
    "radiocinconoticias"
    "centralmexico"
    "reportecentralmx"
    "tvmexico"
    "verticenoticias"
)

# CMS Nuevos - 17 sitios
SITES_NUEVOS=(
    "boominformativo"
    "capitalpress"
    "diarioexpress"
    "elpulsomexicano"
    "enfoquecapital"
    "enfoquedirecto"
    "formulacdmx"
    "mradio"
    "mexicantimes"
    "mexico360noticias"
    "noticiashorizonte"
    "pulsodiario"
    "puntoclave"
    "puntonoticias"
    "radarinformativo"
    "reportediario"
    "televisionabc"
)

# CMS Nuevos 2 - 8 sitios
SITES_NUEVOS2=(
    "centronews"
    "noticias123"
    "breakingcentermexico"
    "alavistanoticias"
    "socialmexiconews"
    "tmznews"
    "radioabc"
    "noticiasintegra"
)

echo "📊 TOTAL DE SITIOS A DESPLEGAR: $(( ${#SITES_ORIGINAUX[@]} + ${#SITES_NUEVOS[@]} + ${#SITES_NUEVOS2[@]} ))"
echo ""

# Función para desplegar un sitio
deploy_site() {
    local site=$1
    local cms=$2
    
    echo "🌐 Desplegando: $site (CMS: $cms)"
    
    if [ -d "sites/$site" ]; then
        cd "sites/$site"
        
        # Desplegar con wrangler pages
        wrangler pages deploy . --project-name="$site" --branch=master --commit-dirty=true 2>&1 | grep -E "Deployed|Upload|complete|success|Error|error" || echo "   ⚠️  Verificar estado de $site"
        
        cd ../..
        echo "   ✅ $site procesado"
    else
        echo "   ❌ Directorio no encontrado: sites/$site"
    fi
    echo ""
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔵 CMS ORIGINAUX (${#SITES_ORIGINAUX[@]} sitios)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for site in "${SITES_ORIGINAUX[@]}"; do
    deploy_site "$site" "originaux"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🟢 CMS NUEVOS (${#SITES_NUEVOS[@]} sitios)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for site in "${SITES_NUEVOS[@]}"; do
    deploy_site "$site" "nuevos"
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🟠 CMS NUEVOS 2 (${#SITES_NUEVOS2[@]} sitios)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for site in "${SITES_NUEVOS2[@]}"; do
    deploy_site "$site" "nuevos2"
done

echo ""
echo "=================================================="
echo "✅ PROCESO COMPLETADO"
echo "=================================================="
echo ""
echo "📋 Resumen:"
echo "   • CMS Originaux: ${#SITES_ORIGINAUX[@]} sitios"
echo "   • CMS Nuevos: ${#SITES_NUEVOS[@]} sitios"
echo "   • CMS Nuevos 2: ${#SITES_NUEVOS2[@]} sitios"
echo "   • TOTAL: $(( ${#SITES_ORIGINAUX[@]} + ${#SITES_NUEVOS[@]} + ${#SITES_NUEVOS2[@]} )) sitios"
echo ""
echo "🌐 Los sitios estarán disponibles en:"
echo "   https://[nombre-del-sitio].pages.dev"
echo ""

