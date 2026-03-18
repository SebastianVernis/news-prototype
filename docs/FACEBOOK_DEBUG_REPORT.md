# Facebook Publishing Debug Report

**Date:** 2026-03-09  
**Status:** Critical Issues Identified

---

## 🔍 Executive Summary

The Facebook publishing system has **multiple critical issues** preventing efficient article distribution:

1. **Facebook Graph API Error (#100)** - "Only owners of the URL have the ability to specify the picture, name, thumbnail or description params"
2. **Site Configuration Issues** - Some sites are inactive (`FACEBOOK_ACTIVO = 0`)
3. **Potential Token Issues** - Need verification
4. **Image URL Format** - Using R2 uploads which may trigger Facebook's URL ownership check

---

## 📊 Current Status Analysis

### Cron Status (from `/api/cron/status`)

```json
{
  "lastRun": "2026-03-09T21:37:47.041Z",
  "tasks": {
    "fb_radiocinconoticias": "No published (check logs)",
    "fb_centralmexico": "No published (check logs)",
    "fb_enfoquecapital": "Error: (#100) Only owners of the URL...",
    "fb_enfoquedirecto": "Error: (#100) Only owners of the URL...",
    "fb_formulacdmx": "Error: (#100) Only owners of the URL...",
    "fb_noticiashorizonte": "Error: Site not found or inactive",
    "fb_pulsodiario": "Error: (#100) Only owners of the URL...",
    "fb_puntoclave": "Error: (#100) Only owners of the URL..."
  }
}
```

### Key Findings

#### ✅ What's Working
- RSS ingestion: **OK** (2 articles in last run)
- Ticker updates: **OK**
- Some sites successfully publish: `radiocinconoticias`, `centralmexico`, `tvmexico`, `cbnnoticias`, `mexicoinformado`, `nodoinformativo`, `bitacoraurbana`, `reportecentralmx`, `verticenoticias`, `noticiasobjetivo`

#### ❌ What's Failing

**Error Type 1: Facebook Graph API Error #100**
```
(#100) Only owners of the URL have the ability to specify 
the picture, name, thumbnail or description params.
```

**Affected Sites:**
- `enfoquecapital`
- `enfoquedirecto`
- `formulacdmx`
- `pulsodiario`
- `puntoclave`
- `radarinformativo` (potential)
- `reportediario` (potential)

**Error Type 2: Site Not Found or Inactive**
- `noticiashorizonte` - `FACEBOOK_ACTIVO = 0` in database

**Error Type 3: No Published (Check Logs)**
- Most stable sites show this - likely timer-based (3-hour window not elapsed)

---

## 🐛 Root Cause Analysis

### Issue #1: Facebook Graph API Error #100

**What it means:**
Facebook is rejecting the `picture` parameter because the domain in the `link` URL doesn't match the domain that owns the image URL.

**Technical Details:**

When posting to Facebook with:
```javascript
formData.append('link', 'https://enfoquecapital.top/articulo/?slug=article-slug');
formData.append('picture', 'https://uploads.sebastianvernis.space/auto/image.jpg');
```

Facebook checks:
1. Does `enfoquecapital.top` own `uploads.sebastianvernis.space`?
2. Answer: **NO** → Error #100

**Why it works for some sites:**
- Sites that successfully publish likely have articles with **original source images** (from RSS feeds like El País, Proceso, etc.)
- Sites failing are trying to post with **R2-uploaded images** (`uploads.sebastianvernis.space`)

**Evidence from Database:**
```sql
-- Pending articles with R2 images
SELECT ID, URL_IMAGEN FROM ARTICULOS_PARAFRASEADOS 
WHERE FB_PUBLICADO = 0 
AND URL_IMAGEN LIKE '%uploads.sebastianvernis.space%';
```

Results show ALL pending articles use R2 images:
- `https://uploads.sebastianvernis.space/auto/5ce7054c-510e-4fff-b31c-52ac966cb97d.jpg`
- `https://uploads.sebastianvernis.space/auto/75784fb2-3c7b-4fb7-92fe-2da971a3dffb.jpg`
- etc.

### Issue #2: Site Configuration

**Database Check:**
```sql
SELECT SLUG, FACEBOOK_ACTIVO FROM SITIOS WHERE SLUG = 'noticiashorizonte';
```

Result:
```
| noticiashorizonte | 0 |  ← INACTIVE
```

### Issue #3: Token Verification Needed

All required secrets exist in Cloudflare:
- ✅ `FB_TOKEN_ENFOQUECAPITAL`
- ✅ `FB_TOKEN_PULSODIARIO`
- ✅ `FB_TOKEN_PUNTOCLAVE`
- ✅ `FB_TOKEN_FORMULACDMX`
- ✅ etc.

**But tokens need validation** - they may be expired or have incorrect permissions.

---

## 🔧 Recommended Fixes

### Fix #1: Remove `picture` Parameter for R2 Images

**Problem:** Facebook rejects R2 image URLs when the link domain doesn't match.

**Solution:** Let Facebook scrape the OG image from the page instead of forcing it via API.

**Code Change in `publishToFB` function:**

```javascript
// CURRENT CODE (line ~2119)
if (imageUrl && imageUrl.trim() !== '' && 
    !imageUrl.includes('logo.png') && 
    !imageUrl.includes('unsplash.com')) {
  formData.append('picture', imageUrl);
}

// FIXED CODE
// Only include picture if it's from a trusted external source (not R2)
// Facebook will scrape OG:image from the link page for R2 images
if (imageUrl && imageUrl.trim() !== '' && 
    !imageUrl.includes('logo.png') && 
    !imageUrl.includes('unsplash.com') &&
    !imageUrl.includes('uploads.sebastianvernis.space')) {
  formData.append('picture', imageUrl);
}
```

**Why this works:**
1. For RSS articles with original images (El País, Proceso, etc.): Facebook will use the provided `picture` URL
2. For CMS articles with R2 images: Facebook will scrape the `og:image` meta tag from the article page
3. The article page already has correct OG tags via Cloudflare Functions middleware

### Fix #2: Activate `noticiashorizonte`

```sql
UPDATE SITIOS 
SET FACEBOOK_ACTIVO = 1 
WHERE SLUG = 'noticiashorizonte';
```

### Fix #3: Verify Facebook Tokens

Run token verification script:
```bash
python3 scripts/verify_fb_tokens.py
```

Or manually test one token:
```bash
curl -s "https://graph.facebook.com/v19.0/457328060805587?access_token=[TOKEN]&fields=name"
```

### Fix #4: Add Better Error Logging

Add structured logging to track failures:

```javascript
console.log(`[FB] Article ID: ${article.ID}`);
console.log(`[FB] Sites to publish: ${sitesToPublish.join(', ')}`);
console.log(`[FB] Image URL: ${imageUrl}`);
console.log(`[FB] Is R2 image: ${imageUrl.includes('uploads.sebastianvernis.space')}`);
console.log(`[FB] Token exists: ${!!token}`);
console.log(`[FB] Page ID: ${site.FACEBOOK_PAGE_ID}`);
```

---

## 📋 Action Plan

### Immediate Actions (High Priority)

1. **Apply Fix #1** - Modify `publishToFB` to skip `picture` parameter for R2 images
2. **Deploy to production**
3. **Test with pending articles**
4. **Monitor logs**

### Secondary Actions (Medium Priority)

5. **Activate `noticiashorizonte`** if needed
6. **Verify all Facebook tokens** are valid and not expired
7. **Add better error logging** for future debugging

### Long-term Improvements (Low Priority)

8. **Implement token refresh mechanism** (tokens expire every ~60 days)
9. **Add Facebook publishing dashboard** in CMS
10. **Create automated alerts** for publishing failures

---

## 🧪 Testing Plan

### Test Case 1: RSS Article with External Image

```sql
-- Find an article with external image
SELECT ID, TITULO_PARAFRASEADO, URL_IMAGEN 
FROM ARTICULOS_PARAFRASEADOS 
WHERE URL_IMAGEN LIKE '%elpais.com%' 
  OR URL_IMAGEN LIKE '%proceso.com.mx%'
LIMIT 1;
```

**Expected:** Facebook should use the `picture` parameter successfully

### Test Case 2: CMS Article with R2 Image

```sql
-- Find an article with R2 image
SELECT ID, TITULO, URL_IMAGEN 
FROM ARTICULOS_CMS 
WHERE URL_IMAGEN LIKE '%uploads.sebastianvernis.space%'
LIMIT 1;
```

**Expected:** Facebook should scrape OG:image from the page (no `picture` parameter)

### Test Case 3: Manual Publish Test

```bash
# Trigger manual Facebook publish
curl -X POST https://news-api.sebastianvernis.workers.dev/api/articles/publish-fb/[ARTICLE_ID] \
  -H "Authorization: Bearer [ADMIN_TOKEN]"
```

**Expected:** Article publishes successfully to Facebook

---

## 📈 Success Metrics

After applying fixes, monitor:

1. **Publish Success Rate:** Should increase from ~40% to >90%
2. **Error #100 Occurrences:** Should drop to 0
3. **Articles Published per Day:** Should increase
4. **Time to Publish:** Should remain <5 seconds per article

---

## 🔗 Related Files

- **Main Code:** `/src/index.js` (function `publishToFB`, line 2054)
- **Append Code:** `/src/index_append.js` (function `publishToFB`, line 48)
- **Config:** `/src/wrangler.toml`
- **Database:** Cloudflare D1 `news_db`
- **Secrets:** Cloudflare Workers Secrets (50+ FB_TOKEN_*)

---

## 📝 Notes

- Facebook Graph API v19.0 is being used (current stable)
- Publishing happens every 3 hours per site (timer-based)
- Cron runs every 30 minutes
- Articles must have `FB_REQUERIDO = 1` to be published
- Image filter: No `logo.png`, no `unsplash.com`, and now no R2 images

---

**Next Steps:** Apply Fix #1 immediately and test.
