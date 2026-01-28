/**
 * Cloudflare Workers Backend - News Generator API
 * 
 * Este worker maneja:
 * - Endpoints REST para generación de sitios
 * - Procesamiento asíncrono con Queues
 * - Almacenamiento en R2
 * - Metadata en D1
 */

import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { prettyJSON } from 'hono/pretty-json';

// Types
type Bindings = {
  AI: any;
  SITES_BUCKET: R2Bucket;
  IMAGES_BUCKET: R2Bucket;
  DB: D1Database;
  CACHE: KVNamespace;
  SITE_GENERATION_QUEUE: Queue;
  ASSETS: Fetcher;
  BLACKBOX_API_KEY: string;
  NEWSAPI_KEY: string;
  CLOUDFLARE_API_TOKEN: string;
  ENVIRONMENT: string;
};

type Variables = {
  user?: string;
};

// Initialize Hono app
const app = new Hono<{ Bindings: Bindings; Variables: Variables }>();

// Middleware
app.use('*', logger());
app.use('*', prettyJSON());
app.use('*', cors({
  origin: ['http://localhost:5173', 'https://news-generator-admin.pages.dev'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization'],
  exposeHeaders: ['Content-Length'],
  maxAge: 600,
  credentials: true,
}));

// Health check
app.get('/api/health', (c) => {
  return c.json({
    status: 'healthy',
    version: '2.0.0',
    environment: c.env.ENVIRONMENT,
    timestamp: new Date().toISOString(),
  });
});

// Get sites list
app.get('/api/sites', async (c) => {
  try {
    // Query D1 for sites metadata
    const { results } = await c.env.DB.prepare(
      'SELECT * FROM sites ORDER BY created_at DESC LIMIT 100'
    ).all();

    return c.json({
      success: true,
      sites: results,
      total: results.length,
    });
  } catch (error) {
    return c.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    }, 500);
  }
});

// Get site stats
app.get('/api/sites/stats', async (c) => {
  try {
    const { results: totalResults } = await c.env.DB.prepare(
      'SELECT COUNT(*) as total FROM sites'
    ).all();
    
    const { results: recentResults } = await c.env.DB.prepare(
      'SELECT COUNT(*) as recent FROM sites WHERE created_at > datetime("now", "-24 hours")'
    ).all();

    const total = (totalResults[0] as any)?.total || 0;
    const recent = (recentResults[0] as any)?.recent || 0;

    return c.json({
      success: true,
      stats: {
        totalSites: total,
        recentSites: recent,
        totalArticles: total * 15,
      },
    });
  } catch (error) {
    return c.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    }, 500);
  }
});

// Generate sites (async)
app.post('/api/sites/generate', async (c) => {
  try {
    const body = await c.req.json();
    const { quantity = 5, verifyDomains = false } = body;

    // Validate input
    if (quantity < 1 || quantity > 10) {
      return c.json({
        success: false,
        error: 'Quantity must be between 1 and 10',
      }, 400);
    }

    // Create job
    const jobId = crypto.randomUUID();
    const job = {
      jobId,
      quantity,
      verifyDomains,
      status: 'queued',
      createdAt: new Date().toISOString(),
    };

    // Save job to DB
    await c.env.DB.prepare(
      'INSERT INTO jobs (id, status, params, created_at) VALUES (?, ?, ?, ?)'
    ).bind(
      jobId,
      'queued',
      JSON.stringify({ quantity, verifyDomains }),
      new Date().toISOString()
    ).run();

    // Send to queue
    await c.env.SITE_GENERATION_QUEUE.send(job);

    return c.json({
      success: true,
      jobId,
      status: 'queued',
      message: 'Site generation job queued. Use /api/jobs/:jobId to check status.',
    });
  } catch (error) {
    return c.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    }, 500);
  }
});

// Get job status
app.get('/api/jobs/:jobId', async (c) => {
  try {
    const jobId = c.req.param('jobId');

    const { results } = await c.env.DB.prepare(
      'SELECT * FROM jobs WHERE id = ?'
    ).bind(jobId).all();

    if (results.length === 0) {
      return c.json({
        success: false,
        error: 'Job not found',
      }, 404);
    }

    const job = results[0];

    return c.json({
      success: true,
      job: {
        id: job.id,
        status: job.status,
        params: JSON.parse(job.params as string),
        createdAt: job.created_at,
        updatedAt: job.updated_at,
        result: job.result ? JSON.parse(job.result as string) : null,
      },
    });
  } catch (error) {
    return c.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    }, 500);
  }
});

// Delete site
app.delete('/api/sites/:siteId', async (c) => {
  try {
    const siteId = c.req.param('siteId');

    // Delete from DB
    await c.env.DB.prepare('DELETE FROM sites WHERE id = ?').bind(siteId).run();

    // Delete from R2 (TODO: implement cleanup)

    return c.json({
      success: true,
      message: `Site ${siteId} deleted`,
    });
  } catch (error) {
    return c.json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    }, 500);
  }
});

// Queue consumer (procesamiento asíncrono)
async function handleQueue(batch: MessageBatch, env: Bindings): Promise<void> {
  for (const message of batch.messages) {
    try {
      const job = message.body as any;
      const { jobId, quantity, verifyDomains } = job;

      // Update status to processing
      await env.DB.prepare(
        'UPDATE jobs SET status = ?, updated_at = ? WHERE id = ?'
      ).bind('processing', new Date().toISOString(), jobId).run();

      // TODO: Implementar lógica de generación
      // Por ahora, solo simulamos
      await new Promise(resolve => setTimeout(resolve, 5000));

      // Resultado simulado
      const result = {
        sitesGenerated: quantity,
        executionTime: '5s',
      };

      // Update status to completed
      await env.DB.prepare(
        'UPDATE jobs SET status = ?, result = ?, updated_at = ? WHERE id = ?'
      ).bind(
        'completed',
        JSON.stringify(result),
        new Date().toISOString(),
        jobId
      ).run();

      message.ack();
    } catch (error) {
      console.error('Error processing job:', error);
      message.retry();
    }
  }
}

// Export
export default {
  fetch: app.fetch,
  queue: handleQueue,
};
