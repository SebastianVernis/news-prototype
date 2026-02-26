const fs = require('fs');

const sites = [
  'bitacoraurbana',
  'cbnnoticias',
  'centralmexico',
  'mexicoinformado',
  'nodoinformativo',
  'noticiasobjetivo',
  'radiocinconoticias',
  'reportecentralmx',
  'tvmexico',
  'verticenoticias'
];

let updated = 0;

for (const site of sites) {
  const filePath = `sites/${site}/components.js`;
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;

  // 1. Reduce footer padding (if not already done)
  if (!content.includes('<footer class="footer" style="padding:24px 0 12px;">')) {
    content = content.replace(
      '<footer class="footer">',
      '<footer class="footer" style="padding:24px 0 12px;">'
    );
  }

  // 2. Reduce footer-grid gap (if not already done)
  if (!content.includes('<div class="footer-grid cols-3" style="gap:16px;">')) {
    content = content.replace(
      '<div class="footer-grid cols-3">',
      '<div class="footer-grid cols-3" style="gap:16px;">'
    );
  }

  // 3. Make Secciones ul 2-column grid — use regex to handle \r\n or \n
  content = content.replace(
    /(<h4[^>]*>Secciones<\/h4>[\r\n\s]+)<ul class="footer-links">/,
    '<h4 style="margin-bottom:8px;font-size:0.85rem;">Secciones</h4>\n                <ul class="footer-links" style="display:grid;grid-template-columns:1fr 1fr;gap:3px 12px;">'
  );

  // 4. Reduce footer-bottom padding (if not already done)
  if (!content.includes('<div class="footer-bottom" style="padding-top:10px;margin-top:0;">')) {
    content = content.replace(
      '<div class="footer-bottom">',
      '<div class="footer-bottom" style="padding-top:10px;margin-top:0;">'
    );
  }

  // 5. Reduce footer-about font size (if not already done)
  if (!content.includes('<p class="footer-about" style=')) {
    content = content.replace(
      '<p class="footer-about">',
      '<p class="footer-about" style="font-size:0.82rem;line-height:1.5;margin:8px 0 10px;">'
    );
  }

  // 6. Reduce Información h4 size (if not already done)
  if (!content.includes('<h4 style="margin-bottom:8px;font-size:0.85rem;">Información</h4>')) {
    content = content.replace(
      '<h4>Información</h4>',
      '<h4 style="margin-bottom:8px;font-size:0.85rem;">Información</h4>'
    );
  }

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated: ${filePath}`);
    updated++;
  } else {
    console.log(`No changes: ${filePath}`);
  }
}

console.log(`\nDone! Updated ${updated}/${sites.length} files.`);
