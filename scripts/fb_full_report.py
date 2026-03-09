#!/usr/bin/env python3
"""
Reporte completo del estado de Facebook para todos los sitios de NexoPress
Verifica: DB, Cloudflare Secrets, y Facebook API
"""

import urllib.request
import json
import subprocess

USER_TOKEN = "EAAmv1Puxa7wBQ6O7QvBJOrytadcmXBda9OtXDJ81zGAi5rlVZAvZCITeEbF0bghDwXVuzQWIp9edbfjOAudqtp5EcQEvdaB0FnsoAW3UYybPHMZBZBvDV9emA0sZCok84LqQRUfAIhx0xUaUVxiiX2LZBEcFEZCMuQa6XTFa6lRZA8NxCzxeZAcnQV9ZAQu2EW1R8SvV3eXYUndpLf2fvK"

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


def get_db_status():
    """Obtiene el estado de FACEBOOK_ACTIVO desde la DB"""
    cmd = [
        "wrangler", "d1", "execute", "news_db",
        "--command", "SELECT SLUG, FACEBOOK_ACTIVO, FACEBOOK_TOKEN_SECRET FROM SITIOS ORDER BY SLUG",
        "--remote"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True,
                           cwd="/mnt/c/Users/soluc/cloudflare-news-project/src")
    
    db_status = {}
    try:
        data = json.loads(result.stdout)
        for row in data[0].get('results', []):
            db_status[row['SLUG']] = {
                'activo': row['FACEBOOK_ACTIVO'],
                'secret': row['FACEBOOK_TOKEN_SECRET']
            }
    except:
        pass
    return db_status


def get_cf_secrets():
    """Obtiene la lista de secrets de Cloudflare"""
    cmd = [
        "wrangler", "secret", "list", "--name", "news-api"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True,
                           cwd="/mnt/c/Users/soluc/cloudflare-news-project/src")
    
    secrets = set()
    for line in result.stdout.split('\n'):
        if '"name": "FB_TOKEN' in line:
            try:
                name = line.split('"name": "')[1].split('"')[0]
                secrets.add(name)
            except:
                pass
    return secrets


def test_fb_page(page_id, page_name):
    """Prueba el acceso a una página de Facebook"""
    url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={USER_TOKEN}&fields=name,access_token"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            if 'access_token' in data:
                return True, data.get('name', page_name), data['access_token'][:20] + "..."
            else:
                return False, data.get('name', page_name), "No token"
    except Exception as e:
        return False, page_name, str(e)[:50]


def main():
    print("="*80)
    print("REPORTE COMPLETO DE FACEBOOK - NEXOPRESS")
    print("="*80)
    print()
    
    # Obtener estados
    db_status = get_db_status()
    cf_secrets = get_cf_secrets()
    
    # Tabla de resultados
    print("│ {:<25} │ {:<8} │ {:<8} │ {:<30} │".format("SITIO", "DB", "SECRET", "FACEBOOK"))
    print("│" + "─"*27 + "│" + "─"*10 + "│" + "─"*10 + "│" + "─"*32 + "│")
    
    all_ok = []
    db_inactive = []
    secret_missing = []
    fb_error = []
    
    for site_slug, page_id in SITES:
        db_info = db_status.get(site_slug, {})
        db_activo = db_info.get('activo', 0)
        db_secret = db_info.get('secret', 'N/A')
        
        # Verificar secret en Cloudflare
        secret_exists = db_secret in cf_secrets
        
        # Verificar Facebook
        fb_ok, fb_name, fb_token = test_fb_page(page_id, site_slug)
        
        # Determinar estado
        if db_activo == 1 and secret_exists and fb_ok:
            status_db = "✅"
            status_secret = "✅"
            status_fb = "✅"
            all_ok.append(site_slug)
        else:
            status_db = "✅" if db_activo == 1 else "❌"
            status_secret = "✅" if secret_exists else "❌"
            status_fb = "✅" if fb_ok else "❌"
            
            if db_activo == 0:
                db_inactive.append(site_slug)
            if not secret_exists:
                secret_missing.append(site_slug)
            if not fb_ok:
                fb_error.append(site_slug)
        
        print("│ {:<25} │ {:^8} │ {:^8} │ {:<30} │".format(
            site_slug[:25],
            status_db,
            status_secret,
            f"{fb_name[:28]}" if fb_ok else f"Error: {fb_token[:28]}"
        ))
    
    print()
    print("="*80)
    print("RESUMEN")
    print("="*80)
    print(f"✅ TOTAL OPERATIVOS: {len(all_ok)}/27")
    print()
    
    if all_ok:
        print(f"📋 Sitios listos para publicar ({len(all_ok)}):")
        for s in sorted(all_ok):
            print(f"   • {s}")
    
    if db_inactive:
        print(f"\n⚠️  Inactivos en DB ({len(db_inactive)}):")
        for s in db_inactive:
            print(f"   • {s}")
    
    if secret_missing:
        print(f"\n⚠️  Secrets faltantes en Cloudflare ({len(secret_missing)}):")
        for s in secret_missing:
            print(f"   • {s}")
    
    if fb_error:
        print(f"\n⚠️  Errores en Facebook API ({len(fb_error)}):")
        for s in fb_error:
            print(f"   • {s}")
    
    print()
    print("="*80)
    print("PRÓXIMO CRON: Se ejecutará automáticamente cada 30 minutos")
    print("Para verificar estado: curl https://news-api.sebastianvernis.workers.dev/api/cron/status")
    print("="*80)
    print()


if __name__ == "__main__":
    main()
