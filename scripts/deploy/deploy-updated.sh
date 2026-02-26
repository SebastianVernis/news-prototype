#!/bin/bash

# Deployment script for News Website to Cloudflare

set -e  # Exit on any error

echo "🚀 Starting deployment of News Website to Cloudflare..."

# Check if wrangler is installed
if ! command -v wrangler &> /dev/null; then
    echo "❌ Wrangler CLI is not installed. Installing..."
    npm install -g wrangler
fi

# Login to Cloudflare
echo "🔐 Logging in to Cloudflare..."
wrangler login

# Deploy the frontend to Cloudflare Pages
echo "📤 Deploying frontend to Cloudflare Pages..."
wrangler pages deploy ./public --project-name=noticias-hoy

# Deploy the functions
echo "⚙️ Deploying functions..."
wrangler pages functions deploy functions --project-name=noticias-hoy

echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Your website is now live at: https://noticias-hoy.pages.dev"
echo ""
echo "📋 Next steps:"
echo "   1. Verify that the API endpoints are working correctly"
echo "   2. Check that the new articles are displaying properly"
echo "   3. Test the search functionality"
echo "   4. Verify all categories are showing correct counts"