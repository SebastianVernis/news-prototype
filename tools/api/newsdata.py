#!/usr/bin/env python3
"""
Script para descargar noticias de Newsdata.io
API: https://newsdata.io
Registro: https://newsdata.io/register
Ventaja: Incluye contenido completo en la respuesta
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

API_KEY = os.getenv('NEWSDATA_KEY')
BASE_URL = 'https://newsdata.io/api/1/news'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'}


def fetch_newsdata(query: str = 'política México',
                   country: str = 'mx',
                   language: str = 'es',
                   category: str = 'politics',
                   page_size: int = 10,
                   from_date: str | None = None,
                   to_date: str | None = None,
                   silent: bool = False) -> list:
    """
    Descarga noticias de Newsdata.io
    
    Args:
        query: Términos de búsqueda
        country: Código de país
        language: Código de idioma
        category: Categoría de noticias
        page_size: Número de artículos (máx 10 en plan gratuito)
        
    Returns:
        Lista de artículos descargados
    """
    if not API_KEY:
        raise ValueError("❌ NEWSDATA_KEY no encontrada en .env")
    
    if not silent:
        print(f"\n{'='*70}")
        print("📥 Descargando noticias de Newsdata.io")
        print(f"{'='*70}")
        print(f"🔍 Query: {query}")
        print(f"🌍 País: {country.upper()}")
        print(f"🌐 Idioma: {language}")
        print(f"📂 Categoría: {category}")
        print(f"📊 Cantidad: {page_size}")
    
    params = {
        'q': query,
        'country': country,
        'language': language,
        'category': category,
        'apikey': API_KEY
    }
    if from_date:
        params['from_date'] = from_date
    if to_date:
        params['to_date'] = to_date
    
    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('status') != 'success':
            raise Exception(f"Error en respuesta API: {data.get('results', {}).get('message', 'Unknown error')}")
        
        articles = data.get('results', [])
        
        if not articles:
            if not silent:
                print("⚠️  No se encontraron artículos")
            return []
        
        if not silent:
            print(f"✅ Descargados {len(articles)} artículos con contenido completo")
        
        # Normalizar estructura
        normalized = []
        for article in articles:
            normalized.append(normalize_article(article, 'newsdata'))
        
        # Guardar resultados solo si no es modo silencioso
        if not silent:
            json_file, csv_file = save_articles(normalized, 'newsdata')
            print_summary(normalized, 'Newsdata.io', json_file, csv_file)
        
        return normalized
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        raise
    except Exception as e:
        print(f"❌ Error procesando datos: {e}")
        raise


def main():
    """Función principal para ejecutar el script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Descargar noticias de Newsdata.io')
    parser.add_argument('--query', type=str, default='política México',
                       help='Términos de búsqueda (default: "política México")')
    parser.add_argument('--country', type=str, default='mx',
                       help='Código de país (default: mx)')
    parser.add_argument('--language', type=str, default='es',
                       help='Código de idioma (default: es)')
    parser.add_argument('--category', type=str, default='politics',
                       help='Categoría (default: politics)')
    parser.add_argument('--size', type=int, default=10,
                       help='Número de artículos (default: 10, máx 10 en plan gratuito)')
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
                    past_articles = fetch_newsdata(
                        query=args.query,
                        country=args.country,
                        language=args.language,
                        category=args.category,
                        page_size=min(args.past_size, 10),
                        from_date=past_from,
                        to_date=past_to,
                        silent=True,
                    )
                    all_articles.extend(past_articles)
                else:
                    print("⚠️  Rango de fechas pasadas inválido, se omite")

            if args.today_size:
                today_str = today.isoformat()
                today_articles = fetch_newsdata(
                    query=args.query,
                    country=args.country,
                    language=args.language,
                    category=args.category,
                    page_size=min(args.today_size, 10),
                    from_date=today_str,
                    to_date=today_str,
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

            json_file, csv_file = save_articles(merged, 'newsdata')
            print_summary(merged, 'Newsdata.io', json_file, csv_file)
            print(f"🎉 Proceso completado: {len(merged)} artículos guardados")
        else:
            articles = fetch_newsdata(
                query=args.query,
                country=args.country,
                language=args.language,
                category=args.category,
                page_size=args.size
            )
            
            print(f"🎉 Proceso completado: {len(articles)} artículos guardados")
        
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        exit(1)


if __name__ == '__main__':
    main()
