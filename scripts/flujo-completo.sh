#!/bin/bash
# Script de flujo completo: Descarga → Parafraseo → Imágenes → Sitios
# Uso: ./flujo-completo.sh [cantidad_noticias] [cantidad_sitios]

set -e

CANTIDAD_NOTICIAS=${1:-5}
CANTIDAD_SITIOS=${2:-10}
VARIACIONES=40

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║  🚀 FLUJO COMPLETO - NEWS PROTOTYPE                              ║"
echo "║  Generación automática de sitios de noticias                     ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Configuración:"
echo "   • Noticias originales: $CANTIDAD_NOTICIAS"
echo "   • Variaciones por noticia: $VARIACIONES"
echo "   • Total de artículos: $((CANTIDAD_NOTICIAS * VARIACIONES))"
echo "   • Sitios a generar: $CANTIDAD_SITIOS"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Cambiar al directorio de scripts
cd "$(dirname "$0")"

# PASO 1: Descargar noticias
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📥 PASO 1/4: Descargando noticias de NewsAPI"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 api/newsapi.py --size "$CANTIDAD_NOTICIAS"

if [ $? -ne 0 ]; then
    echo "❌ Error descargando noticias"
    exit 1
fi

echo ""
echo "✅ Noticias descargadas"
echo ""
sleep 2

# PASO 2: Parafrasear noticias
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✍️  PASO 2/4: Parafraseando noticias (${VARIACIONES} variaciones)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Encontrar el último archivo de noticias
LATEST_NEWS=$(ls -t newsapi_*.json newsdata_*.json worldnews_*.json apitube_*.json 2>/dev/null | head -1)

if [ -z "$LATEST_NEWS" ]; then
    echo "❌ No se encontró archivo de noticias"
    exit 1
fi

echo "📂 Usando: $LATEST_NEWS"

# Llamar al parafraseador con el archivo correcto
python3 -c "
import json
import sys
from paraphrase import NewsParaphraser

# Cargar noticias
with open('$LATEST_NEWS', 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f'📰 Cargados {len(articles)} artículos')
print(f'🎯 Generando ${VARIACIONES} variaciones por artículo...')

# Procesar
paraphraser = NewsParaphraser()
variations = paraphraser.process_articles(articles, variations_per_article=${VARIACIONES})

# Guardar
output_file = 'noticias_paraphrased.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(variations, f, ensure_ascii=False, indent=2)

print(f'\n💾 Guardadas {len(variations)} variaciones en: {output_file}')
"

if [ $? -ne 0 ]; then
    echo "❌ Error parafraseando noticias"
    exit 1
fi

echo ""
echo "✅ Parafraseo completado"
echo ""
sleep 2

# PASO 3: Generar imágenes con IA
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎨 PASO 3/4: Generando imágenes con IA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 -c "
import json
from generate-images-ai import AIImageGenerator
from pathlib import Path

# Cargar noticias parafraseadas
with open('noticias_paraphrased.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

print(f'📰 Procesando {len(articles)} artículos')

# Generar imágenes
generator = AIImageGenerator(output_dir='../images/news')
output_file = generator.process_all_articles(articles)

print(f'\n✅ Imágenes generadas')
print(f'💾 Datos guardados en: {output_file}')
"

if [ $? -ne 0 ]; then
    echo "❌ Error generando imágenes"
    exit 1
fi

echo ""
echo "✅ Imágenes generadas"
echo ""
sleep 2

# PASO 4: Generar sitios HTML
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🏗️  PASO 4/4: Generando ${CANTIDAD_SITIOS} sitios HTML"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 generate-sites.py --cantidad "$CANTIDAD_SITIOS" --no-interactivo

if [ $? -ne 0 ]; then
    echo "❌ Error generando sitios"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "🎉 ¡FLUJO COMPLETADO!"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "📊 Resultados:"
echo "   ✅ Noticias originales: $CANTIDAD_NOTICIAS"
echo "   ✅ Total de artículos: $((CANTIDAD_NOTICIAS * VARIACIONES))"
echo "   ✅ Imágenes generadas: $((CANTIDAD_NOTICIAS * VARIACIONES))"
echo "   ✅ Sitios HTML: $CANTIDAD_SITIOS"
echo ""
echo "📁 Archivos:"
echo "   • Noticias: $LATEST_NEWS"
echo "   • Parafraseadas: noticias_paraphrased.json"
echo "   • Imágenes: ../images/news/"
echo "   • Sitios: ../sites/site*.html"
echo ""
echo "👀 Abre los sitios en tu navegador:"
echo "   file://$(pwd)/../sites/site1.html"
echo ""
