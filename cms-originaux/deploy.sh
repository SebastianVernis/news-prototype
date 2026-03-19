#!/bin/bash
# Deploy script for cms-originaux (10 sitios originales)

set -e

echo "=== Deploying cms-originaux ==="
cd "$(dirname "$0")"

# Install dependencies
npm install

# Deploy Worker
wrangler deploy --config wrangler.toml

echo "=== cms-originaux deployed ==="
echo "Worker URL: https://cms-originaux.sebastianvernis.workers.dev"
echo ""
echo "Next steps:"
echo "1. Set secrets: wrangler secret put ADMIN_TOKEN --name cms-originaux"
echo "2. Set FB tokens: wrangler secret put FB_TOKEN_RADIOCINCONOTICIAS --name cms-originaux"
echo "   (repeat for each site)"
