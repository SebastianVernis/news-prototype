#!/usr/bin/env python3
"""Verify that generated sites use multiple distinct layouts."""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def extract_layout(html: str) -> str | None:
    m = re.search(r'<meta name="layout" content="([^"]+)"', html)
    return m.group(1) if m else None


def required_elements_checks(html: str) -> dict:
    checks = {
        "has_header": bool(re.search(r"<header[\\s\\S]*?</header>", html, re.IGNORECASE)),
        "has_nav": bool(re.search(r"<nav[\\s\\S]*?</nav>", html, re.IGNORECASE)),
        "has_footer": bool(re.search(r"<footer[\\s\\S]*?</footer>", html, re.IGNORECASE)),
        "has_main": bool(re.search(r"<main[\\s\\S]*?</main>", html, re.IGNORECASE)),
        "has_hero": "hero" in html.lower(),
        "has_grid": "news-grid" in html.lower(),
        "has_sidebar": "sidebar" in html.lower(),
        "has_carousel": "carrusel" in html.lower(),
        "has_preloader": "id=\"preloader\"" in html.lower(),
        "legal_terms": "terminos.html" in html,
        "legal_privacy": "privacidad.html" in html,
        "legal_cookies": "cookies.html" in html,
        "legal_contact": "contacto.html" in html,
        "legal_about": "acerca-de.html" in html,
    }
    checks["legal_links_ok"] = all(
        checks[k]
        for k in [
            "legal_terms",
            "legal_privacy",
            "legal_cookies",
            "legal_contact",
            "legal_about",
        ]
    )
    return checks


def main():
    parser = argparse.ArgumentParser(description="Verify unique layouts across sites")
    parser.add_argument("--sites-dir", default=os.getenv("SITES_DIR", "./sites"))
    parser.add_argument("--min-unique", type=int, default=3)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    sites_dir = Path(args.sites_dir)
    layouts = {}
    elements_report = {}

    for site_path in sorted(sites_dir.glob("site*.html")):
        html = site_path.read_text(encoding="utf-8", errors="ignore")
        layout = extract_layout(html) or "unknown"
        layouts.setdefault(layout, []).append(site_path.name)
        elements_report[site_path.name] = required_elements_checks(html)

    unique_layouts = len(layouts)
    elements_ok = all(
        all(v is True for k, v in checks.items() if k != "legal_links_ok") and checks["legal_links_ok"]
        for checks in elements_report.values()
    )

    ok = unique_layouts >= args.min_unique and elements_ok

    report = {
        "sites_dir": str(sites_dir),
        "min_unique": args.min_unique,
        "unique_layouts": unique_layouts,
        "layouts": layouts,
        "elements": elements_report,
        "status": "PASS" if ok else "FAIL",
    }

    if args.output:
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        data_dir = Path(os.getenv("NEWS_DATA_DIR", "./data"))
        data_dir.mkdir(parents=True, exist_ok=True)
        out_path = data_dir / "layout_verification.json"
        out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if not ok:
        if unique_layouts < args.min_unique:
            print(f"❌ Layouts únicos: {unique_layouts} < {args.min_unique}")
        if not elements_ok:
            print("❌ Faltan elementos requeridos en uno o más sitios")
        sys.exit(1)

    print(f"✅ Layouts únicos: {unique_layouts} >= {args.min_unique}")


if __name__ == "__main__":
    main()
