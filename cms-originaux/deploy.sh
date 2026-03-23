#!/bin/bash
set -e

echo "=== Deploying cms-originaux ==="
cd "$(dirname "$0")"

npm install

wrangler deploy --config wrangler.toml

echo "--- Deploying Admin UI to Pages ---"
wrangler pages deploy public/admin --project-name=cms-admin-originaux --branch=main --commit-dirty=true

echo "=== cms-originaux deployed ==="
echo "Worker API: https://cms-originaux.sebastianvernis.workers.dev"
echo "Admin UI:   https://cms-admin-originaux.pages.dev"
