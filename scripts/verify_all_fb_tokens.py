#!/usr/bin/env python3
"""
Script para verificar todos los Facebook tokens configurados
"""

import urllib.request
import json
import subprocess

WORKER_NAME = "news-api"

# User Token para obtener los Page Tokens
USER_TOKEN = "EAAmv1Puxa7wBQ6O7QvBJOrytadcmXBda9OtXDJ81zGAi5rlVZAvZCITeEbF0bghDwXVuzQWIp9edbfjOAudqtp5EcQEvdaB0FnsoAW3UYybPHMZBZBvDV9emA0sZCok84LqQRUfAIhx0xUaUVxiiX2LZBEcFEZCMuQa6XTFa6lRZA8NxCzxeZAcnQV9ZAQu2EW1R8SvV3eXYUndpLf2fvK"

# Lista de sitios con sus Page IDs
SITES = [
    ("radiocinconoticias", "639476222579619"),
    ("centralmexico", "618190118045350"),
    ("tvmexico", "844452595886758"),
    ("cbnnoticias", "580707195132774"),
    ("mexicoinformado", "635096593022455"),
    ("nodoinformativo", "891600150711683"),
    ("bitacoraurbana", "887254687809731"),
    ("reportecentralmx", "496061180253373"),
    ("verticenoticias", "1007206479132086"),
    ("noticiasobjetivo", "1015387651656200"),
    ("boominformativo", "501728116348917"),
    ("capitalpress", "458242550714232"),
    ("diarioexpress", "270142869517794"),
    ("elpulsomexicano", "253187761218980"),
    ("enfoquecapital", "457328060805587"),
    ("enfoquedirecto", "454841367704076"),
    ("formulacdmx", "500033023189155"),
    ("mexicantimes", "578088192045850"),
    ("mexico360noticias", "286495644543503"),
    ("mradio", "472254365974557"),
    ("noticiashorizonte", "403046706229851"),
    ("pulsodiario", "429372300256610"),
    ("puntoclave", "497685936753403"),
    ("puntonoticias", "216140764924862"),
    ("radarinformativo", "405301062674763"),
    ("reportediario", "274537812414282"),
    ("televisionabc", "481562451709320"),
]


def get_page_token(page_id):
    """Obtiene el Page Access Token actual"""
    url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={USER_TOKEN}&fields=access_token,name"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('access_token'), data.get('name')
    except Exception as e:
        return None, str(e)


def test_page_token(page_token, page_id):
    """Prueba si el token es válido"""
    url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={page_token}&fields=name"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            if 'name' in data:
                return True, data['name']
            return False, "No name in response"
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return False, f"HTTP {e.code}: {error_body}"
    except Exception as e:
        return False, str(e)


def main():
    print("="*70)
    print("Verificación de Facebook Tokens")
    print("="*70)
    print()
    
    valid = []
    invalid = []
    
    for site_slug, page_id in SITES:
        print(f"📌 {site_slug}")
        print(f"   Page ID: {page_id}")
        
        # Obtener token actual de Facebook
        page_token, page_name = get_page_token(page_id)
        
        if not page_token:
            print(f"   ❌ No se pudo obtener el token: {page_name}")
            invalid.append(site_slug)
            print()
            continue
        
        # Probar el token
        is_valid, result = test_page_token(page_token, page_id)
        
        if is_valid:
            print(f"   ✅ Token válido: {page_name}")
            valid.append(site_slug)
        else:
            print(f"   ❌ Token inválido: {result}")
            invalid.append(site_slug)
        
        print()
    
    # Resumen
    print("="*70)
    print("Resumen")
    print("="*70)
    print(f"✅ Válidos: {len(valid)}")
    print(f"❌ Inválidos: {len(invalid)}")
    print(f"📊 Total: {len(SITES)}")
    
    if invalid:
        print(f"\n⚠️  Tokens inválidos:")
        for slug in invalid:
            print(f"   • {slug}")
    
    print()


if __name__ == "__main__":
    main()
