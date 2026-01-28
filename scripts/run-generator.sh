#!/bin/bash
# Script para ejecutar el sistema automatizado de noticias con IA
# Usa el entorno virtual automáticamente

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🤖 Sistema Automatizado de Noticias con IA${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚙️  Creando entorno virtual...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
    echo ""
fi

# Activar el entorno virtual e instalar dependencias
echo -e "${YELLOW}📦 Instalando/verificando dependencias...${NC}"
venv/bin/pip install -q requests beautifulsoup4 python-dotenv pandas Pillow
echo -e "${GREEN}✅ Dependencias instaladas${NC}"
echo ""

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: Archivo .env no encontrado${NC}"
    echo -e "${YELLOW}💡 Crea un archivo .env con:${NC}"
    echo "NEWSAPI_KEY=tu_api_key"
    echo "BLACKBOX_API_KEY=tu_api_key"
    exit 1
fi

# Verificar que las API keys estén configuradas
if ! grep -q "BLACKBOX_API_KEY" .env || grep -q "tu_api_key_aqui" .env; then
    echo -e "${YELLOW}⚠️  Advertencia: BLACKBOX_API_KEY no configurada en .env${NC}"
    echo -e "${YELLOW}💡 Edita .env y agrega tu API key de Blackbox${NC}"
    echo ""
fi

# Modo de ejecución
MODE="${1:-normal}"

if [ "$MODE" == "test" ]; then
    echo -e "${YELLOW}🧪 MODO PRUEBA: 2 artículos, 5 variaciones${NC}"
    echo ""
    venv/bin/python3 main.py --test
else
    echo -e "${GREEN}🚀 MODO COMPLETO: Ejecutando sistema completo${NC}"
    echo ""
    venv/bin/python3 main.py "$@"
fi

# Verificar resultado
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✨ ¡Proceso completado exitosamente!${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Mostrar estadísticas
    if [ -d "images/news" ]; then
        echo -e "${BLUE}📊 Estadísticas:${NC}"
        
        if [ "$(ls -A images/news/*.jpg 2>/dev/null)" ]; then
            echo -e "  🎨 Imágenes generadas: $(ls images/news/*.jpg 2>/dev/null | wc -l)"
            echo -e "  💾 Espacio usado: $(du -sh images/news/ 2>/dev/null | cut -f1)"
        fi
        
        echo -e "  📂 Ubicación: $(pwd)/images/news/"
        echo ""
    fi
    
    # Mostrar archivos generados
    echo -e "${BLUE}📁 Archivos generados:${NC}"
    ls -lh noticias_*_$(date +%Y%m%d)*.json 2>/dev/null | tail -3 | while read line; do
        filename=$(echo "$line" | awk '{print $9}')
        size=$(echo "$line" | awk '{print $5}')
        echo -e "  • $filename ($size)"
    done
    echo ""
    
    echo -e "${YELLOW}💡 Tip: Abre index.html en tu navegador para ver las plantillas${NC}"
else
    echo ""
    echo -e "${RED}════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}❌ Error en la ejecución${NC}"
    echo -e "${RED}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}💡 Verifica:${NC}"
    echo "  • API keys configuradas en .env"
    echo "  • Conexión a internet"
    echo "  • Logs de error arriba"
fi

exit $EXIT_CODE
