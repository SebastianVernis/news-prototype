const fs = require('fs');
const path = require('path');

// Exact colors extracted from existing components.js files
const SITES = [
    // puntoclave already fixed
    { slug: 'diarioexpress',     name: 'DiarioExpress',      bg: '#1A1A1A', pri: '#FF4F00' },
    { slug: 'enfoquedirecto',    name: 'EnfoqueDirecto',     bg: '#0a0a0a', pri: '#c5a059' },
    { slug: 'noticiashorizonte', name: 'NoticiasHorizonte',  bg: '#111111', pri: '#E07A5F' },
    { slug: 'mexico360noticias', name: 'México360Noticias',  bg: '#1F2937', pri: '#DC2626' },
    { slug: 'capitalpress',      name: 'CapitalPress',       bg: '#2C2C2C', pri: '#A89F91' },
    { slug: 'boominformativo',   name: 'BoomInformativo',    bg: '#0A192F', pri: '#FF007F' },
    { slug: 'puntonoticias',     name: 'PuntoNoticias',      bg: '#111827', pri: '#3B82F6' },
    { slug: 'reportediario',     name: 'ReporteDiario',      bg: '#111111', pri: '#800020' },
    { slug: 'pulsodiario',       name: 'PulsoDiario',        bg: '#1C1E21', pri: '#00FF66' },
    { slug: 'radarinformativo',  name: 'RadarInformativo',   bg: '#121212', pri: '#8B5CF6' },
    { slug: 'formulacdmx',       name: 'FormulaCDMX',        bg: '#0f172a', pri: '#38bdf8' },
    { slug: 'enfoquecapital',    name: 'EnfoqueCapital',     bg: '#1A3626', pri: '#C5A059' },
    { slug: 'mexicantimes',      name: 'MexicanTimes',       bg: '#1C1E21', pri: '#005FFF' },
    { slug: 'elpulsomexicano',   name: 'ElPulsoMexicano',    bg: '#111111', pri: '#FF00FF' },
    { slug: 'mradio',            name: 'MRadio',             bg: '#4A5568', pri: '#3182CE' },
    { slug: 'televisionabc',     name: 'TelevisiónABC',      bg: '#111111', pri: '#D4AF37' },
];

function gen(s) {
    return '(function(){\n' +
'    var p=window.location.pathname;\n' +
'    var isSubdir=/\\/(categoria|articulo|admin)\\//.test(p);\n' +
'    var base=isSubdir?"../":"./";\n' +
'\n' +
'    // PRELOADER\n' +
'    var PRE=\'<div class="site-preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;background:' + s.bg + ';display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:99999;gap:20px;transition:opacity 0.6s;">\'+\n' +
'        \'<img src="\'+base+\'logo.png" alt="' + s.name + '" style="height:80px;width:auto;object-fit:contain;">\'+\n' +
'        \'<p style="font-family:sans-serif;color:rgba(255,255,255,0.7);font-size:1rem;letter-spacing:2px;text-transform:uppercase;">' + s.name + '</p></div>\';\n' +
'\n' +
'    // HEADER\n' +
'    var HDR=\'<header class="injected-header" style="background:' + s.bg + ';border-bottom:3px solid ' + s.pri + ';position:sticky;top:0;z-index:1000;box-shadow:0 4px 20px rgba(0,0,0,0.3);">\'+\n' +
'        \'<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 24px;max-width:1400px;margin:0 auto;">\'+\n' +
'        \'<a href="\'+base+\'index.html" style="display:flex;align-items:center;"><img src="\'+base+\'logo.png" alt="' + s.name + '" style="height:48px;width:auto;object-fit:contain;"></a>\'+\n' +
'        \'<nav style="display:flex;flex-wrap:wrap;gap:0;">\'+\n' +
'        \'<a href="\'+base+\'categoria/nacional.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Nacional</a>\'+\n' +
'        \'<a href="\'+base+\'categoria/politica.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Política</a>\'+\n' +
'        \'<a href="\'+base+\'categoria/economia.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Economía</a>\'+\n' +
'        \'<a href="\'+base+\'categoria/deportes.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Deportes</a>\'+\n' +
'        \'<a href="\'+base+\'categoria/cultura.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Cultura</a>\'+\n' +
'        \'<a href="\'+base+\'categoria/tecnologia.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Tecnología</a>\'+\n' +
'        \'</nav></div></header>\';\n' +
'\n' +
'    // FOOTER with logo.png\n' +
'    var FTR=\'<footer style="background:' + s.bg + ';color:rgba(255,255,255,0.6);padding:50px 24px 30px;margin-top:60px;">\'+\n' +
'        \'<div style="max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:40px;align-items:start;">\'+\n' +
'        \'<div style="display:flex;flex-direction:column;gap:12px;">\'+\n' +
'        \'<img src="\'+base+\'logo.png" alt="' + s.name + '" style="height:50px;width:auto;object-fit:contain;margin-bottom:8px;">\'+\n' +
'        \'<p style="font-size:0.95rem;line-height:1.5;max-width:280px;">Noticias digitales en tiempo real. Información verificada las 24 horas.</p>\'+\n' +
'        \'</div>\'+\n' +
'        \'<div style="display:flex;flex-direction:column;gap:10px;">\'+\n' +
'        \'<h4 style="color:#fff;margin-bottom:5px;font-family:sans-serif;font-size:1rem;">Secciones</h4>\'+\n' +
'        \'<a href="\'+base+\'categoria/nacional.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Nacional</a>\'+\n' +
'        \'<a href="\'+base+\'categoria/politica.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Política</a>\'+\n' +
'        \'<a href="\'+base+\'categoria/economia.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Economía</a>\'+\n' +
'        \'<a href="\'+base+\'categoria/deportes.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Deportes</a>\'+\n' +
'        \'</div>\'+\n' +
'        \'<div style="display:flex;flex-direction:column;gap:10px;">\'+\n' +
'        \'<h4 style="color:#fff;margin-bottom:5px;font-family:sans-serif;font-size:1rem;">Legal</h4>\'+\n' +
'        \'<a href="\'+base+\'acerca-de.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Acerca de</a>\'+\n' +
'        \'<a href="\'+base+\'privacidad.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Privacidad</a>\'+\n' +
'        \'<a href="\'+base+\'terminos.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Términos</a>\'+\n' +
'        \'<a href="\'+base+\'contacto.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Contacto</a>\'+\n' +
'        \'</div>\'+\n' +
'        \'</div>\'+\n' +
'        \'<div style="border-top:1px solid rgba(255,255,255,0.1);margin-top:40px;padding-top:20px;text-align:center;font-size:0.9rem;max-width:1400px;margin-left:auto;margin-right:auto;">© 2026 ' + s.name + '. Todos los derechos reservados.</div>\'+\n' +
'        \'</footer>\';\n' +
'\n' +
'    function init(){\n' +
'        var pre=document.getElementById("site-preloader");if(pre)pre.outerHTML=PRE;\n' +
'        var hdr=document.getElementById("site-header");if(hdr)hdr.outerHTML=HDR;\n' +
'        var ftr=document.getElementById("site-footer");if(ftr)ftr.outerHTML=FTR;\n' +
'        setTimeout(function(){\n' +
'            var p=document.querySelector(".site-preloader");\n' +
'            if(p){p.style.opacity="0";setTimeout(function(){p.style.display="none";},600);}\n' +
'        },800);\n' +
'        document.querySelectorAll("img").forEach(function(i){\n' +
'            i.addEventListener("error",function(){this.src=base+"logo.png";});\n' +
'        });\n' +
'    }\n' +
'\n' +
'    if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);\n' +
'    else init();\n' +
'})();';
}

// Write all files
var count = 0;
SITES.forEach(function(s) {
    var fp = path.join(__dirname, 'sites', s.slug, 'components.js');
    try {
        fs.writeFileSync(fp, gen(s));
        count++;
        console.log('OK ' + s.slug);
    } catch(e) {
        console.log('ERR ' + s.slug + ': ' + e.message);
    }
});
console.log('Done: ' + count + '/' + SITES.length);
process.exit(0);
