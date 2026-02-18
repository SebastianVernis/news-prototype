#!/usr/bin/env python3
"""
Script para generar 2 ejemplos completos del flujo
Optimizado para testing rápido
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'api'))

# Imports
from newsapi import fetch_newsapi
from paraphrase import NewsParaphraser

print("""
╔══════════════════════════════════════════════════════════╗
║  🎯 GENERADOR DE 2 EJEMPLOS COMPLETOS                   ║
║  Flujo: Descarga → Parafraseo → JSON                    ║
╚══════════════════════════════════════════════════════════╝
""")

# ============================================================================
# PASO 1: Descargar 2 noticias
# ============================================================================
print("\n" + "="*70)
print("📥 PASO 1: Descargando 2 noticias de NewsAPI")
print("="*70)

noticias = fetch_newsapi(
    query='política México',
    language='es',
    page_size=2,
    enrich=True,
    silent=False
)

if len(noticias) < 2:
    print("❌ ERROR: No se pudieron descargar 2 noticias")
    sys.exit(1)

print(f"✅ Descargadas {len(noticias)} noticias\n")

# ============================================================================
# PASO 2: Parafrasear cada noticia UNA VEZ
# ============================================================================
print("\n" + "="*70)
print("📝 PASO 2: Parafraseando noticias (1 variación cada una)")
print("="*70)

paraphraser = NewsParaphraser()
noticias_parafraseadas = []

for idx, noticia in enumerate(noticias, 1):
    print(f"\n[{idx}/2] Parafraseando: {noticia.get('title', 'Sin título')[:60]}...")
    
    # Generar 1 variación con estilo formal
    variacion = paraphraser.paraphrase_article(noticia, style="formal y objetivo")
    
    # Agregar metadata
    variacion['original_title'] = noticia.get('title', '')
    variacion['paraphrased'] = True
    variacion['style'] = "formal y objetivo"
    
    noticias_parafraseadas.append(variacion)
    
    print(f"  ✅ Título nuevo: {variacion.get('title', 'Sin título')[:70]}...")
    print(f"  📊 Longitud: {len(variacion.get('full_text', ''))} caracteres")

print(f"\n✅ {len(noticias_parafraseadas)} noticias parafraseadas")

# ============================================================================
# PASO 3: Guardar resultados
# ============================================================================
print("\n" + "="*70)
print("💾 PASO 3: Guardando resultados")
print("="*70)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Guardar noticias originales
original_file = f'noticias_originales_{timestamp}.json'
with open(original_file, 'w', encoding='utf-8') as f:
    json.dump(noticias, f, ensure_ascii=False, indent=2)
print(f"  📄 Originales: {original_file}")

# Guardar noticias parafraseadas
paraphrased_file = f'noticias_parafraseadas_{timestamp}.json'
with open(paraphrased_file, 'w', encoding='utf-8') as f:
    json.dump(noticias_parafraseadas, f, ensure_ascii=False, indent=2)
print(f"  📄 Parafraseadas: {paraphrased_file}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "="*70)
print("✨ RESUMEN FINAL")
print("="*70)
print(f"📰 Noticias originales: {len(noticias)}")
print(f"📝 Noticias parafraseadas: {len(noticias_parafraseadas)}")
print(f"💾 Archivos generados:")
print(f"   - {original_file}")
print(f"   - {paraphrased_file}")

# Mostrar preview
print("\n" + "="*70)
print("👀 PREVIEW DE RESULTADOS")
print("="*70)

for idx, noticia in enumerate(noticias_parafraseadas, 1):
    print(f"\n📰 NOTICIA {idx}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Título original: {noticia.get('original_title', 'N/A')[:70]}...")
    print(f"Título nuevo:    {noticia.get('title', 'N/A')[:70]}...")
    print(f"Estilo:          {noticia.get('style', 'N/A')}")
    print(f"Fuente:          {noticia.get('source_name', noticia.get('source', 'N/A'))}")
    print(f"URL:             {noticia.get('url', 'N/A')[:70]}...")
    print(f"\nPrimeras 200 caracteres del artículo:")
    print(f"{noticia.get('full_text', 'Sin contenido')[:200]}...")

print("\n" + "="*70)
print("✅ PROCESO COMPLETADO")
print("="*70)
