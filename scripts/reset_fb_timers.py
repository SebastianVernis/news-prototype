#!/usr/bin/env python3
"""
Script para resetear timers de Facebook y forzar publicación inmediata
"""
import subprocess
import time

SITIOS = [
    'radiocinconoticias', 'centralmexico', 'tvmexico', 'cbnnoticias',
    'mexicoinformado', 'nodoinformativo', 'bitacoraurbana',
    'reportecentralmx', 'verticenoticias', 'noticiasobjetivo'
]

print("=" * 70)
print("=== RESETEO DE TIMERS DE FACEBOOK ===")
print("=" * 70)
print()
print("Reseteando timers KV a 0 (nunca publicado)...")
print()

for sitio in SITIOS:
    kv_key = f"last_fb_post_{sitio}"
    # Usar wrangler para actualizar KV
    cmd = f'echo "0" | wrangler secret put {kv_key} --name news-api 2>&1'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if "Success" in result.stdout or "Updating" in result.stdout:
        print(f"✅ {sitio:<25} → Timer reseteado")
    else:
        print(f"⚠️  {sitio:<25} → {result.stdout.strip()[:50]}")

print()
print("=" * 70)
print("✅ TIMERS RESETEADOS")
print("=" * 70)
print()
print("El próximo cron (en ~25 mins) publicará en TODOS los sitios.")
print()
print("Para verificar estado:")
print("  curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status")
print()
print("=" * 70)
