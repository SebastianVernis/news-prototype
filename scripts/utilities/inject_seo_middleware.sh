#!/bin/bash
# Inyectar Middleware de SEO y wrangler.toml en todos los sitios de la red

SITIOS=(
    "noticiasobjetivo" "mexicoinformado" "bitacoraurbana" "nodoinformativo"
    "cbnnoticias" "radiocinconoticias" "centralmexico" "reportecentralmx"
    "tvmexico" "verticenoticias"
)

SOURCE="public/functions/articulo/_middleware.js"
DB_ID="039ec6ab-8f14-4e79-8f02-021df67a6c18"

if [ ! -f "$SOURCE" ]; then
    echo "❌ Error: No se encuentra el archivo fuente en $SOURCE"
    exit 1
fi

echo "🚀 Configurando lógica de SEO y D1 en 10 sitios..."

for sitio in "${SITIOS[@]}"; do
    # 1. Inyectar Middleware
    DEST_FUNC="sites/$sitio/functions/articulo"
    mkdir -p "$DEST_FUNC"
    cp "$SOURCE" "$DEST_FUNC/_middleware.js"
    
    # 2. Inyectar wrangler.toml específico con el campo 'name' requerido por Pages
    CAT_FILE="sites/$sitio/wrangler.toml"
    cat > "$CAT_FILE" <<EOF
name = "$sitio"
pages_build_output_dir = "."
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "news_db"
database_id = "$DB_ID"
EOF

    echo "   ✅ Configurado: sites/$sitio"
done

echo "✨ ¡Listo! Ahora wrangler detectará las Functions automáticamente."
