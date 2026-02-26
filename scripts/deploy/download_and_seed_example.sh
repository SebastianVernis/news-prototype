#!/bin/bash

# Ejemplo de uso del sistema de descarga y seed de noticias

echo "=========================================="
echo "Sistema de Descarga de Noticias - Ejemplo"
echo "=========================================="
echo ""

# Paso 1: Descargar y procesar noticias
echo "📥 Paso 1: Descargando noticias..."
echo "   Categorías: política, economía, deportes, tecnología, nacional, internacional, ciencia, entretenimiento"
echo "   Requisitos: mínimo 500 palabras, parafraseo con IA, imágenes descargadas"
echo ""
node seed_news_to_db.js --limit 20

echo ""
echo "=========================================="
echo "📋 Instrucciones para completar el seed:"
echo "=========================================="
echo ""
echo "1. El script generará archivos SQL en ./data/news_downloaded/"
echo ""
echo "2. Para aplicar a la base de datos D1, ejecuta:"
echo "   npx wrangler d1 execute news-db --file=./data/news_downloaded/seed_articles_*.sql"
echo ""
echo "3. O usa la API REST:"
echo "   curl -X POST https://tu-worker.pages.dev/api/articles/bulk \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d @./data/news_downloaded/news_processed_*.json"
echo ""
echo "4. O inserta individualmente:"
echo "   curl -X POST https://tu-worker.pages.dev/api/articles \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"title\":\"...\",\"content\":\"...\",\"category\":\"politica\",...}'"
echo ""
echo "=========================================="
echo "✅ Configuración completada"
echo "=========================================="
