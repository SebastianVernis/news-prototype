#!/usr/bin/env python3
"""
Script para resetear el timer de Facebook para un sitio específico.
Usa la API de Cloudflare KV directamente.
"""

import os
import requests

# Configuración
ACCOUNT_ID = "adf5d76bca341500fec8b8c04941978a"
KV_NAMESPACE_ID = "fbf21fb75f5647a8966858d199b44e0b"
API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")

if not API_TOKEN:
    print("Error: Debes establecer CLOUDFLARE_API_TOKEN como variable de entorno")
    print("Puedes obtener un token en: https://dash.cloudflare.com/profile/api-tokens")
    exit(1)

def reset_timer(site_slug):
    """Resetear el timer de Facebook para un sitio"""
    kv_key = f"last_fb_post_{site_slug}"
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/storage/kv/namespaces/{KV_NAMESPACE_ID}/values/{kv_key}"
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "text/plain"
    }
    
    # Resetear a 0 (epoch time)
    response = requests.put(url, data="0", headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Timer reseteado para {site_slug}")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        site_slug = sys.argv[1]
    else:
        site_slug = "noticiasobjetivo"
    
    print(f"Reseteando timer para: {site_slug}")
    reset_timer(site_slug)
