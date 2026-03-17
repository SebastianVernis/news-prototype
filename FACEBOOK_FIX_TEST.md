# Facebook Publishing Fix - Test Plan

**Date:** 2026-03-09  
**Fix Applied:** Exclude R2 images from `picture` parameter  
**Deployment:** ✅ Successful (Version ID: 9f3787ff-ed0b-4f11-a217-98fc55e56890)

---

## 🧪 Test Articles (R2 Images)

These articles have R2 images and were failing with Error #100:

| ID | Title | Sites | Image |
|----|-------|-------|-------|
| `9f91cdce-e1c7-4342-a2b5-993d2d2082d8` | Mujer denuncia robo con violencia... | puntonoticias,radarinformativo,reportediario | R2 |
| `c28ea366-3cf2-4653-bfa5-f9c839106079` | Libros antes que ladrillos... | verticenoticias,noticiasobjetivo,boominformativo | R2 |
| `129c6b56-1c18-403b-b5ac-478985965dad` | Las arquitectas invisibles... | noticiashorizonte,pulsodiario,puntoclave | R2 |
| `2616d55f-2a51-4a02-aee2-eb3f3d69fd6c` | Europa en vilo... | puntonoticias,radarinformativo,reportediario | R2 |
| `1a7a6e3c-b214-4d36-9980-d563a949fa04` | "Pueden viajar seguros"... | verticenoticias,noticiasobjetivo,boominformativo | R2 |

**Total pending:** 33 articles with `FB_PUBLICADO = 0` and `FB_REQUERIDO = 1`

---

## ✅ Test Steps

### Step 1: Manual Publish Test

Trigger manual Facebook publish for one article:

```bash
# Get admin token from environment or CMS
ADMIN_TOKEN="your-admin-token"

# Test with first article (Mujer denuncia robo...)
ARTICLE_ID="9f91cdce-e1c7-4342-a2b5-993d2d2082d8"

curl -X POST "https://news-api.sebastianvernis.workers.dev/api/articles/publish-fb/${ARTICLE_ID}" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"
```

**Expected Result:**
- ✅ Article publishes to Facebook without Error #100
- ✅ Facebook scrapes OG:image from the article page
- ✅ DB updates with `FB_PUBLICADO = 1` and `FB_FECHA = now`

### Step 2: Check Cron Status

Wait for next cron run (or trigger manually):

```bash
# Check status
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | python3 -m json.tool

# Or trigger manual cron
curl -X POST https://news-api.sebastianvernis.workers.dev/api/cron/manual \
  -H "Authorization: Bearer ${ADMIN_TOKEN}"
```

**Expected Result:**
- ✅ Facebook tasks show "OK" or "Published" instead of "Error: (#100)..."
- ✅ No more R2 image errors

### Step 3: Verify in Database

```sql
-- Check if article was published
SELECT ID, TITULO_PARAFRASEADO, FB_PUBLICADO, FB_FECHA, FB_SITIOS_PUBLICADOS
FROM ARTICULOS_PARAFRASEADOS
WHERE ID = '9f91cdce-e1c7-4342-a2b5-993d2d2082d8';
```

**Expected Result:**
- ✅ `FB_PUBLICADO = 1`
- ✅ `FB_FECHA` is recent timestamp
- ✅ `FB_SITIOS_PUBLICADOS` contains published site slugs

### Step 4: Check Facebook Pages

Visit the Facebook pages to verify posts:

- https://www.facebook.com/puntonoticias
- https://www.facebook.com/radarinformativo
- https://www.facebook.com/reportediario

**Expected Result:**
- ✅ Post appears with title and link
- ✅ Image is displayed (scraped from OG tags)
- ✅ Post links to correct article URL

---

## 📊 Success Criteria

| Metric | Before Fix | After Fix (Target) |
|--------|------------|-------------------|
| Error #100 occurrences | ~10/day | 0 |
| Publish success rate | ~40% | >90% |
| Articles pending FB | 33 | <10 |
| R2 image articles published | 0 | All |

---

## 🔍 Monitoring

### Logs to Watch

```bash
# Watch for successful publishes
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | \
  python3 -c "import sys,json; d=json.load(sys.stdin); \
    print('\n'.join([f\"{k}: {v}\" for k,v in d['tasks'].items() if k.startswith('fb_')]))"
```

### Key Log Messages

**Before Fix:**
```
[FB] Publicando en puntonoticias: Mujer denuncia robo...
Error: (#100) Only owners of the URL...
```

**After Fix (Expected):**
```
[FB] Publicando en puntonoticias: Mujer denuncia robo...
[FB] Artículo 9f91cdce-e1c7-4342-a2b5-993d2d2082d8 actualizado: FB_SITIOS_PUBLICADOS = "puntonoticias,radarinformativo,reportediario"
```

---

## 🐛 Rollback Plan

If issues occur, revert the fix:

```bash
cd /home/sebastianvernis/cloudflare-news-project/src
git checkout HEAD -- index.js
wrangler deploy
```

---

## 📝 Notes

- **Why this works:** Facebook scrapes the `og:image` meta tag from the article page when no `picture` parameter is provided
- **Article pages already have correct OG tags:** Cloudflare Functions middleware sets `og:image` to the R2 URL
- **No breaking changes:** External images (El País, Proceso, etc.) still use the `picture` parameter
- **Graceful fallback:** If OG image scraping fails, Facebook still posts with just the link and title

---

**Test Status:** ⏳ Ready for testing
