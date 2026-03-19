#!/bin/bash
# Deploy script for cms-nuevos2 (8 sitios nuevos fase 2)

set -e

echo "=== Deploying cms-nuevos2 ==="
cd "$(dirname "$0")"

# Install dependencies
npm install

# Deploy Worker
wrangler deploy --config wrangler.toml

echo "=== cms-nuevos2 deployed ==="
echo "Worker URL: https://cms-nuevos2.sebastianvernis.workers.dev"
echo ""
echo "Next steps:"
echo "1. Set secrets: wrangler secret put ADMIN_TOKEN --name cms-nuevos2"
echo "2. Configure Facebook tokens for each site when ready"
