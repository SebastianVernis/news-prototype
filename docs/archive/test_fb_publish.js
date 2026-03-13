// Test script to diagnose Facebook publishing issue
// Run with: node test_fb_publish.js

const SITE_SLUG = 'radiocinconoticias';
const API_URL = 'https://news-api.sebastianvernis.workers.dev/api';

async function test() {
  console.log('=== Facebook Publishing Diagnostic ===\n');
  
  // 1. Check site configuration
  console.log('1. Checking site configuration...');
  const sitesRes = await fetch(`${API_URL}/sites`);
  const sites = await sitesRes.json();
  const site = sites.find(s => s.SLUG === SITE_SLUG);
  
  if (!site) {
    console.error(`❌ Site ${SITE_SLUG} not found`);
    return;
  }
  
  console.log(`   ✓ Site: ${site.NOMBRE}`);
  console.log(`   ✓ Facebook Activo: ${site.FACEBOOK_ACTIVO ? 'YES' : 'NO'}`);
  console.log(`   ✓ Page ID: ${site.FACEBOOK_PAGE_ID || 'MISSING'}`);
  console.log(`   ✓ Token Secret: ${site.FACEBOOK_TOKEN_SECRET || 'MISSING'}`);
  
  // 2. Check pending articles
  console.log('\n2. Checking pending articles...');
  const monitorRes = await fetch(`${API_URL}/facebook/monitor`);
  const monitor = await monitorRes.json();
  const pendingForSite = monitor.filter(a => a.SITIO === SITE_SLUG);
  
  console.log(`   ✓ Found ${pendingForSite.length} pending articles for ${SITE_SLUG}`);
  
  if (pendingForSite.length > 0) {
    const article = pendingForSite[0];
    console.log(`   ✓ First article: ${article.TITULO?.substring(0, 50)}...`);
    console.log(`   ✓ Image: ${article.URL_IMAGEN?.substring(0, 60)}...`);
    console.log(`   ✓ Slug: ${article.ID_PARAFRASEADO}`);
  }
  
  // 3. Test URL construction
  console.log('\n3. Testing URL construction...');
  if (pendingForSite.length > 0) {
    const slug = pendingForSite[0].ID_PARAFRASEADO;
    const pagesUrl = `https://main.${SITE_SLUG}.pages.dev/articulo/?slug=${slug}`;
    console.log(`   ✓ Pages URL: ${pagesUrl}`);
    
    // Test if URL is accessible
    try {
      const testRes = await fetch(pagesUrl, { method: 'HEAD' });
      console.log(`   ✓ URL Status: ${testRes.status} ${testRes.ok ? '✓' : '✗'}`);
    } catch (e) {
      console.log(`   ✗ URL Error: ${e.message}`);
    }
  }
  
  // 4. Check cron status
  console.log('\n4. Checking cron status...');
  const cronRes = await fetch(`${API_URL}/cron/status`);
  const cron = await cronRes.json();
  console.log(`   ✓ Last Run: ${cron.lastRun}`);
  console.log(`   ✓ FB Task: ${cron.tasks?.fb}`);
  console.log(`   ✓ Next Run: ${cron.nextRunInMinutes} minutes`);
  
  // 5. Summary
  console.log('\n=== Summary ===');
  const issues = [];
  
  if (!site.FACEBOOK_ACTIVO) issues.push('Facebook is not active for this site');
  if (!site.FACEBOOK_PAGE_ID) issues.push('Missing Facebook Page ID');
  if (!site.FACEBOOK_TOKEN_SECRET) issues.push('Missing Facebook Token Secret');
  if (pendingForSite.length === 0) issues.push('No pending articles to publish');
  
  if (issues.length > 0) {
    console.log('⚠️  Issues found:');
    issues.forEach(i => console.log(`   - ${i}`));
  } else {
    console.log('✓ All checks passed - Facebook publishing should work');
    console.log('\n💡 To force publish, run:');
    console.log(`   curl -X POST ${API_URL}/facebook/force-publish/${SITE_SLUG}`);
  }
}

test().catch(console.error);
