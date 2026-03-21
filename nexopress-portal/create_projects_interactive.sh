#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     CREACIÓN INTERACTIVA DE PROYECTOS CLOUDFLARE PAGES        ║"
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

echo "📊 Se crearán proyectos para $TOTAL_SITES sitios:"
echo ""
echo "  🔵 CMS Originaux: 10 sitios"
echo "  🟢 CMS Nuevos: 17 sitios"
echo "  🟠 CMS Nuevos 2: 8 sitios"
echo ""
echo "⚠️  Este proceso creará los proyectos en Cloudflare."
echo ""
read -p "¿Deseas continuar? (s/n): " CONFIRM

if [[ $CONFIRM != "s" && $CONFIRM != "S" ]]; then
    echo "❌ Operación cancelada."
    exit 0
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""

CREATED=0
FAILED=0
SKIPPED=0

# Función para crear proyecto
create_project() {
    local site=$1
    local cms=$2
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🌐 Proyecto: $site"
    echo "   CMS: ${CMS_NAMES[$cms]}"
    echo ""
    
    read -p "   ¿Crear proyecto para $site? (s/n/saltar): " RESPONSE
    
    if [[ $RESPONSE == "saltar" || $RESPONSE == "Saltar" ]]; then
        echo "   ⏭️  Saltando $site"
        SKIPPED=$((SKIPPED + 1))
        return
    fi
    
    if [[ $RESPONSE != "s" && $RESPONSE != "S" ]]; then
        echo "   ❌ Omitido $site"
        SKIPPED=$((SKIPPED + 1))
        return
    fi
    
    # Crear el proyecto
    echo "   📦 Creando proyecto en Cloudflare..."
    
    if wrangler pages project create "$site" --production-branch=master 2>&1 | grep -q "Successfully\|already exists"; then
        echo "   ✅ Proyecto $site creado correctamente"
        CREATED=$((CREATED + 1))
    else
        echo "   ⚠️  No se pudo crear $site (puede que ya exista)"
        FAILED=$((FAILED + 1))
    fi
}

# Crear proyectos para cada CMS
for cms in originaux nuevos nuevos2; do
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  ${CMS_NAMES[$cms]}"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    
    for site in ${SITES[$cms]}; do
        create_project "$site" "$cms"
    done
done

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "✅ PROCESO COMPLETADO"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📊 Resumen:"
echo "   • Proyectos creados: $CREATED"
echo "   • Fallidos/Ya existían: $FAILED"
echo "   • Omitidos/Saltados: $SKIPPED"
echo "   • Total procesado: $((CREATED + FAILED + SKIPPED))"
echo ""
echo "🚀 Próximo paso: Desplegar los sitios"
echo "   Usa: ./deploy_all_sites.sh"
echo ""

