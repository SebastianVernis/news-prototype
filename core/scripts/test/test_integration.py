#!/usr/bin/env python3
"""
Script de prueba de integración completa
Verifica que todos los componentes funcionen correctamente
"""

import json
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

def test_scrapers():
    """Prueba todos los scrapers individualmente"""
    print("="*70)
    print("🧪 PRUEBA DE SCRAPERS")
    print("="*70)
    
    results = {}
    
    # Test NewsAPI
    try:
        from newsapi import fetch_newsapi
        print("\n1️⃣  Probando NewsAPI.org...")
        articles = fetch_newsapi(page_size=2, enrich=False, silent=True)
        results['newsapi'] = {
            'status': '✅',
            'count': len(articles),
            'sample_keys': list(articles[0].keys()) if articles else []
        }
        print(f"   ✅ NewsAPI: {len(articles)} artículos")
    except Exception as e:
        results['newsapi'] = {'status': '❌', 'error': str(e)}
        print(f"   ❌ NewsAPI: {e}")
    
    # Test APITube
    try:
        from apitube import fetch_apitube
        print("\n2️⃣  Probando APITube.io...")
        articles = fetch_apitube(page_size=2, silent=True)
        results['apitube'] = {
            'status': '✅',
            'count': len(articles),
            'sample_keys': list(articles[0].keys()) if articles else []
        }
        print(f"   ✅ APITube: {len(articles)} artículos")
    except Exception as e:
        results['apitube'] = {'status': '❌', 'error': str(e)}
        print(f"   ❌ APITube: {e}")
    
    # Test Newsdata
    try:
        from newsdata import fetch_newsdata
        print("\n3️⃣  Probando Newsdata.io...")
        articles = fetch_newsdata(page_size=2, silent=True)
        results['newsdata'] = {
            'status': '✅',
            'count': len(articles),
            'sample_keys': list(articles[0].keys()) if articles else []
        }
        print(f"   ✅ Newsdata: {len(articles)} artículos")
    except Exception as e:
        results['newsdata'] = {'status': '❌', 'error': str(e)}
        print(f"   ❌ Newsdata: {e}")
    
    # Test WorldNews
    try:
        from worldnews import fetch_worldnews
        print("\n4️⃣  Probando WorldNewsAPI...")
        articles = fetch_worldnews(number=2, silent=True)
        results['worldnews'] = {
            'status': '✅',
            'count': len(articles),
            'sample_keys': list(articles[0].keys()) if articles else []
        }
        print(f"   ✅ WorldNews: {len(articles)} artículos")
    except Exception as e:
        results['worldnews'] = {'status': '❌', 'error': str(e)}
        print(f"   ❌ WorldNews: {e}")
    
    return results


def test_paraphrase():
    """Prueba el parafraseador con un artículo de ejemplo"""
    print("\n" + "="*70)
    print("📝 PRUEBA DE PARAFRASEADO")
    print("="*70)
    
    try:
        from paraphrase import NewsParaphraser
        
        # Crear artículo de prueba (formato normalizado)
        test_article = {
            'source': 'test',
            'title': 'Título de prueba sobre política',
            'description': 'Esta es una descripción breve del artículo de prueba',
            'content': 'Contenido completo del artículo de prueba con más detalles',
            'full_text': 'Texto completo del artículo de prueba con más detalles e información',
            'url': 'https://example.com/test',
            'published_at': '2024-01-07T10:00:00Z'
        }
        
        print("\n📄 Artículo de prueba:")
        print(f"   Título: {test_article['title']}")
        print(f"   Descripción: {test_article['description'][:50]}...")
        
        paraphraser = NewsParaphraser()
        print("\n🔄 Generando 2 variaciones...")
        
        variations = paraphraser.generate_variations(test_article, num_variations=2)
        
        print(f"\n✅ Generadas {len(variations)} variaciones")
        
        for i, var in enumerate(variations, 1):
            print(f"\n   Variación {i} ({var.get('style')}):")
            print(f"   - Título: {var['title'][:60]}...")
            print(f"   - Descripción: {var['description'][:60]}...")
        
        return {'status': '✅', 'variations': len(variations)}
        
    except Exception as e:
        print(f"\n❌ Error en parafraseado: {e}")
        return {'status': '❌', 'error': str(e)}


def test_format_compatibility():
    """Prueba que el parafraseador maneje ambos formatos"""
    print("\n" + "="*70)
    print("🔀 PRUEBA DE COMPATIBILIDAD DE FORMATOS")
    print("="*70)
    
    try:
        from paraphrase import NewsParaphraser
        paraphraser = NewsParaphraser()
        
        # Formato normalizado (nuevo)
        normalized = {
            'source': 'newsapi',
            'title': 'Título normalizado',
            'description': 'Descripción normalizada',
            'content': 'Contenido normalizado',
            'full_text': 'Texto completo normalizado'
        }
        
        # Formato original (legacy)
        original = {
            'source': {'id': 'test', 'name': 'Test'},
            'title': 'Título original',
            'description': 'Descripción original',
            'content': 'Contenido original'
        }
        
        print("\n1️⃣  Probando formato normalizado...")
        var1 = paraphraser.generate_variations(normalized, num_variations=1)
        print(f"   ✅ Formato normalizado: {len(var1)} variación")
        
        print("\n2️⃣  Probando formato original...")
        var2 = paraphraser.generate_variations(original, num_variations=1)
        print(f"   ✅ Formato original: {len(var2)} variación")
        
        return {'status': '✅', 'normalized': True, 'original': True}
        
    except Exception as e:
        print(f"\n❌ Error en compatibilidad: {e}")
        return {'status': '❌', 'error': str(e)}


def main():
    """Ejecuta todas las pruebas"""
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🧪 SUITE DE PRUEBAS DE INTEGRACIÓN                              ║
║  Sistema Multi-API de Noticias + Parafraseado                    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar API keys
    print("🔑 Verificando API keys...")
    api_keys = {
        'NEWSAPI_KEY': bool(os.getenv('NEWSAPI_KEY')),
        'APITUBE_KEY': bool(os.getenv('APITUBE_KEY')),
        'NEWSDATA_KEY': bool(os.getenv('NEWSDATA_KEY')),
        'WORLDNEWS_KEY': bool(os.getenv('WORLDNEWS_KEY')),
        'BLACKBOX_API_KEY': bool(os.getenv('BLACKBOX_API_KEY'))
    }
    
    for key, exists in api_keys.items():
        status = "✅" if exists else "❌"
        print(f"   {status} {key}: {'Configurada' if exists else 'NO ENCONTRADA'}")
    
    # Ejecutar pruebas
    results = {
        'scrapers': test_scrapers(),
        'paraphrase': test_paraphrase(),
        'compatibility': test_format_compatibility()
    }
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    
    total_tests = 0
    passed_tests = 0
    
    for category, result in results.items():
        if isinstance(result, dict):
            if result.get('status') == '✅':
                passed_tests += 1
            elif isinstance(result, dict) and 'status' not in result:
                # Para scrapers, contar individualmente
                for api_result in result.values():
                    total_tests += 1
                    if api_result.get('status') == '✅':
                        passed_tests += 1
            else:
                total_tests += 1
    
    print(f"\n✅ Pruebas exitosas: {passed_tests}")
    print(f"❌ Pruebas fallidas: {total_tests - passed_tests if total_tests > passed_tests else 0}")
    
    # Guardar resultados
    output_dir = Path(__file__).resolve().parents[3] / 'output' / 'tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'test_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Resultados guardados en: {output_file}")
    print("\n" + "="*70)
    print("🎉 Pruebas completadas")
    print("="*70)


if __name__ == '__main__':
    main()
