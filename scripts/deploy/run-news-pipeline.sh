#!/bin/bash

# Pipeline completo de descarga, parafraseo y seed de noticias
# Usa OpenRouter con Arcee Trinity Large para parafraseo

echo "=========================================="
echo "  PIPELINE DE NOTICIAS CON OPENROUTER"
echo "=========================================="
echo ""

# Verificar variables de entorno
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  ADVERTENCIA: OPENROUTER_API_KEY no está configurada"
    echo "   El parafraseo usará modo simulado"
    echo ""
    echo "   Para usar Arcee Trinity Large, configura:"
    echo "   export OPENROUTER_API_KEY=sk-or-v1-xxxxxxxx"
    echo ""
fi

# Paso 1: Descargar y parafrasear noticias
echo "📥 PASO 1: Descargando noticias..."
echo "   Categorías: política, economía, deportes, tecnología"
echo "   Nacional, internacional, ciencia, entretenimiento"
echo "   Mínimo: 500 palabras"
echo "   Parafraseo: Arcee Trinity Large (OpenRouter)"
echo ""

node seed_news_to_db.js --pipeline --sql

echo ""
echo "=========================================="
echo "  INSTRUCCIONES PARA COMPLETAR"
echo "=========================================="
echo ""
echo "1. El pipeline ha generado:"
echo "   - Noticias procesadas en: ./data/news_downloaded/"
echo "   - Archivo SQL para importar a D1"
echo ""
echo "2. Para aplicar a la base de datos:"
echo "   npx wrangler d1 execute news-db --file=./data/news_downloaded/seed_articles_*.sql"
echo ""
echo "3. O insertar vía API (requiere worker desplegado):"
echo "   node seed_news_to_db.js --api --url=https://tu-worker.pages.dev"
echo ""
echo "4. Para insertar en bulk (más rápido):"
echo "   node seed_news_to_db.js --api --bulk --url=https://tu-worker.pages.dev"
echo ""
echo "=========================================="
echo "  CONFIGURACIÓN DE OPENROUTER"
echo "=========================================="
echo ""
echo "Modelo: arcee-ai/arcee-trinity-large"
echo "Temperatura: 0.7"
echo "Max tokens: 4000"
echo ""
echo "Para obtener API key de OpenRouter:"
echo "   https://openrouter.ai/keys"
echo ""
echo "=========================================="
