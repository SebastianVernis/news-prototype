#!/usr/bin/env node
/**
 * Cleanup Facebook Timers Script
 * 
 * Purpose: Reset all Facebook publishing timers in KV to force immediate publishing
 * on the next cron run. Use this when timers are stuck or publishing has stopped.
 * 
 * Usage:
 *   node scripts/cleanup_fb_timers.js
 * 
 * This script:
 * 1. Lists all KV keys matching `last_fb_post_*`
 * 2. Deletes all matching keys
 * 3. After running, the next cron will publish immediately (lastPostTime = 0)
 */

import { execSync } from 'child_process';

const SITIOS_LIST = [
  // Sitios Estables (10)
  'radiocinconoticias', 'centralmexico', 'tvmexico', 'cbnnoticias',
  'mexicoinformado', 'nodoinformativo', 'bitacoraurbana',
  'reportecentralmx', 'verticenoticias', 'noticiasobjetivo',
  // Nuevos Sitios (17)
  'boominformativo', 'capitalpress', 'diarioexpress', 'elpulsomexicano',
  'enfoquecapital', 'enfoquedirecto', 'formulacdmx', 'mexicantimes',
  'mexico360noticias', 'mradio', 'noticiashorizonte', 'pulsodiario',
  'puntoclave', 'puntonoticias', 'radarinformativo', 'reportediario',
  'televisionabc',
];

const KV_NAMESPACE_ID = 'fbf21fb75f5647a8966858d199b44e0b'; // ARTICLES_KV

console.log('🔧 Facebook Timer Cleanup Script');
console.log('=================================\n');

async function cleanupTimers() {
  const keysToDelete = SITIOS_LIST.map(slug => `last_fb_post_${slug}`);
  
  console.log(`📋 Will delete ${keysToDelete.length} timer keys:`);
  keysToDelete.forEach(key => console.log(`   - ${key}`));
  console.log('');
  
  // Ask for confirmation
  console.log('⚠️  This will reset all Facebook publishing timers.');
  console.log('⚠️  The next cron run will publish immediately to all sites with pending articles.');
  console.log('');
  
  const readline = await import('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise((resolve) => {
    rl.question('Continue? (yes/no): ', (answer) => {
      rl.close();
      if (answer.toLowerCase() !== 'yes') {
        console.log('❌ Cancelled by user');
        resolve(false);
        return;
      }
      resolve(true);
    });
  });
}

async function deleteKey(key) {
  try {
    execSync(`wrangler kv key delete "${key}" --namespace-id ${KV_NAMESPACE_ID} --remote`, {
      stdio: ['pipe', 'pipe', 'pipe']
    });
    return { success: true, key };
  } catch (error) {
    // Key might not exist, which is fine
    if (error.status === 1 && error.stderr.toString().includes('not found')) {
      return { success: true, key, skipped: 'not_found' };
    }
    return { success: false, key, error: error.message };
  }
}

async function main() {
  const confirmed = await cleanupTimers();
  if (!confirmed) return;
  
  console.log('\n🗑️  Deleting timer keys...\n');
  
  const results = [];
  for (const key of SITIOS_LIST.map(slug => `last_fb_post_${slug}`)) {
    const result = await deleteKey(key);
    results.push(result);
    
    if (result.skipped) {
      console.log(`   ⚪ ${key} (not found, OK)`);
    } else if (result.success) {
      console.log(`   ✅ ${key} deleted`);
    } else {
      console.log(`   ❌ ${key} FAILED: ${result.error}`);
    }
  }
  
  console.log('\n📊 Summary:');
  const deleted = results.filter(r => r.success && !r.skipped).length;
  const skipped = results.filter(r => r.skipped).length;
  const failed = results.filter(r => !r.success).length;
  
  console.log(`   ✅ Deleted: ${deleted}`);
  console.log(`   ⚪ Skipped (not found): ${skipped}`);
  console.log(`   ❌ Failed: ${failed}`);
  
  console.log('\n✨ Done! The next cron run will publish immediately.');
  console.log('   Check status with: curl -s https://news-api.sebastianvernis.workers.dev/api/cron/status | jq');
}

main().catch(console.error);
