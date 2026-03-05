/**
 * migrate-v2/run.js — Main orchestrator
 * Preserves original Titulares layouts, only adds API integration
 * Run: node migrate-v2/run.js
 */
var fs = require('fs');
var path = require('path');

var { SITES, CATS } = require('./config');
var { mkdirp, write, copy, extractStyle, extractMain, extractVars, getColors } = require('./helpers');
var genIndex = require('./gen-index');
var genComponents = require('./gen-components');
var { genLegal, genArticulo, genCategoria } = require('./gen-pages');
var { genScriptJS, genRedirects, genWrangler, genMetadata } = require('./gen-misc');

var BASE_DIR = path.join(__dirname, '..');
var TITULARES = path.join(BASE_DIR, 'Titulares');
var SITES_DIR = path.join(BASE_DIR, 'sites');
var META_DIR  = path.join(BASE_DIR, 'data', 'sites_metadata');

console.log('=== MIGRATE V2: Preserving Original Layouts ===\n');

// Shared script.js content (same for all sites)
var SCRIPT_JS = genScriptJS();

var processed = 0;
var errors = [];

SITES.forEach(function(site) {
    var num = site.num;
    var slug = site.slug;
    var name = site.name;
    var srcDir = path.join(TITULARES, String(num));
    var dstDir = path.join(SITES_DIR, slug);

    console.log('[' + num + '/17] Processing ' + name + ' (' + slug + ')...');

    // 1. Read original HTML
    var srcHTML = path.join(srcDir, 'index.html');
    if (!fs.existsSync(srcHTML)) {
        console.log('    ERROR: ' + srcHTML + ' not found!');
        errors.push(slug);
        return;
    }
    var html = fs.readFileSync(srcHTML, 'utf8');

    // 2. Extract CSS and main content from original
    var origCSS = extractStyle(html);
    var mainHTML = extractMain(html);

    // 3. Extract color variables for components/metadata
    var vars = extractVars(origCSS);
    var colors = getColors(vars);

    console.log('    CSS: ' + origCSS.length + ' chars, Main: ' + mainHTML.length + ' chars');
    console.log('    Colors: primary=' + colors.primary + ' bg=' + colors.bg + ' text=' + colors.text);

    // 4. Create directory structure
    mkdirp(dstDir);
    mkdirp(path.join(dstDir, 'admin'));
    mkdirp(path.join(dstDir, 'articulo'));
    mkdirp(path.join(dstDir, 'categoria'));
    mkdirp(path.join(dstDir, 'assets'));
    mkdirp(path.join(dstDir, 'functions'));

    // 5. Write style-custom.css (ORIGINAL CSS preserved as-is)
    write(path.join(dstDir, 'style-custom.css'), '/* ' + name + ' - Original Theme CSS */\n' + origCSS);
    console.log('    ✓ style-custom.css (original CSS preserved)');

    // 6. Write index.html (original layout + API integration)
    write(path.join(dstDir, 'index.html'), genIndex(site, mainHTML));
    console.log('    ✓ index.html (original layout + API)');

    // 7. Write components.js (header/footer/preloader injection)
    write(path.join(dstDir, 'components.js'), genComponents(site, colors));
    console.log('    ✓ components.js');

    // 8. Write script.js
    write(path.join(dstDir, 'script.js'), SCRIPT_JS);
    console.log('    ✓ script.js');

    // 9. Write _redirects
    write(path.join(dstDir, '_redirects'), genRedirects(slug));
    console.log('    ✓ _redirects');

    // 10. Write wrangler.toml
    write(path.join(dstDir, 'wrangler.toml'), genWrangler(slug));
    console.log('    ✓ wrangler.toml');

    // 11. Copy logo files
    var logoSrc = path.join(srcDir, 'logo.png');
    copy(logoSrc, path.join(dstDir, 'logo.png'));
    copy(logoSrc, path.join(dstDir, 'logo-header.png'));
    console.log('    ✓ logo.png + logo-header.png');

    // 12. Write legal pages
    ['acerca-de', 'contacto', 'privacidad', 'terminos'].forEach(function(type) {
        write(path.join(dstDir, type + '.html'), genLegal(site, type));
    });
    console.log('    ✓ Legal pages (4)');

    // 13. Write articulo/index.html
    write(path.join(dstDir, 'articulo', 'index.html'), genArticulo(site));
    console.log('    ✓ articulo/index.html');

    // 14. Write categoria pages
    CATS.forEach(function(cat) {
        write(path.join(dstDir, 'categoria', cat + '.html'), genCategoria(site, cat));
    });
    console.log('    ✓ Categoria pages (' + CATS.length + ')');

    // 15. Write metadata JSON
    mkdirp(META_DIR);
    write(path.join(META_DIR, slug + '.json'), genMetadata(site, colors));
    console.log('    ✓ metadata JSON');

    // 16. Write admin placeholder
    write(path.join(dstDir, 'admin', 'index.html'), '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Admin - ' + name + '</title></head><body><h1>Admin Panel - ' + name + '</h1><p>Panel de administración en desarrollo.</p></body></html>');

    // 17. Write functions placeholder
    write(path.join(dstDir, 'functions', 'api.js'), '// API functions placeholder for ' + slug + '\n');

    processed++;
    console.log('    ✓ DONE\n');
});

// ── CLEANUP: Remove old wrong files ──
console.log('=== CLEANUP ===');

// Remove old titular*.json files
for (var i = 1; i <= 17; i++) {
    var oldMeta = path.join(META_DIR, 'titular' + i + '.json');
    if (fs.existsSync(oldMeta)) {
        fs.unlinkSync(oldMeta);
        console.log('  Removed: ' + oldMeta);
    }
}

// Remove old sites/titular1 directory
var oldDir = path.join(SITES_DIR, 'titular1');
if (fs.existsSync(oldDir)) {
    fs.rmSync(oldDir, { recursive: true, force: true });
    console.log('  Removed: sites/titular1/');
}

console.log('\n=== SUMMARY ===');
console.log('Processed: ' + processed + '/17 sites');
if (errors.length) console.log('Errors: ' + errors.join(', '));
else console.log('All sites migrated successfully!');
console.log('\nEach site preserves its ORIGINAL Titulares layout and CSS.');
console.log('API integration added to populate content dynamically.');
