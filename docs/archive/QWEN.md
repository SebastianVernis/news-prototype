# Cloudflare News Project - Context Guide

## Project Overview

This is a **multi-site news publishing platform** built for deployment on Cloudflare's edge infrastructure (Pages + Workers). The system automates news acquisition from multiple APIs (NewsAPI, WorldNews, NewsData), processes content through paraphrasing, and generates static sites for multiple domains.

### Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  News APIs      │────▶│  Python Tools    │────▶│  Sites/         │
│  (external)     │     │  (download/      │     │  (generated     │
└─────────────────┘     │   paraphrase)    │     │   static HTML)  │
                        └──────────────────┘     └─────────────────┘
                                 │                       │
                                 ▼                       ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │  Cloudflare      │◀────│  Cloudflare     │
                        │  Worker API      │     │  Pages          │
                        │  (src/index.js)  │     │  (public/)      │
                        └──────────────────┘     └─────────────────┘
```

### Tech Stack

- **Frontend**: Static HTML/CSS/JS (Cloudflare Pages)
- **Backend**: Cloudflare Workers with Hono framework
- **Database**: Cloudflare D1 (SQLite)
- **Storage**: Cloudflare KV (caching), R2 (images)
- **Automation**: Python scripts for news ingestion and site generation
- **Deployment**: Wrangler CLI

---

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `public/` | Static site files (HTML, CSS, JS) served by Pages |
| `src/` | Cloudflare Worker API code (Hono-based REST API) |
| `functions/` | Pages Functions (serverless endpoints) |
| `workers/` | Additional Worker implementations |
| `tools/` | Python utilities (news, site, images, api subdirs) |
| `scripts/` | Shell scripts for deployment/setup |
| `docs/` | Documentation (INDEX.md, STATUS.md, legal texts) |
| `sites/` | Generated static sites (per-site folders) |
| `data/` | Local data (news JSON, logs, queues) |
| `assets/` | Image assets and cached images |
| `generated_images/` | AI/image pipeline outputs |
| `backups/` | Database/content backups |

---

## Building and Running

### Installation

```bash
npm install
```

### Local Development

**Run Pages dev server:**
```bash
npm run dev
# or with live reload
npm run preview
```

**Run Worker API locally:**
```bash
npx wrangler dev src/index.js --port 8787
```

**Run CMS locally:**
```bash
npx wrangler pages dev ./public --port 8788
# Open http://localhost:8788/admin.html
```

### Environment Configuration

Create `.dev.vars` for local development:
```env
ADMIN_TOKEN=your_admin_token
CF_ACCOUNT_ID=your_account_id
CF_API_TOKEN=your_api_token
NEWSAPI_KEY=your_newsapi_key
WORLDNEWS_KEY=your_worldnews_key
NEWSDATA_KEY=your_newsdata_key
```

### Python News Flow

**Master orchestration script:**
```bash
.venv/bin/python tools/news/master-news-flow.py \
  --source newsapi \
  --query "México" \
  --past-size 30 \
  --today-size 10 \
  --count 3
```

**Key flags:**
- `--source`: `newsapi`, `worldnews`, or `newsdata`
- `--query`: Search query for news
- `--past-size`: Number of past articles to fetch
- `--today-size`: Number of today's articles to fetch
- `--manual-sites`: Enable manual site input
- `--count`: Number of articles to process
- `--no-cache-images`: Skip image caching

### Deployment

**Deploy static site to Pages:**
```bash
npm run deploy
# or
wrangler pages deploy ./public --project-name=your-project-name
```

**Deploy Worker API:**
```bash
wrangler deploy src/index.js --name news-api
```

**Database migration (add sites column):**
```bash
npx wrangler d1 execute news_db --command "ALTER TABLE articles ADD COLUMN sites TEXT;"
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/articles` | - | List articles (pagination, filters) |
| `GET` | `/api/articles?site=a,b` | - | Filter by site(s) |
| `GET` | `/api/articles?category=x` | - | Filter by category |
| `GET` | `/api/articles/:slug` | - | Get single article |
| `POST` | `/api/articles` | ✓ | Create article |
| `PUT` | `/api/articles/:id` | ✓ | Update article |
| `DELETE` | `/api/articles/:id` | ✓ | Delete article |
| `PATCH` | `/api/articles/:id/featured` | ✓ | Toggle featured |
| `GET` | `/api/categories` | - | List categories |
| `GET` | `/api/search?q=query` | - | Search articles |
| `GET` | `/api/sites/list` | - | List unique sites |
| `POST` | `/api/ingest` | ✓ | Bulk ingest articles |
| `POST` | `/api/paraphrase` | ✓ | Paraphrase articles |
| `GET` | `/api/health` | - | Health check |

**Auth**: Bearer token via `Authorization: Bearer <ADMIN_TOKEN>`

---

## Development Conventions

### Code Style

- **JavaScript**: 2-space indentation, existing style in `src/index.js` and `public/script.js`
- **Naming**: Descriptive names for articles, categories, API routes
- **No formatter/linter**: Match existing code formatting

### Testing

- No automated test framework present
- Test command: `npm test` (runs `node --test`)
- Manual testing via local dev servers

### Git

- No commit convention enforced
- PR guidelines (from AGENTS.md):
  - Summary of user-visible changes
  - Deployment impact notes (Pages vs Worker)
  - Screenshots for UI changes

### Security

- **Secrets**: Store in `.dev.vars` (local) or Cloudflare dashboard (production)
- **Never hardcode tokens**: Use `c.env.*` in Workers
- **Admin token**: Used for Bearer auth in CMS/API

---

## Key Configuration Files

### `wrangler.toml`

Main Cloudflare configuration:
- Environment variables (`SITE_TITLE`, `ADMIN_TOKEN`, API keys)
- KV namespaces (`ARTICLES_KV`)
- D1 database (`news_db`)
- Cron triggers (hourly news fetch, 30-min featured updates, daily cleanup)
- Build configuration

### `package.json`

NPM scripts and dependencies:
- `hono`: Web framework for Workers
- `wrangler`: Cloudflare CLI
- `@cloudflare/workers-types`: TypeScript types

### `src/schema.sql`

D1 database schema:
```sql
CREATE TABLE articles (
  id TEXT PRIMARY KEY,
  slug TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  excerpt TEXT,
  content TEXT,
  category TEXT,
  author TEXT,
  image_url TEXT,
  published_at TEXT,
  updated_at TEXT,
  featured INTEGER DEFAULT 0,
  views INTEGER DEFAULT 0,
  tags TEXT,
  sites TEXT
);
```

---

## Cron Jobs (Automated Tasks)

| Schedule | Task |
|----------|------|
| `0 * * * *` | Fetch new news every hour |
| `*/30 * * * *` | Update featured articles every 30 min |
| `0 2 * * *` | Clean old articles daily (2 AM) |
| `0 9 * * 0` | Weekly analytics reports (Sundays 9 AM) |

---

## LLM Integration (Optional)

The pipeline supports LLM-assisted paraphrasing and supervision:

**Environment variables:**
- `PARAPHRASE_PROVIDER` / `PARAPHRASE_MODEL`: Text correction
- `SUPERVISOR_PROVIDER` / `SUPERVISOR_MODEL`: Grammar/structure checks
- `GEMINI_API_KEY` / `GEMINI_MODEL`: Style audits

**Supported providers:**
- Groq (`GROQ_API_KEY`)
- OpenRouter (`OPENROUTER_API_KEY`)
- Ollama (`OLLAMA_HOST`, default `http://localhost:11434`)
- Gemini (`GEMINI_API_KEY`)

**Recommended free-tier defaults:**
```env
PARAPHRASE_PROVIDER=openrouter
PARAPHRASE_MODEL=openrouter/free
SUPERVISOR_PROVIDER=groq
SUPERVISOR_MODEL=llama-3.1-8b-instant
GEMINI_MODEL=gemini-1.5-flash
```

---

## Documentation Index

| File | Description |
|------|-------------|
| `README.md` | Main project overview |
| `AGENTS.md` | Repository guidelines |
| `docs/INDEX.md` | Full documentation index |
| `docs/STATUS.md` | Current status and flow notes |
| `docs/legal/TEXTOS_LEGALES.md` | Terms & Privacy texts |
| `tools/INDEX.md` | Python tools documentation |

---

## Common Tasks

### Add new news source
1. Add API key to `.dev.vars` and Cloudflare dashboard
2. Update `tools/news/` scripts for new source
3. Modify `master-news-flow.py` to include source option

### Customize site branding
1. Update `SITE_TITLE` and `SITE_DESCRIPTION` in `wrangler.toml`
2. Modify `public/style.css` for colors/branding
3. Replace `public/favicon.ico` and logo placeholders

### Database changes
1. Update `src/schema.sql`
2. Run migration: `npx wrangler d1 execute news_db --command "<SQL>"`

### Deploy to multiple sites
1. Run master flow with `--manual-sites`
2. Generated sites output to `sites/<sitio>/`
3. Deploy each to Cloudflare Pages

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing `sites` column | Run D1 migration (see above) |
| Auth failures | Verify `ADMIN_TOKEN` in `.dev.vars` |
| KV/D1 errors | Check namespace/database IDs in `wrangler.toml` |
| Deployment errors | Check Cloudflare dashboard logs |
| Python script failures | Verify API keys in environment or `.env` |

---

## Output Directories (Generated Content)

| Directory | Contents | Override Env Var |
|-----------|----------|------------------|
| `sites/` | Generated site HTML | `SITES_DIR` |
| `data/` | News JSON, logs, queues | `NEWS_DATA_DIR` |
| `assets/` | Images | `NEWS_ASSETS_DIR` |
| `generated_images/` | AI outputs | - |
| `assets/images/` | Cached original images | `NEWS_IMAGES_DIR` |
