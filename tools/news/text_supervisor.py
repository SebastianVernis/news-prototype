#!/usr/bin/env python3
"""Supervisión de textos: ortografía, gramática y estructura sin alterar hechos."""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from llm_client import chat


def _clean_text(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("[…]", "").replace("...", "")
    text = re.sub(r"\[(PARAFRASEADO|CONTENIDO ACTUALIZADO|CONTENIDO AMPLIADO)\]\s*", "", text, flags=re.IGNORECASE)
    return text.strip()


def _extract_sentences(text: str, max_sentences: int = 2) -> str:
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    parts = [p for p in parts if p]
    return " ".join(parts[:max_sentences]).strip()


def detect_issues(article: Dict) -> List[str]:
    issues = []
    title = (article.get("title") or "").strip()
    description = (article.get("description") or "").strip()
    content = (article.get("content") or article.get("full_text") or "").strip()

    if not title or title.lower().startswith("noticia"):
        issues.append("missing_or_placeholder_title")
    if not description or "..." in description:
        issues.append("missing_or_placeholder_description")
    if not content or "..." in content:
        issues.append("missing_or_placeholder_content")
    if len(content.split()) < 120:
        issues.append("content_too_short")

    return issues


def local_fix(article: Dict) -> Dict:
    fixed = dict(article)
    title = _clean_text(fixed.get("title") or "")
    description = _clean_text(fixed.get("description") or "")
    content = _clean_text(fixed.get("content") or fixed.get("full_text") or "")

    if not title:
        title = _extract_sentences(description or content, 1)
    if not description:
        description = _extract_sentences(content, 2)

    fixed["title"] = title
    fixed["description"] = description
    fixed["content"] = content
    fixed["full_text"] = fixed.get("full_text") or content
    return fixed


def _prompt(article: Dict) -> List[Dict]:
    system = (
        "Eres un corrector profesional. Solo corrige ortografía, gramática y estructura. "
        "No cambies hechos ni agregues información nueva. No inventes datos. "
        "Devuelve JSON con title, description, content y full_text."
    )
    user = {
        "title": article.get("title", ""),
        "description": article.get("description", ""),
        "content": article.get("content", ""),
        "full_text": article.get("full_text", ""),
    }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
    ]


def _parse_json(text: str) -> Dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in response")
    return json.loads(match.group(0))


def supervise_article(article: Dict, provider: str, model: str) -> Dict:
    issues = detect_issues(article)
    if not issues:
        return article

    try:
        content = chat(provider, model, _prompt(article), temperature=0.2, max_tokens=1200)
        data = _parse_json(content)
        fixed = dict(article)
        fixed.update({
            "title": _clean_text(data.get("title", "")),
            "description": _clean_text(data.get("description", "")),
            "content": _clean_text(data.get("content", "")),
            "full_text": _clean_text(data.get("full_text", "")),
            "supervised": True,
            "supervisor_provider": provider,
            "supervisor_model": model,
        })
        return local_fix(fixed)
    except Exception:
        fallback = local_fix(article)
        fallback["supervised"] = False
        fallback["supervisor_provider"] = provider
        fallback["supervisor_model"] = model
        return fallback


def main():
    parser = argparse.ArgumentParser(description="Supervisión de textos")
    parser.add_argument("--input", required=True, help="Archivo JSON de entrada")
    parser.add_argument("--output", help="Archivo JSON de salida")
    parser.add_argument("--provider", default=os.getenv("SUPERVISOR_PROVIDER", ""))
    parser.add_argument("--model", default=os.getenv("SUPERVISOR_MODEL", ""))
    parser.add_argument("--force", action="store_true", help="Forzar supervisión aunque no se detecten issues")
    parser.add_argument("--limit", type=int, default=200)
    args = parser.parse_args()

    input_path = Path(args.input)
    data_dir = Path(os.getenv("NEWS_DATA_DIR", Path(__file__).resolve().parents[2] / "data"))
    data_dir.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        articles = json.load(f)

    provider = args.provider
    model = args.model

    supervised = []
    for article in articles[: args.limit]:
        if provider and model:
            if args.force or detect_issues(article):
                supervised.append(supervise_article(article, provider, model))
            else:
                supervised.append(local_fix(article))
        else:
            supervised.append(local_fix(article))

    output_path = Path(args.output) if args.output else data_dir / f"noticias_supervised_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(supervised, f, ensure_ascii=False, indent=2)

    print(f"✅ Supervisión completa: {output_path}")


if __name__ == "__main__":
    main()
