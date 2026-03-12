#!/bin/bash

# Script para desplegar todos los sitios uno por uno con Wrangler Pages
# Usage: bash scripts/deploy/deploy_all_sites.sh

set -e

# Get root directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SITES_DIR="$ROOT_DIR/sites"
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_RED='\033[0;31m'
COLOR_RESET='\033[0m'

echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo -e "${COLOR_BLUE}Despliegue de Sitios - Cloudflare Pages${COLOR_RESET}"
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

# Iterar sobre cada directorio en sites
for site_dir in "$SITES_DIR"/*/; do
    # Verificar que es un directorio válido
    if [ ! -d "$site_dir" ]; then
        continue
    fi
    
    # Obtener nombre del sitio (nombre del directorio)
    site_name=$(basename "$site_dir")
    
    # Verificar que el directorio tenga contenido (al menos un archivo index.html o similar)
    if [ -z "$(ls -A "$site_dir" 2>/dev/null)" ]; then
        echo -e "${COLOR_YELLOW}⚠️  Saltando '$site_name' (directorio vacío)${COLOR_RESET}"
        continue
    fi
    
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    
    echo -e "${COLOR_BLUE}----------------------------------------${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}[$TOTAL_COUNT] Desplegando: ${COLOR_GREEN}$site_name${COLOR_RESET}"
    echo -e "${COLOR_BLUE}----------------------------------------${COLOR_RESET}"
    
    # Entrar al directorio del sitio para que wrangler detecte el wrangler.toml local
    cd "$site_dir"
    
    # Ejecutar wrangler pages deploy
    if wrangler pages deploy "." --project-name "$site_name" --branch main; then
        echo -e "${COLOR_GREEN}✓ Éxito: $site_name desplegado correctamente${COLOR_RESET}"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo -e "${COLOR_RED}✗ Error: Fallo al desplegar $site_name${COLOR_RESET}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    
    # Volver a la raíz
    cd "$ROOT_DIR"
    
    echo ""
    
    # Pequeña pausa entre despliegues para evitar rate limiting
    sleep 2
done

# Resumen final
echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo -e "${COLOR_BLUE}Resumen del Despliegue${COLOR_RESET}"
echo -e "${COLOR_BLUE}========================================${COLOR_RESET}"
echo -e "Total procesados: ${COLOR_YELLOW}$TOTAL_COUNT${COLOR_RESET}"
echo -e "Exitosos:         ${COLOR_GREEN}$SUCCESS_COUNT${COLOR_RESET}"
echo -e "Fallidos:         ${COLOR_RED}$FAIL_COUNT${COLOR_RESET}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${COLOR_GREEN}¡Todos los sitios fueron desplegados exitosamente!${COLOR_RESET}"
else
    echo -e "${COLOR_RED}⚠️  $FAIL_COUNT sitio(s) fallaron. Revisa los errores arriba.${COLOR_RESET}"
    exit 1
fi
