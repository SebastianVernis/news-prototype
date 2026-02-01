# AGENTS.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project overview
This repo contains:
- A Python-based site generator (core logic under `scripts/`) that produces static news sites.
- A local admin UI (React + Vite under `frontend/`, driven by the root `package.json`/`vite.config.js`).
- A local Flask API (`backend/app.py`) used by the admin UI to trigger generation and manage outputs.
- A Cloudflare Workers backend prototype (`workers/`) that models a production architecture (D1/R2/Queues), but still has TODOs for the actual generation logic.

## Common commands

### Python setup (generator + backend)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

### Menu-driven workflow (recommended for the full generator)
Runs the interactive menu that wraps common generation + tests + local serving:
```bash
./menu.sh
# or
python3 menu.py
```

### Full site generation (folder-per-site output)
Generates into `generated_sites/site_N/`.
```bash
python3 scripts/master_orchestrator.py

# optional flags
python3 scripts/master_orchestrator.py --verificar-dominios
python3 scripts/master_orchestrator.py --usar-cache
python3 scripts/master_orchestrator.py --offline
python3 scripts/master_orchestrator.py --output-dir /custom/path
python3 scripts/master_orchestrator.py --api-whois
```

### Serve generated sites locally (for `generated_sites/` output)
```bash
python3 scripts/serve_sites.py --list
python3 scripts/serve_sites.py --site site_1 --port 8000
python3 scripts/serve_sites.py --all --port 8000
```

### HTML-only generation (single-file per site)
Generates `sites/site*.html` (this is the output the Flask backend manages).
```bash
# interactive
python3 scripts/generate-sites.py

# non-interactive
python3 scripts/generate-sites.py --cantidad 10 --no-interactivo --generar-metadata
python3 scripts/generate-sites.py --cantidad 5 --no-interactivo --metadata-file ../data/sites_metadata/<file>.json
python3 scripts/generate-sites.py --cantidad 5 --no-interactivo --verificar-dominios
```

### Local admin UI (Vite)
Vite is configured with `root: 'frontend'` in `vite.config.js`, so run from repo root:
```bash
npm install
npm run dev
npm run build
npm run preview
```

### Local Flask API (used by the admin UI)
Serves on port `5000` by default and writes outputs under `sites/`.
```bash
python3 backend/app.py
```

Deployment reference: `render.yaml` starts the backend as:
```bash
gunicorn -w 2 -t 300 -b 0.0.0.0:$PORT backend.app:app
```

### Cloudflare Workers prototype
```bash
cd workers
npm install
npm run dev
npm run deploy
npm run types
```
Note: there is no `wrangler.toml` tracked under `workers/` currently; `wrangler` may prompt for config or require it depending on how you run it.

### Lint / type checks
- The root `package.json` does not define lint/test scripts (only `dev`, `build`, `preview`).
- `workers/` includes a strict `tsconfig.json` and exposes `npm run types` / `npm run cf-typegen` (both run `wrangler types`).

### Tests
Tests are implemented as standalone scripts (not a single pytest/jest runner).

Common ones (also accessible via `./menu.sh`):
```bash
python3 scripts/test/test_modulos_completo.py
python3 scripts/test/test_flujo_completo.py
python3 scripts/test/test_blackbox.py
python3 scripts/test/test_paraphrase_quick.py
python3 scripts/test/test_integration.py
```
Run a “single test” by executing the specific script you care about (e.g. `python3 scripts/test/test_apilayer_whois.py`).

## High-level architecture

### 1) Generator core (`scripts/`)
There are two main generation paths:

- **Full pipeline (multi-page site folders)**: `scripts/master_orchestrator.py`
  - Output: `generated_sites/site_N/`.
  - Coordinates the end-to-end flow: news sourcing → paraphrase/expansion → images → metadata/domain verification → CSS assembly → HTML pages (home/articles/categories) + legal pages + SEO artifacts.
  - Many modules have hyphens in filenames (e.g. `generate-images-unified.py`), so the orchestrator uses `importlib` loaders to import them.

- **Simpler pipeline (single HTML file per site)**: `scripts/generate-sites.py`
  - Output: `sites/site*.html`.
  - Uses `templates/css/template*.css` and a selected `data/noticias_final_*.json` input to render multiple standalone HTML pages.

### 2) Data & generated assets
- `data/` stores JSON snapshots: raw news, paraphrased/expanded variants, and final enriched items (including image paths).
- `templates/css/` contains the CSS templates consumed by the generator.
- `generated_sites/` is the “full pipeline” output (directory per site).
- `sites/` is the “single-file” output (HTML files).

### 3) Local admin stack (frontend + Flask)
- `frontend/` (React) is built and served by Vite configured in `vite.config.js`.
- `backend/app.py` exposes REST endpoints under `/api/*` and shells out to `scripts/generate-sites.py` to generate/update the `sites/` output. The Vite dev server proxies `/api` to `http://localhost:5000`.

### 4) Cloudflare Workers backend prototype (`workers/`)
- `workers/src/index.ts` (Hono) defines `/api/*` endpoints, reads/writes metadata to D1 (`schema.sql`), stores assets in R2, and queues generation jobs.
- The queue consumer currently simulates work and has TODOs where the real generation should be implemented.

## Documentation pointers (high-signal)
- `docs/guides/MENU-PRINCIPAL.md`: authoritative map of what `./menu.sh` runs.
- `docs/guides/DIAGRAMA-FLUJO-COMPLETO.md`: detailed end-to-end generator flow.
- `docs/SITE-PRE-CREATION.md`: metadata/name/domain pre-creation system.
- `docs/guides/DEPLOYMENT-ARCHITECTURE.md`: Render+Vercel vs Cloudflare deployment options.
- `docs/design/README.md`: design/system CSS improvements and related docs.

## Existing agent-specific docs
There is a much longer agent guide at `docs/guides/AGENTS.md`. This root-level `AGENTS.md` is intentionally a concise, “get productive fast” version focused on commands + architecture.