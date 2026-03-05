/**
 * fix-components.js — Fixes all 17 site components.js files:
 * 1. Removes filter:brightness(0) invert(1) from logos
 * 2. Fixes font sizes (nav links, preloader text, footer text)
 * 3. Replaces footer placeholder with proper logo.png + grid layout
 * 4. Uses logo.png instead of logo-header.png
 * 
 * Run: node fix-components.js
 */
const fs = require('fs');
const path = require('path');

const SITES = [
    { num: 1,  slug: 'puntoclave',        name: 'PuntoClave' },
    { num: 2,  slug: 'diarioexpress',      name: 'DiarioExpress' },
    { num: 3,  slug: 'enfoquedirecto',     name: 'EnfoqueDirecto' },
    { num: 4,  slug: 'noticiashorizonte',  name: 'NoticiasHorizonte' },
    { num: 5,  slug: 'mexico360noticias',  name: 'México360Noticias' },
    { num: 6,  slug: 'capitalpress',       name: 'CapitalPress' },
    { num: 7,  slug: 'boominformativo',    name: 'BoomInformativo' },
    { num: 8,  slug: 'puntonoticias',      name: 'PuntoNoticias' },
    { num: 9,  slug: 'reportediario',      name: 'ReporteDiario' },
    { num: 10, slug: 'pulsodiario',        name: 'PulsoDiario' },
    { num: 11, slug: 'radarinformativo',   name: 'RadarInformativo' },
    { num: 12, slug: 'formulacdmx',        name: 'FormulaCDMX' },
    { num: 13, slug: 'enfoquecapital',     name: 'EnfoqueCapital' },
    { num: 14, slug: 'mexicantimes',       name: 'MexicanTimes' },
    { num: 15, slug: 'elpulsomexicano',    name: 'ElPulsoMexicano' },
    { num: 16, slug: 'mradio',             name: 'MRadio' },
    { num: 17, slug: 'televisionabc',      name: 'TelevisiónABC' },
];

// Read existing components.js to extract the colors used
function extractColors(content) {
    var hdrBgMatch = content.match(/background:([^;]+);border-bottom:3px solid ([^;]+);/);
    var hdrBg = hdrBgMatch ? hdrBgMatch[1].trim() : '#111';
    var pri = hdrBgMatch ? hdrBgMatch[2].trim() : '#1a73e8';
    return { hdrBg, pri };
}

function genComponentsFixed(site, hdrBg, pri) {
    var n = site.name;
    var lines = [];
    lines.push('(function(){');
    lines.push('    var p=window.location.pathname;');
    lines.push('    var isSubdir=/\\/(categoria|articulo|admin)\\//.test(p);');
    lines.push('    var base=isSubdir?"../":"./";');
    lines.push('');
    lines.push('    // PRELOADER');
    lines.push('    var PRE=\'<div class="site-preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;background:' + hdrBg + ';display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:99999;gap:20px;transition:opacity 0.6s;">\'+');
    lines.push('        \'<img src="\'+base+\'logo.png" alt="' + n + '" style="height:80px;width:auto;object-fit:contain;">\'+');
    lines.push('        \'<p style="font-family:sans-serif;color:rgba(255,255,255,0.7);font-size:1rem;letter-spacing:2px;text-transform:uppercase;">' + n + '</p></div>\';');
    lines.push('');
    lines.push('    // HEADER');
    lines.push('    var HDR=\'<header class="injected-header" style="background:' + hdrBg + ';border-bottom:3px solid ' + pri + ';position:sticky;top:0;z-index:1000;box-shadow:0 4px 20px rgba(0,0,0,0.3);">\'+');
    lines.push('        \'<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 24px;max-width:1400px;margin:0 auto;">\'+');
    lines.push('        \'<a href="\'+base+\'index.html" style="display:flex;align-items:center;"><img src="\'+base+\'logo.png" alt="' + n + '" style="height:48px;width:auto;object-fit:contain;"></a>\'+');
    lines.push('        \'<nav style="display:flex;flex-wrap:wrap;gap:0;">\'+');
    lines.push('        \'<a href="\'+base+\'categoria/nacional.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;transition:opacity 0.3s;">Nacional</a>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/politica.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;transition:opacity 0.3s;">Política</a>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/economia.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;transition:opacity 0.3s;">Economía</a>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/deportes.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;transition:opacity 0.3s;">Deportes</a>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/cultura.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;transition:opacity 0.3s;">Cultura</a>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/tecnologia.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;transition:opacity 0.3s;">Tecnología</a>\'+');
    lines.push('        \'</nav></div></header>\';');
    lines.push('');
    lines.push('    // FOOTER with logo.png');
    lines.push('    var FTR=\'<footer style="background:' + hdrBg + ';color:rgba(255,255,255,0.6);padding:50px 24px 30px;margin-top:60px;">\'+');
    lines.push('        \'<div style="max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:40px;align-items:start;">\'+');
    lines.push('');
    lines.push('        \'<div style="display:flex;flex-direction:column;gap:12px;">\'+');
    lines.push('        \'<img src="\'+base+\'logo.png" alt="' + n + '" style="height:50px;width:auto;object-fit:contain;margin-bottom:8px;">\'+');
    lines.push('        \'<p style="font-size:0.95rem;line-height:1.5;max-width:280px;">Noticias digitales en tiempo real. Información verificada las 24 horas.</p>\'+');
    lines.push('        \'</div>\'+');
    lines.push('');
    lines.push('        \'<div style="display:flex;flex-direction:column;gap:10px;">\'+');
    lines.push('        \'<h4 style="color:#fff;margin-bottom:5px;font-family:sans-serif;font-size:1rem;">Secciones</h4>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/nacional.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Nacional</a>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/politica.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Política</a>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/economia.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Economía</a>\'+');
    lines.push('        \'<a href="\'+base+\'categoria/deportes.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Deportes</a>\'+');
    lines.push('        \'</div>\'+');
    lines.push('');
    lines.push('        \'<div style="display:flex;flex-direction:column;gap:10px;">\'+');
    lines.push('        \'<h4 style="color:#fff;margin-bottom:5px;font-family:sans-serif;font-size:1rem;">Legal</h4>\'+');
    lines.push('        \'<a href="\'+base+\'acerca-de.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Acerca de</a>\'+');
    lines.push('        \'<a href="\'+base+\'privacidad.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Privacidad</a>\'+');
    lines.push('        \'<a href="\'+base+\'terminos.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Términos</a>\'+');
    lines.push('        \'<a href="\'+base+\'contacto.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Contacto</a>\'+');
    lines.push('        \'</div>\'+');
    lines.push('');
    lines.push('        \'</div>\'+');
    lines.push('        \'<div style="border-top:1px solid rgba(255,255,255,0.1);margin-top:40px;padding-top:20px;text-align:center;font-size:0.9rem;max-width:1400px;margin-left:auto;margin-right:auto;">© 2026 ' + n + '. Todos los derechos reservados.</div>\'+');
    lines.push('        \'</footer>\';');
    lines.push('');
    lines.push('    function init(){');
    lines.push('        var pre=document.getElementById("site-preloader");if(pre)pre.outerHTML=PRE;');
    lines.push('        var hdr=document.getElementById("site-header");if(hdr)hdr.outerHTML=HDR;');
    lines.push('        var ftr=document.getElementById("site-footer");if(ftr)ftr.outerHTML=FTR;');
    lines.push('        setTimeout(function(){');
    lines.push('            var p=document.querySelector(".site-preloader");');
    lines.push('            if(p){p.style.opacity="0";setTimeout(function(){p.style.display="none";},600);}');
    lines.push('        },800);');
    lines.push('        document.querySelectorAll("img").forEach(function(i){');
    lines.push('            i.addEventListener("error",function(){this.src=base+"logo.png";});');
    lines.push('        });');
    lines.push('    }');
    lines.push('');
    lines.push('    if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);');
    lines.push('    else init();');
    lines.push('})();');
    return lines.join('\n');
}

// Main
var sitesDir = path.join(__dirname, 'sites');
var fixed = 0;

SITES.forEach(function(site) {
    var compPath = path.join(sitesDir, site.slug, 'components.js');
    if (!fs.existsSync(compPath)) {
        console.log('SKIP: ' + compPath + ' not found');
        return;
    }
    
    var content = fs.readFileSync(compPath, 'utf8');
    var colors = extractColors(content);
    
    var newContent = genComponentsFixed(site, colors.hdrBg, colors.pri);
    fs.writeFileSync(compPath, newContent, 'utf8');
    
    console.log('[✓] ' + site.slug + ' — bg:' + colors.hdrBg + ' pri:' + colors.pri);
    fixed++;
});

console.log('\nFixed ' + fixed + '/17 components.js files');
console.log('Changes: removed logo filters, fixed font sizes, added logo.png to footer');
