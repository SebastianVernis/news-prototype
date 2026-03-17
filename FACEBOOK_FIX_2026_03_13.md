# Facebook Publishing Fix - 2026-03-13

## Problem Diagnosed

Facebook publishing stopped working because:

1. **KV Timer Logic Bug**: The `processFBTimer` function in `src/cron/facebook.js` was resetting the timer to `now` when no pending articles existed, creating an infinite wait loop.

2. **Timer Never Expired**: Sites with pending articles were being skipped because the timer hadn't expired (3 hours), but the timer was being incorrectly maintained.

3. **No Visibility**: The logging didn't show WHY sites were being skipped, making debugging impossible.

## Root Cause

```javascript
// BEFORE (buggy code):
if (pending === 0) {
  FB_LOG(`${siteSlug}: No pending articles`);
  await env.ARTICLES_KV.put(kvKey, now.toString()); // ❌ BUG: Resets timer!
  stats.skipped++;
  continue;
}
```

This meant:
- When a site had no articles, timer was set to NOW
- Next cron run: timer shows "just published", wait 3 hours
- By the time timer expires, new articles may exist but timer keeps extending

## Solution Applied

### 1. Fixed Timer Logic (`src/cron/facebook.js`)

**Changed**: Don't reset timer when skipping due to no articles
```javascript
// AFTER (fixed code):
if (pending === 0) {
  FB_LOG(`${siteSlug}: SKIP - No pending articles (timer preserved)`);
  stats.skipped_no_articles++;
  continue; // ✅ Timer preserved, will expire naturally
}
```

**Added**: Detailed skip reason logging
- `skipped_timer`: Timer hasn't expired yet
- `skipped_no_articles`: No pending articles
- `skipped_no_image`: No articles with valid R2 image

**Added**: Valid image count logging to see how many articles are eligible

### 2. Created Cleanup Script (`scripts/cleanup_fb_timers.js`)

Purpose: Reset all 27 site timers to force immediate publishing

Usage:
```bash
node scripts/cleanup_fb_timers.js
# Answer "yes" to confirm
```

What it does:
- Deletes all `last_fb_post_[site]` keys from KV
- Next cron run treats all sites as "never published" (`lastPostTime = 0`)
- All sites with pending articles will publish immediately

## Files Modified

1. **src/cron/facebook.js**
   - Fixed `processFBTimer()` logic
   - Added detailed skip reason tracking
   - Improved logging visibility

2. **scripts/cleanup_fb_timers.js** (new)
   - Interactive cleanup script
   - Deletes all 27 timer keys from KV
   - Safe: skips non-existent keys

## Deployment

```bash
# Deploy Worker
cd src && wrangler deploy

# Run cleanup
node scripts/cleanup_fb_timers.js
```

## Expected Behavior After Fix

### Next Cron Run (within 30 min)
```
fb: OK (27/27)  # Will attempt to publish on all 27 sites
```

### Ongoing Behavior
- Each site publishes 1 article every 3 hours
- Sites without pending articles: timer preserved (no reset)
- Sites with pending articles: publish when timer expires
- Clear logging shows why each site is skipped or published

## Verification Commands

```bash
# Check cron status
curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | jq

# Check Facebook monitor
curl -s https://news-api.sebastianvernis.workers.dev/api/facebook/monitor | jq '.[] | select(.FB_PUBLICADO == 0)' | wc -l

# Count pending articles per site
wrangler d1 execute news_db --command "
  SELECT 'radiocinconoticias' as site, COUNT(*) as pending 
  FROM ARTICULOS_SITIO_RADIOCINCONOTICIAS WHERE FB_PUBLICADO = 0
" --remote
```

## Timeline

- **2026-03-13 05:00**: Last cron run with bug (OK (0/27))
- **2026-03-13 05:25**: Bug identified and fixed
- **2026-03-13 05:30**: Worker deployed
- **2026-03-13 05:32**: KV timers cleaned up
- **Next cron run**: Expected to publish to all 27 sites with pending articles

## Prevention

To avoid this issue in the future:

1. **Never reset timers when skipping** - only update on successful publish
2. **Add skip reason logging** - always log WHY something was skipped
3. **Monitor timer state** - add metrics for timer age vs pending articles
4. **Test timer expiry** - simulate timer scenarios in staging

---

*Fix applied by: AI Agent*
*Date: 2026-03-13*
*Issue: Facebook publishing stopped for all 27 sites*
