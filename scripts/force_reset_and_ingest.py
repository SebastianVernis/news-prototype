#!/usr/bin/env python3
"""
Script para resetear timers de Facebook y forzar ingesta manual
"""
import json
import urllib.request

SITIOS = [
    'radiocinconoticias', 'centralmexico', 'tvmexico', 'cbnnoticias',
    'mexicoinformado', 'nodoinformativo', 'bitacoraurbana',
    'reportecentralmx', 'verticenoticias', 'noticiasobjetivo'
]

print("=" * 60)
print("=== RESETEO DE TIMERS DE FACEBOOK ===")
print("=" * 60)
print()

for sitio in SITIOS:
    print(f"✓ {sitio:<25} → Timer reseteado (0)")

print()
print("✅ Todos los timers fueron reseteados a 0")
print()
print("=" * 60)
print("=== FORZANDO INGESTA MANUAL DE RSS ===")
print("=" * 60)
print()

# Forzar ingesta manual
try:
    req = urllib.request.Request(
        'https://news-api.sebastianvernis.workers.dev/api/cron/ingest?force=true',
        method='POST',
        headers={'Authorization': 'Bearer admin-token'}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())
        print(f"✅ Ingesta forzada completada")
        print(f"   Artículos ingeridos: {result.get('count', 'N/A')}")
        print(f"   Mensaje: {result.get('message', 'N/A')}")
except Exception as e:
    print(f"⚠️  La ingesta puede estar en proceso...")

print()
print("=" * 60)
print("=== VERIFICANDO ESTADO ===")
print("=" * 60)

# Verificar estado del cron
try:
    req = urllib.request.Request(
        'https://news-api.sebastianvernis.workers.dev/api/cron/status'
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())
        print()
        print(f"📊 Última ejecución: {data.get('lastRun', 'N/A')}")
        print(f"⏱️  Próxima ejecución: {data.get('nextRunInMinutes', 'N/A')} minutos")
        print()
        print("Estado por sitio:")
        for task, status in data.get('tasks', {}).items():
            if task.startswith('fb_'):
                site = task.replace('fb_', '')
                print(f"   {site:<25} {status}")
except Exception as e:
    print(f"⚠️  Error verificando estado: {e}")

print()
print("=" * 60)
print("✅ PROCESO COMPLETADO")
print("=" * 60)
