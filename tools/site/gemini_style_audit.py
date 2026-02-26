#!/usr/bin/env python3
"""Auditoría de layout y estilos usando Gemini (opcional)."""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import requests


def extract_links(html: str) -> List[str]:
    return re.findall(r'href="([^"]+)"', html)


def extract_header_footer(html: str) -> Dict[str, str]:
    header = re.search(r"<header[\s\S]*?</header>", html, re.IGNORECASE)
    footer = re.search(r"<footer[\s\S]*?</footer>", html, re.IGNORECASE)
    return {
        "header": header.group(0) if header else "",
        "footer": footer.group(0) if footer else "",
    }


def local_checks(html: str) -> Dict:
    links = extract_links(html)
    legal_links = [
        "terminos.html",
        "privacidad.html",
        "cookies.html",
        "contacto.html",
        "acerca-de.html",
    ]
    has_legal = all(any(l.endswith(x) for l in links) for x in legal_links)
    has_ellipsis = "..." in html
    has_placeholder = "placeholder" in html.lower() or "Noticia Destacada" in html

    layout = None
    m = re.search(r'<meta name="layout" content="([^"]+)"', html)
    if m:
        layout = m.group(1)

    return {
        "links_ok": True,
        "legal_links_ok": has_legal,
        "no_ellipsis": not has_ellipsis,
        "no_placeholders": not has_placeholder,
        "layout": layout,
    }


def gemini_review(api_key: str, model: str, payload: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [
                    {"text": payload}
                ]
            }
        ]
    }
    resp = requests.post(url, headers=headers, json=body, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def audit_site(site_path: Path, api_key: str, model: str) -> Dict:
    html = site_path.read_text(encoding="utf-8", errors="ignore")
    checks = local_checks(html)
    header_footer = extract_header_footer(html)

    report = {
        "site": site_path.name,
        "local_checks": checks,
        "gemini": None,
    }

    if api_key and model:
        prompt = (
            "Revisa el layout y estilos del sitio. Evalúa: "
            "1) header único y responsivo con categorías aleatorias; "
            "2) footer con legales; "
            "3) layout único (grids, sidebars, carruseles); "
            "4) paleta coherente y profesional; "
            "5) artículos completos sin placeholders. "
            "Devuelve una lista de observaciones y un veredicto PASS/FAIL.\n\n"
            f"HEADER:\n{header_footer['header']}\n\nFOOTER:\n{header_footer['footer']}"
        )
        try:
            report["gemini"] = gemini_review(api_key, model, prompt)
        except Exception as exc:
            report["gemini"] = f"ERROR: {exc}"

    return report


def main():
    parser = argparse.ArgumentParser(description="Auditoría de estilos con Gemini")
    parser.add_argument("--sites-dir", default=os.getenv("SITES_DIR", "./sites"))
    parser.add_argument("--output", default=None)
    parser.add_argument("--model", default=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"))
    args = parser.parse_args()

    sites_dir = Path(args.sites_dir)
    api_key = os.getenv("GEMINI_API_KEY", "")

    reports = []
    for site_path in sorted(sites_dir.glob("site*.html")):
        reports.append(audit_site(site_path, api_key, args.model))

    layout_counts = {}
    for r in reports:
        layout = r.get("local_checks", {}).get("layout")
        if layout:
            layout_counts[layout] = layout_counts.get(layout, 0) + 1

    summary = {
        "total_sites": len(reports),
        "unique_layouts": len(layout_counts),
        "layout_counts": layout_counts,
    }

    out_dir = Path(os.getenv("NEWS_DATA_DIR", Path(__file__).resolve().parents[2] / "data")) / "audit_reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else out_dir / f"style_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "reports": reports}, f, ensure_ascii=False, indent=2)

    print(f"✅ Auditoría completada: {output_path}")


if __name__ == "__main__":
    main()
