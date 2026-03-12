#!/bin/bash
# Deploy CMS a Cloudflare Pages

cd /home/sebastianvernis/cloudflare-news-project

echo "=== Deploying CMS to Cloudflare Pages ==="
echo "Project: cms"
echo "Branch: main"
echo ""

wrangler pages deploy public/admin \
  --project-name=cms \
  --branch=main \
  --commit-dirty=true

echo ""
echo "=== Deploy Complete ==="
