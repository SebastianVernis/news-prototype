#!/usr/bin/env python3
"""
Script para configurar TODOS los Facebook tokens disponibles
usando el User Token de larga duración.

Ejecuta desde cualquier directorio.
"""

import subprocess

WORKER_NAME = "news-api"

# Mapeo actualizado de páginas de Facebook a sitios
# Formato: (site_slug, secret_name, page_id, page_name)
PAGES_TO_CONFIGURE = [
    # Sitios Estables (10) - Ya deberían estar configurados
    ("radiocinconoticias", "FB_TOKEN_RADIOCINCONOTICIAS", "639476222579619", "Radio Cinco Noticias"),
    ("centralmexico", "FB_TOKEN_CENTRALMEXICO", "618190118045350", "Central México News"),
    ("tvmexico", "FB_TOKEN_TVMEXICO", "844452595886758", "TV México"),
    ("cbnnoticias", "FB_TOKEN_CBNNOTICIAS", "580707195132774", "CBN Noticias"),
    ("mexicoinformado", "FB_TOKEN_MEXICOINFORMADO", "635096593022455", "México Informado"),
    ("nodoinformativo", "FB_TOKEN_NODOINFORMATIVO", "891600150711683", "Nodo Informativo"),
    ("bitacoraurbana", "FB_TOKEN_BITACORAURBANA", "887254687809731", "Bitácora Urbana"),
    ("reportecentralmx", "FB_TOKEN_REPORTECENTRALMX", "496061180253373", "Reporte Central MX"),
    ("verticenoticias", "FB_TOKEN_VERTICENOTICIAS", "1007206479132086", "Vértice Noticias"),
    ("noticiasobjetivo", "FB_TOKEN_NOTICIASOBJETIVO", "1015387651656200", "Noticias Objetivo"),
    
    # Nuevos Sitios (17) - Los que encontramos
    ("boominformativo", "FB_TOKEN_BOOMINFORMATIVO", "501728116348917", "Boom Informativo"),
    ("capitalpress", "FB_TOKEN_CAPITALPRESS", "458242550714232", "Capital Press"),
    ("diarioexpress", "FB_TOKEN_DIARIOEXPRESS", "270142869517794", "Diario Express"),
    ("elpulsomexicano", "FB_TOKEN_ELPULSOMEXICANO", "253187761218980", "El Pulso Mexicano"),
    ("enfoquecapital", "FB_TOKEN_ENFOQUECAPITAL", "457328060805587", "Enfoque capital"),
    ("enfoquedirecto", "FB_TOKEN_ENFOQUEDIRECTO", "454841367704076", "Enfoque Directo"),
    ("formulacdmx", "FB_TOKEN_FORMULACDMX", "500033023189155", "Formula CDMX"),
    ("mexicantimes", "FB_TOKEN_MEXICANTIMES", "578088192045850", "Mexican Times"),
    ("mexico360noticias", "FB_TOKEN_MEXICO360NOTICIAS", "286495644543503", "México 360 Noticias"),
    ("mradio", "FB_TOKEN_MRADIO", "472254365974557", "M radio"),
    ("noticiashorizonte", "FB_TOKEN_NOTICIASHORIZONTE", "403046706229851", "Noticias Horizonte"),
    ("pulsodiario", "FB_TOKEN_PULSODIARIO", "429372300256610", "Pulso Diario"),
    ("puntoclave", "FB_TOKEN_PUNTOCLAVE", "497685936753403", "Punto Clave"),
    ("puntonoticias", "FB_TOKEN_PUNTONOTICIAS", "216140764924862", "Punto Noticias"),
    ("radarinformativo", "FB_TOKEN_RADARINFORMATIVO", "405301062674763", "Radar Informativo"),
    ("reportediario", "FB_TOKEN_REPORTEDIARIO", "274537812414282", "Reporte Diario"),
    ("televisionabc", "FB_TOKEN_TELEVISIONABC", "481562451709320", "ABC Television"),
]

# User Token de larga duración
USER_TOKEN = "EAAmv1Puxa7wBQ6O7QvBJOrytadcmXBda9OtXDJ81zGAi5rlVZAvZCITeEbF0bghDwXVuzQWIp9edbfjOAudqtp5EcQEvdaB0FnsoAW3UYybPHMZBZBvDV9emA0sZCok84LqQRUfAIhx0xUaUVxiiX2LZBEcFEZCMuQa6XTFa6lRZA8NxCzxeZAcnQV9ZAQu2EW1R8SvV3eXYUndpLf2fvK"


def get_page_token(page_id, user_token):
    """Obtiene el Page Access Token para una página específica"""
    import urllib.request
    import json
    
    url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={user_token}&fields=access_token,name"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get('access_token'), data.get('name')
    except Exception as e:
        return None, str(e)


def setup_secret(secret_name, token):
    """Configura un secret usando wrangler"""
    src_dir = "/mnt/c/Users/soluc/cloudflare-news-project/src"
    
    cmd = ["wrangler", "secret", "put", secret_name, "--name", WORKER_NAME]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=src_dir
        )
        
        stdout, stderr = process.communicate(input=f"{token}\n")
        
        if process.returncode == 0:
            return True, ""
        else:
            return False, stderr
            
    except Exception as e:
        return False, str(e)


def main():
    print("="*70)
    print("Configuración de Facebook Tokens - TODOS los Sitios")
    print("="*70)
    print(f"\nWorker: {WORKER_NAME}")
    print(f"Total de sitios: {len(PAGES_TO_CONFIGURE)}\n")
    
    configured = []
    failed = []
    skipped = []
    
    for site_slug, secret_name, page_id, page_name in PAGES_TO_CONFIGURE:
        print(f"📌 {site_slug.upper()}")
        print(f"   Página: {page_name} (ID: {page_id})")
        print(f"   Secret: {secret_name}")
        
        # Obtener Page Access Token
        page_token, token_name = get_page_token(page_id, USER_TOKEN)
        
        if not page_token:
            print(f"   ⚠️  No se pudo obtener el token: {token_name}")
            skipped.append(site_slug)
            print()
            continue
        
        # Configurar en Cloudflare
        success, error = setup_secret(secret_name, page_token)
        
        if success:
            print(f"   ✅ Token configurado exitosamente")
            configured.append(site_slug)
        else:
            print(f"   ❌ Error: {error[:100]}")
            failed.append(site_slug)
        
        print()
    
    # Resumen
    print("="*70)
    print("Resumen Final")
    print("="*70)
    print(f"✅ Configurados: {len(configured)}")
    print(f"❌ Fallidos: {len(failed)}")
    print(f"⚠️  Saltados: {len(skipped)}")
    print(f"📊 Total: {len(PAGES_TO_CONFIGURE)}")
    
    if configured:
        print(f"\n📋 Sitios configurados:")
        for slug in configured:
            print(f"   • {slug}")
    
    if failed:
        print(f"\n⚠️  Sitios fallidos:")
        for slug in failed:
            print(f"   • {slug}")
    
    if skipped:
        print(f"\n⚠️  Sitios saltados (no se obtuvo token):")
        for slug in skipped:
            print(f"   • {slug}")
    
    print("\n" + "="*70)
    print("Para verificar:")
    print("="*70)
    print(f"  wrangler secret list --name {WORKER_NAME}")
    print()


if __name__ == "__main__":
    main()
