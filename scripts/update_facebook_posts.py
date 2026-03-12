#!/usr/bin/env python3
"""
Script para actualizar publicaciones de Facebook de las últimas 24 horas.

Esto fuerza a Facebook a re-scrapear las OG tags y mostrar las miniaturas correctamente.
Las publicaciones mantienen su ID, fecha y horario original.

Uso:
    python3 scripts/update_facebook_posts.py [--hours 24] [--sites sitio1,sitio2]
"""

import requests
import time
import argparse
from datetime import datetime
from collections import defaultdict

# Token de administrador para la API
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


def get_recent_posts(site_slug, hours=24):
    """
    Obtener publicaciones de Facebook de un sitio de las últimas N horas.
    """
    url = f"{BASE_URL}/facebook/recent-posts/{site_slug}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"hours": str(hours)}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"   ⚠️ Error obteniendo posts: {e}")
        return []


def update_post(site_slug, post_id):
    """
    Actualizar un post específico de Facebook para re-scrapear OG tags.
    """
    url = f"{BASE_URL}/facebook/update-post/{site_slug}/{post_id}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.post(url, headers=headers, timeout=30)
        result = response.json()
        
        if result.get("success"):
            return True, "Updated"
        else:
            error = result.get("error", "Unknown error")
            return False, error
    except Exception as e:
        return False, str(e)


def update_all_recent(site_slug, hours=24):
    """
    Actualizar todos los posts recientes de un sitio usando el endpoint batch.
    """
    url = f"{BASE_URL}/facebook/update-recent/{site_slug}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"hours": str(hours)}
    
    try:
        response = requests.post(url, headers=headers, params=params, timeout=60)
        result = response.json()
        
        if result.get("success"):
            results = result.get("results", {})
            return True, results
        else:
            error = result.get("error", "Unknown error")
            return False, error
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(
        description="Actualizar publicaciones de Facebook de las últimas N horas"
    )
    parser.add_argument(
        "--hours", "-h",
        type=int,
        default=24,
        help="Número de horas hacia atrás (default: 24)"
    )
    parser.add_argument(
        "--sites", "-s",
        type=str,
        default=None,
        help="Lista de sitios separados por coma (default: todos)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo mostrar qué se actualizaría, sin ejecutar"
    )
    
    args = parser.parse_args()
    
    # Determinar qué sitios procesar
    if args.sites:
        sitios_to_process = [s.strip() for s in args.sites.split(",")]
    else:
        sitios_to_process = SITIOS
    
    print("="*80)
    print("ACTUALIZANDO PUBLICACIONES DE FACEBOOK")
    print("="*80)
    print()
    print(f"📅 Rango: Últimas {args.hours} horas")
    print(f"🌐 Sitios: {len(sitios_to_process)} seleccionados")
    if args.dry_run:
        print("⚠️  DRY RUN - No se realizarán actualizaciones")
    print()
    print("Este script actualiza las publicaciones existentes para forzar")
    print("el re-scrapeo de OG tags y mostrar miniaturas correctamente.")
    print("Las publicaciones mantienen su fecha y horario original.")
    print()
    
    stats = defaultdict(lambda: {"total": 0, "updated": 0, "failed": 0, "skipped": 0})
    
    for sitio in sitios_to_process:
        print(f"📌 {sitio}:")
        
        # Obtener publicaciones recientes
        posts = get_recent_posts(sitio, hours=args.hours)
        
        if not posts:
            print(f"   ℹ️ No hay publicaciones en las últimas {args.hours} horas")
            stats[sitio]["skipped"] += 1
            continue
        
        stats[sitio]["total"] = len(posts)
        print(f"   📋 {len(posts)} publicaciones encontradas")
        
        if args.dry_run:
            for i, post in enumerate(posts[:5], 1):
                post_id = post.get('FB_POST_ID', 'N/A')
                title = post.get('TITULO', 'Sin título')[:50]
                fb_fecha = post.get('FB_FECHA', 'N/A')
                print(f"   📝 Post {i}: {post_id[:20] if len(post_id) > 20 else post_id} - {title}... ({fb_fecha})")
            if len(posts) > 5:
                print(f"   ... y {len(posts) - 5} más")
            continue
        
        # Usar endpoint batch para actualizar todos
        success, result = update_all_recent(sitio, hours=args.hours)
        
        if success:
            updated = result.get("updated", 0)
            failed = result.get("failed", 0)
            errors = result.get("errors", [])
            
            stats[sitio]["updated"] = updated
            stats[sitio]["failed"] = failed
            
            print(f"   ✅ {updated} publicaciones actualizadas")
            if failed > 0:
                print(f"   ⚠️ {failed} fallidas")
                for err in errors[:3]:
                    print(f"      - Post {err.get('post_id', 'N/A')}: {err.get('error', 'Unknown')}")
        else:
            stats[sitio]["failed"] += 1
            print(f"   ⚠️ Error: {result}")
        
        # Delay entre sitios para evitar rate limiting
        time.sleep(2)
        print()
    
    # Resumen
    print("="*80)
    print("RESUMEN")
    print("="*80)
    
    total_posts = sum(s["total"] for s in stats.values())
    total_updated = sum(s["updated"] for s in stats.values())
    total_failed = sum(s["failed"] for s in stats.values())
    total_skipped = sum(s["skipped"] for s in stats.values())
    
    print(f"Total publicaciones encontradas: {total_posts}")
    print(f"Total actualizadas: {total_updated}")
    print(f"Total fallidas: {total_failed}")
    print(f"Sitios sin posts: {total_skipped}")
    print()
    
    if total_updated > 0:
        print("✅ ¡Actualización completada!")
        print()
        print("Las miniaturas deberían verse correctamente en Facebook en unos minutos.")
        print("Facebook puede tardar hasta 10 minutos en re-scrapear las OG tags.")
    else:
        print("ℹ️ No hubo publicaciones que actualizar.")


if __name__ == "__main__":
    main()
