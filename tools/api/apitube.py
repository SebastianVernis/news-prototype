#!/usr/bin/env python3
"""
Script para descargar noticias de APITube.io
API: https://apitube.io
Registro: https://apitube.io/register
Ventaja: Incluye body completo sin scraping adicional
"""

# NOTA: No ejecutamos load_dotenv() aquí porque el script principal
# (ai_multi_source_publish_flow.py) ya carga las variables de entorno
# correctamente antes de importar este módulo.
# Las variables se cargan desde tools/news/.env con prioridad.

import os
import sys
import requests

# Agregar raíz del repo al path para imports
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from utils.utils import normalize_article, save_articles, print_summary

# Las variables de entorno ya están cargadas por el script principal
BASE_URL = os.getenv('APITUBE_URL', 'https://api.apitube.io/v1/news/top-headlines')
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'}


def fetch_apitube(country: str = 'mx',
                  category: str = 'politics',
                  language: str = 'es',
                  page_size: int = 20,
                  silent: bool = False) -> list:
    """
    Descarga noticias de APITube.io
    
    Args:
        country: Código de país (mx, us, etc.)
        category: Categoría de noticias (politics, business, etc.)
        language: Código de idioma
        page_size: Número de artículos a obtener
        
    Returns:
        Lista de artículos descargados
    """
    api_key = os.getenv('APITUBE_KEY') or os.getenv('APITUBE_API_KEY')
    if not api_key:
        raise ValueError("APITUBE_KEY no encontrada en .env")
    
    if not silent:
        print(f"\n{'='*70}")
        print("📥 Descargando noticias de APITube.io")
        print(f"{'='*70}")
        print(f"🌍 País: {country.upper()}")
        print(f"📂 Categoría: {category}")
        print(f"🌐 Idioma: {language}")
        print(f"📊 Cantidad: {page_size}")
    
    params = {
        'country': country,
        'category': category,
        'language': language,
        'pageSize': page_size,
        'apiKey': api_key
    }
    
    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get('data', [])
        
        if not articles:
            if not silent:
                print("⚠️  No se encontraron artículos")
            return []
        
        if not silent:
            print(f"✅ Descargados {len(articles)} artículos con body completo")
        
        # Normalizar estructura
        normalized = []
        for article in articles:
            normalized.append(normalize_article(article, 'apitube'))
        
        # Guardar resultados solo si no es modo silencioso
        if not silent:
            json_file, csv_file = save_articles(normalized, 'apitube')
            print_summary(normalized, 'APITube.io', json_file, csv_file)
        
        return normalized
        
    except requests.exceptions.RequestException as e:
        print(f"Error de conexion: {e}")
        raise
    except Exception as e:
        print(f"Error procesando datos: {e}")
        raise


def main():
    """Función principal para ejecutar el script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Descargar noticias de APITube.io')
    parser.add_argument('--country', type=str, default='mx',
                       help='Código de país (default: mx)')
    parser.add_argument('--category', type=str, default='politics',
                       help='Categoría (default: politics)')
    parser.add_argument('--language', type=str, default='es',
                       help='Código de idioma (default: es)')
    parser.add_argument('--size', type=int, default=20,
                       help='Número de artículos (default: 20)')
    
    args = parser.parse_args()
    
    try:
        articles = fetch_apitube(
            country=args.country,
            category=args.category,
            language=args.language,
            page_size=args.size
        )
        
        print(f"🎉 Proceso completado: {len(articles)} artículos guardados")
        
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        exit(1)


if __name__ == '__main__':
    main()
