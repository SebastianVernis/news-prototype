#!/usr/bin/env python3
"""
Script para extraer todos los tokens de Facebook Pages usando el User Token
y configurarlos como Cloudflare Secrets en el Worker news-api.

Uso:
  python3 scripts/extract_all_fb_tokens.py

Requisitos:
  - wrangler CLI instalado y autenticado
  - User Token con permisos para gestionar páginas
"""

import subprocess
import sys
import json
import urllib.request
import urllib.error

# User Token proporcionado (token de larga duración)
USER_TOKEN = "EAAmv1Puxa7wBQ6O7QvBJOrytadcmXBda9OtXDJ81zGAi5rlVZAvZCITeEbF0bghDwXVuzQWIp9edbfjOAudqtp5EcQEvdaB0FnsoAW3UYybPHMZBZBvDV9emA0sZCok84LqQRUfAIhx0xUaUVxiiX2LZBEcFEZCMuQa6XTFa6lRZA8NxCzxeZAcnQV9ZAQu2EW1R8SvV3eXYUndpLf2fvK"

WORKER_NAME = "news-api"

# Mapeo de nombres de páginas a slugs de sitios
PAGE_TO_SITE = {
    "noticias objetivo": "noticiasobjetivo",
    "nodo informativo": "nodoinformativo",
    "bitácora urbana": "bitacoraurbana",
    "bitacora urbana": "bitacoraurbana",
    "vértice noticias": "verticenoticias",
    "vertice noticias": "verticenoticias",
    "méxico informado": "mexicoinformado",
    "mexico informado": "mexicoinformado",
    "radio cinco noticias": "radiocinconoticias",
    "central méxico news": "centralmexico",
    "central mexico news": "centralmexico",
    "cbn noticias": "cbnnoticias",
    "reporte central mx": "reportecentralmx",
    "abc television": "televisionabc",
    "capital press": "capitalpress",
    "m radio": "mradio",
    "formula cdmx": "formulacdmx",
    "enfoque capital": "enfoquecapital",
    "boom informativo": "boominformativo",
    "punto clave": "puntoclave",
    "mexican times": "mexicantimes",
    "fuerza ciudadana": None,  # No es un sitio de la red
    "visión ciudadana": None,  # No es un sitio de la red
    "vision ciudadana": None,  # No es un sitio de la red
    "colectivo manos buscadoras": None,  # No es un sitio de la red
    "radar de tecámac": None,  # No es un sitio de la red
    "radar de tecamac": None,  # No es un sitio de la red
    "rhonita vive": None,  # No es un sitio de la red
    "news capital": None,  # No es un sitio de la red
    "pulso ciudadano": None,  # No es un sitio de la red
}

# Nuevos sitios que necesitan tokens
NEW_SITES = {
    "boominformativo": "FB_TOKEN_BOOMINFORMATIVO",
    "capitalpress": "FB_TOKEN_CAPITALPRESS",
    "diarioexpress": "FB_TOKEN_DIARIOEXPRESS",
    "elpulsomexicano": "FB_TOKEN_ELPULSOMEXICANO",
    "enfoquecapital": "FB_TOKEN_ENFOQUECAPITAL",
    "enfoquedirecto": "FB_TOKEN_ENFOQUEDIRECTO",
    "formulacdmx": "FB_TOKEN_FORMULACDMX",
    "mexicantimes": "FB_TOKEN_MEXICANTIMES",
    "mexico360noticias": "FB_TOKEN_MEXICO360NOTICIAS",
    "mradio": "FB_TOKEN_MRADIO",
    "noticiashorizonte": "FB_TOKEN_NOTICIASHORIZONTE",
    "pulsodiario": "FB_TOKEN_PULSODIARIO",
    "puntoclave": "FB_TOKEN_PUNTOCLAVE",
    "puntonoticias": "FB_TOKEN_PUNTONOTICIAS",
    "radarinformativo": "FB_TOKEN_RADARINFORMATIVO",
    "reportediario": "FB_TOKEN_REPORTEDIARIO",
    "televisionabc": "FB_TOKEN_TELEVISIONABC",
}

# Sitios estables que ya tienen tokens
STABLE_SITES = {
    "radiocinconoticias": "FB_TOKEN_RADIOCINCONOTICIAS",
    "centralmexico": "FB_TOKEN_CENTRALMEXICO",
    "tvmexico": "FB_TOKEN_TVMEXICO",
    "cbnnoticias": "FB_TOKEN_CBNNOTICIAS",
    "mexicoinformado": "FB_TOKEN_MEXICOINFORMADO",
    "nodoinformativo": "FB_TOKEN_NODOINFORMATIVO",
    "bitacoraurbana": "FB_TOKEN_BITACORAURBANA",
    "reportecentralmx": "FB_TOKEN_REPORTECENTRALMX",
    "verticenoticias": "FB_TOKEN_VERTICENOTICIAS",
    "noticiasobjetivo": "FB_TOKEN_NOTICIASOBJETIVO",
}


def get_page_access_token(page_id, user_token):
    """Obtiene el Page Access Token usando el User Token"""
    url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={user_token}&fields=access_token,name"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get('access_token'), data.get('name')
    except urllib.error.HTTPError as e:
        print(f"  ❌ Error HTTP {e.code}: {e.read().decode()}")
        return None, None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None, None


def get_all_pages(user_token):
    """Obtiene todas las páginas accesibles con el User Token"""
    pages = []
    url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={user_token}&limit=100"
    
    while url:
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                
                if 'data' in data:
                    for page in data['data']:
                        pages.append({
                            'id': page.get('id'),
                            'name': page.get('name'),
                            'access_token': page.get('access_token'),
                            'category': page.get('category')
                        })
                
                # Paginación
                if 'paging' in data and 'next' in data['paging']:
                    url = data['paging']['next']
                else:
                    url = None
                    
        except Exception as e:
            print(f"❌ Error al obtener páginas: {e}")
            break
    
    return pages


def setup_cloudflare_secret(secret_name, token):
    """Configura un token como Cloudflare Secret en el Worker"""
    # Usar wrangler secret put (para Workers, no Pages)
    cmd = f'wrangler secret put {secret_name} --name {WORKER_NAME}'
    
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=f"{token}\n")
        
        if process.returncode == 0:
            return True
        else:
            print(f"    ❌ Error: {stderr}")
            return False
            
    except Exception as e:
        print(f"    ❌ Error: {e}")
        return False


def main():
    print("="*70)
    print("Extracción y Configuración de Facebook Tokens")
    print("="*70)
    print(f"\nWorker: {WORKER_NAME}")
    print(f"User Token: {USER_TOKEN[:20]}...\n")
    
    # Paso 1: Obtener todas las páginas
    print("📋 Obteniendo todas las páginas de Facebook...")
    pages = get_all_pages(USER_TOKEN)
    
    if not pages:
        print("❌ No se pudieron obtener las páginas. Verifica el User Token.")
        return
    
    print(f"✅ Se encontraron {len(pages)} páginas\n")
    
    # Paso 2: Mostrar todas las páginas encontradas
    print("="*70)
    print("Páginas encontradas:")
    print("="*70)
    for i, page in enumerate(pages, 1):
        site_slug = PAGE_TO_SITE.get(page['name'].lower())
        status = ""
        if site_slug:
            if site_slug in STABLE_SITES:
                status = f"✅ (Estable: {STABLE_SITES[site_slug]})"
            elif site_slug in NEW_SITES:
                status = f"🆕 (Nuevo: {NEW_SITES[site_slug]})"
        else:
            status = "⚠️ (No asociado a un sitio)"
        
        print(f"{i}. {page['name']} (ID: {page['id']}) {status}")
    
    # Paso 3: Configurar tokens para nuevos sitios
    print("\n" + "="*70)
    print("Configuración de tokens para NUEVOS sitios")
    print("="*70)
    
    configured = []
    missing = []
    
    for page in pages:
        page_name_lower = page['name'].lower()
        site_slug = PAGE_TO_SITE.get(page_name_lower)
        
        if not site_slug:
            continue
        
        if site_slug not in NEW_SITES:
            continue  # Es un sitio estable o no es de la red
        
        secret_name = NEW_SITES[site_slug]
        page_token = page.get('access_token')
        
        if not page_token:
            print(f"\n⚠️  {site_slug}: No tiene token (necesita permisos)")
            missing.append(site_slug)
            continue
        
        print(f"\n📌 {site_slug.upper()}")
        print(f"   Página: {page['name']} (ID: {page['id']})")
        print(f"   Secret: {secret_name}")
        
        # Configurar en Cloudflare
        result = setup_cloudflare_secret(secret_name, page_token)
        
        if result:
            print(f"   ✅ Token configurado en Cloudflare")
            configured.append(site_slug)
        else:
            print(f"   ❌ Error al configurar en Cloudflare")
            missing.append(site_slug)
    
    # Paso 4: Reportar sitios sin página encontrada
    print("\n" + "="*70)
    print("Sitios sin página de Facebook encontrada")
    print("="*70)
    
    configured_slugs = [PAGE_TO_SITE.get(p['name'].lower()) for p in pages if PAGE_TO_SITE.get(p['name'].lower())]
    
    for site_slug, secret_name in NEW_SITES.items():
        if site_slug not in configured and site_slug not in missing:
            print(f"⚠️  {site_slug} ({secret_name}) - No se encontró la página en Facebook")
    
    # Resumen final
    print("\n" + "="*70)
    print("Resumen")
    print("="*70)
    print(f"✅ Configurados: {len(configured)}")
    print(f"⚠️  Faltantes: {len(missing)}")
    
    if configured:
        print(f"\n📋 Sitios configurados:")
        for slug in configured:
            print(f"   • {slug}")
    
    print(f"\nPara verificar los secrets:")
    print(f"  wrangler secret list --name {WORKER_NAME}")
    
    print(f"\nPara verificar un token específico:")
    print(f"  curl -s 'https://graph.facebook.com/v19.0/[PAGE_ID]?access_token=[TOKEN]'")
    print()


if __name__ == "__main__":
    main()
