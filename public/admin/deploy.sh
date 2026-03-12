#!/bin/bash
# Deploy del CMS a Cloudflare Pages

echo "================================================================================"
echo "DESPLEGANDO CMS EN CLOUDFLARE PAGES"
echo "================================================================================"
echo ""

cd /home/sebastianvernis/cloudflare-news-project/public/admin

echo "📍 Directorio: $(pwd)"
echo ""
echo "Iniciando deploy..."
echo ""

# Deploy con yes para confirmar automáticamente
yes | wrangler pages deploy . --project-name=cms --branch=main 2>&1 | grep -E "Deployed|Upload|complete"

echo ""
echo "================================================================================"
echo "✅ CMS DESPLEGADO"
echo "================================================================================"
echo ""
echo "URL: https://cms.sebastianvernis.space/admin/"
echo ""
