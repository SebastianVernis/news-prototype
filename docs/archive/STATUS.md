# Status (Feb 2026)

## Recent System Changes
- CMS batch publish, filters by site/category, and paraphrase toggle.
- Worker API: `/api/ingest`, `/api/paraphrase`, `/api/sites/list`, plus `site`/`category` filters on `/api/articles`.
- Templates: main layout fixed with sidebar, tuned header padding, adaptive preloader, logo image styles.
- Legal: footer links to `#descargo` and full Terms/Privacy in `docs/legal/TEXTOS_LEGALES.md`.
- Site generator: per-site folders, `logo.png` placeholder, and `site_config.json`.
- News download scripts support `past` + `today` ranges (`newsapi`, `newsdata`, `worldnews`).
- Master flow orchestrates download → paraphrase → cache images → generate sites → preloaders.

## Local Flow (Single Command)
Use the venv python:
```
/mnt/c/Users/soluc/cloudflare-news-project/.venv/bin/python tools/news/master-news-flow.py
```

Key flags:
- `--source newsapi|worldnews|newsdata`
- `--query "México"`
- `--past-size 30 --today-size 10`
- `--manual-sites`
- `--count 3`
- `--no-cache-images`

## Inputs / Secrets
- `NEWSAPI_KEY`, `WORLDNEWS_KEY`, `NEWSDATA_KEY` via environment or `.env`.

## Outputs
- Sites in `sites/<sitio>/index.html`
- Logo placeholder in `sites/<sitio>/logo.png`
- Config in `sites/<sitio>/site_config.json`
- Cached images in `assets/images/`
