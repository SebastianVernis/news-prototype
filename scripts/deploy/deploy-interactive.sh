#!/bin/bash

# Script de despliegue interactivo corregido para el proyecto de noticias en Cloudflare

set -e  # Salir en caso de error

echo "🚀 Bienvenido al Asistente de Despliegue Interactivo para el Sitio Web de Noticias"
echo "==============================================================================="
echo ""

# Función para validar entradas
validate_input() {
    local input="$1"
    local field_name="$2"
    
    if [ -z "$input" ]; then
        echo "❌ Error: $field_name es requerido"
        return 1
    fi
    return 0
}

# Función para validar longitud mínima
validate_min_length() {
    local input="$1"
    local field_name="$2"
    local min_length="$3"
    
    if [ ${#input} -lt $min_length ]; then
        echo "❌ Error: $field_name debe tener al menos $min_length caracteres"
        return 1
    fi
    return 0
}

# Función para confirmar valores
confirm_values() {
    echo ""
    echo "📋 Resumen de valores a configurar:"
    echo "   Account ID: $CF_ACCOUNT_ID"
    echo "   API Token: ${CF_API_TOKEN:0:10}...(oculto)"
    echo "   Admin Token: ${ADMIN_TOKEN:0:10}...(oculto)"
    echo "   NewsAPI Key: ${NEWSAPI_KEY:0:10}...(si se proporcionó)"
    echo "   Nombre del Proyecto: $PROJECT_NAME"
    echo "   Dominio Personalizado: $CUSTOM_DOMAIN"
    echo ""
    
    read -p "¿Deseas continuar con estos valores? (s/n): " confirm
    if [[ ! "$confirm" =~ ^[Ss]$ ]]; then
        echo "❌ Despliegue cancelado por el usuario"
        exit 1
    fi
}

# Función para verificar si wrangler está instalado
check_wrangler() {
    if ! command -v wrangler &> /dev/null; then
        echo "❌ Wrangler CLI no está instalado."
        echo ""
        echo "Por favor, instala Wrangler ejecutando:"
        echo "   npm install -g wrangler"
        echo ""
        echo "Luego vuelve a ejecutar este script."
        exit 1
    fi
}

# Función para verificar si jq está instalado
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo "⚠️  JQ no está instalado. Intentando instalar..."
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get install -y jq
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            brew install jq
        else
            echo "⚠️  No se pudo instalar JQ automáticamente. Continuando sin él..."
        fi
    fi
}

# Verificar prerequisitos
echo "🔍 Verificando prerequisitos..."
check_wrangler
check_jq
echo "✅ Prerequisitos verificados"
echo ""

# Iniciar el proceso interactivo
echo "📝 Por favor, proporciona la siguiente información para configurar tu despliegue:"
echo ""

# 1. Account ID
while true; do
    read -p "Ingrese su Account ID de Cloudflare: " CF_ACCOUNT_ID
    if validate_input "$CF_ACCOUNT_ID" "Account ID"; then
        break
    fi
done

# 2. API Token
while true; do
    read -s -p "Ingrese su API Token de Cloudflare (https://dash.cloudflare.com/profile/api-tokens): " CF_API_TOKEN
    echo ""
    if validate_input "$CF_API_TOKEN" "API Token"; then
        break
    fi
done

# 3. Admin Token
while true; do
    read -s -p "Ingrese un token de administrador (mínimo 32 caracteres): " ADMIN_TOKEN
    echo ""
    if validate_input "$ADMIN_TOKEN" "Admin Token" && validate_min_length "$ADMIN_TOKEN" "Admin Token" 32; then
        break
    fi
done

# 4. NewsAPI Key (opcional)
read -s -p "Ingrese su clave de API de NewsAPI (opcional, presiona Enter para omitir): " NEWSAPI_KEY
echo ""

# 5. Nombre del proyecto
while true; do
    read -p "Ingrese el nombre para su proyecto de Pages (ej: noticias-hoy): " PROJECT_NAME
    if validate_input "$PROJECT_NAME" "Nombre del Proyecto"; then
        break
    fi
done

# 6. Dominio personalizado (opcional)
read -p "Ingrese su dominio personalizado (ej: misitio.com, presiona Enter para usar dominio de Pages): " CUSTOM_DOMAIN
echo ""

# Confirmar valores
confirm_values

# Iniciar sesión en Cloudflare
echo ""
echo "🔐 Iniciando sesión en Cloudflare..."
echo "$CF_API_TOKEN" | wrangler login

# Actualizar wrangler.toml con los valores proporcionados
echo ""
echo "📝 Actualizando configuración de wrangler.toml..."

# Crear backup del archivo original
cp wrangler.toml wrangler.toml.backup.$(date +%s)

# Actualizar el archivo wrangler.toml
sed -i "s/your_account_id_here/$CF_ACCOUNT_ID/g" wrangler.toml
sed -i "s/name = \"news-website\"/name = \"$PROJECT_NAME\"/g" wrangler.toml

# Si se proporcionó un dominio personalizado, actualizar las rutas
if [ -n "$CUSTOM_DOMAIN" ]; then
    sed -i "s|routes = \[\"https://noticiashoy.pages.dev/\*\"\]|routes = [\"https://$CUSTOM_DOMAIN/*\"]|g" wrangler.toml
else
    sed -i "s|routes = \[\"https://noticiashoy.pages.dev/\*\"\]|routes = [\"https://$PROJECT_NAME.pages.dev/*\"]|g" wrangler.toml
fi

echo "✅ Archivo wrangler.toml actualizado"

# Crear el proyecto de Pages
echo ""
echo "🌐 Creando proyecto de Cloudflare Pages..."
if wrangler pages project list 2>/dev/null | grep -q "$PROJECT_NAME"; then
    echo "ℹ️  Proyecto de Pages '$PROJECT_NAME' ya existe"
else
    wrangler pages project create "$PROJECT_NAME" --production-branch=main
    echo "✅ Proyecto de Pages creado: $PROJECT_NAME"
fi

# Crear namespace KV
echo ""
echo "📦 Creando namespace KV para almacenamiento de artículos..."
KV_NAMESPACE_ID=$(wrangler kv:namespace create "ARTICLES_KV" --env production --preview false)
echo "✅ Namespace KV creado con ID: $KV_NAMESPACE_ID"

# Actualizar wrangler.toml con el ID de KV
sed -i "s/your_kv_namespace_id_here/$KV_NAMESPACE_ID/g" wrangler.toml

# Crear base de datos D1
echo ""
echo "🗄️  Verificando base de datos D1..."
D1_DATABASE_NAME="${PROJECT_NAME}_db"
if wrangler d1 list 2>/dev/null | grep -q "$D1_DATABASE_NAME"; then
    D1_DATABASE_ID=$(wrangler d1 list 2>/dev/null | grep "$D1_DATABASE_NAME" | awk '{print $2}')
    echo "ℹ️  Base de datos D1 '$D1_DATABASE_NAME' ya existe con ID: $D1_DATABASE_ID"
else
    echo "📦 Creando base de datos D1..."
    D1_DATABASE_ID=$(wrangler d1 create "$D1_DATABASE_NAME" 2>&1 | grep -o '[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*' | tail -1)
    echo "✅ Base de datos D1 creada con ID: $D1_DATABASE_ID"
fi

# Actualizar wrangler.toml con el ID de D1
sed -i "s/your_d1_database_id_here/$D1_DATABASE_ID/g" wrangler.toml

# Crear base de datos de vista previa si no existe
echo ""
echo "🔍 Verificando base de datos D1 de vista previa..."
PREVIEW_D1_DATABASE_NAME="${PROJECT_NAME}_db_preview"
if wrangler d1 list 2>/dev/null | grep -q "$PREVIEW_D1_DATABASE_NAME"; then
    PREVIEW_D1_DATABASE_ID=$(wrangler d1 list 2>/dev/null | grep "$PREVIEW_D1_DATABASE_NAME" | awk '{print $2}' | head -n1)
    echo "ℹ️  Base de datos D1 de vista previa ya existe con ID: $PREVIEW_D1_DATABASE_ID"
else
    PREVIEW_D1_DATABASE_ID=$(wrangler d1 create "$PREVIEW_D1_DATABASE_NAME" 2>&1 | grep -o '[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*-[a-z0-9-]*' | tail -1)
    echo "✅ Base de datos D1 de vista previa creada con ID: $PREVIEW_D1_DATABASE_ID"
fi

sed -i "s/your_preview_d1_database_id_here/$PREVIEW_D1_DATABASE_ID/g" wrangler.toml

# Desplegar el worker principal
echo ""
echo "📡 Desplegando worker principal (API)..."
wrangler deploy src/index.js --name "${PROJECT_NAME}-api"

# Desplegar el worker de cron
echo ""
echo "⏰ Desplegando worker de cron..."
wrangler deploy workers/cron-worker.js --name "${PROJECT_NAME}-cron"

# Desplegar el frontend a Cloudflare Pages
echo ""
echo "📤 Desplegando frontend a Cloudflare Pages..."
wrangler pages deploy ./public --project-name="$PROJECT_NAME"

# Configurar variables de entorno de forma segura
echo ""
echo "🔒 Configurando variables de entorno de forma segura..."

# Configurar variables usando wrangler secret:put para mayor seguridad
echo "Configurando ADMIN_TOKEN..."
echo "$ADMIN_TOKEN" | wrangler secret:put ADMIN_TOKEN --env production

if [ -n "$NEWSAPI_KEY" ]; then
    echo "Configurando NEWSAPI_KEY..."
    echo "$NEWSAPI_KEY" | wrangler secret:put NEWSAPI_KEY --env production
fi

echo "✅ Variables de entorno configuradas de forma segura"

# Crear archivo de configuración de despliegue
echo ""
echo "📋 Creando archivo de configuración de despliegue..."
cat > deployment-config.json << EOF
{
  "deployment_date": "$(date -u)",
  "account_id": "$CF_ACCOUNT_ID",
  "project_name": "$PROJECT_NAME",
  "custom_domain": "$(if [ -n "$CUSTOM_DOMAIN" ]; then echo "$CUSTOM_DOMAIN"; else echo "null"; fi)",
  "kv_namespace_id": "$KV_NAMESPACE_ID",
  "d1_database_id": "$D1_DATABASE_ID",
  "d1_preview_database_id": "$PREVIEW_D1_DATABASE_ID",
  "api_worker_name": "${PROJECT_NAME}-api",
  "cron_worker_name": "${PROJECT_NAME}-cron",
  "pages_project_name": "$PROJECT_NAME",
  "admin_token_set": true,
  "newsapi_key_set": $(if [ -n "$NEWSAPI_KEY" ]; then echo true; else echo false; fi),
  "deployment_status": "completed"
}
EOF

# Mensaje final de éxito
echo ""
echo "🎉 ¡Despliegue completado exitosamente!"
echo "====================================="
echo ""
echo "🌐 Su sitio web está ahora disponible en:"
if [ -n "$CUSTOM_DOMAIN" ]; then
    echo "   https://$CUSTOM_DOMAIN"
else
    echo "   https://$PROJECT_NAME.pages.dev"
fi
echo ""
echo "📡 Recursos disponibles:"
echo "   API: https://${PROJECT_NAME}-api.$CF_ACCOUNT_ID.workers.dev"
echo "   Cron: https://${PROJECT_NAME}-cron.$CF_ACCOUNT_ID.workers.dev"
echo "   Pages: https://$PROJECT_NAME.pages.dev"
echo ""
echo "📋 Recursos creados:"
echo "   - Proyecto de Pages: $PROJECT_NAME"
echo "   - Worker API: ${PROJECT_NAME}-api"
echo "   - Worker Cron: ${PROJECT_NAME}-cron"
echo "   - Namespace KV: $KV_NAMESPACE_ID"
echo "   - Base de datos D1: $D1_DATABASE_ID"
echo ""
echo "🔐 Acceso al panel de administración:"
echo "   https://$PROJECT_NAME.pages.dev/admin.html"
echo "   (Usa tu ADMIN_TOKEN para autenticarte)"
echo ""
echo "📁 Archivo de configuración de despliegue guardado como deployment-config.json"
echo ""
echo "💡 Próximos pasos:"
echo "   1. Visita https://dash.cloudflare.com para ver tu configuración"
echo "   2. Si usaste un dominio personalizado, configúralo en el panel de Cloudflare"
echo "   3. Prueba la API en https://${PROJECT_NAME}-api.$CF_ACCOUNT_ID.workers.dev/api/health"
echo "   4. Accede al panel de administración con tu token de admin"
echo ""
echo "🔐 Tus credenciales están almacenadas de forma segura en Cloudflare"
echo "🔑 No compartas tu ADMIN_TOKEN con nadie"
echo ""
echo "✅ ¡Tu sitio web de noticias está listo para usar!"