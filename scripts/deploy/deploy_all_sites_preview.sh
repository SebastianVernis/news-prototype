#!/bin/bash

# Deploy all 10 sites to Cloudflare Pages preview

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

echo "=========================================="
echo "Deploying all sites to preview"
echo "=========================================="

for site in "${SITES[@]}"; do
    echo ""
    echo "--- Deploying $site ---"
    npx wrangler pages deploy "sites/$site" --project-name="$site" --branch=preview --commit-dirty=true
    if [ $? -eq 0 ]; then
        echo "✅ $site deployed successfully"
    else
        echo "❌ $site deployment failed"
    fi
done

echo ""
echo "=========================================="
echo "All deployments completed!"
echo "=========================================="
