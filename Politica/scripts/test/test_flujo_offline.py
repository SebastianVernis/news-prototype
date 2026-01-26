#!/usr/bin/env python3
"""
Test de Flujo Completo Offline (Sin IA)
Usando LinguisticParaphraser
"""

import sys
import json
import time
from pathlib import Path

# Añadir directorio scripts al path
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))

from linguistic_paraphraser import LinguisticParaphraser
from api.newsapi import fetch_newsapi

def main():
    print("🧪 Test Flujo Offline (Linguistic Paraphraser)...")
    
    # 1. Obtener noticias (o usar mock)
    print("📥 Obteniendo noticia de ejemplo...")
    try:
        articles = fetch_newsapi(page_size=1, silent=True)
    except:
        # Mock si falla API internet
        articles = [{
            'title': 'El gobierno presenta un plan estratégico para energías renovables',
            'description': 'El ministro de energía detalló las nuevas inversiones en parques solares y eólicos para reducir la dependencia de combustibles fósiles en la próxima década.',
            'content': 'El gobierno ha anunciado hoy un ambicioso plan. Se espera que las energías renovables cubran el 50% de la demanda en 2030.',
            'author': 'Redacción',
            'publishedAt': '2026-01-20T10:00:00Z',
            'urlToImage': None
        }]

    if not articles:
        print("❌ No se obtuvieron artículos")
        return

    article = articles[0]
    print(f"Original Title: {article['title']}")
    print(f"Original Desc:  {article['description']}")
    
    # 2. Parafrasear
    print("\n🔄 Parafraseando...")
    rewriter = LinguisticParaphraser()
    
    start = time.time()
    new_article = rewriter.paraphrase_article(article)
    elapsed = time.time() - start
    
    print(f"\nNew Title: {new_article['title']}")
    print(f"New Desc:  {new_article['description']}")
    if 'full_text' in new_article:
        print(f"Full Text: {new_article['full_text'][:100]}...")
        
    print(f"\n⏱️ Tiempo: {elapsed:.4f}s")
    
    # Verificar cambios via levenshtein simple o comparacion
    if new_article['title'] != article['title']:
        print("✅ Título modificado")
    else:
        print("⚠️ Título idéntico (threshold muy alto?)")
        
    if new_article['description'] != article['description']:
        print("✅ Descripción modificada")
    else:
        print("⚠️ Descripción idéntica")

if __name__ == "__main__":
    main()
