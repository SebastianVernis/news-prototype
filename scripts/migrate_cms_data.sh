#!/bin/bash
set -e

echo "=========================================="
echo "MIGRACIÓN DE DATOS A CMS INDEPENDIENTES"
echo "=========================================="
echo ""

SITIOS_ORIGINAUX="radiocinconoticias centralmexico tvmexico cbnnoticias mexicoinformado nodoinformativo bitacoraurbana reportecentralmx verticenoticias noticiasobjetivo"
SITIOS_NUEVOS="boominformativo capitalpress diarioexpress elpulsomexicano enfoquecapital enfoquedirecto formulacdmx mexicantimes mexico360noticias mradio noticiashorizonte pulsodiario puntoclave puntonoticias radarinformativo reportediario televisionabc"
SITIOS_NUEVOS2="alavistanoticias breakingcentermexico centronews noticias123 noticiasintegra radioabc socialmexiconews tmznews"

generate_sites_where() {
    local sites=$1
    local where=""
    for site in $sites; do
        if [ -z "$where" ]; then
            where="SLUG = '$site'"
        else
            where="$where OR SLUG = '$site'"
        fi
    done
    echo "$where"
}

echo "PASO 1: Creando esquemas..."
echo ""

echo "1.1. cms-originaux - Esquema ya existe"
echo "1.2. cms-nuevos - Creando esquema..."
cd /home/sebastianvernis/ProyectosActivos/cloudflare-news-project/cms-nuevos
wrangler d1 execute news_db_cms_nuevos --file=schema.sql --remote 2>&1 | tail -5

echo "1.3. cms-nuevos2 - Creando esquema..."
cd /home/sebastianvernis/ProyectosActivos/cloudflare-news-project/cms-nuevos2
wrangler d1 execute news_db_cms_nuevos2 --file=schema.sql --remote 2>&1 | tail -5

echo ""
echo "=========================================="
echo "PASO 2: Generando scripts de migración..."
echo "=========================================="
echo ""

WHERE_ORIGINAUX=$(generate_sites_where "$SITIOS_ORIGINAUX")
WHERE_NUEVOS=$(generate_sites_where "$SITIOS_NUEVOS")
WHERE_NUEVOS2=$(generate_sites_where "$SITIOS_NUEVOS2")

echo "Generando scripts SQL de migración..."

mkdir -p /tmp/cms_migration

EXPORT_FILE="/tmp/news_db_export.sql"

echo "2.1. Extrayendo datos de SITIOS..."
grep "INSERT INTO \"SITIOS\"" "$EXPORT_FILE" | grep -E "(radiocinconoticias|centralmexico|tvmexico|cbnnoticias|mexicoinformado|nodoinformativo|bitacoraurbana|reportecentralmx|verticenoticias|noticiasobjetivo)" > /tmp/cms_migration/sitios_originaux.sql
grep "INSERT INTO \"SITIOS\"" "$EXPORT_FILE" | grep -E "(boominformativo|capitalpress|diarioexpress|elpulsomexicano|enfoquecapital|enfoquedirecto|formulacdmx|mexicantimes|mexico360noticias|mradio|noticiashorizonte|pulsodiario|puntoclave|puntonoticias|radarinformativo|reportediario|televisionabc)" > /tmp/cms_migration/sitios_nuevos.sql
grep "INSERT INTO \"SITIOS\"" "$EXPORT_FILE" | grep -E "(alavistanoticias|breakingcentermexico|centronews|noticias123|noticiasintegra|radioabc|socialmexiconews|tmznews)" > /tmp/cms_migration/sitios_nuevos2.sql

echo "2.2. Extrayendo datos de CATEGORIAS..."
grep "INSERT INTO \"CATEGORIAS\"" "$EXPORT_FILE" > /tmp/cms_migration/categorias.sql

echo "2.3. Extrayendo datos de USUARIOS..."
grep "INSERT INTO \"USUARIOS\"" "$EXPORT_FILE" > /tmp/cms_migration/usuarios.sql

echo "2.4. Extrayendo datos de LEGALES..."
grep "INSERT INTO \"LEGALES\"" "$EXPORT_FILE" > /tmp/cms_migration/legales.sql 2>/dev/null || echo "-- No hay datos de LEGALES" > /tmp/cms_migration/legales.sql

echo "2.5. Extrayendo datos de CANALES_EXTERNOS..."
grep "INSERT INTO \"CANALES_EXTERNOS\"" "$EXPORT_FILE" > /tmp/cms_migration/canales.sql 2>/dev/null || echo "-- No hay datos de CANALES_EXTERNOS" > /tmp/cms_migration/canales.sql

echo "2.6. Extrayendo datos de MENUS_NAVEGACION..."
grep "INSERT INTO \"MENUS_NAVEGACION\"" "$EXPORT_FILE" > /tmp/cms_migration/menus.sql 2>/dev/null || echo "-- No hay datos de MENUS_NAVEGACION" > /tmp/cms_migration/menus.sql

echo ""
echo "Scripts generados en /tmp/cms_migration/"
echo ""

echo "=========================================="
echo "INSTRUCCIONES PARA COMPLETAR MIGRACIÓN"
echo "=========================================="
echo ""
echo "Los archivos SQL han sido generados. Para completar la migración:"
echo ""
echo "1. Verificar que Cloudflare API token esté configurado:"
echo "   export CLOUDFLARE_API_TOKEN='tu_token_aqui'"
echo ""
echo "2. Migrar datos a cada CMS:"
echo ""
echo "   cms-originaux:"
echo "   cd /home/sebastianvernis/ProyectosActivos/cloudflare-news-project/cms-originaux"
echo "   wrangler d1 execute news_db_cms_originaux --file=/tmp/cms_migration/sitios_originaux.sql --remote"
echo "   wrangler d1 execute news_db_cms_originaux --file=/tmp/cms_migration/categorias.sql --remote"
echo "   wrangler d1 execute news_db_cms_originaux --file=/tmp/cms_migration/usuarios.sql --remote"
echo ""
echo "   cms-nuevos:"
echo "   cd /home/sebastianvernis/ProyectosActivos/cloudflare-news-project/cms-nuevos"
echo "   wrangler d1 execute news_db_cms_nuevos --file=/tmp/cms_migration/sitios_nuevos.sql --remote"
echo "   wrangler d1 execute news_db_cms_nuevos --file=/tmp/cms_migration/categorias.sql --remote"
echo "   wrangler d1 execute news_db_cms_nuevos --file=/tmp/cms_migration/usuarios.sql --remote"
echo ""
echo "   cms-nuevos2:"
echo "   cd /home/sebastianvernis/ProyectosActivos/cloudflare-news-project/cms-nuevos2"
echo "   wrangler d1 execute news_db_cms_nuevos2 --file=/tmp/cms_migration/sitios_nuevos2.sql --remote"
echo "   wrangler d1 execute news_db_cms_nuevos2 --file=/tmp/cms_migration/categorias.sql --remote"
echo "   wrangler d1 execute news_db_cms_nuevos2 --file=/tmp/cms_migration/usuarios.sql --remote"
echo ""
echo "=========================================="
