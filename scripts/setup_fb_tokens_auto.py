#!/usr/bin/env python3
"""
Script para configurar los Facebook tokens directamente en Cloudflare
usando los tokens extraídos con el User Token.

Ejecutar desde cualquier directorio.
"""

import subprocess
import os

WORKER_NAME = "news-api"

# Tokens extraídos directamente (Page Access Tokens)
TOKENS = {
    # Nuevos sitios - Tokens encontrados
    ("mexicantimes", "FB_TOKEN_MEXICANTIMES"): 
        "EAAmv1Puxa7wBQ6cYjgpntD2DQt9OQoDfr9lhcP0GeYvOc1ER6um1WHd9bcmP9J1Nl7nX4WUZBWsFaCPRFZCPkeX0iCLRp795IkCHOKeijeUtJa82NRlkkaxeB9GEuKCrrzn4nPf0TtM6eqJy4qwLBwpwn2ZASfqwMMEZBafxJuVXZBrmYsmZCPuHwTAU499BdxYtqLimVilUpeQhZBPxhWHIeF0",
    
    ("televisionabc", "FB_TOKEN_TELEVISIONABC"): 
        "EAAmv1Puxa7wBQ4RhPiEM1ZCn8rZCYwZCKQk5RlVXAa3T94sLxWoRjODqCCJDY961gFdihqFSQ1IZCaYeBHl627Pimk9UeMSvp3ZCrZAQ9LhiIUf9xpXgCsuAWBCV4Jl94TG9ZCGplZAWUp9CfkqcwmH5bPPWi1os0rumx6SMpodJvapT6ZCAFmDAHWVlFZCQYVZAqh86wXZCyzlCrZAngsIyRSLTKdcUu",
    
    ("capitalpress", "FB_TOKEN_CAPITALPRESS"): 
        "EAAmv1Puxa7wBQ6cYjgpntD2DQt9OQoDfr9lhcP0GeYvOc1ER6um1WHd9bcmP9J1Nl7nX4WUZBWsFaCPRFZCPkeX0iCLRp795IkCHOKeijeUtJa82NRlkkaxeB9GEuKCrrzn4nPf0TtM6eqJy4qwLBwpwn2ZASfqwMMEZBafxJuVXZBrmYsmZCPuHwTAU499BdxYtqLimVilUpeQhZBPxhWHIeF0",
    
    ("mradio", "FB_TOKEN_MRADIO"): 
        "EAAmv1Puxa7wBQzVMK1vCknwZAOPgtFAcajt39R85lpGaAuitWbEZCOnh53rPahcIRsgaK6gAYWwxZBZBWvheAQAJiAmQCYcZAQtdXo2v8CvHIVaPAEWDRPyQZA2ebfLWU2uOkZABZCzNwsdSBQkJapTS9vOMuR12ZBhVCCLzkmxiJRGFBcIT8gqQie8VXYGmSH2SDM9zQgtAoDPp1BLYdKL3QpokK",
    
    ("formulacdmx", "FB_TOKEN_FORMULACDMX"): 
        "EAAmv1Puxa7wBQzgcpCloTFckjHW8iMBCrRPkiZAI1JJZCHs3lFuWIOowgrRZBMyyZCpygbxeyntI4gUOKZBRjxajhrN6ZBM9MUjuSRsYjS6yvvehtkFWmLNDCdMngdWJjpEOOluyuvdX2w8ae6JYdmiIZA16Pz5BunZAu9x0HGj18nQn53xiShOW8KiVZCjsWIz0s7lBZBWgE03KMiZC4iYHRHZBCZCcZA",
    
    ("enfoquecapital", "FB_TOKEN_ENFOQUECAPITAL"): 
        "EAAmv1Puxa7wBQ7LjrdPqWTewrCsr6zVJCdTuvYbcrXct6zZB2cKEWBxR9XBXFNLsr6x8s3vzumQW4DW5PtffgjrsUShwxYNE3C2KfWEwZCZCXmH2PSAPDbejSJisIkSjubHg9DVCZAYKoEjjzs5uDGjGZBEy0SYIX7elRIIRFVdw2kGdfDMbae8z8YZBq6PaLooTEmEaVojxPWFNsLlXL9fJJ5",
    
    ("boominformativo", "FB_TOKEN_BOOMINFORMATIVO"): 
        "EAAmv1Puxa7wBQwU6SAoc0xuYNMyYHKrybgFzSSu28sWjpZAEI8hI5AQkBZCoUBt6ZBbLVcZCQSDERbErwUxo1ph9VHpet4P5QZA4krS5XIrsxsOjuTRLx1nSZCjNZCg5DOsHV7XQHrZAZC3Kh2d3uAgpl3mWAGXcHijdkIpHVt8Li8NOjCJX6nTAf1ZBsjO3Gdu1Ax8xxuZAvrZB2zogBkt3HcnMuCH8",
    
    ("puntoclave", "FB_TOKEN_PUNTOCLAVE"): 
        "EAAmv1Puxa7wBQ5N9Q4ltG5BAHzLSLViwD9iykOe5tAp5GZCijhfGzeaT6hi9BhfOFesZB1SB7FdhcaPMsfYyrx0lWM4fpcFdAJde6KDtSZCVjStVCDuZAYA7iv1leZC7NzcLHlNaPUZBmGkaoFn9OAZBYmeI5xcnVGyepyJpIMKYNUMYbgdcbOERZAjOlfLu40CdyCp4eOYgzYu2Os8S2LGGBIO0",
}

# Sitios sin token encontrado
MISSING = [
    ("diarioexpress", "FB_TOKEN_DIARIOEXPRESS"),
    ("elpulsomexicano", "FB_TOKEN_ELPULSOMEXICANO"),
    ("enfoquedirecto", "FB_TOKEN_ENFOQUEDIRECTO"),
    ("mexico360noticias", "FB_TOKEN_MEXICO360NOTICIAS"),
    ("noticiashorizonte", "FB_TOKEN_NOTICIASHORIZONTE"),
    ("pulsodiario", "FB_TOKEN_PULSODIARIO"),
    ("puntonoticias", "FB_TOKEN_PUNTONOTICIAS"),
    ("radarinformativo", "FB_TOKEN_RADARINFORMATIVO"),
    ("reportediario", "FB_TOKEN_REPORTEDIARIO"),
]


def setup_secret(secret_name, token):
    """Configura un secret usando wrangler con input pipe"""
    # Cambiar al directorio src para evitar conflicto con Pages
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
    print("Configuración de Facebook Tokens - Nuevos Sitios")
    print("="*70)
    print(f"\nWorker: {WORKER_NAME}")
    print(f"Total de tokens a configurar: {len(TOKENS)}\n")
    
    configured = []
    failed = []
    
    for (site_slug, secret_name), token in TOKENS.items():
        print(f"📌 {site_slug.upper()}")
        print(f"   Secret: {secret_name}")
        
        success, error = setup_secret(secret_name, token)
        
        if success:
            print(f"   ✅ Configurado exitosamente")
            configured.append(site_slug)
        else:
            print(f"   ❌ Error: {error[:100]}")
            failed.append(site_slug)
        
        print()
    
    # Resumen
    print("="*70)
    print("Resumen")
    print("="*70)
    print(f"✅ Configurados: {len(configured)}")
    print(f"❌ Fallidos: {len(failed)}")
    
    if configured:
        print(f"\n📋 Sitios configurados:")
        for slug in configured:
            print(f"   • {slug}")
    
    if failed:
        print(f"\n⚠️  Sitios fallidos:")
        for slug in failed:
            print(f"   • {slug}")
    
    # Sitios sin token
    print("\n" + "="*70)
    print("Sitios sin página de Facebook encontrada")
    print("="*70)
    for site_slug, secret_name in MISSING:
        print(f"⚠️  {site_slug} ({secret_name}) - No se encontró la página")
    
    print("\n" + "="*70)
    print("Para verificar:")
    print("="*70)
    print(f"  wrangler secret list --name {WORKER_NAME}")
    print()


if __name__ == "__main__":
    main()
