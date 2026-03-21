#!/bin/bash

set -e

echo "🚀 DESPLEGANDO PORTAL NEXOPRESS"
echo "================================"
echo ""

cd "$(dirname "$0")"

echo "📍 Directorio: $(pwd)"
echo "🌐 URL destino: https://nexopress.sebastianvernis.space"
echo ""

# Deploy a Cloudflare Pages
wrangler pages deploy . --project-name=nexopress --branch=main

echo ""
echo "================================"
echo "✅ PORTAL DESPLEGADO"
echo ""
echo "🌐 Accede en:"
echo "   https://nexopress.sebastianvernis.space"
echo ""
echo "Los 3 CMS disponibles:"
echo "   • CMS Originaux (10 sitios)"
echo "   • CMS Nuevos (9 sitios)"
echo "   • CMS Nuevos 2 (8 sitios)"
echo ""
