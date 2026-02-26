#!/bin/bash

# Script de despliegue completo para el sitio web de noticias en Cloudflare
# Este script automatiza la creación y despliegue de todos los recursos necesarios

set -e  # Salir en caso de error

echo "🚀 Iniciando despliegue completo del sitio web de noticias..."

# Verificar que wrangler esté instalado
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI no está instalado. Instalando..."
    npm install -g wrangler
fi

# Verificar que jq esté instalado (para manipular JSON)
if ! command -v jq &> /dev/null; then
    echo "❌ JQ no está instalado. Instalando..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get install jq
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install jq
    fi
fi

# Variables de entorno (deberían ser proporcionadas por el usuario)
echo "🔐 Por favor, ingrese las variables de entorno necesarias:"

read -p "Ingrese su Account ID de Cloudflare: " CF_ACCOUNT_ID
read -s -p "Ingrese su API Token de Cloudflare: " CF_API_TOKEN
echo
read -p "Ingrese su clave de API de NewsAPI (opcional): " NEWSAPI_KEY
read -s -p "Ingrese el token de administrador (mínimo 32 caracteres): " ADMIN_TOKEN
echo

# Validar que los campos requeridos no estén vacíos
if [ -z "$CF_ACCOUNT_ID" ] || [ -z "$CF_API_TOKEN" ]; then
    echo "❌ Error: Account ID y API Token son requeridos"
    exit 1
fi

if [ ${#ADMIN_TOKEN} -lt 32 ]; then
    echo "❌ Error: El token de administrador debe tener al menos 32 caracteres"
    exit 1
fi

# Iniciar sesión en Cloudflare
echo "🔐 Iniciando sesión en Cloudflare..."
echo "$CF_API_TOKEN" | wrangler login

# Actualizar el archivo wrangler.toml con los valores proporcionados
echo "📝 Actualizando configuración de wrangler.toml..."
sed -i "s/your_account_id_here/$CF_ACCOUNT_ID/g" wrangler.toml
sed -i "s/your_secure_admin_token_here/$ADMIN_TOKEN/g" wrangler.toml

if [ -n "$NEWSAPI_KEY" ]; then
    sed -i "s/your_newsapi_key_here/$NEWSAPI_KEY/g" wrangler.toml
else
    sed -i "s/your_newsapi_key_here//g" wrangler.toml
fi

# Crear el proyecto de Pages si no existe
echo "🌐 Creando proyecto de Cloudflare Pages..."
if ! wrangler pages project list | grep -q "news-website"; then
    wrangler pages project create news-website --production-branch=main
    echo "✅ Proyecto de Pages creado: news-website"
else
    echo "ℹ️  Proyecto de Pages ya existe: news-website"
fi

# Crear el namespace KV para almacenamiento de artículos
echo "📦 Creando namespace KV..."
KV_NAMESPACE_ID=$(wrangler kv:namespace create "ARTICLES_KV" --env production --preview false)
PREVIEW_KV_NAMESPACE_ID=$(wrangler kv:namespace create "ARTICLES_KV" --env production --preview true)

# Actualizar wrangler.toml con los IDs de KV
sed -i "s/your_kv_namespace_id_here/$KV_NAMESPACE_ID/g" wrangler.toml
sed -i "s/your_preview_kv_namespace_id_here/$PREVIEW_KV_NAMESPACE_ID/g" wrangler.toml

echo "✅ Namespace KV creado con ID: $KV_NAMESPACE_ID"

# Crear base de datos D1 si no existe
echo "🗄️  Verificando base de datos D1..."
if ! wrangler d1 list | grep -q "news_db"; then
    echo "📦 Creando base de datos D1..."
    D1_DATABASE_ID=$(wrangler d1 create news_db | grep -o '[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*')
    echo "✅ Base de datos D1 creada con ID: $D1_DATABASE_ID"
else
    D1_DATABASE_ID=$(wrangler d1 list | grep "news_db" | awk '{print $2}')
    echo "ℹ️  Base de datos D1 ya existe con ID: $D1_DATABASE_ID"
fi

# Actualizar wrangler.toml con el ID de D1
sed -i "s/your_d1_database_id_here/$D1_DATABASE_ID/g" wrangler.toml

# Crear base de datos de vista previa si no existe
PREVIEW_D1_DATABASE_ID=$(wrangler d1 list | grep "news_db_preview\|news_db_dev" | head -n1 | awk '{print $2}')

if [ -z "$PREVIEW_D1_DATABASE_ID" ]; then
    PREVIEW_D1_DATABASE_ID=$(wrangler d1 create news_db_preview | grep -o '[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*')
    echo "✅ Base de datos D1 de vista previa creada con ID: $PREVIEW_D1_DATABASE_ID"
else
    echo "ℹ️  Base de datos D1 de vista previa ya existe con ID: $PREVIEW_D1_DATABASE_ID"
fi

sed -i "s/your_preview_d1_database_id_here/$PREVIEW_D1_DATABASE_ID/g" wrangler.toml

# Desplegar el worker principal
echo "📡 Desplegando worker principal..."
wrangler deploy src/index.js --name news-api

# Desplegar el worker de cron
echo "⏰ Desplegando worker de cron..."
wrangler deploy workers/cron-worker.js --name news-cron

# Desplegar el frontend a Cloudflare Pages
echo "📤 Desplegando frontend a Cloudflare Pages..."
wrangler pages deploy ./public --project-name=news-website

# Configurar variables de entorno en Cloudflare
echo "🔒 Configurando variables de entorno..."
wrangler secret:put ADMIN_TOKEN --env production <<< "$ADMIN_TOKEN"
if [ -n "$NEWSAPI_KEY" ]; then
    wrangler secret:put NEWSAPI_KEY --env production <<< "$NEWSAPI_KEY"
fi

echo "✅ Variables de entorno configuradas"

# Crear archivo de configuración para futuras referencias
cat > deployment-config.json << EOF
{
  "deployment_date": "$(date)",
  "account_id": "$CF_ACCOUNT_ID",
  "project_name": "news-website",
  "kv_namespace_id": "$KV_NAMESPACE_ID",
  "d1_database_id": "$D1_DATABASE_ID",
  "api_worker_url": "https://news-api.$CF_ACCOUNT_ID.workers.dev",
  "cron_worker_url": "https://news-cron.$CF_ACCOUNT_ID.workers.dev",
  "pages_url": "https://news-website.pages.dev",
  "admin_token_set": true,
  "newsapi_key_set": $(if [ -n "$NEWSAPI_KEY" ]; then echo true; else echo false; fi)
}
EOF

echo "✅ Despliegue completado exitosamente!"

echo ""
echo "🌐 Su sitio web está ahora disponible en: https://news-website.pages.dev"
echo "📡 API está disponible en: https://news-api.$CF_ACCOUNT_ID.workers.dev"
echo "⏰ Cron Worker en: https://news-cron.$CF_ACCOUNT_ID.workers.dev"
echo ""
echo "📋 Recursos creados:"
echo "   - Proyecto de Pages: news-website"
echo "   - Worker API: news-api"
echo "   - Worker Cron: news-cron"
echo "   - Namespace KV: $KV_NAMESPACE_ID"
echo "   - Base de datos D1: $D1_DATABASE_ID"
echo ""
echo "🔐 Token de administrador configurado (almacenado de forma segura)"
echo "🔑 API Keys configuradas (almacenadas de forma segura)"
echo ""
echo "📁 Archivo de configuración de despliegue guardado como deployment-config.json"
echo ""
echo "💡 Próximos pasos:"
echo "   1. Visite https://dash.cloudflare.com para ver su configuración"
echo "   2. Configure su dominio personalizado si lo desea"
echo "   3. Pruebe la API en https://news-api.$CF_ACCOUNT_ID.workers.dev/api/health"
echo "   4. Acceda al panel de administración en https://news-website.pages.dev/admin.html"