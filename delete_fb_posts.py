#!/usr/bin/env python3
"""
Script para eliminar publicaciones de Facebook de los sitios NexoPress
Uso: python3 delete_fb_posts.py
"""

import requests
import json

# Configuraci�n de sitios con sus Page IDs
SITIOS = {
    1: {"slug": "radiocinconoticias", "page_id": "639476222579619", "nombre": "Radio Cinco Noticias"},
    2: {"slug": "centralmexico", "page_id": "618190118045350", "nombre": "Central M�xico"},
    3: {"slug": "tvmexico", "page_id": "844452595886758", "nombre": "TV M�xico"},
    4: {"slug": "cbnnoticias", "page_id": "580707195132774", "nombre": "CBN Noticias"},
    5: {"slug": "mexicoinformado", "page_id": "635096593022455", "nombre": "M�xico Informado"},
    6: {"slug": "nodoinformativo", "page_id": "891600150711683", "nombre": "Nodo Informativo"},
    7: {"slug": "bitacoraurbana", "page_id": "887254687809731", "nombre": "Bit�cora Urbana"},
    8: {"slug": "reportecentralmx", "page_id": "496061180253373", "nombre": "Reporte Central MX"},
    9: {"slug": "verticenoticias", "page_id": "1007206479132086", "nombre": "V�rtice Noticias"},
    10: {"slug": "noticiasobjetivo", "page_id": "591610227368886", "nombre": "Noticias Objetivo"},
    11: {"slug": "boominformativo", "page_id": "122108195378548904", "page_id": "122108195378548904", "nombre": "Boominformativo"},
    12: {"slug": "capitalpress", "page_id": "122098826052548904", "nombre": "Capital Press"},
    13: {"slug": "diarioexpress", "page_id": "122116728060548904", "nombre": "Diario Express"},
    14: {"slug": "elpulsomexicano", "page_id": "122100824929548904", "nombre": "El Pulso Mexicano"},
    15: {"slug": "enfoquecapital", "page_id": "457328060805587", "nombre": "Enfoque Capital"},
    16: {"slug": "enfoquedirecto", "page_id": "122124424060548904", "nombre": "Enfoque Directo"},
    17: {"slug": "formulacdmx", "page_id": "122108195378548904", "nombre": "F�rmula CDMX"},
    18: {"slug": "mexicantimes", "page_id": "122108195378548904", "nombre": "The Mexican Times"},
    19: {"slug": "mexico360noticias", "page_id": "122108195378548904", "nombre": "M�xico 360 Noticias"},
    20: {"slug": "mradio", "page_id": "122108195378548904", "nombre": "M Radio"},
    21: {"slug": "noticiashorizonte", "page_id": "403046706229851", "nombre": "Noticias Horizonte"},
    22: {"slug": "pulsodiario", "page_id": "429372300256610", "nombre": "Pulso Diario"},
    23: {"slug": "puntoclave", "page_id": "497685936753403", "nombre": "Punto Clave"},
    24: {"slug": "puntonoticias", "page_id": "122108195378548904", "nombre": "Punto Noticias"},
    25: {"slug": "radarinformativo", "page_id": "122108195378548904", "nombre": "Radar Informativo"},
    26: {"slug": "reportediario", "page_id": "122108195378548904", "nombre": "Reporte Diario"},
    27: {"slug": "televisionabc", "page_id": "122108195378548904", "nombre": "Televisi�n ABC"}
}

def mostrar_sitios():
    """Muestra la lista de sitios disponibles"""
    print("\n" + "="*80)
    print("SITIOS DISPONIBLES PARA ELIMINAR PUBLICACIONES")
    print("="*80)

    for i, sitio in SITIOS.items():
        print(f"  [{i:2d}] {sitio['nombre']:30s} (Page ID: {sitio['page_id']})")

    print("\n  [0] TODOS los sitios")
    print("="*80)

def seleccionar_sitios():
    """Permite al usuario seleccionar uno o m�ltiples sitios"""
    mostrar_sitios()

    seleccion = input("\nSelecciona los sitios (ej: 1,2,3 o 1-5 o 0 para todos): ").strip()

    if seleccion == "0":
        return list(SITIOS.keys())

    sitios_seleccionados = set()

    # Procesar selecci�n m�ltiple
    for parte in seleccion.split(","):
        parte = parte.strip()

        if "-" in parte:
            # Rango (ej: 1-5)
            try:
                inicio, fin = map(int, parte.split("-"))
                sitios_seleccionados.update(range(inicio, fin + 1))
            except ValueError:
                print(f"??  Rango inv�lido:{parte}")
        else:
            # Individual
            try:
                sitios_seleccionados.add(int(parte))
            except ValueError:
                print(f"??  N�mero inv�lido:{parte}")

    # Filtrar sitios v�lidos
    sitios_validos = [s for s in sitios_seleccionados if s in SITIOS]

    if not sitios_validos:
        print("? No se seleccionaron sitios v�lidos")
        return seleccionar_sitios()

    return sitios_validos

def obtener_posts(page_id, user_token):
    """Obtiene las publicaciones de una p�gina"""
    url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
    params = {
        "access_token": user_token,
        "limit": 100,
        "fields": "id,message,created_time"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "data" in data:
            return data["data"]
        return []

    except requests.exceptions.RequestException as e:
        print(f"? Error al obtener posts: {e}")
        return []

def eliminar_post(post_id, user_token):
    """Elimina una publicaci�n espec�fica"""
    url = f"https://graph.facebook.com/v19.0/{post_id}"
    params = {
        "access_token": user_token
    }

    try:
        response = requests.delete(url, params=params, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"   ? Error: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("ELIMINADOR DE PUBLICACIONES FACEBOOK - NexoPress")
    print("="*80)

    # Seleccionar sitios
    sitios_ids = seleccionar_sitios()

    print(f"\n? Sitios seleccionados: {len(sitios_ids)}")
    for sid in sitios_ids:
        print(f"    {SITIOS[sid]['nombre']}")

    # Solicitar User Token
    print("\n" + "="*80)
    print("INGRESA TU USER TOKEN DE FACEBOOK")
    print("="*80)
    print("??  El token debe tener permisos: pages_manage_posts, pages_read_engagement)
    print("??  Puedes obtenerlo en: https://developers.facebook.com/tools/explorer/")
    print("="*80)

    user_token = input("\nUser Token: ").strip()

    if not user_token:
        print("? Token requerido")
        return

    # Confirmar
    print("\n" + "="*80)
    confirm = input(f"�Eliminar TODAS las publicaciones de {len(sitios_ids)} sitio(s)? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("? Operaci�n cancelada")
        return

    # Procesar cada sitio
    total_eliminados = 0
    total_error = 0

    for sid in sitios_ids:
        sitio = SITIOS[sid]
        print(f"\n{'='*80}")
        print(f"?? Procesando: {sitio['nombre']} (Page ID: {sitio['page_id']})")
        print(f"{'='*80}")

        # Obtener posts
        print("   ?? Obteniendo publicaciones...")
        posts = obtener_posts(sitio['page_id'], user_token)

        if not posts:
            print("   ??  No se encontraron publicaciones)
            continue

        print(f"   ?? {len(posts)} publicaciones encontradas")

        # Eliminar posts
        eliminados = 0
        errores = 0

        for post in posts:
            post_id = post.get('id', '')
            created = post.get('created_time', 'N/A')[:10]
            message = post.get('message', '')[:50].replace('\n', ' ')

            print(f"   ???  {post_id}] ({created}) {message}...", end=" ")

            if eliminar_post(post_id, user_token):
                print("? OK")
                eliminados += 1
            else:
                errores += 1

        total_eliminados += eliminados
        total_error += errores

        print(f"\n   ?? Resultado: {eliminados} eliminados, {errores} errores")

    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN FINAL")
    print("="*80)
    print(f"? Publicaciones eliminadas: {total_eliminados}")
    print(f"? Errores: {total_error}")
    print("="*80)
    print("�Proceso completado!")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n??  Proceso interrumpido por el usuario)
    except Exception as e:
        print(f"\n? Error inesperado: {e}")
