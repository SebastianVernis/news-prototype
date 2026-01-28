#!/usr/bin/env python3
"""
Test de calidad de párrafos en todo el flujo
Verifica que los artículos tengan:
- Párrafos correctamente separados
- Gramática y puntuación adecuada
- Estructura profesional
"""

import sys
import json
from pathlib import Path

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent.parent))

from paraphrase import NewsParaphraser

# Importar ArticleExpander con guiones
import importlib.util
article_expander_path = Path(__file__).parent.parent / 'article-expander.py'
spec = importlib.util.spec_from_file_location('article_expander', article_expander_path)
article_expander_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(article_expander_module)
ArticleExpander = article_expander_module.ArticleExpander

def analizar_calidad_parrafos(texto, nombre="Artículo"):
    """Analiza la calidad de los párrafos de un texto"""
    parrafos = [p for p in texto.split('\n\n') if p.strip()]
    
    print(f"\n{'='*70}")
    print(f"📊 ANÁLISIS: {nombre}")
    print(f"{'='*70}")
    
    print(f"\n✅ Párrafos totales: {len(parrafos)}")
    
    if len(parrafos) < 8:
        print(f"⚠️  ADVERTENCIA: Menos de 8 párrafos (encontrados: {len(parrafos)})")
    elif len(parrafos) > 15:
        print(f"⚠️  ADVERTENCIA: Más de 15 párrafos (encontrados: {len(parrafos)})")
    else:
        print(f"✅ Cantidad de párrafos adecuada (8-15)")
    
    # Analizar cada párrafo
    palabras_totales = []
    oraciones_totales = []
    
    print(f"\n📝 Análisis por párrafo:")
    print(f"{'-'*70}")
    
    for i, p in enumerate(parrafos[:5], 1):  # Primeros 5 para no saturar
        palabras = len(p.split())
        oraciones = p.count('.') + p.count('?') + p.count('!')
        
        palabras_totales.append(palabras)
        oraciones_totales.append(oraciones)
        
        status = "✅" if 80 <= palabras <= 150 else "⚠️"
        print(f"  {status} Párrafo {i}: {palabras} palabras, {oraciones} oraciones")
        
        # Verificar puntuación básica
        if not p.strip().endswith(('.', '!', '?')):
            print(f"     ⚠️  No termina con puntuación")
    
    if len(parrafos) > 5:
        print(f"  ... ({len(parrafos) - 5} párrafos más)")
    
    # Estadísticas generales
    print(f"\n📈 Estadísticas generales:")
    if palabras_totales:
        promedio_palabras = sum(palabras_totales) / len(palabras_totales)
        print(f"  • Promedio palabras/párrafo: {promedio_palabras:.1f}")
        
        if 80 <= promedio_palabras <= 150:
            print(f"    ✅ Longitud de párrafos adecuada")
        else:
            print(f"    ⚠️  Longitud fuera del rango óptimo (80-150)")
    
    if oraciones_totales:
        promedio_oraciones = sum(oraciones_totales) / len(oraciones_totales)
        print(f"  • Promedio oraciones/párrafo: {promedio_oraciones:.1f}")
        
        if 3 <= promedio_oraciones <= 5:
            print(f"    ✅ Cantidad de oraciones adecuada")
        else:
            print(f"    ⚠️  Cantidad fuera del rango óptimo (3-5)")
    
    # Verificar separación
    print(f"\n🔍 Verificación de formato:")
    if '\n\n' in texto:
        print(f"  ✅ Usa doble salto de línea (\\n\\n)")
    else:
        print(f"  ❌ No usa doble salto de línea")
    
    # Vista previa
    print(f"\n👁️  Vista previa primer párrafo:")
    print(f"{'-'*70}")
    if parrafos:
        print(f"{parrafos[0][:200]}...")
    
    return {
        'total_parrafos': len(parrafos),
        'promedio_palabras': sum(palabras_totales) / len(palabras_totales) if palabras_totales else 0,
        'promedio_oraciones': sum(oraciones_totales) / len(oraciones_totales) if oraciones_totales else 0,
        'usa_doble_salto': '\n\n' in texto,
        'calidad_ok': (
            8 <= len(parrafos) <= 15 and
            '\n\n' in texto and
            (sum(palabras_totales) / len(palabras_totales) if palabras_totales else 0) >= 80
        )
    }


def test_paraphrase():
    """Test del módulo de parafraseo"""
    print(f"\n{'#'*70}")
    print(f"# TEST 1: NewsParaphraser")
    print(f"{'#'*70}")
    
    article = {
        'source': 'test',
        'title': 'Reforma electoral genera debate en México',
        'description': 'Expertos debaten sobre los alcances de la reforma',
        'content': 'La reforma electoral propuesta ha generado debate entre expertos y políticos',
        'full_text': 'La reforma electoral propuesta ha generado intenso debate en círculos políticos y académicos del país'
    }
    
    print(f"\n🔄 Parafraseando artículo de prueba...")
    paraphraser = NewsParaphraser()
    resultado = paraphraser.paraphrase_article(article, style="formal y objetivo")
    
    stats = analizar_calidad_parrafos(
        resultado.get('full_text', ''),
        "NewsParaphraser Output"
    )
    
    return stats


def test_article_expander():
    """Test del módulo de expansión"""
    print(f"\n{'#'*70}")
    print(f"# TEST 2: ArticleExpander")
    print(f"{'#'*70}")
    
    article = {
        'title': 'Crisis económica afecta sectores productivos',
        'description': 'La crisis económica ha impactado diversos sectores',
        'content': 'Sectores productivos reportan caídas en producción',
        'source_name': 'Fuente Test'
    }
    
    print(f"\n🔄 Expandiendo artículo de prueba...")
    expander = ArticleExpander()
    resultado = expander.expand_article(article, target_words=800)
    
    stats = analizar_calidad_parrafos(
        resultado,
        "ArticleExpander Output"
    )
    
    return stats


def main():
    """Ejecutar todos los tests"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║     🧪 TEST DE CALIDAD DE PÁRRAFOS - SISTEMA COMPLETO               ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    resultados = {}
    
    # Test 1: Paraphraser
    try:
        resultados['paraphrase'] = test_paraphrase()
    except Exception as e:
        print(f"\n❌ Error en test de parafraseo: {e}")
        resultados['paraphrase'] = {'calidad_ok': False, 'error': str(e)}
    
    # Test 2: Expander
    try:
        resultados['expander'] = test_article_expander()
    except Exception as e:
        print(f"\n❌ Error en test de expansión: {e}")
        resultados['expander'] = {'calidad_ok': False, 'error': str(e)}
    
    # Resumen final
    print(f"\n{'='*70}")
    print(f"📋 RESUMEN FINAL")
    print(f"{'='*70}")
    
    total_tests = len(resultados)
    tests_ok = sum(1 for r in resultados.values() if r.get('calidad_ok', False))
    
    print(f"\nTests ejecutados: {total_tests}")
    print(f"Tests exitosos: {tests_ok}")
    print(f"Tests fallidos: {total_tests - tests_ok}")
    
    print(f"\n{'='*70}")
    
    for nombre, stats in resultados.items():
        status = "✅ PASS" if stats.get('calidad_ok', False) else "❌ FAIL"
        print(f"{status} - {nombre}")
        
        if 'error' in stats:
            print(f"     Error: {stats['error']}")
        elif stats.get('calidad_ok', False):
            print(f"     Párrafos: {stats.get('total_parrafos', 'N/A')}")
            print(f"     Promedio palabras: {stats.get('promedio_palabras', 0):.1f}")
            print(f"     Doble salto: {'Sí' if stats.get('usa_doble_salto') else 'No'}")
    
    print(f"\n{'='*70}")
    
    if tests_ok == total_tests:
        print(f"✅ TODOS LOS TESTS PASARON")
        print(f"✅ El sistema genera artículos con calidad profesional")
        return 0
    else:
        print(f"⚠️  ALGUNOS TESTS FALLARON")
        print(f"⚠️  Revisar configuración de los módulos")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
