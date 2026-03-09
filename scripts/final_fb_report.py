#!/usr/bin/env python3
"""Reporte final de Facebook para NexoPress"""

import subprocess
import json
import urllib.request

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
    cmd = [
        "wrangler", "d1", "execute", "news_db",
        "--command", "SELECT SLUG, FACEBOOK_ACTIVO, FACEBOOK_TOKEN_SECRET FROM SITIOS ORDER BY SLUG",
        "--remote"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True,
                           cwd="/mnt/c/Users/soluc/cloudflare-news-project/src")
    
    # Extraer JSON del output
    start = result.stdout.find('[')
    if start == -1:
        return {}
    
    try:
        data = json.loads(result.stdout[start:])
        db_status = {}
        for row in data[0].get('results', []):
            db_status[row['SLUG']] = {
                'activo': row['FACEBOOK_ACTIVO'],
                'secret': row['FACEBOOK_TOKEN_SECRET']
            }
        return db_status
    except:
        return {}

def get_cf_secrets():
    cmd = ["wrangler", "secret", "list", "--name", "news-api"]
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

def test_fb_page(page_id):
    url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={USER_TOKEN}&fields=name,access_token"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            if 'access_token' in data:
                return True, data.get('name', ''), data['access_token'][:20] + "..."
            else:
                return False, data.get('name', ''), "No token"
    except Exception as e:
        return False, '', str(e)[:40]

def main():
    print("="*80)
    print("REPORTE FINAL DE FACEBOOK - NEXOPRESS")
    print("="*80)
    print()
    
    db_status = get_db_status()
    cf_secrets = get_cf_secrets()
    
    all_ok = []
    issues = []
    
    print("│ {:<25} │ {:<6} │ {:<35} │ {:<6} │".format("SITIO", "DB", "SECRET", "FB"))
    print("│" + "─"*27 + "│" + "─"*8 + "│" + "─"*37 + "│" + "─"*8 + "│")
    
    for site_slug, page_id in SITES:
        db_info = db_status.get(site_slug, {})
        db_activo = db_info.get('activo', 0)
        db_secret = db_info.get('secret', 'N/A')
        
        secret_exists = db_secret in cf_secrets
        fb_ok, fb_name, fb_token = test_fb_page(page_id)
        
        # Estado completo
        is_ok = (db_activo == 1) and secret_exists and fb_ok
        
        status_db = "✅" if db_activo == 1 else "❌"
        status_secret = "✅" if secret_exists else "❌"
        status_fb = "✅" if fb_ok else "❌"
        
        if is_ok:
            all_ok.append(site_slug)
            display = "✅"
        else:
            reason = []
            if db_activo == 0: reason.append("DB")
            if not secret_exists: reason.append("SECRET")
            if not fb_ok: reason.append("FB")
            display = "⚠️ " + ",".join(reason)
            issues.append((site_slug, reason))
        
        print("│ {:<25} │   {}    │  {:<33} │   {}    │".format(
            site_slug[:25], status_db, db_secret[:33], status_fb
        ))
    
    print()
    print("="*80)
    print("RESUMEN")
    print("="*80)
    print(f"✅ TOTAL OPERATIVOS: {len(all_ok)}/27")
    print(f"⚠️  CON PROBLEMAS: {len(issues)}")
    print()
    
    if all_ok:
        print("📋 SITIOS LISTOS PARA PUBLICAR:")
        for s in sorted(all_ok):
            print(f"   ✅ {s}")
    
    if issues:
        print("\n⚠️  SITIOS CON PROBLEMAS:")
        for slug, reasons in issues:
            print(f"   ⚠️  {slug}: {', '.join(reasons)}")
    
    print()
    print("="*80)
    print("PRÓXIMOS PASOS")
    print("="*80)
    print("1. El cron se ejecuta automáticamente cada 30 minutos")
    print("2. Verificar estado: curl https://news-api.sebastianvernis.workers.dev/api/cron/status")
    print("3. Los artículos pendientes se publicarán en el próximo ciclo")
    print("="*80)
    print()

if __name__ == "__main__":
    main()
