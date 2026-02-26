#!/bin/bash
# Script de Despliegue Total - Red de Noticias Cloudflare

# Lista de proyectos a crear en Pages
SITIOS=(
    "radiocinconoticias" "centralmexico" "tvmexico" "cbnnoticias" 
    "mexicoinformado" "nodoinformativo" "bitacoraurbana" 
    "reportecentralmx" "verticenoticias" "noticiasobjetivo"
)

echo "🛰️  PASO 1: Desplegando el Worker (Cerebro)..."
cd src
# Desplegar y capturar la salida para extraer la URL
DEPLOY_LOG=$(sudo wrangler deploy)
WORKER_URL='https://news-api.sebastianvernis.workers.dev'

if [ -z "$WORKER_URL" ]; then
    echo "❌ Error: No se pudo obtener la URL del Worker. ¿Estás logueado en Cloudflare?"
    exit 1
fi

echo "✅ Worker desplegado en: $WORKER_URL"
API_URL="${WORKER_URL}/api"
cd ..

echo "🗄️  PASO 2: Configurando Base de Datos de Producción..."
sudo wrangler d1 execute news_db --remote --file=src/schema.sql --config=src/wrangler.toml --yes
sudo wrangler d1 execute news_db --remote --file=setup_all_sites.sql --config=src/wrangler.toml --yes
sudo wrangler d1 execute news_db --remote --file=populate_legals.sql --config=src/wrangler.toml --yes

echo "📦 PASO 3: Preparando archivos con la URL de Producción..."
rm -rf dist
mkdir -p dist/site dist/admin

# Preparar Site Template
cp public/index.html dist/site/index.html
cp public/_routes.json dist/site/_routes.json
sed -i "s|http://localhost:8781/api|$API_URL|g" dist/site/index.html

# Preparar Admin Panel
cp -r public/admin/* dist/admin/
sed -i "s|http://localhost:8781/api|$API_URL|g" dist/admin/js/api.js

echo "🌐 PASO 4: Desplegando los 10 sitios independientes..."
for SITE in "${SITIOS[@]}"
do
    echo "   🚀 Desplegando: $SITE"
    sudo wrangler pages project create "$SITE" --production-branch main || true
    sudo wrangler pages deploy dist/site --project-name "$SITE"
done

echo "🔐 PASO 5: Desplegando Panel de Administración..."
sudo wrangler pages project create "noticias-hoy-admin" --production-branch main || true
sudo wrangler pages deploy dist/admin --project-name "noticias-hoy-admin"

echo ""
echo "🎉 ¡DESPLIEGUE FINALIZADO EXITOSAMENTE!"
echo "==========================================="
echo "CMS ADMIN: https://noticias-hoy-admin.pages.dev"
echo "API URL:   $API_URL"
echo "==========================================="
echo "Tus 10 sitios están online y conectados."
