#!/usr/bin/env python3
"""
Script para descargar noticias de WorldNewsAPI
API: https://worldnewsapi.com
Registro: https://worldnewsapi.com/register
Ventaja: Búsqueda avanzada con filtros detallados
"""

import os
import sys
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Agregar raíz del repo al path para imports
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from utils.utils import normalize_article, save_articles, print_summary

load_dotenv()

API_KEY = os.getenv('WORLDNEWS_KEY')
BASE_URL = 'https://api.worldnewsapi.com/search-news'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)',
    'x-api-key': API_KEY
}


def fetch_worldnews(query: str = 'política México',
                    source_country: str = 'mx',
                    language: str = 'es',
                    number: int = 20,
                    earliest_publish_date: str = None,
                    latest_publish_date: str = None,
                    silent: bool = False) -> list:
    """
    Descarga noticias de WorldNewsAPI
    
    Args:
        query: Términos de búsqueda
        source_country: Código de país
        language: Código de idioma
        number: Número de artículos a obtener
        earliest_publish_date: Fecha mínima (YYYY-MM-DD)
        
    Returns:
        Lista de artículos descargados
    """
    if not API_KEY:
        raise ValueError("❌ WORLDNEWS_KEY no encontrada en .env")
    
    if not silent:
        print(f"\n{'='*70}")
        print("📥 Descargando noticias de WorldNewsAPI")
        print(f"{'='*70}")
        print(f"🔍 Query: {query}")
        print(f"🌍 País: {source_country.upper()}")
        print(f"🌐 Idioma: {language}")
        print(f"📊 Cantidad: {number}")
    
    params = {
        'text': query,
        'source-countries': source_country,
        'language': language,
        'number': number
    }
    
    if earliest_publish_date:
        params['earliest-publish-date'] = earliest_publish_date
        if not silent:
            print(f"📅 Desde: {earliest_publish_date}")
    if latest_publish_date:
        params['latest-publish-date'] = latest_publish_date
        if not silent:
            print(f"📅 Hasta: {latest_publish_date}")
    
    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get('news', [])
        
        if not articles:
            if not silent:
                print("⚠️  No se encontraron artículos")
            return []
        
        if not silent:
            print(f"✅ Descargados {len(articles)} artículos")
        
        # Normalizar estructura
        normalized = []
        for article in articles:
            normalized.append(normalize_article(article, 'worldnews'))
        
        # Guardar resultados solo si no es modo silencioso
        if not silent:
            json_file, csv_file = save_articles(normalized, 'worldnews')
            print_summary(normalized, 'WorldNewsAPI', json_file, csv_file)
        
        return normalized
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        print(f"💡 Verifica que tu API key de WorldNewsAPI sea válida")
        raise
    except Exception as e:
        print(f"❌ Error procesando datos: {e}")
        raise


def main():
    """Función principal para ejecutar el script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Descargar noticias de WorldNewsAPI')
    parser.add_argument('--query', type=str, default='política México',
                       help='Términos de búsqueda (default: "política México")')
    parser.add_argument('--country', type=str, default='mx',
                       help='Código de país (default: mx)')
    parser.add_argument('--language', type=str, default='es',
                       help='Código de idioma (default: es)')
    parser.add_argument('--size', type=int, default=20,
                       help='Número de artículos (default: 20)')
    parser.add_argument('--from-date', type=str,
                       help='Fecha mínima YYYY-MM-DD (ej: 2024-01-01)')
    parser.add_argument('--to-date', type=str,
                       help='Fecha máxima YYYY-MM-DD (ej: 2024-01-31)')
    parser.add_argument(
        '--past-size',
        type=int,
        default=0,
        help='Cantidad de noticias anteriores a hoy (default: 0)',
    )
    parser.add_argument(
        '--today-size',
        type=int,
        default=0,
        help='Cantidad de noticias de hoy (default: 0)',
    )
    parser.add_argument(
        '--past-days',
        type=int,
        default=7,
        help='Rango de días hacia atrás para noticias pasadas (default: 7)',
    )
    parser.add_argument(
        '--past-from',
        type=str,
        help='Fecha inicio para noticias pasadas (YYYY-MM-DD)',
    )
    parser.add_argument(
        '--past-to',
        type=str,
        help='Fecha fin para noticias pasadas (YYYY-MM-DD)',
    )
    
    args = parser.parse_args()
    
    try:
        if args.past_size or args.today_size:
            all_articles = []
            today = datetime.utcnow().date()

            if args.past_size:
                past_from = args.past_from or (today - timedelta(days=args.past_days)).isoformat()
                past_to = args.past_to or (today - timedelta(days=1)).isoformat()
                if past_from <= past_to:
                    past_articles = fetch_worldnews(
                        query=args.query,
                        source_country=args.country,
                        language=args.language,
                        number=args.past_size,
                        earliest_publish_date=past_from,
                        latest_publish_date=past_to,
                        silent=True,
                    )
                    all_articles.extend(past_articles)
                else:
                    print("⚠️  Rango de fechas pasadas inválido, se omite")

            if args.today_size:
                today_str = today.isoformat()
                today_articles = fetch_worldnews(
                    query=args.query,
                    source_country=args.country,
                    language=args.language,
                    number=args.today_size,
                    earliest_publish_date=today_str,
                    latest_publish_date=today_str,
                    silent=True,
                )
                all_articles.extend(today_articles)

            seen = set()
            merged = []
            for a in all_articles:
                key = a.get("url") or a.get("title")
                if key and key in seen:
                    continue
                if key:
                    seen.add(key)
                merged.append(a)

            json_file, csv_file = save_articles(merged, 'worldnews')
            print_summary(merged, 'WorldNewsAPI', json_file, csv_file)
            print(f"🎉 Proceso completado: {len(merged)} artículos guardados")
        else:
            articles = fetch_worldnews(
                query=args.query,
                source_country=args.country,
                language=args.language,
                number=args.size,
                earliest_publish_date=args.from_date,
                latest_publish_date=args.to_date,
            )
            
            print(f"🎉 Proceso completado: {len(articles)} artículos guardados")
        
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        exit(1)


if __name__ == '__main__':
    main()
