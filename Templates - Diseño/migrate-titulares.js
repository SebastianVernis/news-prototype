/**
 * migrate-titulares.js
 * Automates the integration of 17 Titulares templates into the sites/ ecosystem.
 * Run: node migrate-titulares.js
 */

const fs = require('fs');
const path = require('path');

const { SITES, TITULARES_DIR, SITES_DIR, METADATA_DIR, CATEGORIES } = require('./migrate/config');
const { mkdirSafe, writeF, copyF, extractStyle, extractVars, getColors, getBodyFont } = require('./migrate/helpers');
const genStyleCSS = require('./migrate/gen-style-css');
const genStyleCustomCSS = require('./migrate/gen-style-custom');
const { genIndexHTML, genArticuloHTML, genCategoriaHTML } = require('./migrate/gen-html');
const genLegalPage = require('./migrate/gen-legal');
const genComponentsJS = require('./migrate/gen-components');
const { genScriptJS, genRedirects, genWranglerToml, genLegalCSS, genArticleCSS, genMetadataJSON } = require('./migrate/gen-misc');

console.log('=== Migracion de Titulares ===\n');
console.log('Sitios a migrar: ' + SITES.length);

var errors = [];
var success = 0;

SITES.forEach(function(site) {
    try {
        console.log('\n--- [' + site.num + '] ' + site.name + ' (' + site.slug + ') ---');

        // 1. Read source HTML
        var srcHTML = path.join(TITULARES_DIR, String(site.num), 'index.html');
        if (!fs.existsSync(srcHTML)) {
            throw new Error('No se encontro ' + srcHTML);
        }
        var html = fs.readFileSync(srcHTML, 'utf8');

        // 2. Extract CSS
        var origCSS = extractStyle(html);
        var vars = extractVars(origCSS);
        var colors = getColors(vars);
        var bodyFont = getBodyFont(origCSS);

        console.log('  Colors: primary=' + colors.primary + ' secondary=' + colors.secondary + ' accent=' + colors.accent);

        // 3. Create site directory
        var siteDir = path.join(SITES_DIR, site.slug);
        mkdirSafe(siteDir);
        mkdirSafe(path.join(siteDir, 'articulo'));
        mkdirSafe(path.join(siteDir, 'categoria'));
        mkdirSafe(path.join(siteDir, 'admin'));
        mkdirSafe(path.join(siteDir, 'assets', 'images'));
        mkdirSafe(path.join(siteDir, 'functions'));

        // 4. Copy logo
        var logoSrc = path.join(TITULARES_DIR, String(site.num), 'logo.png');
        copyF(logoSrc, path.join(siteDir, 'logo.png'));
        copyF(logoSrc, path.join(siteDir, 'logo-header.png'));
        console.log('  Logo copiado');

        // 5. Generate style.css
        writeF(path.join(siteDir, 'style.css'), genStyleCSS(site, vars, colors, bodyFont));
        console.log('  style.css generado');

        // 6. Generate style-custom.css
        writeF(path.join(siteDir, 'style-custom.css'), genStyleCustomCSS(site, origCSS, colors));
        console.log('  style-custom.css generado');

        // 7. Generate index.html
        writeF(path.join(siteDir, 'index.html'), genIndexHTML(site));
        console.log('  index.html generado');

        // 8. Generate components.js
        writeF(path.join(siteDir, 'components.js'), genComponentsJS(site, colors));
        console.log('  components.js generado');

        // 9. Generate script.js
        writeF(path.join(siteDir, 'script.js'), genScriptJS());
        console.log('  script.js generado');

        // 10. Generate _redirects
        writeF(path.join(siteDir, '_redirects'), genRedirects(site.slug));
        console.log('  _redirects generado');

        // 11. Generate wrangler.toml
        writeF(path.join(siteDir, 'wrangler.toml'), genWranglerToml(site.slug));
        console.log('  wrangler.toml generado');

        // 12. Generate legal.css and article.css
        writeF(path.join(siteDir, 'legal.css'), genLegalCSS());
        writeF(path.join(siteDir, 'article.css'), genArticleCSS());
        console.log('  legal.css + article.css generados');

        // 13. Generate legal pages
        ['acerca-de', 'contacto', 'privacidad', 'terminos'].forEach(function(type) {
            writeF(path.join(siteDir, type + '.html'), genLegalPage(site, type));
        });
        console.log('  Paginas legales generadas');

        // 14. Generate articulo/index.html
        writeF(path.join(siteDir, 'articulo', 'index.html'), genArticuloHTML(site));
        console.log('  articulo/index.html generado');

        // 15. Generate categoria/*.html
        CATEGORIES.forEach(function(cat) {
            writeF(path.join(siteDir, 'categoria', cat + '.html'), genCategoriaHTML(site, cat));
        });
        console.log('  Paginas de categoria generadas (' + CATEGORIES.length + ')');

        // 16. Generate metadata JSON
        writeF(path.join(METADATA_DIR, site.slug + '.json'), genMetadataJSON(site, colors));
        console.log('  Metadata JSON generado');

        success++;
    } catch(e) {
        console.error('  ERROR: ' + e.message);
        errors.push({ site: site.slug, error: e.message });
    }
});

// CLEANUP: Remove wrong titular* files
console.log('\n=== Limpieza ===');

// Remove wrong metadata files
for (var i = 1; i <= 17; i++) {
    var wrongMeta = path.join(METADATA_DIR, 'titular' + i + '.json');
    if (fs.existsSync(wrongMeta)) {
        fs.unlinkSync(wrongMeta);
        console.log('  Eliminado: ' + wrongMeta);
    }
}

// Remove wrong sites/titular1 directory
var wrongDir = path.join(SITES_DIR, 'titular1');
if (fs.existsSync(wrongDir)) {
    fs.rmSync(wrongDir, { recursive: true, force: true });
    console.log('  Eliminado: ' + wrongDir);
}

// SUMMARY
console.log('\n=== Resumen ===');
console.log('Sitios migrados exitosamente: ' + success + '/' + SITES.length);
if (errors.length > 0) {
    console.log('Errores:');
    errors.forEach(function(e) { console.log('  - ' + e.site + ': ' + e.error); });
}
console.log('\nMigracion completada.');
