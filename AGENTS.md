# Repository Guidelines

## Project Structure & Module Organization
- `public/` holds the static site (HTML/CSS/JS) served by Cloudflare Pages.
- `functions/` contains Pages Functions (serverless endpoints, if used).
- `workers/` and `src/` contain Cloudflare Worker code; the main API is in `src/index.js`.
- `docs/` centralizes project documentation and summaries.
- `docs/legal/` stores shareable legal texts (Terms & Privacy).
- `scripts/` contains shell tooling (deploy, verify, setup, templates).
- `tools/` contains Python utilities grouped by domain (`tools/news`, `tools/site`, `tools/images`, `tools/api`).
- `wrangler.toml` (root and `src/wrangler.toml`) define Cloudflare configuration.
- `sites/` is the local output for generated sites. Current generator writes per-site folders with `index.html`, `logo.png`, and `site_config.json`.

## Build, Test, and Development Commands
- `npm install` installs dependencies used by Wrangler tooling.
- `npm run dev` runs a local Pages dev server for `public/`.
- `npm run preview` runs Pages dev with live reload.
- `npm run build` is a placeholder build step (currently echoes a message).
- `npm run deploy` deploys `public/` to Cloudflare Pages.
- `wrangler deploy src/index.js --name news-api` deploys the Worker API.
- Local CMS + API:
  - `npx wrangler dev src/index.js --port 8787`
  - `npx wrangler pages dev ./public --port 8788`
  - Open `http://localhost:8788/admin.html` and set `ADMIN_TOKEN` in `.dev.vars`.
- D1 migration for sites filter:
  - `npx wrangler d1 execute news_db --command "ALTER TABLE articles ADD COLUMN sites TEXT;"`
- Local one-shot flow (master orchestration):
  - `/mnt/c/Users/soluc/cloudflare-news-project/.venv/bin/python tools/news/master-news-flow.py`
  - Use `--source`, `--query`, `--past-size`, `--today-size`, `--manual-sites`, `--count`.

## Coding Style & Naming Conventions
- Codebase is primarily JavaScript; follow existing style in `src/index.js` and `public/script.js`.
- Indentation appears to be 2 spaces (preserve existing formatting).
- No formatter or linter config is present; keep changes consistent with nearby code.
- Use clear, descriptive names for articles, categories, and API routes (e.g., `/api/articles/:id`).
- New API routes: `/api/ingest`, `/api/paraphrase`, `/api/sites/list`, and `/api/articles?site=a,b`.

## Testing Guidelines
- No automated test framework or test directory is present.
- If you add tests, document the runner and add a `test` script to `package.json`.

## Commit & Pull Request Guidelines
- A `.git` directory exists; no commit convention is enforced.
- If contributing via PR, include:
  - A short summary of user-visible changes.
  - Deployment impact notes (Pages vs Worker).
  - Screenshots or clips for UI changes in `public/`.

## Configuration & Security Notes
- Local secrets belong in `.dev.vars` (example in `README.md`).
- Do not hardcode tokens; use `c.env.*` in Workers (see `src/index.js`).
- CMS uses `ADMIN_TOKEN` (Bearer) to create/update/delete and ingest in batch.
- News download keys:
  - `NEWSAPI_KEY`, `WORLDNEWS_KEY`, `NEWSDATA_KEY` (loaded via environment or `.env`).

## Recent Changes (Feb 2026)
- CMS: batch publish, filters by site/category, paraphrase toggle, and additional screens (categorías/usuarios/configuración).
- Worker API: `/api/ingest`, `/api/paraphrase`, `/api/sites/list`, and site/category filters.
- Templates: fixed main layout with sidebar, tuned header padding, added adaptive preloader, and logo image styles.
- Legal: dynamic footer links to `#descargo` and full Terms/Privacy text in `docs/legal/TEXTOS_LEGALES.md`.
- Generator:
  - `tools/site/generate-sites.py` supports manual per-site input, per-site folders, `logo.png`, and `site_config.json`.
  - `tools/images/cache_original_images.py` caches original article images into `assets/images`.
  - `tools/news/master-news-flow.py` orchestrates download → paraphrase → cache images → generate sites → preloaders.
- News download scripts now accept past/today ranges (`tools/news/newsapi.py`, `tools/api/newsapi.py`, `tools/api/newsdata.py`, `tools/api/worldnews.py`).
