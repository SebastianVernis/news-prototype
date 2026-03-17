#!/usr/bin/env python3
"""
Script para configurar los Facebook tokens de los 17 nuevos sitios
como Cloudflare Secrets en el Worker news-api.

Uso:
  python3 setup_new_sites_fb_tokens.py

Requisitos:
  - wrangler CLI instalado y autenticado
  - Tokens de Facebook generados para cada sitio
"""

import subprocess
import sys

# Lista de nuevos sitios con sus nombres de secret
NEW_SITES = [
    ("boominformativo", "FB_TOKEN_BOOMINFORMATIVO"),
    ("capitalpress", "FB_TOKEN_CAPITALPRESS"),
    ("diarioexpress", "FB_TOKEN_DIARIOEXPRESS"),
    ("elpulsomexicano", "FB_TOKEN_ELPULSOMEXICANO"),
    ("enfoquecapital", "FB_TOKEN_ENFOQUECAPITAL"),
    ("enfoquedirecto", "FB_TOKEN_ENFOQUEDIRECTO"),
    ("formulacdmx", "FB_TOKEN_FORMULACDMX"),
    ("mexicantimes", "FB_TOKEN_MEXICANTIMES"),
    ("mexico360noticias", "FB_TOKEN_MEXICO360NOTICIAS"),
    ("mradio", "FB_TOKEN_MRADIO"),
    ("noticiashorizonte", "FB_TOKEN_NOTICIASHORIZONTE"),
    ("pulsodiario", "FB_TOKEN_PULSODIARIO"),
    ("puntoclave", "FB_TOKEN_PUNTOCLAVE"),
    ("puntonoticias", "FB_TOKEN_PUNTONOTICIAS"),
    ("radarinformativo", "FB_TOKEN_RADARINFORMATIVO"),
    ("reportediario", "FB_TOKEN_REPORTEDIARIO"),
    ("televisionabc", "FB_TOKEN_TELEVISIONABC"),
]

WORKER_NAME = "news-api"


def setup_fb_token(site_slug, secret_name):
    """Configura un Facebook token como Cloudflare Secret"""
    print(f"\n{'='*60}")
    print(f"Sitio: {site_slug}")
    print(f"Secret: {secret_name}")
    print(f"{'='*60}")
    
    # Pedir el token al usuario
    print(f"\nIngresa el Facebook Page Access Token para '{site_slug}':")
    print("(El token no se mostrará en pantalla mientras escribes)")
    
    try:
        # Usar getpass para no mostrar el token
        import getpass
        token = getpass.getpass("Token: ")
        
        if not token.strip():
            print("⚠️  Token vacío, saltando...")
            return False
        
        # Ejecutar wrangler secret put
        cmd = f"wrangler secret put {secret_name} --name {WORKER_NAME}"
        
        # Usar subprocess con input para pasar el token
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
            print(f"✅ Token configurado exitosamente para {site_slug}")
            return True
        else:
            print(f"❌ Error al configurar token: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("="*60)
    print("Configuración de Facebook Tokens - Nuevos Sitios")
    print("="*60)
    print(f"\nWorker: {WORKER_NAME}")
    print(f"Total de sitios: {len(NEW_SITES)}")
    print("\nNota: Los tokens se guardarán como Cloudflare Secrets.")
    print("      Cada token debe ser un Page Access Token permanente.\n")
    
    success_count = 0
    skip_count = 0
    
    for site_slug, secret_name in NEW_SITES:
        result = setup_fb_token(site_slug, secret_name)
        if result:
            success_count += 1
        else:
            skip_count += 1
    
    print("\n" + "="*60)
    print("Resumen")
    print("="*60)
    print(f"✅ Configurados: {success_count}")
    print(f"⚠️  Saltados/Fallidos: {skip_count}")
    print(f"📊 Total: {len(NEW_SITES)}")
    
    if success_count == len(NEW_SITES):
        print("\n🎉 ¡Todos los tokens fueron configurados exitosamente!")
    else:
        print(f"\n⚠️  {skip_count} sitios quedaron sin configurar.")
        print("   Puedes ejecutar el script nuevamente para configurarlos.")
    
    print("\nPara verificar los secrets configurados:")
    print(f"  wrangler secret list --name {WORKER_NAME}")
    print()


if __name__ == "__main__":
    main()
