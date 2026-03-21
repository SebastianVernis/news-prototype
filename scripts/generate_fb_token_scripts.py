#!/usr/bin/env python3
"""
Script maestro que genera scripts de configuración individuales para cada CMS.
Crea dos scripts ejecutables en las raíces de cms-originaux y cms-nuevos.

Uso:
  python3 scripts/generate_fb_token_scripts.py

Salida:
  - cms-originaux/configure_fb_tokens.sh (ejecutable)
  - cms-nuevos/configure_fb_tokens.sh (ejecutable)

Cada script generado puede ejecutarse independientemente en su directorio.
"""

import subprocess
import sys
import json
import urllib.request
import urllib.error
import os

USER_TOKEN = "EAAmv1Puxa7wBQ6O7QvBJOrytadcmXBda9OtXDJ81zGAi5rlVZAvZCITeEbF0bghDwXVuzQWIp9edbfjOAudqtp5EcQEvdaB0FnsoAW3UYybPHMZBZBvDV9emA0sZCok84LqQRUfAIhx0xUaUVxiiX2LZBEcFEZCMuQa6XTFa6lRZA8NxCzxeZAcnQV9ZAQu2EW1R8SvV3eXYUndpLf2fvK"

CMS_CONFIGS = {
    "cms-originaux": {
        "worker_name": "cms-originaux",
        "sites": [
            "noticiasobjetivo",
            "nodoinformativo",
            "bitacoraurbana",
            "verticenoticias",
            "mexicoinformado",
            "centralmexico",
            "radiocinconoticias",
            "cbnnoticias",
            "reportecentralmx",
            "televisionabc",
        ],
    },
    "cms-nuevos": {
        "worker_name": "cms-nuevos",
        "sites": [
            "boominformativo",
            "capitalpress",
            "diarioexpress",
            "elpulsomexicano",
            "enfoquecapital",
            "enfoquedirecto",
            "formulacdmx",
            "mexicantimes",
            "mexico360noticias",
            "mradio",
            "noticiashorizonte",
            "pulsodiario",
            "puntoclave",
            "puntonoticias",
            "radarinformativo",
            "reportediario",
        ],
    },
}

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
    "boominformativo": "boominformativo",
    "boom informativo": "boominformativo",
    "capital press": "capitalpress",
    "diario express": "diarioexpress",
    "el pulso mexicano": "elpulsomexicano",
    "enfoque capital": "enfoquecapital",
    "enfoque directo": "enfoquedirecto",
    "fórmula cdmx": "formulacdmx",
    "formula cdmx": "formulacdmx",
    "mexican times": "mexicantimes",
    "the mexican times": "mexicantimes",
    "méxico 360 noticias": "mexico360noticias",
    "mexico 360 noticias": "mexico360noticias",
    "m radio": "mradio",
    "noticias horizonte": "noticiashorizonte",
    "pulso diario": "pulsodiario",
    "punto clave": "puntoclave",
    "punto noticias": "puntonoticias",
    "radar informativo": "radarinformativo",
    "reporte diario": "reportediario",
}

NON_WORKING_SITES = ["tvmexico", "alavistanoticias"]


def get_page_access_token(page_id, user_token):
    url = f"https://graph.facebook.com/v19.0/{page_id}?access_token={user_token}&fields=access_token,name"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data.get("access_token"), data.get("name")
    except urllib.error.HTTPError as e:
        print(f"  ❌ Error HTTP {e.code}: {e.read().decode()}")
        return None, None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None, None


def get_all_pages(user_token):
    pages = []
    url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={user_token}&limit=100"

    while url:
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())

                if "data" in data:
                    for page in data["data"]:
                        pages.append(
                            {
                                "id": page.get("id"),
                                "name": page.get("name"),
                                "access_token": page.get("access_token"),
                                "category": page.get("category"),
                            }
                        )

                if "paging" in data and "next" in data["paging"]:
                    url = data["paging"]["next"]
                else:
                    url = None

        except Exception as e:
            print(f"❌ Error al obtener páginas: {e}")
            break

    return pages


def generate_config_script(cms_name, pages, config):
    """Genera un script de configuración para un CMS específico"""
    script_lines = [
        "#!/bin/bash",
        "# Script generado automáticamente para configurar tokens de Facebook",
        "# CMS: " + cms_name,
        "# Fecha: " + subprocess.getoutput("date"),
        "",
        "echo '=========================================='",
        "echo 'Configurando tokens para " + cms_name + "'",
        "echo '=========================================='",
        "echo ''",
    ]

    configured_count = 0
    missing_count = 0

    for site_slug in config["sites"]:
        page_info = None
        for page in pages:
            if PAGE_TO_SITE.get(page["name"].lower()) == site_slug:
                page_info = page
                break

        if not page_info:
            script_lines.append(
                f"echo '⚠️  {site_slug}: No se encontró la página en Facebook'"
            )
            missing_count += 1
            continue

        page_token = page_info.get("access_token")

        if not page_token:
            script_lines.append(
                f"echo '⚠️  {site_slug}: No tiene token (necesita permisos)'"
            )
            missing_count += 1
            continue

        secret_name = f"FB_TOKEN_{site_slug.upper()}"
        script_lines.append(f"echo '📌 Configurando {site_slug.upper()}...'")
        script_lines.append(f"echo '   Secret: {secret_name}'")
        script_lines.append(
            f"echo '{page_token}' | wrangler pages secret put {secret_name} --project-name {config['worker_name']}"
        )
        script_lines.append("if [ $? -eq 0 ]; then")
        script_lines.append(f"    echo '   ✅ {site_slug} configurado correctamente'")
        script_lines.append("else")
        script_lines.append(f"    echo '   ❌ Error configurando {site_slug}'")
        script_lines.append("fi")
        script_lines.append("echo ''")
        configured_count += 1

    script_lines.append("echo '=========================================='")
    script_lines.append("echo 'Resumen'")
    script_lines.append("echo '=========================================='")
    script_lines.append(f"echo '✅ Configurados: {configured_count}'")
    script_lines.append(f"echo '⚠️  Faltantes: {missing_count}'")
    script_lines.append("echo ''")

    return script_lines, configured_count, missing_count


def main():
    print("=" * 70)
    print("Generador de Scripts de Configuración de Facebook Tokens")
    print("=" * 70)
    print(f"\nUser Token: {USER_TOKEN[:20]}...\n")

    print("📋 Obteniendo todas las páginas de Facebook...")
    pages = get_all_pages(USER_TOKEN)

    if not pages:
        print("❌ No se pudieron obtener las páginas. Verifica el User Token.")
        return

    print(f"✅ Se encontraron {len(pages)} páginas\n")

    all_stats = {}

    for cms_name, config in CMS_CONFIGS.items():
        print(f"📁 Generando script para {cms_name}...")

        script_lines, configured, missing = generate_config_script(
            cms_name, pages, config
        )

        script_path = f"/home/sebastianvernis/ProyectosActivos/cloudflare-news-project/{cms_name}/configure_fb_tokens.sh"

        with open(script_path, "w") as f:
            f.write("\n".join(script_lines) + "\n")

        os.chmod(script_path, 0o755)

        all_stats[cms_name] = {
            "configured": configured,
            "missing": missing,
            "script_path": script_path,
        }

        print(f"   ✅ Script generado: {script_path}")
        print(f"   📊 Configurados: {configured}, Faltantes: {missing}")
        print()

    print("=" * 70)
    print("Resumen de Generación")
    print("=" * 70)

    total_configured = 0
    total_missing = 0

    for cms_name, stats in all_stats.items():
        print(f"\n📁 {cms_name}:")
        print(f"   Script: {stats['script_path']}")
        print(f"   ✅ Configurados: {stats['configured']}")
        print(f"   ⚠️  Faltantes: {stats['missing']}")

        total_configured += stats["configured"]
        total_missing += stats["missing"]

    print(f"\n📊 TOTAL:")
    print(f"   ✅ Configurados: {total_configured}")
    print(f"   ⚠️  Faltantes: {total_missing}")

    print(f"\n💡 Para ejecutar la configuración:")
    for cms_name, stats in all_stats.items():
        print(f"   cd {cms_name}")
        print(f"   ./configure_fb_tokens.sh")
        print(f"   cd ..")
        print()

    print("ℹ️  Los scripts generados son independientes y pueden ejecutarse")
    print("    en cualquier momento. Cada uno configurará solo los tokens")
    print("    correspondientes a su CMS.")
    print()


if __name__ == "__main__":
    main()
