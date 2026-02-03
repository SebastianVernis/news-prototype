#!/usr/bin/env python3
"""
Script para descargar noticias de NewsAPI.org
API: https://newsapi.org
Registro: https://newsapi.org/register
"""

import os
import sys

import requests
from dotenv import load_dotenv

# Agregar directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.utils import enrich_with_full_text, print_summary, save_articles

load_dotenv()

API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/everything"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"}


def fetch_newsapi(
    query: str = "política México",
    language: str = "es",
    page_size: int = 20,
    enrich: bool = True,
    silent: bool = False,
) -> list:
    """
    Descarga noticias de NewsAPI.org

    Args:
        query: Términos de búsqueda
        language: Código de idioma
        page_size: Número de artículos a obtener
        enrich: Si debe extraer texto completo

    Returns:
        Lista de artículos descargados
    """
    if not API_KEY:
        raise ValueError("❌ NEWSAPI_KEY no encontrada en .env")

    if not silent:
        print(f"\n{'=' * 70}")
        print("📥 Descargando noticias de NewsAPI.org")
        print(f"{'=' * 70}")
        print(f"🔍 Query: {query}")
        print(f"🌐 Idioma: {language}")
        print(f"📊 Cantidad: {page_size}")

    params = {
        "q": query,
        "apiKey": API_KEY,
        "language": language,
        "sortBy": "publishedAt",
        "pageSize": page_size,
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()

        data = response.json()

        if data.get("status") != "ok":
            raise Exception(
                f"Error en respuesta API: {data.get('message', 'Unknown error')}"
            )

        articles = data.get("articles", [])

        if not silent:
            print(f"✅ Descargados {len(articles)} artículos")

        # Enriquecer con texto completo si se solicita
        if enrich and articles:
            if not silent:
                print(f"\n📝 Extrayendo texto completo...")
            articles = enrich_with_full_text(articles, "newsapi", verbose=not silent)

        # Guardar resultados solo si no es modo silencioso
        if not silent:
            # Obtener directorio raíz del sitio
            from pathlib import Path

            generated_sites_dir = (
                Path(__file__).parent.parent.parent / "generated_sites"
            )
            output_dir = (
                str(generated_sites_dir) if generated_sites_dir.exists() else "."
            )

            json_file, csv_file = save_articles(articles, "newsapi", output_dir)
            print_summary(articles, "NewsAPI.org", json_file, csv_file)

        return articles

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        raise
    except Exception as e:
        print(f"❌ Error procesando datos: {e}")
        raise


def main():
    """Función principal para ejecutar el script"""
    import argparse

    parser = argparse.ArgumentParser(description="Descargar noticias de NewsAPI.org")
    parser.add_argument(
        "--query",
        type=str,
        default="política México",
        help='Términos de búsqueda (default: "política México")',
    )
    parser.add_argument(
        "--language", type=str, default="es", help="Código de idioma (default: es)"
    )
    parser.add_argument(
        "--size", type=int, default=20, help="Número de artículos (default: 20)"
    )
    parser.add_argument(
        "--no-enrich", action="store_true", help="No extraer texto completo"
    )

    args = parser.parse_args()

    try:
        articles = fetch_newsapi(
            query=args.query,
            language=args.language,
            page_size=args.size,
            enrich=not args.no_enrich,
        )

        print(f"🎉 Proceso completado: {len(articles)} artículos guardados")

    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        exit(1)


if __name__ == "__main__":
    main()
