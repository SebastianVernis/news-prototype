// src/routes/cron.js — Rutas de control y monitoreo del cron job

import { Hono } from 'hono';
import { checkAuth } from '../middleware/auth.js';
import { runMasterCron } from '../cron/master.js';

const cron = new Hono();

// ── GET /cron/status — Estado del último cron ejecutado ──────
cron.get('/status', async (c) => {
  const s    = await c.env.ARTICLES_KV.get('cron_status');
  const data = s ? JSON.parse(s) : { lastRun: 'Never' };

  if (data.lastRun !== 'Never') {
    const lastTs = new Date(data.lastRun).getTime();
    const nextTs = lastTs + 30 * 60 * 1000;
    const diff   = Math.max(0, nextTs - Date.now());
    data.nextRunInMinutes = Math.floor(diff / 60000);
    data.nextRunInSeconds = Math.floor((diff % 60000) / 1000);
  }

  // Interpretar estados de tareas para evitar falsos errores
  if (data.tasks) {
    const taskStatus = {};
    for (const [key, value] of Object.entries(data.tasks)) {
      if (key.startsWith('fb_') && value && value.includes('pending')) {
        taskStatus[key] = { status: 'pending',  message: value, isError: false };
      } else if (key.startsWith('fb_') && value && value.startsWith('OK')) {
        taskStatus[key] = { status: 'success',  message: value, isError: false };
      } else if (key.startsWith('fb_') && value && (value.startsWith('Error') || value.startsWith('No published'))) {
        taskStatus[key] = { status: 'issue',    message: value, isError: false };
      } else if (key.startsWith('fb_') && value && value.includes('No eligible')) {
        taskStatus[key] = { status: 'idle',     message: value, isError: false };
      } else {
        const isError = value && value.startsWith('Error');
        taskStatus[key] = { status: isError ? 'error' : 'ok', message: value, isError };
      }
    }
    data.taskDetails = taskStatus;
  }

  return c.json(data);
});

// ── GET /cron/manual — Ejecutar cron manualmente ─────────────
cron.get('/manual', async (c) => {
  try {
    await runMasterCron(c.env);
  } catch (e) {
    console.error('Cron manual error:', e.message);
    return c.json({ error: e.message }, 500);
  }
  const s = await c.env.ARTICLES_KV.get('cron_status');
  return c.json(s ? JSON.parse(s) : { message: 'Cron executed' });
});

// ── POST /cron/ingest — Información sobre ingesta RSS ────────
cron.post('/ingest', async (c) => {
  if (!await checkAuth(c)) return c.json({ error: '401' }, 401);
  try {
    return c.json({
      success: true,
      message: 'RSS ingestion runs automatically every 30 minutes via scheduled trigger',
      note:    'Manual ingestion is not required - articles are ingested automatically',
    });
  } catch (e) {
    return c.json({ success: false, error: e.message }, 500);
  }
});

export default cron;
