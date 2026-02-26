// serve-local.js - Servidor local para probar sitios con proxy a la API del worker
// Uso: node serve-local.js <nombre-sitio> [puerto]
// Ejemplo: node serve-local.js bitacoraurbana 8888

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const url = require('url');

const WORKER_URL = 'https://news-api.sebastianvernis.workers.dev';

const siteName = process.argv[2] || 'bitacoraurbana';
const port = parseInt(process.argv[3] || '8888');
const siteDir = path.join(__dirname, 'sites', siteName);

if (!fs.existsSync(siteDir)) {
  console.error(`❌ Sitio no encontrado: ${siteDir}`);
  console.error(`Sitios disponibles: bitacoraurbana, cbnnoticias, centralmexico, mexicoinformado, nodoinformativo, noticiasobjetivo, radiocinconoticias, reportecentralmx, tvmexico, verticenoticias`);
  process.exit(1);
}

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif':  'image/gif',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.woff': 'font/woff',
  '.woff2':'font/woff2',
  '.ttf':  'font/ttf',
};

function proxyToWorker(req, res) {
  const workerPath = req.url; // e.g. /api/articles?site=bitacoraurbana&limit=12
  const workerFullUrl = WORKER_URL + workerPath;
  console.log(`  → PROXY: ${workerFullUrl}`);

  const parsed = url.parse(workerFullUrl);
  const options = {
    hostname: parsed.hostname,
    port: 443,
    path: parsed.path,
    method: req.method,
    headers: { 'Accept': 'application/json' }
  };

  const proxyReq = https.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode, {
      'Content-Type': proxyRes.headers['content-type'] || 'application/json',
      'Access-Control-Allow-Origin': '*',
    });
    proxyRes.pipe(res);
  });

  proxyReq.on('error', (e) => {
    console.error('Proxy error:', e.message);
    res.writeHead(502);
    res.end(JSON.stringify({ error: 'Proxy error: ' + e.message }));
  });

  proxyReq.end();
}

function serveFile(req, res) {
  let filePath = req.url.split('?')[0]; // strip query string
  if (filePath === '/' || filePath === '') filePath = '/index.html';

  const fullPath = path.join(siteDir, filePath);

  // Security: prevent directory traversal
  if (!fullPath.startsWith(siteDir)) {
    res.writeHead(403); res.end('Forbidden'); return;
  }

  // Try exact path, then with .html, then index.html in directory
  let resolvedPath = fullPath;
  if (!fs.existsSync(resolvedPath)) {
    if (fs.existsSync(resolvedPath + '.html')) {
      resolvedPath = resolvedPath + '.html';
    } else if (fs.existsSync(path.join(resolvedPath, 'index.html'))) {
      resolvedPath = path.join(resolvedPath, 'index.html');
    } else {
      res.writeHead(404); res.end('404 Not Found: ' + filePath); return;
    }
  }

  const ext = path.extname(resolvedPath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  fs.readFile(resolvedPath, (err, data) => {
    if (err) { res.writeHead(500); res.end('Error reading file'); return; }
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const reqUrl = req.url || '/';
  console.log(`${req.method} ${reqUrl}`);

  // Proxy /api/* to worker
  if (reqUrl.startsWith('/api/')) {
    proxyToWorker(req, res);
  } else {
    serveFile(req, res);
  }
});

server.listen(port, () => {
  console.log(`\n✅ Servidor local corriendo en http://localhost:${port}`);
  console.log(`📰 Sitio: ${siteName} (${siteDir})`);
  console.log(`🔗 API proxy → ${WORKER_URL}`);
  console.log(`\nPresiona Ctrl+C para detener.\n`);
});
