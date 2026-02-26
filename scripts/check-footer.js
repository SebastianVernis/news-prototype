const fs = require('fs');
const c = fs.readFileSync('sites/cbnnoticias/components.js', 'utf8');
const idx = c.indexOf('Secciones');
const snippet = c.slice(idx - 50, idx + 350);
fs.writeFileSync('scripts/footer-debug.txt', snippet, 'utf8');
console.log('Written to scripts/footer-debug.txt');
