#!/usr/bin/env python3
"""
Utilities for news ingestion pipelines.
"""

from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Dict, Any

import requests

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:  # pragma: no cover
    BeautifulSoup = None

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = Path(os.getenv("NEWS_DATA_DIR", REPO_ROOT / "data"))
DEFAULT_DATA_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def normalize_article(article: Dict[str, Any], source: str) -> Dict[str, Any]:
    """Normalize article payloads into a consistent schema."""
    return {
        "source": source,
        "title": article.get("title") or article.get("headline") or "",
        "description": article.get("description") or article.get("summary") or "",
        "content": article.get("content") or article.get("full_text") or "",
        "url": article.get("url") or article.get("link") or "",
        "image": article.get("urlToImage") or article.get("image") or "",
        "author": article.get("author") or article.get("creator") or "Redacción",
        "published_at": article.get("publishedAt") or article.get("pubDate") or "",
    }


def save_articles(
    articles: Iterable[Dict[str, Any]],
    source: str,
    output_dir: str | None = None,
) -> tuple[str, str]:
    """Save articles to JSON and CSV files."""
    output_path = Path(output_dir) if output_dir else DEFAULT_DATA_DIR
    output_path.mkdir(parents=True, exist_ok=True)

    json_file = output_path / f"{source}_{_timestamp()}.json"
    csv_file = output_path / f"{source}_{_timestamp()}.csv"

    articles_list = list(articles)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(articles_list, f, ensure_ascii=False, indent=2)

    fieldnames = [
        "source",
        "title",
        "description",
        "content",
        "url",
        "image",
        "author",
        "published_at",
    ]
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles_list:
            normalized = normalize_article(article, source)
            writer.writerow(normalized)

    return str(json_file), str(csv_file)


def print_summary(
    articles: Iterable[Dict[str, Any]],
    source_name: str,
    json_file: str,
    csv_file: str,
) -> None:
    articles_list = list(articles)
    print("\n" + "=" * 70)
    print(f"✅ {source_name}: {len(articles_list)} artículos")
    print(f"📄 JSON: {json_file}")
    print(f"📄 CSV: {csv_file}")
    print("=" * 70)


def _extract_full_text(url: str, timeout: int = 15) -> str | None:
    if not url or BeautifulSoup is None:
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        
        # Detectar encoding correctamente
        if resp.encoding == 'ISO-8859-1':
            resp.encoding = resp.apparent_encoding
            
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        text = "\n\n".join(p for p in paragraphs if p)
        return text.strip() or None
    except Exception:
        return None


def enrich_with_full_text(
    articles: List[Dict[str, Any]],
    source: str,
    verbose: bool = False,
) -> List[Dict[str, Any]]:
    """Attempt to enrich articles with full text (limited for performance)."""
    max_fetch = int(os.getenv("FULLTEXT_MAX", "100"))  # Aumentado de 5 a 100
    enriched = []

    for idx, article in enumerate(articles):
        # Para NewsAPI, el content ya viene truncado, intentar extraer full text
        if source == "newsapi":
            content = article.get("content", "")
            # Si el content tiene [+XXXX chars], significa que está truncado
            if "[+" in content and "]" in content:
                url = article.get("url") or ""
                if idx < max_fetch:
                    full_text = _extract_full_text(url)
                    if full_text:
                        article["full_text"] = full_text
                        if verbose:
                            print(f"✅ Texto completo extraído ({source}): {article.get('title', '')[:60]}")
                    else:
                        # Usar content truncado como fallback
                        article["full_text"] = content.replace(f"[+{content.split('[+')[1]}", "") if "[+" in content else content
                else:
                    # Usar content truncado como fallback
                    article["full_text"] = content.split("[+")[0].strip() if "[+" in content else content
            else:
                article["full_text"] = content
        else:
            # Otros sources
            url = article.get("url") or ""
            if idx < max_fetch:
                full_text = _extract_full_text(url)
                if full_text:
                    article["full_text"] = full_text
                    if verbose:
                        print(f"✅ Texto completo extraído ({source}): {article.get('title', '')[:60]}")
        
        enriched.append(article)

    return enriched
