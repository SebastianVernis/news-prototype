#!/usr/bin/env python3
"""
Flujo IA multi-fuente para crear y publicar 10 articulos.

Pipeline:
1) Descarga 12 titulares de NewsAPI, APITube y GNews.
2) OpenRouter (modelo free) selecciona los 10 mejores por titulo + snippet.
3) Por cada tema, busca 3 fuentes distintas y extrae texto completo.
4) IA sintetiza un resumen ~1200 palabras (fallback Gemini si se trunca).
5) Genera descripcion + HTML y publica 1 articulo por sitio en D1.
6) Guarda 3 URLs multimedia por articulo (thumbnail, cuerpo, destacado).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

try:
    import requests
except ModuleNotFoundError:
    sys.stderr.write(
        "ERROR: falta el modulo 'requests' en este Python.\n"
        "Solucion rapida:\n"
        "  python -m pip install requests python-dotenv\n"
        "Nota: en este proyecto existe .venv/bin (entorno Linux/WSL). "
        "Si ejecutas desde PowerShell, usa un Python de Windows con dependencias instaladas.\n"
    )
    raise SystemExit(2)

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    sys.stderr.write(
        "ERROR: falta el modulo 'python-dotenv' en este Python.\n"
        "Ejecuta: python -m pip install python-dotenv\n"
    )
    raise SystemExit(2)

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
ENV_IN_SCRIPT_DIR = SCRIPT_DIR / ".env"
ENV_IN_REPO_ROOT = REPO_ROOT / ".env"
sys.path.insert(0, str(REPO_ROOT))

def load_env_with_priority() -> str:
    """
    Carga variables de entorno con prioridad:
    1) .env junto al script (tools/news/.env)
    2) .env en la raiz del repo
    """
    loaded = []
    if ENV_IN_REPO_ROOT.exists():
        load_dotenv(dotenv_path=ENV_IN_REPO_ROOT, override=False)
        loaded.append(str(ENV_IN_REPO_ROOT))
    if ENV_IN_SCRIPT_DIR.exists():
        # override=True para que el .env local del script tenga prioridad
        load_dotenv(dotenv_path=ENV_IN_SCRIPT_DIR, override=True)
        loaded.append(str(ENV_IN_SCRIPT_DIR))
    if loaded:
        return loaded[-1]
    load_dotenv(override=False)
    return "dotenv_default_lookup"


ENV_SOURCE = load_env_with_priority()

# Importar despues de cargar .env para que los modulos que leen keys al import
# tomen los valores correctos del entorno priorizado.
from tools.api.apitube import fetch_apitube
from tools.api.newsapi import fetch_newsapi
from tools.news.llm_client import chat
from utils.utils import _extract_full_text

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

DEFAULT_SITES = [
    "noticias-objetivo",
    "mexico-informado",
    "bitacora-urbana",
    "nodo-informativo",
    "cbn-noticias",
    "central-mexico",
    "vertice-noticias",
    "radio-cinco-noticias",
    "reporte-central",
    "tv-mexico",
]


def mask_secret(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "*" * len(value)
    return value[:4] + "..." + value[-4:]


def command_exists(cmd: str) -> bool:
    try:
        base = resolve_command_base(cmd)
        proc = subprocess.run(base + ["--version"], capture_output=True, text=True)
        return proc.returncode == 0
    except Exception:
        return False


def resolve_command_base(cmd: str) -> List[str]:
    if cmd != "wrangler":
        return [cmd]

    # Windows + subprocess no siempre ejecuta correctamente "wrangler" (ps1).
    # Probar candidatos en orden y elegir el primero que realmente responde.
    candidates: List[List[str]] = []
    if shutil.which("wrangler.cmd"):
        candidates.append(["wrangler.cmd"])
    if shutil.which("wrangler"):
        candidates.append(["wrangler"])
    if shutil.which("npx"):
        candidates.append(["npx", "wrangler"])
    if not candidates:
        candidates = [["wrangler.cmd"], ["wrangler"], ["npx", "wrangler"]]

    for cand in candidates:
        try:
            proc = subprocess.run(cand + ["--version"], capture_output=True, text=True)
            if proc.returncode == 0:
                return cand
        except Exception:
            continue
    return candidates[0]


def ask_yes_no(prompt: str, default_yes: bool = True) -> bool:
    suffix = "[Y/n]" if default_yes else "[y/N]"
    ans = input(f"{prompt} {suffix}: ").strip().lower()
    if not ans:
        return default_yes
    return ans in ("y", "yes", "s", "si")


def preflight_interactive(args: argparse.Namespace) -> bool:
    print("\n=== Preflight Interactivo ===")
    print(f"ENV source: {ENV_SOURCE}")
    print(f"Query: {args.query}")
    print(f"Locale: {args.country}")
    print(f"Language: {args.language}")
    print(f"Objetivo articulos: {args.select_count}")
    print(f"DB mode: {args.db_mode}")
    print(f"Publicar DB: {'no' if (args.skip_db or args.dry_run) else 'si'}")

    required_env = {
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY", ""),
        "NEWSAPI_KEY": os.getenv("NEWSAPI_KEY", ""),
        "APITUBE_KEY": os.getenv("APITUBE_KEY", ""),
        "GNEWS_API_KEY": os.getenv("GNEWS_API_KEY", ""),
    }
    gemini = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GEMINI_API_KEY_1")
        or os.getenv("GEMINI_API_KEY_2")
        or os.getenv("GEMINI_API_KEY_3")
        or ""
    )

    print("\nClaves detectadas:")
    for k, v in required_env.items():
        status = "OK" if v else "MISSING"
        masked = mask_secret(v) if v else "-"
        print(f"- {k}: {status} ({masked})")
    print(f"- GEMINI_API_KEY*: {'OK' if gemini else 'MISSING'} ({mask_secret(gemini) if gemini else '-'})")

    missing = [k for k, v in required_env.items() if not v]
    if not gemini:
        missing.append("GEMINI_API_KEY*")

    if not (args.skip_db or args.dry_run):
        wrangler_ok = command_exists("wrangler")
        print(f"- wrangler CLI: {'OK' if wrangler_ok else 'MISSING'}")
        if not wrangler_ok:
            missing.append("wrangler")

    if missing:
        print("\nFaltantes criticos:")
        for m in missing:
            print(f"- {m}")
        if not ask_yes_no("Hay faltantes. Deseas continuar de todos modos?", default_yes=False):
            return False

    if args.preflight_api_check:
        print("\nChequeo rapido de APIs...")
        checks = run_api_preflight_checks(args)
        for name, ok, detail in checks:
            print(f"- {name}: {'OK' if ok else 'FAIL'} ({detail})")
        hard_fail = [x for x in checks if not x[1] and x[0] in ("OpenRouter", "NewsAPI", "GNews", "APITube")]
        if hard_fail and not ask_yes_no("Hay APIs fallando. Continuar de todos modos?", default_yes=False):
            return False

    if not ask_yes_no("Iniciar ejecucion del flujo ahora?", default_yes=True):
        return False
    return True


def now_iso() -> str:
    return datetime.now().isoformat()


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text or ""))


def strip_fences(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def try_parse_json(text: str) -> Optional[Dict[str, Any]]:
    raw = strip_fences(text)
    try:
        return json.loads(raw)
    except Exception:
        pass
    match = re.search(r"\{[\s\S]*\}", raw)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None
    return None


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def compact_query_from_title(title: str, max_words: int = 10, max_chars: int = 90) -> str:
    words = re.findall(r"[\wáéíóúñÁÉÍÓÚÑ]+", title or "")
    if not words:
        return "Mexico"
    q = " ".join(words[:max_words]).strip()
    if len(q) > max_chars:
        q = q[:max_chars].rsplit(" ", 1)[0].strip() or q[:max_chars]
    return q


def slugify(text: str) -> str:
    text = (text or "").lower().strip()
    mapping = str.maketrans(
        "áàäâãéèëêíìïîóòöôõúùüûñçý",
        "aaaaaeeeeiiiiooooouuuuncy",
    )
    text = text.translate(mapping)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:100] or "articulo"


def esc(value: Any) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def as_candidate(article: Dict[str, Any], source_name: str, idx: int) -> Dict[str, Any]:
    title = clean_text(article.get("title") or article.get("headline") or "")
    description = clean_text(article.get("description") or article.get("summary") or "")
    snippet = description or clean_text((article.get("content") or "")[:240])
    return {
        "id": f"{source_name}-{idx}",
        "source": source_name,
        "title": title,
        "snippet": snippet[:320],
        "url": article.get("url") or article.get("link") or "",
        "image": article.get("image") or article.get("urlToImage") or "",
        "published_at": article.get("published_at") or article.get("publishedAt") or article.get("pubDate") or "",
        "raw": article,
    }


def fetch_gnews(
    query: str,
    limit: int,
    language: str = "es",
    country: str = "mx",
) -> List[Dict[str, Any]]:
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key:
        print("WARN: GNEWS_API_KEY no configurada. Se omite GNews.")
        return []
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": query,
        "lang": language,
        "country": country,
        "max": limit,
        "sortby": "publishedAt",
        "apikey": api_key,
    }
    try:
        resp = requests.get(url, params=params, timeout=40)
        resp.raise_for_status()
        payload = resp.json()
        out = []
        for article in payload.get("articles", []):
            out.append(
                {
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "content": article.get("content", ""),
                    "url": article.get("url", ""),
                    "image": article.get("image", ""),
                    "publishedAt": article.get("publishedAt", ""),
                    "source_name": (article.get("source") or {}).get("name", "gnews"),
                }
            )
        return out
    except Exception as e:
        print(f"WARN: fallo GNews: {e}")
        return []


def fetch_newsapi_with_retry(query: str, language: str, page_size: int, retries: int = 2) -> List[Dict[str, Any]]:
    last_err = None
    for attempt in range(retries + 1):
        try:
            return fetch_newsapi(
                query=query,
                language=language,
                page_size=page_size,
                enrich=False,
                silent=True,
            )
        except Exception as e:
            last_err = e
            if "429" in str(e) and attempt < retries:
                time.sleep(1.2 * (attempt + 1))
                continue
            break
    raise last_err if last_err else RuntimeError("fetch_newsapi fallo")


def run_api_preflight_checks(args: argparse.Namespace) -> List[Tuple[str, bool, str]]:
    checks: List[Tuple[str, bool, str]] = []

    # OpenRouter
    try:
        _ = chat(
            provider="openrouter",
            model=args.openrouter_model,
            messages=[{"role": "user", "content": "Responde solo: ok"}],
            temperature=0.0,
            max_tokens=6,
        )
        checks.append(("OpenRouter", True, "auth/model OK"))
    except Exception as e:
        checks.append(("OpenRouter", False, str(e)[:120]))

    # NewsAPI
    try:
        sample = fetch_newsapi_with_retry("Mexico", args.language, 1, retries=1)
        checks.append(("NewsAPI", True, f"{len(sample)} articulo(s) sample"))
    except Exception as e:
        checks.append(("NewsAPI", False, str(e)[:120]))

    # GNews
    try:
        sample_g = fetch_gnews("Mexico", 1, args.language, args.country)
        checks.append(("GNews", True, f"{len(sample_g)} articulo(s) sample"))
    except Exception as e:
        checks.append(("GNews", False, str(e)[:120]))

    # APITube
    try:
        sample_a = fetch_apitube(
            country=args.country,
            category=args.apitube_category,
            language=args.language,
            page_size=1,
            silent=True,
        )
        checks.append(("APITube", True, f"{len(sample_a)} articulo(s) sample"))
    except Exception as e:
        checks.append(("APITube", False, str(e)[:120]))

    return checks


def dedupe_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for c in candidates:
        key = (c.get("url") or "").strip().lower()
        if not key:
            key = clean_text(c.get("title", "")).lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def fetch_headlines(args: argparse.Namespace, query: Optional[str] = None) -> List[Dict[str, Any]]:
    all_candidates: List[Dict[str, Any]] = []
    q = query or args.query

    try:
        n = fetch_newsapi_with_retry(q, args.language, args.headlines_per_api, retries=2)
    except Exception as e:
        print(f"WARN: fallo NewsAPI: {e}")
        n = []
    all_candidates.extend(as_candidate(a, "newsapi", i) for i, a in enumerate(n, 1))

    try:
        a = fetch_apitube(country=args.country,
                  category=args.apitube_category,
                  language=args.language,
                  page_size=args.headlines_per_api,
                  silent=True,
        )
    except Exception as e:
        print(f"WARN: fallo APITube: {e}")
        a = []
    all_candidates.extend(as_candidate(x, "apitube", i) for i, x in enumerate(a, 1))

    g = fetch_gnews(
        query=q,
        limit=args.headlines_per_api,
        language=args.language,
        country=args.country,
    )
    all_candidates.extend(as_candidate(x, "gnews", i) for i, x in enumerate(g, 1))

    deduped = dedupe_candidates(all_candidates)
    print(f"Titulares obtenidos: {len(deduped)} (deduplicados)")
    return deduped


def choose_top_headlines(
    candidates: List[Dict[str, Any]],
    select_count: int,
    model: str,
) -> List[Dict[str, Any]]:
    compact = [
        {
            "id": c["id"],
            "source": c["source"],
            "title": c["title"],
            "snippet": c["snippet"],
        }
        for c in candidates
    ]
    prompt = (
        "Eres editor jefe de una red de noticias.\n"
        f"Selecciona exactamente {select_count} titulares con mayor valor periodistico.\n"
        "Evalua solo por titulo y snippet: actualidad, claridad, impacto y posibilidad de cobertura completa.\n"
        "Devuelve JSON estricto:\n"
        '{ "selected_ids": ["id1","id2"], "reasons": { "id1": "motivo corto" } }\n'
        f"Candidatos:\n{json.dumps(compact, ensure_ascii=False)}"
    )
    try:
        raw = chat(
            provider="openrouter",
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2200,
        )
        parsed = try_parse_json(raw) or {}
        ids = parsed.get("selected_ids") or []
        selected = [c for c in candidates if c["id"] in ids][:select_count]
        if len(selected) >= min(3, select_count):
            return selected
        print("WARN: OpenRouter devolvio pocos IDs. Se aplica fallback.")
    except Exception as e:
        print(f"WARN: seleccion IA fallo: {e}")

    # fallback determinista: prioridad por longitud y recencia disponible
    sorted_candidates = sorted(
        candidates,
        key=lambda c: (len(c.get("snippet") or ""), len(c.get("title") or "")),
        reverse=True,
    )
    return sorted_candidates[:select_count]


def fetch_headlines_with_retries(args: argparse.Namespace, min_candidates: int) -> List[Dict[str, Any]]:
    queries = [args.query]
    if args.retry_queries:
        queries.extend([q.strip() for q in args.retry_queries.split(",") if q.strip()])
    else:
        # Backups razonables para llenar pool si la consulta principal trae poco.
        queries.extend(["Mexico", "Actualidad Mexico", "Ultimas noticias"])

    all_candidates: List[Dict[str, Any]] = []
    rounds = max(1, args.headline_rounds)
    for i in range(min(rounds, len(queries))):
        q = queries[i]
        print(f"  Ronda titulares {i+1}/{min(rounds, len(queries))} con query: {q}")
        chunk = fetch_headlines(args, query=q)
        all_candidates.extend(chunk)
        all_candidates = dedupe_candidates(all_candidates)
        if len(all_candidates) >= min_candidates:
            break
    return all_candidates


def domain_of(url: str) -> str:
    try:
        return (urlparse(url).netloc or "").lower()
    except Exception:
        return ""


def score_related(seed_title: str, cand: Dict[str, Any]) -> float:
    t = cand.get("title", "")
    sim = SequenceMatcher(None, seed_title.lower(), t.lower()).ratio()
    bonus = 0.05 if cand.get("snippet") else 0.0
    return sim + bonus


def fetch_full_text_strict(url: str, timeout: int = 20) -> str:
    if not url:
        return ""

    # intento 1: extractor existente del proyecto
    text = _extract_full_text(url) or ""
    if word_count(text) >= 120:
        return clean_text(text)

    # intento 2: parseo simple de <p> como respaldo de scraping
    try:
        resp = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"},
        )
        resp.raise_for_status()
        html = resp.text or ""
        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", html, flags=re.I | re.S)
        stripped = []
        for p in paragraphs:
            s = re.sub(r"<[^>]+>", " ", p)
            s = re.sub(r"&nbsp;|&#160;", " ", s)
            s = re.sub(r"&amp;", "&", s)
            s = re.sub(r"\s+", " ", s).strip()
            if s:
                stripped.append(s)
        text2 = "\n\n".join(stripped).strip()
        return clean_text(text2)
    except Exception:
        return ""


def fetch_related_for_topic(seed: Dict[str, Any], args: argparse.Namespace) -> List[Dict[str, Any]]:
    q = compact_query_from_title(seed["title"], max_words=10, max_chars=90)
    per_source = args.related_pool_per_source
    pool: List[Dict[str, Any]] = []

    try:
        n = fetch_newsapi_with_retry(q, args.language, per_source, retries=2)
        pool.extend(as_candidate(a, "newsapi", i) for i, a in enumerate(n, 1))
    except Exception:
        pass

    try:
        a = fetch_apitube(
            country=args.country,
            category=args.apitube_category,
            language=args.language,
            page_size=per_source,
            silent=True,
        )
        pool.extend(as_candidate(x, "apitube", i) for i, x in enumerate(a, 1))
    except Exception:
        pass

    g = fetch_gnews(
        query=q,
        limit=per_source,
        language=args.language,
        country=args.country,
    )
    pool.extend(as_candidate(x, "gnews", i) for i, x in enumerate(g, 1))

    pool = dedupe_candidates(pool)
    pool.sort(key=lambda x: score_related(q, x), reverse=True)

    enriched: List[Dict[str, Any]] = []
    used_domains = set()
    used_sources = set()

    # Necesitamos 3 fuentes con full text valido.
    for cand in pool:
        src = cand.get("source", "")
        dom = domain_of(cand.get("url", ""))
        if src in used_sources:
            continue
        if dom and dom in used_domains:
            continue

        # Si no viene full text suficiente, se hace fetch obligatorio del URL.
        text = cand.get("raw", {}).get("full_text") or cand.get("raw", {}).get("content") or ""
        if "[+" in text or word_count(text) < args.min_source_words:
            text = fetch_full_text_strict(cand.get("url", ""))

        # Sin full text suficiente, no se usa esta fuente.
        if word_count(text) < args.min_source_words:
            continue

        cloned = dict(cand)
        cloned["full_text"] = clean_text(text)
        enriched.append(cloned)
        used_sources.add(src)
        if dom:
            used_domains.add(dom)
        if len(enriched) >= args.min_sources_required:
            break

    return enriched[:args.min_sources_required]


def call_openrouter_raw(
    messages: List[Dict[str, str]],
    model: str,
    temperature: float,
    max_tokens: int,
) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Falta OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.getenv("SITE_URL", "http://localhost"),
        "X-Title": "Cloudflare News Pipeline",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def call_gemini(prompt: str, model: str) -> str:
    key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GEMINI_API_KEY_1")
        or os.getenv("GEMINI_API_KEY_2")
        or os.getenv("GEMINI_API_KEY_3")
    )
    if not key:
        raise ValueError("No hay key de Gemini configurada")
    url = f"{GEMINI_API_BASE}/{model}:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.35,
            "maxOutputTokens": 8192,
        },
    }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def synthesize_article(
    topic_title: str,
    sources: List[Dict[str, Any]],
    openrouter_model: str,
    gemini_model: str,
) -> Optional[Dict[str, str]]:
    source_payload = []
    for idx, src in enumerate(sources, 1):
        source_payload.append(
            {
                "n": idx,
                "source": src.get("source"),
                "title": src.get("title"),
                "snippet": src.get("snippet"),
                "url": src.get("url"),
                "full_text": (src.get("full_text") or "")[:4500],
            }
        )

    prompt = (
        "Analiza 3 notas de la misma noticia y crea una sintesis periodistica.\n"
        "Reglas:\n"
        "1) Usa solo hechos inferibles de las fuentes dadas.\n"
        "2) No inventes datos.\n"
        "3) Debe quedar en espanol neutral.\n"
        "4) Mantener el titulo exacto que se proporciona.\n"
        "Devuelve JSON estricto con estas claves:\n"
        '{'
        '"title":"(exactamente el titulo dado)",'
        '"description":"130-220 caracteres",'
        '"summary_1200":"texto de 1050 a 1350 palabras, varios parrafos",'
        '"category":"NACIONAL|MUNDO|ECONOMIA|POLITICA|SEGURIDAD|DEPORTES|TECNOLOGIA"'
        "}\n"
        f'Titulo fijo: "{topic_title}"\n'
        f"Fuentes:\n{json.dumps(source_payload, ensure_ascii=False)}"
    )

    # intento 1: OpenRouter/free
    try:
        raw = call_openrouter_raw(
            messages=[{"role": "user", "content": prompt}],
            model=openrouter_model,
            temperature=0.3,
            max_tokens=3800,
        )
        parsed = try_parse_json(raw)
        if parsed and word_count(parsed.get("summary_1200", "")) >= 1000:
            parsed["title"] = topic_title
            return parsed  # type: ignore[return-value]
    except Exception as e:
        print(f"WARN: sintesis OpenRouter fallo: {e}")

    # fallback Gemini cuando OpenRouter se trunca o falla
    try:
        raw_g = call_gemini(prompt, gemini_model)
        parsed_g = try_parse_json(raw_g)
        if parsed_g and word_count(parsed_g.get("summary_1200", "")) >= 1000:
            parsed_g["title"] = topic_title
            return parsed_g  # type: ignore[return-value]
    except Exception as e:
        print(f"WARN: sintesis Gemini fallback fallo: {e}")

    # Sin salida IA valida, se descarta el tema.
    return None


def split_paragraphs(summary: str) -> List[str]:
    parts = [p.strip() for p in re.split(r"\n\s*\n", summary or "") if p.strip()]
    if parts:
        return parts

    words = (summary or "").split()
    chunks = []
    size = 120
    for i in range(0, len(words), size):
        chunks.append(" ".join(words[i : i + size]).strip())
    return [c for c in chunks if c]


def build_html(
    title: str,
    description: str,
    summary: str,
    article_image_url: str,
    featured_image_url: str,
    featured: bool,
    source_urls: List[str],
) -> str:
    paragraphs = split_paragraphs(summary)
    sections = [
        "Contexto",
        "Hechos clave",
        "Implicaciones",
        "Que sigue",
    ]
    lines = []
    lines.append("<article class=\"news-article\">")
    lines.append(f"  <header><h1>{title}</h1><p>{description}</p></header>")
    if article_image_url:
        lines.append(
            "  <figure class=\"article-image\">"
            f"<img src=\"{article_image_url}\" alt=\"{title}\" loading=\"lazy\"/>"
            "</figure>"
        )
    if featured and featured_image_url:
        lines.append(
            "  <aside class=\"featured-image\">"
            f"<img src=\"{featured_image_url}\" alt=\"Imagen destacada de {title}\" loading=\"lazy\"/>"
            "</aside>"
        )

    sec_idx = 0
    for i, p in enumerate(paragraphs):
        if i % 3 == 0:
            lines.append(f"  <section><h2>{sections[min(sec_idx, len(sections) - 1)]}</h2>")
            sec_idx += 1
        lines.append(f"    <p>{p}</p>")
        if i % 3 == 2:
            lines.append("  </section>")
    if not lines[-1].endswith("</section>"):
        lines.append("  </section>")

    valid_urls = [u for u in source_urls if u]
    if valid_urls:
        lines.append("  <footer><h3>Fuentes consultadas</h3><ul>")
        for u in valid_urls[:3]:
            lines.append(f"    <li><a href=\"{u}\" target=\"_blank\" rel=\"noopener\">{u}</a></li>")
        lines.append("  </ul></footer>")
    lines.append("</article>")
    return "\n".join(lines)


def run_wrangler_query(
    query: str,
    db_name: str,
    wrangler_config: str,
    db_mode: str,
) -> List[Dict[str, Any]]:
    wr = resolve_command_base("wrangler")
    cmd = wr + ["d1", "execute", db_name, "--config", wrangler_config, "--command", query, "--json"]
    if db_mode == "remote":
        cmd.insert(4, "--remote")
    else:
        cmd.insert(4, "--local")

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    payload = json.loads(proc.stdout or "[]")
    if isinstance(payload, list) and payload:
        return payload[0].get("results", []) or []
    return []


def get_sites(args: argparse.Namespace) -> List[str]:
    if args.sites:
        return [s.strip() for s in args.sites.split(",") if s.strip()][: args.select_count]
    try:
        rows = run_wrangler_query(
            "SELECT SLUG FROM SITIOS WHERE ACTIVO = 1 ORDER BY NOMBRE LIMIT 20",
            args.db_name,
            args.db_config,
            args.db_mode,
        )
        sites = [r.get("SLUG") for r in rows if r.get("SLUG")]
        if sites:
            return sites[: args.select_count]
    except Exception as e:
        print(f"WARN: no se pudo leer SITIOS en D1: {e}")
    return DEFAULT_SITES[: args.select_count]


def build_db_sql(articles: List[Dict[str, Any]], sites: List[str]) -> str:
    statements = []
    statements.append("BEGIN TRANSACTION;")

    for i, art in enumerate(articles):
        site = sites[i % len(sites)] if sites else DEFAULT_SITES[i % len(DEFAULT_SITES)]
        featured = 1 if i == 0 else 0
        orig_id = str(uuid.uuid4())
        para_id = str(uuid.uuid4())
        published = now_iso()

        title = art["title"]
        description = art["description"]
        summary = art["summary_1200"]
        html = art["html_content"]
        category = (art.get("category") or "NACIONAL").upper()
        source_urls = art.get("source_urls", [])
        source_url = source_urls[0] if source_urls else ""

        img_thumb = art.get("image_thumb") or ""
        img_article = art.get("image_article") or ""
        img_featured = art.get("image_featured") or ""
        url_bundle = json.dumps(
            {
                "thumbnail": img_thumb,
                "article": img_article,
                "featured": img_featured,
            },
            ensure_ascii=False,
        )
        original_content = f"{summary}\n\nMULTIMEDIA_JSON:{url_bundle}"

        statements.append(
            "INSERT INTO ARTICULOS_ORIGINALES ("
            "ID, URL, TITULO, DESCRIPCION, URL_IMAGEN, URL_IMAGEN2, URL_IMAGEN3, FECHA, CONTENIDO, CATEGORIA, LONGITUD, SITIOS"
            ") VALUES ("
            f"{esc(orig_id)}, {esc(source_url)}, {esc(title)}, {esc(description)}, {esc(img_thumb)}, {esc(img_article)}, {esc(img_featured)}, "
            f"{esc(published)}, {esc(original_content)}, {esc(category)}, {word_count(summary)}, 1"
            ");"
        )

        statements.append(
            "INSERT INTO ARTICULOS_PARAFRASEADOS ("
            "ID, ID_ARTICULO_ORIGINAL, TITULO_PARAFRASEADO, DESCRIPCION_PARAFRASEADA, CONTENIDO, LONGITUD, SITIO_DESTINO, "
            "CATEGORIA, FECHA_PUBLICACION, AUTOR, VERIFICACION, DESTACADO, URL_IMAGEN, URL_IMAGEN_DESTACADO, SLUG, VISTAS, ESTADO"
            ") VALUES ("
            f"{esc(para_id)}, {esc(orig_id)}, {esc(title)}, {esc(description)}, {esc(html)}, {word_count(summary)}, {esc(site)}, "
            f"{esc(category)}, {esc(published)}, 'Redacción IA', 'openrouter+gemini-fallback', {featured}, {esc(img_thumb)}, "
            f"{esc(img_featured)}, {esc(slugify(title))}, 0, 'PUBLICADO'"
            ");"
        )

    statements.append("COMMIT;")
    return "\n".join(statements)


def execute_sql(sql_text: str, args: argparse.Namespace) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".sql", delete=False, encoding="utf-8") as tmp:
        tmp.write(sql_text)
        tmp_path = tmp.name
    try:
        wr = resolve_command_base("wrangler")
        cmd = wr + [
            "d1",
            "execute",
            args.db_name,
            "--config",
            args.db_config,
            "--file",
            tmp_path,
        ]
        cmd.insert(4, "--remote" if args.db_mode == "remote" else "--local")
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr or proc.stdout)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


def ensure_optional_columns(args: argparse.Namespace) -> None:
    migrations = [
        "ALTER TABLE ARTICULOS_ORIGINALES ADD COLUMN URL_IMAGEN3 TEXT",
        "ALTER TABLE ARTICULOS_PARAFRASEADOS ADD COLUMN URL_IMAGEN TEXT",
        "ALTER TABLE ARTICULOS_PARAFRASEADOS ADD COLUMN URL_IMAGEN_DESTACADO TEXT",
        "ALTER TABLE ARTICULOS_PARAFRASEADOS ADD COLUMN SLUG TEXT",
        "ALTER TABLE ARTICULOS_PARAFRASEADOS ADD COLUMN VISTAS INTEGER DEFAULT 0",
        "ALTER TABLE ARTICULOS_PARAFRASEADOS ADD COLUMN ESTADO TEXT DEFAULT 'PUBLICADO'",
    ]
    for q in migrations:
        try:
            run_wrangler_query(q, args.db_name, args.db_config, args.db_mode)
        except Exception:
            # Se ignora: normalmente "duplicate column name"
            pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flujo IA multi-fuente (NewsAPI + APITube + GNews) con publicacion D1."
    )
    parser.add_argument("--query", default="México", help="Consulta base para titulares")
    parser.add_argument("--language", default="es", help="Idioma de consulta (default: es)")
    parser.add_argument("--country", default="mx", help="Pais (codigo ISO, default: mx)")
    parser.add_argument("--locale", help="Alias de --country (ej: mx)")
    parser.add_argument("--apitube-category", default="politics", help="Categoria para APITube")
    parser.add_argument("--headlines-per-api", type=int, default=12, help="Titulares por API")
    parser.add_argument("--select-count", type=int, default=10, help="Cantidad final de articulos")
    parser.add_argument("--selection-pool-multiplier", type=int, default=4, help="Multiplicador del pool de temas a intentar")
    parser.add_argument("--max-topic-attempts", type=int, default=80, help="Maximo de temas a procesar antes de abortar")
    parser.add_argument("--headline-rounds", type=int, default=3, help="Rondas de busqueda de titulares")
    parser.add_argument("--retry-queries", help="Queries extra separadas por coma para reintentos")
    parser.add_argument("--allow-partial", action="store_true", help="Permite publicar menos de select-count")
    parser.add_argument("--related-pool-per-source", type=int, default=8, help="Pool por fuente para encontrar 3 notas relacionadas")
    parser.add_argument("--min-source-words", type=int, default=120, help="Minimo de palabras para considerar una fuente util")
    parser.add_argument("--min-sources-required", type=int, default=3, help="Minimo de fuentes con full text para aceptar un tema (default: 3)")
    parser.add_argument("--openrouter-model", default=os.getenv("OPENROUTER_MODEL", "openrouter/free"))
    parser.add_argument("--gemini-model", default=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
    parser.add_argument("--db-name", default="news_db")
    parser.add_argument("--db-config", default="src/wrangler.toml")
    parser.add_argument("--db-mode", choices=["local", "remote"], default="local")
    parser.add_argument("--sites", help="Lista de slugs separada por coma para asignacion 1:1")
    parser.add_argument("--skip-db", action="store_true", help="No inyectar en DB")
    parser.add_argument("--dry-run", action="store_true", help="No ejecutar SQL")
    parser.add_argument("--no-interactive", action="store_true", help="Desactiva validacion interactiva previa")
    parser.add_argument("--no-preflight-api-check", action="store_true", help="Desactiva ping previo de APIs en modo interactivo")
    args = parser.parse_args()
    if args.locale:
        args.country = args.locale.lower().strip()
    args.language = (args.language or "es").lower().strip()
    args.country = (args.country or "mx").lower().strip()
    args.preflight_api_check = not args.no_preflight_api_check

    if not args.no_interactive:
        if not preflight_interactive(args):
            print("Ejecucion cancelada por usuario.")
            return 1

    print("Paso 1/6: Descargando titulares...")
    min_candidates = max(args.select_count, args.select_count * args.selection_pool_multiplier)
    candidates = fetch_headlines_with_retries(args, min_candidates=min_candidates)
    if len(candidates) < args.select_count:
        print(f"ERROR: solo hay {len(candidates)} titulares; se requieren al menos {args.select_count}.")
        return 1

    print("Paso 2/6: Seleccion editorial IA (OpenRouter free)...")
    selection_pool_size = min(len(candidates), max(args.select_count, args.select_count * args.selection_pool_multiplier))
    selected = choose_top_headlines(candidates, selection_pool_size, args.openrouter_model)
    selected_ids = {x["id"] for x in selected}
    rest = [c for c in candidates if c["id"] not in selected_ids]
    # Cola total priorizada: IA primero, luego remanente.
    topic_queue = selected + rest
    print(f"Cola de temas priorizada: {len(topic_queue)}")

    print("Paso 3/6: Enriqueciendo cada tema con 3 fuentes y full text...")
    final_articles = []
    used_titles = set()
    attempts = 0
    for i, seed in enumerate(topic_queue, 1):
        if len(final_articles) >= args.select_count:
            break
        if attempts >= args.max_topic_attempts:
            print(f"WARN: se alcanzo max-topic-attempts={args.max_topic_attempts}.")
            break
        attempts += 1

        norm_title = clean_text(seed["title"]).lower()
        if not norm_title or norm_title in used_titles:
            continue
        used_titles.add(norm_title)

        print(f"  Tema {attempts}/{min(len(topic_queue), args.max_topic_attempts)}: {seed['title'][:90]}")
        sources = fetch_related_for_topic(seed, args)
        if len(sources) < args.min_sources_required:
            print("    WARN: no se lograron 3 fuentes con full text valido, se omite.")
            continue

        print("Paso 4/6: Sintesis IA con fallback Gemini si hay truncado...")
        synthesized = synthesize_article(
            topic_title=seed["title"],
            sources=sources,
            openrouter_model=args.openrouter_model,
            gemini_model=args.gemini_model,
        )
        if not synthesized:
            print("    WARN: no hubo reinterpretacion IA valida (OpenRouter/Gemini), se omite.")
            continue

        images = [s.get("image") or "" for s in sources]
        images = [img for img in images if img]
        img_thumb = images[0] if len(images) > 0 else (seed.get("image") or "")
        img_article = images[1] if len(images) > 1 else img_thumb
        img_featured = images[2] if len(images) > 2 else img_article
        featured = len(final_articles) == 0

        print("Paso 5/6: Armando HTML final...")
        html = build_html(
            title=synthesized["title"],
            description=synthesized["description"],
            summary=synthesized["summary_1200"],
            article_image_url=img_article,
            featured_image_url=img_featured,
            featured=featured,
            source_urls=[s.get("url", "") for s in sources],
        )

        final_articles.append(
            {
                "title": synthesized["title"],
                "description": synthesized["description"],
                "summary_1200": synthesized["summary_1200"],
                "category": synthesized.get("category", "NACIONAL"),
                "html_content": html,
                "source_urls": [s.get("url", "") for s in sources],
                "source_titles": [s.get("title", "") for s in sources],
                "image_thumb": img_thumb,
                "image_article": img_article,
                "image_featured": img_featured,
            }
        )
        print(f"    OK: articulo aceptado ({len(final_articles)}/{args.select_count})")

    final_articles = final_articles[: args.select_count]
    if len(final_articles) < args.select_count:
        print(f"WARN: se generaron {len(final_articles)} articulos en vez de {args.select_count}.")
        if not args.allow_partial:
            print("ERROR: objetivo estricto no cumplido. Se guarda JSON parcial y se cancela publicacion.")
            out_file = REPO_ROOT / "data" / f"ai_multi_source_flow_{ts()}.json"
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(final_articles, f, ensure_ascii=False, indent=2)
            print(f"Resultado parcial guardado en: {out_file}")
            return 1

    out_file = REPO_ROOT / "data" / f"ai_multi_source_flow_{ts()}.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_articles, f, ensure_ascii=False, indent=2)
    print(f"Resultado JSON guardado en: {out_file}")

    if args.skip_db or args.dry_run:
        print("Paso 6/6: Publicacion DB omitida por bandera.")
        return 0

    sites = get_sites(args)
    if not sites:
        print("ERROR: no hay sitios para publicar.")
        return 1

    ensure_optional_columns(args)
    sql = build_db_sql(final_articles, sites)
    print("Paso 6/6: Inyectando en D1...")
    try:
        execute_sql(sql, args)
        print(f"Publicacion completada: {len(final_articles)} articulos.")
    except Exception as e:
        print(f"ERROR en inyeccion D1: {e}")
        sql_backup = REPO_ROOT / "data" / f"ai_multi_source_flow_failed_{ts()}.sql"
        sql_backup.write_text(sql, encoding="utf-8")
        print(f"SQL de respaldo guardado en: {sql_backup}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
