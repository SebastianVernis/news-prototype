#!/usr/bin/env python3
"""
Descarga imágenes originales de noticias y actualiza el JSON con rutas locales.
"""

import argparse
import hashlib
import json
import mimetypes
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]


def _safe_ext(url: str, content_type: str | None) -> str:
    ext = Path(urlparse(url).path).suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        return ext
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if guessed:
            return guessed
    return ".jpg"


def _hash_name(url: str, ext: str) -> str:
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    return f"img_{digest}{ext}"


def _get_image_url(article: dict) -> str | None:
    return (
        article.get("image")
        or article.get("urlToImage")
        or article.get("imageUrl")
        or article.get("image_url")
    )


def cache_images(input_path: Path, output_path: Path, assets_dir: Path, max_images: int, timeout: int) -> int:
    assets_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("El archivo de entrada debe ser una lista de artículos")

    cached = 0
    for article in data:
        if max_images and cached >= max_images:
            break
        url = _get_image_url(article)
        if not url or not url.startswith("http"):
            continue

        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            ext = _safe_ext(url, resp.headers.get("content-type"))
            filename = _hash_name(url, ext)
            file_path = assets_dir / filename
            if not file_path.exists():
                file_path.write_bytes(resp.content)
            rel_path = f"assets/images/{filename}"
            article["original_image"] = url
            article["image"] = rel_path
            article["urlToImage"] = rel_path
            article["imageUrl"] = rel_path
            cached += 1
        except Exception:
            continue

    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return cached


def main():
    parser = argparse.ArgumentParser(description="Cachea imágenes originales y actualiza JSON")
    parser.add_argument("--input", required=True, help="Archivo JSON de entrada")
    parser.add_argument("--output", help="Archivo JSON de salida")
    parser.add_argument("--assets-dir", help="Directorio assets/images")
    parser.add_argument("--max", type=int, default=0, help="Máximo de imágenes a descargar (0 = sin límite)")
    parser.add_argument("--timeout", type=int, default=20, help="Timeout por imagen (segundos)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print("❌ Archivo de entrada no encontrado")
        sys.exit(1)

    output_path = Path(args.output) if args.output else input_path.with_name(
        input_path.stem + "_cached_images.json"
    )
    assets_dir = Path(
        args.assets_dir
        or os.getenv("NEWS_ASSETS_DIR", str(REPO_ROOT / "assets"))
    ) / "images"

    cached = cache_images(input_path, output_path, assets_dir, args.max, args.timeout)
    print(f"✅ Imágenes cacheadas: {cached}")
    print(f"📄 Archivo actualizado: {output_path}")


if __name__ == "__main__":
    main()
