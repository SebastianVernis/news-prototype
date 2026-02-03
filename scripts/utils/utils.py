#!/usr/bin/env python3
"""
Utilidades compartidas para scrapers de noticias
Funciones comunes de web scraping y guardado de datos
"""

import json
from datetime import datetime
from typing import Dict, List

import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"}


def get_full_text(url: str, max_paragraphs: int = 10, max_chars: int = 5000) -> str:
    """
    Extrae el texto completo de un artículo web

    Args:
        url: URL del artículo
        max_paragraphs: Número máximo de párrafos a extraer
        max_chars: Número máximo de caracteres a retornar

    Returns:
        Texto completo del artículo
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, "html.parser")

        # Remover elementos no deseados
        for element in soup(
            ["script", "style", "nav", "header", "footer", "aside", "iframe"]
        ):
            element.decompose()

        # Extraer párrafos principales
        paragraphs = soup.find_all("p")[:max_paragraphs]
        text = " ".join(p.get_text(strip=True) for p in paragraphs)

        return text[:max_chars] if text else "Texto no disponible"

    except requests.exceptions.RequestException as e:
        print(f"❌ Error extrayendo texto de {url}: {e}")
        return "Texto no disponible"
    except Exception as e:
        print(f"❌ Error procesando HTML: {e}")
        return "Texto no disponible"


def save_articles(articles: List[Dict], prefix: str, output_dir: str = None) -> tuple:
    """
    Guarda artículos en formato JSON y CSV

    Args:
        articles: Lista de artículos a guardar
        prefix: Prefijo para los nombres de archivo
        output_dir: Directorio de salida. Si es None, usa el directorio raíz del sitio

    Returns:
        Tupla con (ruta_json, ruta_csv)
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    if output_dir is None:
        # Si no se especifica output_dir, usar el directorio raíz del sitio
        # Buscar el último sitio generado
        from pathlib import Path

        generated_sites_dir = Path(__file__).parent.parent.parent / "generated_sites"
        if generated_sites_dir.exists():
            site_dirs = list(generated_sites_dir.glob("site_*"))
            if site_dirs:
                latest_site = max(site_dirs, key=lambda p: p.stat().st_mtime)
                output_dir = str(latest_site.parent)
            else:
                output_dir = str(generated_sites_dir)
        else:
            output_dir = "."

    json_file = f"{output_dir}/{prefix}_{timestamp}.json"
    csv_file = f"{output_dir}/{prefix}_{timestamp}.csv"

    # Guardar JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    # Guardar CSV
    df = pd.DataFrame(articles)
    df.to_csv(csv_file, index=False, encoding="utf-8")

    return json_file, csv_file


def normalize_article(article: Dict, source: str) -> Dict:
    """
    Normaliza estructura de artículo según la fuente

    Args:
        article: Artículo raw de la API
        source: Nombre de la fuente (newsapi, apitube, etc.)

    Returns:
        Artículo con estructura normalizada
    """
    normalized = {
        "source": source,
        "title": "",
        "description": "",
        "url": "",
        "image_url": "",
        "published_at": "",
        "content": "",
        "full_text": "",
        "author": "",
        "source_name": "",
    }

    if source == "newsapi":
        normalized.update(
            {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "image_url": article.get("urlToImage", ""),
                "published_at": article.get("publishedAt", ""),
                "content": article.get("content", ""),
                "author": article.get("author", ""),
                "source_name": article.get("source", {}).get("name", ""),
            }
        )

    elif source == "apitube":
        normalized.update(
            {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "image_url": article.get("image", ""),
                "published_at": article.get("publishedAt", ""),
                "content": article.get("body", ""),
                "full_text": article.get("body", ""),
                "source_name": article.get("source", {}).get("name", ""),
            }
        )

    elif source == "newsdata":
        normalized.update(
            {
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("link", ""),
                "image_url": article.get("image_url", ""),
                "published_at": article.get("pubDate", ""),
                "content": article.get("content", ""),
                "full_text": article.get("content", ""),
                "source_name": article.get("source_id", ""),
            }
        )

    elif source == "worldnews":
        normalized.update(
            {
                "title": article.get("title", ""),
                "description": article.get("summary", ""),
                "url": article.get("url", ""),
                "image_url": article.get("image", ""),
                "published_at": article.get("publish_date", ""),
                "content": article.get("text", ""),
                "full_text": article.get("text", ""),
                "author": article.get("author", ""),
                "source_name": article.get("source", ""),
            }
        )

    return normalized


def enrich_with_full_text(
    articles: List[Dict], source: str, verbose: bool = True
) -> List[Dict]:
    """
    Enriquece artículos con texto completo extraído

    Args:
        articles: Lista de artículos
        source: Nombre de la fuente
        verbose: Mostrar progreso

    Returns:
        Lista de artículos enriquecidos
    """
    enriched = []
    total = len(articles)

    for idx, article in enumerate(articles, 1):
        if verbose:
            print(
                f"  [{idx}/{total}] Extrayendo: {article.get('title', 'Sin título')[:60]}..."
            )

        # Normalizar artículo
        normalized = normalize_article(article, source)

        # Si no tiene full_text, intentar extraerlo
        if not normalized["full_text"] and normalized["url"]:
            normalized["full_text"] = get_full_text(normalized["url"])

        enriched.append(normalized)

    return enriched


def print_summary(articles: List[Dict], source: str, json_file: str, csv_file: str):
    """
    Imprime resumen de descarga de artículos

    Args:
        articles: Lista de artículos
        source: Nombre de la fuente
        json_file: Ruta del archivo JSON
        csv_file: Ruta del archivo CSV
    """
    print(f"\n{'=' * 70}")
    print(f"✅ {source.upper()}: Descarga completada")
    print(f"{'=' * 70}")
    print(f"📰 Artículos descargados: {len(articles)}")
    print(f"💾 JSON: {json_file}")
    print(f"💾 CSV: {csv_file}")
    print(f"{'=' * 70}\n")
