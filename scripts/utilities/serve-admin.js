// Servidor simple para public/admin/ con soporte de query params
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 4001;
const ROOT = path.join(__dirname, 'public', 'admin');

const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.ico': 'image/x-icon',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
};

http.createServer((req, res) => {
  // Ignorar query string para resolver el archivo
  const urlPath = req.url.split('?')[0].split('#')[0];
  let filePath = path.join(ROOT, urlPath === '/' ? 'index.html' : urlPath);

  // Si no tiene extensión, servir index.html (SPA fallback)
  if (!path.extname(filePath)) {
    filePath = path.join(ROOT, 'index.html');
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      // Fallback a index.html para rutas SPA
      fs.readFile(path.join(ROOT, 'index.html'), (err2, data2) => {
        if (err2) {
          res.writeHead(404);
          res.end('Not found');
        } else {
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(data2);
        }
      });
    } else {
      const ext = path.extname(filePath);
      res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
      res.end(data);
    }
  });
}).listen(PORT, () => {
  console.log(`Admin CMS server running at http://localhost:${PORT}`);
  console.log(`Set token: http://localhost:${PORT}/?token=TOKEN_HERE#cms`);
});
