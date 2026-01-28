#!/bin/bash
# Script de prueba para modo interactivo (simula entrada de usuario)

cd "$(dirname "$0")"

echo "🧪 Prueba del Modo Interactivo"
echo "Simulando entrada de usuario..."
echo ""

# Simular entrada:
# - Cantidad: 3 sitios
# - Verificar dominios: No
# - Usar metadatos existentes: No (generar nuevos)
# - Confirmar: Sí

echo -e "3\nn\nn\ns\n" | python3 generate-sites.py
