#!/usr/bin/env python3
"""
Recover missing images for cms-nuevos2 by re-downloading from original sources
and re-uploading to R2.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests

sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.api.r2_image_manager import R2ImageManager

CLOUDLFARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
R2_BUCKET = "cms-news"


def get_original_image_url(cms_url: str, article_id: str) -> str | None:
    """Get original image URL from ARTICULOS_ORIGINALES via API"""
    try:
        resp = requests.get(f"{cms_url}/api/articles/{article_id}/original", timeout=30)
        if resp.ok:
            data = resp.json()
            return data.get("urlImagen") or data.get("URL_IMAGEN")
    except Exception:
        pass
    return None


def download_and_upload_image(
    source_url: str, r2_key: str, manager: R2ImageManager
) -> bool:
    """Download image from source and upload to R2"""
    if not source_url or not source_url.startswith("http"):
        return False

    try:
        resp = requests.get(source_url, timeout=60, stream=True)
        resp.raise_for_status()
        content = resp.content

        existing = manager.check_exists(r2_key)
        if existing:
            print(f"  Already exists: {r2_key}")
            return True

        success = manager.upload(r2_key, content)
        if success:
            print(f"  Uploaded: {r2_key}")
        else:
            print(f"  Failed to upload: {r2_key}")
        return success
    except Exception as e:
        print(f"  Error downloading {source_url}: {e}")
        return False


def extract_r2_key_from_url(url: str) -> str | None:
    """Extract the R2 key (filename) from a URL like https://uploads.sebastianvernis.space/auto/uuid.jpg"""
    if not url:
        return None
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if path.startswith("auto/") or path.startswith("uploads/"):
        return path.split("/")[-1]
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Recover missing images for cms-nuevos2"
    )
    parser.add_argument("--cms-url", required=True, help="Base URL of the CMS")
    parser.add_argument(
        "--articles-file", help="JSON file with articles (alternative to DB)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Don't actually upload")
    parser.add_argument(
        "--limit", type=int, default=0, help="Limit number of articles to process"
    )
    args = parser.parse_args()

    manager = R2ImageManager(R2_BUCKET, CLOUDLFARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN)

    if args.articles_file:
        with open(args.articles_file) as f:
            articles = json.load(f)
    else:
        print("Fetching articles from API...")
        resp = requests.get(
            f"{args.cms_url}/api/articles?site=all&limit=1000", timeout=30
        )
        data = resp.json()
        articles = data.get("articles", [])

    if args.limit:
        articles = articles[: args.limit]

    print(f"Processing {len(articles)} articles...")

    recovered = 0
    missing = 0

    for article in articles:
        article_id = article.get("id")
        current_image_url = article.get("imageUrl", "")
        r2_key = extract_r2_key_from_url(current_image_url)

        if not r2_key:
            print(f"Skipping {article_id}: no R2 key in URL")
            continue

        existing = manager.check_exists(r2_key)
        if existing:
            print(f"✓ {article_id}: Image already exists")
            continue

        print(f"Missing: {article_id} - {r2_key}")
        missing += 1

        if args.dry_run:
            continue

        original_url = article.get("originalImageUrl") or article.get("urlToImage")
        if not original_url:
            orig = get_original_image_url(args.cms_url, article_id)
            if orig:
                original_url = orig

        if original_url:
            success = download_and_upload_image(original_url, r2_key, manager)
            if success:
                recovered += 1
        else:
            print(f"  No original URL found for {article_id}")

    print(f"\nSummary: {missing} missing, {recovered} recovered")


if __name__ == "__main__":
    main()
