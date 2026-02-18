#!/bin/bash
# Script para ejecutar todas las APIs de noticias secuencialmente
# Uso: ./run_all_apis.sh [test]

set -e  # Detener en caso de error

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║  🤖 SISTEMA MULTI-API DE NOTICIAS                                ║"
echo "║  Descarga de noticias usando múltiples APIs                      ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si existe entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias si es necesario
if [ ! -f "venv/.deps_installed" ]; then
    echo "📦 Instalando dependencias..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    touch venv/.deps_installed
fi

# Detectar modo test
MODE="normal"
SIZE=20
if [ "$1" == "test" ]; then
    MODE="test"
    SIZE=5
    echo "⚠️  MODO PRUEBA: Descargando $SIZE artículos por API"
else
    echo "📊 MODO NORMAL: Descargando $SIZE artículos por API"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Array de APIs disponibles
APIS=("newsapi" "apitube" "newsdata" "worldnews")
SUCCESS_COUNT=0
FAIL_COUNT=0
FAILED_APIS=()

# Ejecutar cada API
for API in "${APIS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚀 Ejecutando: $API"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Ejecutar script de la API
    if python3 "${API}.py" --size "$SIZE" 2>&1; then
        echo "✅ $API completado exitosamente"
        ((SUCCESS_COUNT++))
    else
        echo "❌ $API falló (posiblemente API key no configurada)"
        ((FAIL_COUNT++))
        FAILED_APIS+=("$API")
    fi
    
    echo ""
    sleep 2  # Pausa entre APIs
done

# Resumen final
echo "═══════════════════════════════════════════════════════════════════"
echo "📊 RESUMEN DE EJECUCIÓN"
echo "═══════════════════════════════════════════════════════════════════"
echo "✅ APIs exitosas: $SUCCESS_COUNT"
echo "❌ APIs fallidas: $FAIL_COUNT"

if [ $FAIL_COUNT -gt 0 ]; then
    echo ""
    echo "⚠️  APIs que fallaron:"
    for FAILED_API in "${FAILED_APIS[@]}"; do
        echo "   - $FAILED_API"
    done
    echo ""
    echo "💡 Para usar estas APIs, configura las API keys en el archivo .env:"
    for FAILED_API in "${FAILED_APIS[@]}"; do
        KEY_NAME=$(echo "$FAILED_API" | tr '[:lower:]' '[:upper:]')
        case $FAILED_API in
            newsapi)
                echo "   NEWSAPI_KEY=\"tu_api_key\"  # https://newsapi.org/register"
                ;;
            apitube)
                echo "   APITUBE_KEY=\"tu_api_key\"  # https://apitube.io/register"
                ;;
            newsdata)
                echo "   NEWSDATA_KEY=\"tu_api_key\"  # https://newsdata.io/register"
                ;;
            worldnews)
                echo "   WORLDNEWS_KEY=\"tu_api_key\"  # https://worldnewsapi.com/register"
                ;;
        esac
    done
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "🎉 Proceso completado"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Archivos generados:"
ls -lth *.json 2>/dev/null | head -n 10 || echo "   (ninguno encontrado)"
echo ""
