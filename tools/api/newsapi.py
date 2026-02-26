#!/usr/bin/env python3
"""
Script para descargar noticias de NewsAPI.org
API: https://newsapi.org
Registro: https://newsapi.org/register
"""

# NOTA: No ejecutamos load_dotenv() aquí porque el script principal
# (ai_multi_source_publish_flow.py) ya carga las variables de entorno
# correctamente antes de importar este módulo.

import os
import sys
from datetime import datetime, timedelta

import requests

# Agregar raíz del repo al path para imports
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from utils.utils import enrich_with_full_text, print_summary, save_articles

# Las variables de entorno ya están cargadas por el script principal
BASE_URL = os.getenv("NEWSAPI_URL", "https://newsapi.org/v2/everything")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"}


def fetch_newsapi(
    query: str = "política México",
    language: str = "es",
    page_size: int = 20,
    from_date: str | None = None,
    to_date: str | None = None,
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
    api_key = os.getenv("NEWSAPI_KEY") or os.getenv("NEWSAPI_API_KEY")
    if not api_key:
        raise ValueError("NEWSAPI_KEY no encontrada en .env")

    if not silent:
        print(f"\n{'=' * 70}")
        print("📥 Descargando noticias de NewsAPI.org")
        print(f"{'=' * 70}")
        print(f"🔍 Query: {query}")
        print(f"🌐 Idioma: {language}")
        print(f"📊 Cantidad: {page_size}")

    params = {
        "q": query,
        "apiKey": api_key,
        "language": language,
        "sortBy": "publishedAt",
        "pageSize": page_size,
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

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
            # Obtener directorio de salida
            from pathlib import Path

            repo_root = Path(__file__).resolve().parents[2]
            output_dir = os.getenv("NEWS_DATA_DIR", str(repo_root / "data"))

            json_file, csv_file = save_articles(articles, "newsapi", output_dir)
            print_summary(articles, "NewsAPI.org", json_file, csv_file)

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error de conexion: {e}")
        raise
    except Exception as e:
        print(f"Error procesando datos: {e}")
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
        "--past-size",
        type=int,
        default=0,
        help="Cantidad de noticias anteriores a hoy (default: 0)",
    )
    parser.add_argument(
        "--today-size",
        type=int,
        default=0,
        help="Cantidad de noticias de hoy (default: 0)",
    )
    parser.add_argument(
        "--past-days",
        type=int,
        default=7,
        help="Rango de días hacia atrás para noticias pasadas (default: 7)",
    )
    parser.add_argument(
        "--past-from",
        type=str,
        help="Fecha inicio para noticias pasadas (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--past-to",
        type=str,
        help="Fecha fin para noticias pasadas (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--no-enrich", action="store_true", help="No extraer texto completo"
    )

    args = parser.parse_args()

    try:
        # Si se especifica past/today, descargar por rangos y combinar
        if args.past_size or args.today_size:
            all_articles = []
            today = datetime.utcnow().date()

            if args.past_size:
                past_from = args.past_from or (today - timedelta(days=args.past_days)).isoformat()
                past_to = args.past_to or (today - timedelta(days=1)).isoformat()
                if past_from <= past_to:
                    past_articles = fetch_newsapi(
                        query=args.query,
                        language=args.language,
                        page_size=args.past_size,
                        from_date=past_from,
                        to_date=past_to,
                        enrich=not args.no_enrich,
                        silent=True,
                    )
                    all_articles.extend(past_articles)
                else:
                    print("⚠️  Rango de fechas pasadas inválido, se omite")

            if args.today_size:
                today_str = today.isoformat()
                today_articles = fetch_newsapi(
                    query=args.query,
                    language=args.language,
                    page_size=args.today_size,
                    from_date=today_str,
                    to_date=today_str,
                    enrich=not args.no_enrich,
                    silent=True,
                )
                all_articles.extend(today_articles)

            # Deduplicar por URL
            seen = set()
            merged = []
            for a in all_articles:
                key = a.get("url") or a.get("title")
                if key and key in seen:
                    continue
                if key:
                    seen.add(key)
                merged.append(a)

            # Guardar resultados
            repo_root = Path(__file__).resolve().parents[2]
            output_dir = os.getenv("NEWS_DATA_DIR", str(repo_root / "data"))
            json_file, csv_file = save_articles(merged, "newsapi", output_dir)
            print_summary(merged, "NewsAPI.org", json_file, csv_file)
            print(f"🎉 Proceso completado: {len(merged)} artículos guardados")
        else:
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
