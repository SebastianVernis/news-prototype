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
from dotenv import load_dotenv

# Agregar directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
    
    args = parser.parse_args()
    
    try:
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
