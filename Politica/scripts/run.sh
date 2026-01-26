#!/bin/bash
# Script de ejecución rápida para el generador de sitios

cd "$(dirname "$0")"

echo "🚀 Iniciando Generador de Sitios de Noticias..."
echo ""

python3 generate-sites.py "$@"
