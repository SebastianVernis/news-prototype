#!/bin/bash

# Script para desplegar todos los sitios a PREVIEW en Cloudflare Pages
# Usage: ./deploy_preview.sh

set -e

SITES_DIR="./sites"
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_RED='\033[0;31m'
COLOR_RESET='\033[0m'

echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo -e "${COLOR_BLUE}Despliegue PREVIEW - Cloudflare Pages${COLOR_RESET}"
echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo ""

# Verificar que wrangler esté instalado
if ! command -v wrangler &> /dev/null; then
    echo -e "${COLOR_RED}Error: wrangler no está instalado. Ejecuta: npm install -g wrangler${COLOR_RESET}"
    exit 1
fi

# Verificar que el directorio sites exista
if [ ! -d "$SITES_DIR" ]; then
    echo -e "${COLOR_RED}Error: El directorio $SITES_DIR no existe${COLOR_RESET}"
    exit 1
fi

# Contador de éxitos y fallos
SUCCESS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

# Lista de sitios a desplegar
SITES=(
    "bitacoraurbana"
    "cbnnoticias"
    "centralmexico"
    "mexicoinformado"
    "nodoinformativo"
    "noticiasobjetivo"
    "radiocinconoticias"
    "reportecentralmx"
    "tvmexico"
    "verticenoticias"
)

# Desplegar cada sitio a preview
for site_name in "${SITES[@]}"; do
    site_dir="$SITES_DIR/$site_name"
    
    # Verificar que el directorio exista
    if [ ! -d "$site_dir" ]; then
        echo -e "${COLOR_YELLOW}⚠️  Saltando '$site_name' (directorio no existe)${COLOR_RESET}"
        continue
    fi
    
    # Verificar que tenga contenido
    if [ -z "$(ls -A "$site_dir" 2>/dev/null)" ]; then
        echo -e "${COLOR_YELLOW}⚠️  Saltando '$site_name' (directorio vacío)${COLOR_RESET}"
        continue
    fi
    
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    
    echo -e "${COLOR_BLUE}----------------------------------------${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}[$TOTAL_COUNT] Desplegando PREVIEW: ${COLOR_GREEN}$site_name${COLOR_RESET}"
    echo -e "${COLOR_BLUE}----------------------------------------${COLOR_RESET}"
    
    # Desplegar a preview usando --branch preview
    if wrangler pages deploy "$site_dir" --project-name "$site_name" --branch preview; then
        echo -e "${COLOR_GREEN}✓ Éxito: $site_name desplegado a PREVIEW${COLOR_RESET}"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo -e "${COLOR_RED}✗ Error: Fallo al desplegar $site_name${COLOR_RESET}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    
    echo ""
    
    # Pausa entre despliegues
    sleep 2
done

# Resumen final
echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo -e "${COLOR_BLUE}Resumen del Despliegue PREVIEW${COLOR_RESET}"
echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo -e "Total procesados: ${COLOR_YELLOW}$TOTAL_COUNT${COLOR_RESET}"
echo -e "Exitosos:         ${COLOR_GREEN}$SUCCESS_COUNT${COLOR_RESET}"
echo -e "Fallidos:         ${COLOR_RED}$FAIL_COUNT${COLOR_RESET}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${COLOR_GREEN}¡Todos los sitios fueron desplegados a PREVIEW exitosamente!${COLOR_RESET}"
    echo -e "${COLOR_BLUE}URLs de preview: https://preview.$site_name.pages.dev${COLOR_RESET}"
else
    echo -e "${COLOR_RED}⚠️  $FAIL_COUNT sitio(s) fallaron. Revisa los errores arriba.${COLOR_RESET}"
    exit 1
fi
