#!/usr/bin/env python3
"""Test para verificar timeouts y endpoint de parafraseo"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

# Agregar directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from paraphrase import NewsParaphraser

# Intentar importar ArticleExpander
try:
    from article_expander import ArticleExpander
    HAS_EXPANDER = True
except ImportError:
    HAS_EXPANDER = False
    print("⚠️  ArticleExpander no disponible, saltando tests relacionados")

load_dotenv()

API_KEY = os.getenv('BLACKBOX_API_KEY')
API_URL = 'https://api.blackbox.ai/chat/completions'


def test_endpoint_direct():
    """Test directo del endpoint"""
    print("\n" + "="*70)
    print("🔍 TEST 1: Endpoint directo de Blackbox API")
    print("="*70)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    payload = {
        "model": "blackboxai/blackbox-pro",
        "messages": [
            {"role": "user", "content": "Di 'hola' en español"}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    print(f"📡 Endpoint: {API_URL}")
    print(f"🔑 API Key: {API_KEY[:20]}...")
    print(f"⏱️  Timeout configurado: 30s")
    
    try:
        start = time.time()
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        elapsed = time.time() - start
        
        print(f"✅ Status code: {response.status_code}")
        print(f"⏱️  Tiempo de respuesta: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"📝 Respuesta: {content[:100]}")
            return True
        else:
            print(f"❌ Error: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏱️  ❌ TIMEOUT después de 30s")
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False


def test_paraphrase_timeout():
    """Test de timeout en parafraseo"""
    print("\n" + "="*70)
    print("🔍 TEST 2: Timeout en NewsParaphraser")
    print("="*70)
    
    article = {
        'source': 'test',
        'title': 'Título de prueba muy corto',
        'description': 'Descripción breve',
        'content': 'Contenido de prueba',
        'full_text': 'Texto completo de prueba'
    }
    
    try:
        paraphraser = NewsParaphraser()
        print(f"⏱️  Timeout configurado en paraphrase.py línea 102: 90s")
        
        start = time.time()
        result = paraphraser.paraphrase_text("Test de timeout", style="formal")
        elapsed = time.time() - start
        
        print(f"✅ Completado en {elapsed:.2f}s")
        print(f"📝 Resultado: {result[:100]}...")
        return True
        
    except requests.exceptions.Timeout as e:
        elapsed = time.time() - start
        print(f"⏱️  ❌ TIMEOUT después de {elapsed:.2f}s")
        print(f"🔧 Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False


def test_expander_timeout():
    """Test de timeout en expansor"""
    print("\n" + "="*70)
    print("🔍 TEST 3: Timeout en ArticleExpander")
    print("="*70)
    
    if not HAS_EXPANDER:
        print("⚠️  ArticleExpander no disponible - SKIP")
        return None
    
    article = {
        'title': 'Título de prueba',
        'description': 'Descripción de prueba',
        'content': 'Contenido de prueba',
        'source_name': 'Test Source'
    }
    
    try:
        expander = ArticleExpander()
        print(f"⏱️  Timeout configurado en article-expander.py línea 134: 45s")
        
        start = time.time()
        result = expander.expand_article(article, target_words=200)
        elapsed = time.time() - start
        
        print(f"✅ Completado en {elapsed:.2f}s")
        print(f"📝 Resultado: {result[:100]}...")
        return True
        
    except requests.exceptions.Timeout as e:
        elapsed = time.time() - start
        print(f"⏱️  ❌ TIMEOUT después de {elapsed:.2f}s")
        print(f"🔧 Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        return False


def test_error_handling():
    """Test de manejo de errores"""
    print("\n" + "="*70)
    print("🔍 TEST 4: Manejo de errores")
    print("="*70)
    
    # Test con API key inválida
    print("\n📍 Test 4.1: API Key inválida")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer invalid_key_12345'
    }
    
    payload = {
        "model": "blackboxai/blackbox-pro",
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: {response.text[:150]}")
        
        if response.status_code == 401:
            print("   ✅ Error 401 manejado correctamente")
        else:
            print(f"   ⚠️  Código inesperado: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test con payload inválido
    print("\n📍 Test 4.2: Payload inválido")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    
    invalid_payload = {
        "model": "modelo_inexistente",
        "messages": []  # Vacío - inválido
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=invalid_payload, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: {response.text[:150]}")
        
        if response.status_code == 400:
            print("   ✅ Error 400 manejado correctamente")
        else:
            print(f"   ⚠️  Código: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")


def main():
    """Ejecutar todos los tests"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🧪 TEST DE TIMEOUTS Y ENDPOINT - SISTEMA DE PARAFRASEO  ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    if not API_KEY:
        print("❌ ERROR: BLACKBOX_API_KEY no encontrada en .env")
        return
    
    results = {}
    
    # Ejecutar tests
    results['endpoint'] = test_endpoint_direct()
    results['paraphrase'] = test_paraphrase_timeout()
    results['expander'] = test_expander_timeout()
    test_error_handling()
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    
    for test_name, passed in results.items():
        if passed is None:
            status = "⏭️  SKIP"
        elif passed:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        print(f"{status} - {test_name}")
    
    # Análisis de timeouts
    print("\n" + "="*70)
    print("⏱️  ANÁLISIS DE TIMEOUTS")
    print("="*70)
    print("paraphrase.py línea 102:      timeout=90s  (paraphrase_text)")
    print("article-expander.py línea 134: timeout=45s  (expand_article)")
    print("\n💡 RECOMENDACIÓN:")
    print("   - Parafraseo: 90s es adecuado para artículos largos")
    print("   - Expansor: 45s puede ser insuficiente, considerar 60-90s")
    print("   - Implementar retry logic con backoff exponencial")
    print("   - Agregar logging detallado de tiempos de respuesta")
    
    print("\n" + "="*70)
    total_passed = sum(1 for v in results.values() if v is True)
    total_tests = sum(1 for v in results.values() if v is not None)
    print(f"✨ RESULTADO FINAL: {total_passed}/{total_tests} tests pasados")
    print("="*70)


if __name__ == '__main__':
    main()
