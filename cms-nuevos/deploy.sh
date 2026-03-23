#!/bin/bash
set -e

echo "=== Deploying cms-nuevos ==="
cd "$(dirname "$0")"

npm install

wrangler deploy --config wrangler.toml

echo "--- Deploying Admin UI to Pages ---"
wrangler pages deploy public/admin --project-name=cms-admin-nuevos --branch=main --commit-dirty=true

echo "=== cms-nuevos deployed ==="
echo "Worker API: https://cms-nuevos.sebastianvernis.workers.dev"
echo "Admin UI:   https://cms-admin-nuevos.pages.dev"
