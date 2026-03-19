#!/bin/bash
# Deploy script for cms-nuevos (17 sitios nuevos)

set -e

echo "=== Deploying cms-nuevos ==="
cd "$(dirname "$0")"

# Install dependencies
npm install

# Deploy Worker
wrangler deploy --config wrangler.toml

echo "=== cms-nuevos deployed ==="
echo "Worker URL: https://cms-nuevos.sebastianvernis.workers.dev"
echo ""
echo "Next steps:"
echo "1. Set secrets: wrangler secret put ADMIN_TOKEN --name cms-nuevos"
echo "2. Configure Facebook tokens for each site when ready"
