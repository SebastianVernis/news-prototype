#!/usr/bin/env python3
"""
Cron Job para mantener activo el backend en Render Free Tier

Este script hace ping al backend cada 10 minutos para evitar
que entre en modo sleep por inactividad (15 min sin requests).

Uso:
- Se ejecuta automáticamente como Render Cron Job
- También puede ejecutarse manualmente: python3 keep_alive_cron.py
"""

import os
import sys
import requests
from datetime import datetime


BACKEND_URL = os.getenv('BACKEND_URL', 'https://news-generator-backend.onrender.com')
ENDPOINTS = [
    '/api/health',
    '/api/keep-alive'
]


def ping_endpoint(url: str) -> bool:
    """
    Hace ping a un endpoint
    
    Returns:
        True si el ping fue exitoso, False si falló
    """
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ping exitoso a {url}")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"⚠️  [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ping fallido a {url} - Status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏱️  [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Timeout en {url} (normal si el servicio estaba dormido)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error en {url}: {e}")
        return False


def main():
    """Ejecuta el keep-alive ping"""
    print("="*70)
    print(f"🔄 Keep-Alive Cron Job - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target: {BACKEND_URL}")
    print("="*70)
    
    success_count = 0
    
    for endpoint in ENDPOINTS:
        full_url = f"{BACKEND_URL}{endpoint}"
        if ping_endpoint(full_url):
            success_count += 1
    
    print("="*70)
    print(f"📊 Resultados: {success_count}/{len(ENDPOINTS)} pings exitosos")
    print("="*70)
    
    # Exit code 0 = success (aunque algunos pings fallen está OK)
    # El objetivo es despertar el servicio, no validar todos los endpoints
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n⚠️  Cron job interrumpido por usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
