// src/cron/master.js — Orquestador principal del cron job

import { runRSSIngest } from './rss-ingest.js';
import { processFBTimer } from './facebook.js';
import { updateTickerData } from './ticker.js';

// ============================================================
// runMasterCron — Ejecuta todas las tareas programadas
// Orden: 1) RSS Ingestion → 2) Facebook Timer → 3) Ticker
// ============================================================
export async function runMasterCron(env) {
  console.log('[CRON] Starting runMasterCron...');
  const status = { lastRun: new Date().toISOString(), tasks: {} };

  // 1. RSS Ingestion (cada 30 min)
  try {
    console.log('[CRON] Starting RSS ingestion...');
    const ingestCount = await runRSSIngest(env);
    status.tasks.ingest = `OK (${ingestCount} articles)`;
    console.log(`[CRON] RSS ingestion complete: ${ingestCount} articles`);
  } catch (e) {
    console.error('[CRON] RSS ingestion error:', e.message);
    status.tasks.ingest = `Error: ${e.message}`;
  }

  // 2. Facebook Timer (publica 1 artículo aleatorio con R2 si pasaron 3 horas)
  try {
    console.log('[CRON] Starting Facebook Timer processing...');
    const fbStats = await processFBTimer(env);
    console.log(`[CRON] FB Timer result: processed=${fbStats.processed}, success=${fbStats.success}, failed=${fbStats.failed}, skipped_timer=${fbStats.skipped_timer}, skipped_no_articles=${fbStats.skipped_no_articles}, skipped_no_image=${fbStats.skipped_no_image}`);
    status.tasks.fb = `OK (${fbStats.success}/${fbStats.processed})`;
    console.log('[CRON] Facebook Timer processing complete');
  } catch (e) {
    console.error('[CRON] Facebook Timer error:', e.message);
    status.tasks.fb = `Error: ${e.message}`;
  }

  // 3. Ticker update
  try {
    console.log('[CRON] Updating ticker data...');
    await updateTickerData(env);
    status.tasks.ticker = 'OK';
    console.log('[CRON] Ticker update complete');
  } catch (e) {
    console.error('[CRON] Ticker error:', e.message);
    status.tasks.ticker = `Error: ${e.message}`;
  }

  // Guardar estado en KV
  console.log('[CRON] Saving cron status to KV...');
  await env.ARTICLES_KV.put('cron_status', JSON.stringify(status));
  console.log('[CRON] Cron complete');

  return status;
}
