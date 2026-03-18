#!/usr/bin/env python3
"""
Script para corregir artículos existentes con SLUG NULL o vacío
Genera slugs para artículos parafraseados que no tienen slug válido
"""

import subprocess
import json
import re
from datetime import datetime


def slugify(text):
    """Convierte texto a slug URL-friendly"""
    if not text:
        return ""

    text = str(text).lower().strip()

    # Reemplazar acentos
    replacements = [
        (r"[áàäâã]", "a"),
        (r"[éèëê]", "e"),
        (r"[íìïî]", "i"),
        (r"[óòöôõ]", "o"),
        (r"[úùüû]", "u"),
        (r"[ñ]", "n"),
        (r"[ç]", "c"),
        (r"[ý]", "y"),
    ]

    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)

    # Reemplazar espacios y caracteres especiales
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^\w\-]+", "", text)
    text = re.sub(r"\-+", "-", text)
    text = text.strip("-")

    return text[:100]


def normalize_title(text):
    """Normaliza el título para generar slug"""
    if not text:
        return ""

    prefixes = [
        r"^la\s+jornada:\s*",
        r"^el\s+informador:\s*",
        r"^proceso:\s*",
        r"^el\s+universal:\s*",
        r"^milenio:\s*",
        r"^excelsior:\s*",
        r"^excélsior:\s*",
        r"^expansion:\s*",
        r"^expansión:\s*",
        r"^publimetro:\s*",
        r"^azteca\s+noticias:\s*",
        r"^tv\s+azteca:\s*",
    ]

    cleaned = text.strip()
    for prefix in prefixes:
        cleaned = re.sub(prefix, "", cleaned, flags=re.IGNORECASE)

    cleaned = re.sub(
        r"\s*[|\-]\s*(la\s+jornada|el\s+informador|proceso|el\s+universal|milenio|excelsior|excélsior|expansion|expansión|publimetro|azteca\s+noticias|tv\s+azteca)\s*$",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    return cleaned.strip()


def article_slugify(text):
    """Genera slug para artículo"""
    return slugify(normalize_title(text))


def get_null_slug_articles():
    """Obtiene artículos con SLUG NULL o vacío"""
    print("Buscando artículos con SLUG NULL...")

    cmd = [
        "wrangler",
        "d1",
        "execute",
        "news_db",
        "--command",
        'SELECT ID, TITULO_PARAFRASEADO, FECHA_PUBLICACION FROM ARTICULOS_PARAFRASEADOS WHERE SLUG IS NULL OR SLUG = "" LIMIT 100',
        "--remote",
        "--json",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("results", [])
        else:
            print(f"Error: {result.stderr}")
            return []
    except Exception as e:
        print(f"Error ejecutando comando: {e}")
        return []


def update_article_slug(article_id, slug):
    """Actualiza el slug de un artículo"""
    cmd = [
        "wrangler",
        "d1",
        "execute",
        "news_db",
        "--command",
        f'UPDATE ARTICULOS_PARAFRASEADOS SET SLUG = "{slug}" WHERE ID = "{article_id}"',
        "--remote",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        print(f"Error actualizando artículo {article_id}: {e}")
        return False


def main():
    print("=" * 60)
    print("CORRECCIÓN DE ARTÍCULOS SIN SLUG")
    print("=" * 60)

    # Obtener artículos sin slug
    articles = get_null_slug_articles()

    if not articles:
        print("No se encontraron artículos con SLUG NULL.")
        return

    print(f"\nSe encontraron {len(articles)} artículos sin SLUG:\n")

    fixed_count = 0
    error_count = 0

    for article in articles:
        article_id = article.get("ID")
        title = article.get("TITULO_PARAFRASEADO", "")
        fecha = article.get("FECHA_PUBLICACION", "")

        # Generar slug
        slug = article_slugify(title)

        # Si sigue vacío, usar fallback con timestamp
        if not slug:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            slug = f"articulo-{timestamp}"

        print(f"ID: {article_id}")
        print(f"Título: {title[:60]}...")
        print(f"Fecha: {fecha}")
        print(f"Nuevo slug: {slug}")

        # Actualizar en DB
        if update_article_slug(article_id, slug):
            print("✅ Actualizado\n")
            fixed_count += 1
        else:
            print("❌ Error al actualizar\n")
            error_count += 1

    print("=" * 60)
    print(f"Resumen: {fixed_count} corregidos, {error_count} errores")
    print("=" * 60)


if __name__ == "__main__":
    main()
