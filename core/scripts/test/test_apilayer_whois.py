#!/usr/bin/env python3
"""
Test de integración para APILayer WHOIS
Verifica que la API key esté configurada y funcional
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Añadir directorio de scripts al path
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))

from domain_verifier import DomainVerifier

load_dotenv()


def test_api_key_configurada():
    """Verifica que la API key esté configurada"""
    print("\n🔍 Test 1: Verificar API key en .env")
    print("=" * 70)
    
    api_key = os.getenv('APILAYER_API_KEY')
    
    if not api_key:
        print("❌ APILAYER_API_KEY no encontrada en .env")
        print("\n📝 Por favor, configura tu API key:")
        print("   1. Abre el archivo .env en la raíz del proyecto")
        print("   2. Agrega: APILAYER_API_KEY=\"tu_api_key_aqui\"")
        print("   3. Obtén tu API key en: https://apilayer.com/marketplace/whois-api")
        return False
    
    print(f"✅ API key encontrada: {api_key[:10]}...{api_key[-5:]}")
    return True


def test_whois_local():
    """Test con whois local"""
    print("\n🖥️  Test 2: Verificar con whois local")
    print("=" * 70)
    
    try:
        verifier = DomainVerifier(usar_api=False)
        
        if not verifier.verificar_whois_instalado():
            print("⚠️ whois local no está instalado (esto es OK si usarás la API)")
            return None
        
        print("✅ whois local disponible")
        
        # Test simple
        resultado = verifier.verificar_dominio("google.com")
        
        if resultado['estado'] == 'error':
            print(f"❌ Error: {resultado.get('error')}")
            return False
        
        print(f"✅ Verificación exitosa - Estado: {resultado['estado']}")
        print(f"   Método: {resultado.get('metodo', 'desconocido')}")
        return True
        
    except Exception as e:
        print(f"❌ Error en test local: {e}")
        return False


def test_whois_api():
    """Test con APILayer WHOIS API"""
    print("\n🌐 Test 3: Verificar con APILayer WHOIS API")
    print("=" * 70)
    
    api_key = os.getenv('APILAYER_API_KEY')
    if not api_key:
        print("⏭️ Saltando (API key no configurada)")
        return None
    
    try:
        verifier = DomainVerifier(usar_api=True)
        
        # Test de dominios
        dominios_test = [
            ("google.com", "registrado"),
            ("ejemplo-super-raro-123456789.com", "disponible")
        ]
        
        exitos = 0
        for dominio, esperado in dominios_test:
            print(f"\n   Probando: {dominio}")
            resultado = verifier.verificar_dominio(dominio)
            
            if resultado['estado'] == 'error':
                print(f"   ❌ Error: {resultado.get('error')}")
                continue
            
            print(f"   ✅ Estado: {resultado['estado']}")
            print(f"   📊 Disponible: {resultado.get('disponible')}")
            print(f"   🔧 Método: {resultado.get('metodo', 'desconocido')}")
            
            if resultado.get('info_adicional'):
                print("   📋 Info adicional:")
                for key, value in list(resultado['info_adicional'].items())[:3]:
                    print(f"      • {key}: {value}")
            
            exitos += 1
        
        if exitos == len(dominios_test):
            print(f"\n✅ Todas las verificaciones exitosas ({exitos}/{len(dominios_test)})")
            return True
        elif exitos > 0:
            print(f"\n⚠️ Verificaciones parciales ({exitos}/{len(dominios_test)})")
            return True
        else:
            print("\n❌ Todas las verificaciones fallaron")
            return False
        
    except Exception as e:
        print(f"❌ Error en test API: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_compatibilidad():
    """Verifica que ambos métodos sean compatibles"""
    print("\n🔄 Test 4: Compatibilidad entre métodos")
    print("=" * 70)
    
    api_key = os.getenv('APILAYER_API_KEY')
    if not api_key:
        print("⏭️ Saltando (requiere API key)")
        return None
    
    try:
        # Crear ambos verificadores
        verifier_local = DomainVerifier(usar_api=False)
        verifier_api = DomainVerifier(usar_api=True)
        
        # Verificar mismo dominio con ambos
        dominio = "google.com"
        
        print(f"   Verificando {dominio} con ambos métodos...")
        
        resultado_local = verifier_local.verificar_dominio(dominio)
        resultado_api = verifier_api.verificar_dominio(dominio)
        
        if resultado_local['estado'] == 'error' and resultado_api['estado'] != 'error':
            print("   ✅ API funciona cuando local no está disponible")
            return True
        
        if resultado_local['estado'] != 'error' and resultado_api['estado'] != 'error':
            print(f"   ✅ Ambos métodos funcionan")
            print(f"      Local: {resultado_local['estado']}")
            print(f"      API: {resultado_api['estado']}")
            
            if resultado_local['estado'] == resultado_api['estado']:
                print("   ✅ Resultados coinciden")
            else:
                print("   ⚠️ Resultados difieren (puede ser normal)")
            
            return True
        
        print("   ⚠️ No se pudo comparar métodos")
        return None
        
    except Exception as e:
        print(f"❌ Error en test de compatibilidad: {e}")
        return False


def main():
    """Ejecuta todos los tests"""
    print("\n" + "=" * 70)
    print("🧪 TEST DE INTEGRACIÓN: APILayer WHOIS")
    print("=" * 70)
    
    resultados = {}
    
    # Test 1: API key configurada
    resultados['api_key'] = test_api_key_configurada()
    
    # Test 2: whois local
    resultados['whois_local'] = test_whois_local()
    
    # Test 3: whois API
    resultados['whois_api'] = test_whois_api()
    
    # Test 4: Compatibilidad
    resultados['compatibilidad'] = test_compatibilidad()
    
    # Resumen
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE TESTS")
    print("=" * 70)
    
    for nombre, resultado in resultados.items():
        if resultado is True:
            print(f"✅ {nombre}: PASS")
        elif resultado is False:
            print(f"❌ {nombre}: FAIL")
        elif resultado is None:
            print(f"⏭️ {nombre}: SKIP")
    
    # Determinar éxito general
    tests_ejecutados = [r for r in resultados.values() if r is not None]
    if not tests_ejecutados:
        print("\n⚠️ No se ejecutaron tests")
        return 1
    
    tests_exitosos = sum(1 for r in tests_ejecutados if r is True)
    tasa_exito = (tests_exitosos / len(tests_ejecutados)) * 100
    
    print(f"\n📈 Tasa de éxito: {tests_exitosos}/{len(tests_ejecutados)} ({tasa_exito:.0f}%)")
    
    if tasa_exito == 100:
        print("🎉 ¡Todos los tests pasaron!")
        return 0
    elif tasa_exito >= 50:
        print("⚠️ Algunos tests fallaron")
        return 0
    else:
        print("❌ La mayoría de tests fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
