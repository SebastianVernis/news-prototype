// Routes additional que se montan en index.js
// Estas funciones ya están importadas en index.js principal

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/api/cron/manual') { await runMasterCron(env); return new Response("OK"); }
    if (url.pathname.startsWith('/api')) return app.fetch(request, env, ctx);
    const res = await fetch(request);
    return injectMetaTags(request, env, res);
  },
  async scheduled(event, env, ctx) { ctx.waitUntil(runMasterCron(env)); }
};
