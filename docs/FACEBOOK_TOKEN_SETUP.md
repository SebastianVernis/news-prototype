# Facebook Token Setup Guide

## Overview
This guide explains how to set up Facebook Page Access Tokens for all 10 news sites using a long-lived user token.

## Prerequisites

1. **Long-lived User Token**: You need a Facebook user token with extended permissions
2. **Virtual Environment**: Make sure `.venv` is set up in the project root

## Setup Process

### Step 1: Add Your User Token to `.env`

Edit the `.env` file and add your long-lived user token:

```bash
LONG_LIVED_TOKENFB=YOUR_FACEBOOK_USER_TOKEN_HERE
```

Get your token from: https://developers.facebook.com/tools/explorer/

### Step 2: Run the Token Update Script

```bash
# Option A: Using the shell script
./scripts/update_fb_tokens.sh

# Option B: Manual
source .venv/bin/activate
python3 scripts/update_fb_tokens.py
```

### What the Script Does

1. **Fetches Pages**: Uses your user token to get all Facebook pages you manage
2. **Extracts Page Tokens**: Gets the access token for each page
3. **Updates `.env`**: Saves all page tokens locally
4. **Uploads to Cloudflare**: Pushes each token as a secret to the `news-api` Worker

### Expected Output

```
=== Actualización de Tokens Facebook ===

🔑 Usando token de usuario: YOUR_FACEBOOK_USER_TOKEN_HERE

📋 Obteniendo páginas del usuario...
✅ Encontradas 10 páginas

→ Radio Cinco Noticias (639476222579619)
   ✅ .env + Cloudflare actualizados

→ Central México News (618190118045350)
   ✅ .env + Cloudflare actualizados

... (continues for all 10 pages)

=== Resumen ===
✅ Exitosos: 10
❌ Errores: 0

📁 Tokens guardados en: .env
☁️  Secrets actualizados: news-api (Cloudflare)
```

## Manual Setup (Alternative)

If you prefer to set tokens manually:

### 1. Get Page Token from Graph API Explorer

Visit: https://developers.facebook.com/tools/explorer/

```
GET /v19.0/me/accounts?fields=id,name,access_token,tasks
```

### 2. Add to `.env` Locally

```bash
FB_TOKEN_RADIOCINCONOTICIAS=EAAmv1Puxa7wBQ...page_token_1
FB_TOKEN_CENTRALMEXICO=EAAmv1Puxa7wBQ...page_token_2
FB_TOKEN_TVMEXICO=EAAmv1Puxa7wBQ...page_token_3
FB_TOKEN_CBNNOTICIAS=EAAmv1Puxa7wBQ...page_token_4
FB_TOKEN_MEXICOINFORMADO=EAAmv1Puxa7wBQ...page_token_5
FB_TOKEN_NODOINFORMATIVO=EAAmv1Puxa7wBQ...page_token_6
FB_TOKEN_BITACORAURBANA=EAAmv1Puxa7wBQ...page_token_7
FB_TOKEN_REPORTECENTRALMX=EAAmv1Puxa7wBQ...page_token_8
FB_TOKEN_VERTICENOTICIAS=EAAmv1Puxa7wBQ...page_token_9
FB_TOKEN_NOTICIASOBJETIVO=EAAmv1Puxa7wBQ...page_token_10
```

### 3. Upload to Cloudflare

```bash
cd src

wrangler secret put FB_TOKEN_RADIOCINCONOTICIAS --name news-api
wrangler secret put FB_TOKEN_CENTRALMEXICO --name news-api
wrangler secret put FB_TOKEN_TVMEXICO --name news-api
wrangler secret put FB_TOKEN_CBNNOTICIAS --name news-api
wrangler secret put FB_TOKEN_MEXICOINFORMADO --name news-api
wrangler secret put FB_TOKEN_NODOINFORMATIVO --name news-api
wrangler secret put FB_TOKEN_BITACORAURBANA --name news-api
wrangler secret put FB_TOKEN_REPORTECENTRALMX --name news-api
wrangler secret put FB_TOKEN_VERTICENOTICIAS --name news-api
wrangler secret put FB_TOKEN_NOTICIASOBJETIVO --name news-api
```

## Verification

### Check Local `.env`

```bash
grep FB_TOKEN_ .env
```

### Check Cloudflare Secrets

```bash
wrangler secret list --name news-api
```

### Test Token Validity

```bash
# Replace TOKEN and PAGE_ID
curl -s "https://graph.facebook.com/v19.0/[PAGE_ID]?access_token=[TOKEN]&fields=name"
```

### Test Facebook Publishing

```bash
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | python3 -m json.tool
```

## Troubleshooting

### Error: `LONG_LIVED_TOKENFB no está configurado`

**Solution**: Make sure the token is in your `.env` file and you've activated the virtual environment.

### Error: `No se pudieron obtener las páginas`

**Possible causes**:
- Token expired
- Insufficient permissions
- Wrong token type

**Solution**: Generate a new long-lived token with `pages_manage_posts` and `pages_read_engagement` permissions.

### Error: `wrangler: command not found`

**Solution**: 
```bash
npm install -g wrangler
# or
cd src && npm install
```

### Some Pages Not Found

If a page is not in the mapping, add it to `SITE_MAPPING` in the script:

```python
SITE_MAPPING = {
    "Page Name": "FB_TOKEN_SITENAME",
    # Add missing pages here
}
```

## Token Permissions Required

The user token needs these permissions:
- `pages_manage_posts` - Create posts on pages
- `pages_read_engagement` - Read page insights
- `pages_manage_metadata` - Access page information

## Token Expiration

- **User Tokens**: ~60 days (long-lived)
- **Page Tokens**: Do not expire when obtained from long-lived user tokens

**Recommendation**: Run the update script monthly or when you get authentication errors.

## Security Notes

⚠️ **Never commit `.env` to Git** - it's in `.gitignore` for a reason

⚠️ **Keep tokens secure** - they provide full access to your Facebook pages

✅ **Use Cloudflare Secrets** for production - never hardcode tokens in code

---

*Last updated: 2026-03-03*
