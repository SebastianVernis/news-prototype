#!/bin/bash

echo "=== Verificación de Recursos de Cloudflare ==="
echo ""

echo "1. Verificando cuenta de Cloudflare..."
if command -v wrangler &> /dev/null; then
    echo "✅ Wrangler CLI está instalado"
    echo "Cuenta actual:"
    wrangler whoami 2>/dev/null || echo "⚠️  No autenticado - ejecuta: wrangler login"
else
    echo "❌ Wrangler CLI no está instalado - ejecuta: npm install -g wrangler"
fi

echo ""
echo "2. Verificando proyectos de Pages..."
wrangler pages project list 2>/dev/null || echo "⚠️  No se pudo acceder a la lista de proyectos"

echo ""
echo "3. Verificando Workers..."
wrangler whoami 2>/dev/null || echo "⚠️  No se pudo acceder a la lista de workers"

echo ""
echo "4. Verificando bases de datos D1..."
wrangler d1 list 2>/dev/null || echo "⚠️  No se pudo acceder a la lista de bases de datos"

echo ""
echo "5. Verificando namespaces KV..."
wrangler kv:namespace list 2>/dev/null || echo "⚠️  No se pudo acceder a la lista de namespaces"

echo ""
echo "=== Recursos Requeridos ==="
echo ""
echo "Recursos que debes haber creado manualmente:"
echo "✓ Proyecto de Pages: noticias-hoy"
echo "✓ Worker API: news-api"
echo "✓ Worker Cron: news-cron"
echo "✓ Namespace KV: ARTICLES_KV"
echo "✓ Base de datos D1: news_db"
echo ""
echo "=== Próximos Pasos ==="
echo ""
echo "1. Si aún no lo has hecho, crea manualmente los recursos anteriores en:"
echo "   https://dash.cloudflare.com/"
echo ""
echo "2. Una vez creados, configura las variables de entorno como se indicó"
echo ""
echo "3. Despliega los archivos del sitio web"
echo ""
echo "4. Prueba el acceso al panel de administración"
echo ""
echo "Recuerda tener a mano tu token de admin para acceder al panel."