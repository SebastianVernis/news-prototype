#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     DESPLIEGUE INTERACTIVO DE SITIOS CLOUDFLARE PAGES         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

cd /home/sebastianvernis/ProyectosActivos/cloudflare-news-project

# Definir los sitios por CMS
declare -A SITES
declare -A CMS_NAMES

SITES[originaux]="noticiasobjetivo mexicoinformado bitacoraurbana nodoinformativo cbnnoticias radiocinconoticias centralmexico reportecentralmx tvmexico verticenoticias"
SITES[nuevos]="boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mradios mexicantimes mexico360noticias noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc"
SITES[nuevos2]="centronews noticias123 breakingcentermexico alavistanoticias socialmexiconews tmznews radioabc noticiasintegra"

CMS_NAMES[originaux]="CMS Originaux"
CMS_NAMES[nuevos]="CMS Nuevos"
CMS_NAMES[nuevos2]="CMS Nuevos 2"

TOTAL_SITES=0
for cms in originaux nuevos nuevos2; do
    count=$(echo ${SITES[$cms]} | wc -w)
    TOTAL_SITES=$((TOTAL_SITES + count))
done

echo "📊 Sitios disponibles para desplegar: $TOTAL_SITES"
echo ""
echo "  🔵 CMS Originaux: 10 sitios"
echo "  🟢 CMS Nuevos: 17 sitios"
echo "  🟠 CMS Nuevos 2: 8 sitios"
echo ""
echo "ℹ️  Este script desplegará cada sitio interactivamente"
echo ""

DEPLOYED=0
FAILED=0
SKIPPED=0

# Función para desplegar
deploy_site() {
    local site=$1
    local cms=$2
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🌐 Sitio: $site"
    echo "   CMS: ${CMS_NAMES[$cms]}"
    echo "   URL: https://$site.pages.dev"
    echo ""
    
    if [ ! -d "sites/$site" ]; then
        echo "   ❌ Directorio no encontrado: sites/$site"
        FAILED=$((FAILED + 1))
        return
    fi
    
    read -p "   ¿Desplegar $site? (s/n/saltar/ver): " RESPONSE
    
    if [[ $RESPONSE == "ver" || $RESPONSE == "Ver" ]]; then
        echo ""
        echo "   📁 Archivos en sites/$site:"
        ls -1 "sites/$site/" | head -10 | sed 's/^/      - /'
        echo ""
        read -p "   ¿Desplegar $site? (s/n): " RESPONSE2
        if [[ $RESPONSE2 != "s" && $RESPONSE2 != "S" ]]; then
            echo "   ⏭️  Saltando $site"
            SKIPPED=$((SKIPPED + 1))
            return
        fi
    elif [[ $RESPONSE == "saltar" || $RESPONSE == "Saltar" ]]; then
        echo "   ⏭️  Saltando $site"
        SKIPPED=$((SKIPPED + 1))
        return
    elif [[ $RESPONSE != "s" && $RESPONSE != "S" ]]; then
        echo "   ❌ Omitido $site"
        SKIPPED=$((SKIPPED + 1))
        return
    fi
    
    # Desplegar
    echo "   🚀 Desplegando..."
    cd "sites/$site"
    
    if wrangler pages deploy . --project-name="$site" --branch=master --commit-dirty=true 2>&1 | grep -q "Deployed\|Success\|complete"; then
        echo "   ✅ $site desplegado correctamente"
        echo "   🌐 https://$site.pages.dev"
        DEPLOYED=$((DEPLOYED + 1))
    else
        echo "   ⚠️  Posible error al desplegar $site"
        echo "   💡 Verifica si el proyecto existe en Cloudflare"
        FAILED=$((FAILED + 1))
    fi
    
    cd ../..
}

# Desplegar por CMS
for cms in originaux nuevos nuevos2; do
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  ${CMS_NAMES[$cms]}"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    for site in ${SITES[$cms]}; do
        deploy_site "$site" "$cms"
    done
done

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "✅ DESPLIEGUE COMPLETADO"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📊 Resumen:"
echo "   • Sitios desplegados: $DEPLOYED"
echo "   • Fallidos: $FAILED"
echo "   • Omitidos: $SKIPPED"
echo "   • Total procesado: $((DEPLOYED + FAILED + SKIPPED))"
echo ""

if [ $DEPLOYED -gt 0 ]; then
    echo "🌐 Sitios desplegados y listos para usar!"
    echo ""
    echo "💡 Configura los dominios personalizados en el dashboard de Cloudflare:"
    echo "   https://dash.cloudflare.com"
fi

echo ""

