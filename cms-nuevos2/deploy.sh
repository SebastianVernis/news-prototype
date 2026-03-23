#!/bin/bash
set -e

echo "=== Deploying cms-nuevos2 ==="
cd "$(dirname "$0")"

npm install

wrangler deploy --config wrangler.toml

echo "--- Deploying Admin UI to Pages ---"
wrangler pages deploy public/admin --project-name=cms-admin-nuevos2 --branch=main --commit-dirty=true

echo "=== cms-nuevos2 deployed ==="
echo "Worker API: https://cms-nuevos2.sebastianvernis.workers.dev"
echo "Admin UI:   https://cms-admin-nuevos2.pages.dev"
