#!/usr/bin/env python3
"""
Script para publicar 2 artículos por sitio en Facebook
"""

import requests
import time
from collections import defaultdict

TOKEN = "17f616e5c86c4988d2f6a6955ba9a98bc3c7ddda4c3557286ba3b80f8aa76291"
BASE_URL = "https://news-api.sebastianvernis.workers.dev/api"

SITIOS = [
    "radiocinconoticias", "centralmexico", "tvmexico", "cbnnoticias",
    "mexicoinformado", "nodoinformativo", "bitacoraurbana",
    "reportecentralmx", "verticenoticias", "noticiasobjetivo",
    "boominformativo", "capitalpress", "diarioexpress", "elpulsomexicano",
    "enfoquecapital", "enfoquedirecto", "formulacdmx", "mexicantimes",
    "mexico360noticias", "mradio", "noticiashorizonte", "pulsodiario",
    "puntoclave", "puntonoticias", "radarinformativo", "reportediario",
    "televisionabc"
]

def publish_to_facebook(site_slug, attempt=1):
    """Publicar 1 artículo en Facebook para un sitio"""
    url = f"{BASE_URL}/facebook/force-publish/{site_slug}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.post(url, headers=headers, timeout=30)
        result = response.json()
        
        if result.get("success"):
            post_id = result.get("fb_post_id", "N/A")
            return True, post_id[:20] if len(post_id) > 20 else post_id
        else:
            error = result.get("error", "Unknown error")
            return False, error
    except Exception as e:
        return False, str(e)

def main():
    print("="*80)
    print("PUBLICANDO 2 ARTÍCULOS POR SITIO EN FACEBOOK")
    print("="*80)
    print()
    
    stats = defaultdict(lambda: {"success": 0, "failed": 0})
    
    for sitio in SITIOS:
        print(f"📌 {sitio}:")
        
        for i in range(1, 3):  # 2 artículos por sitio
            success, result = publish_to_facebook(sitio, i)
            
            if success:
                print(f"   ✅ Artículo {i}: {result}...")
                stats[sitio]["success"] += 1
            else:
                print(f"   ⚠️ Artículo {i}: {result}")
                stats[sitio]["failed"] += 1
            
            time.sleep(3)  # Delay entre publicaciones
        
        print()
    
    # Resumen
    print("="*80)
    print("RESUMEN")
    print("="*80)
    
    total_success = sum(s["success"] for s in stats.values())
    total_failed = sum(s["failed"] for s in stats.values())
    
    print(f"Total publicados: {total_success}")
    print(f"Total fallidos: {total_failed}")
    print()
    
    print("Por sitio:")
    for sitio, stat in sorted(stats.items()):
        print(f"  {sitio:25s}: {stat['success']} exitosos, {stat['failed']} fallidos")

if __name__ == "__main__":
    main()
