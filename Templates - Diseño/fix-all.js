const fs = require('fs');
const path = require('path');

const SITES = [
    { slug: 'puntoclave',        name: 'PuntoClave',         bg: '#000000', pri: '#FF2A2A' },
    { slug: 'diarioexpress',     name: 'DiarioExpress',      bg: '#111111', pri: '#1a73e8' },
    { slug: 'enfoquedirecto',    name: 'EnfoqueDirecto',     bg: '#0a0a0a', pri: '#C9A84C' },
    { slug: 'noticiashorizonte', name: 'NoticiasHorizonte',  bg: '#3D2C2E', pri: '#C17C5E' },
    { slug: 'mexico360noticias', name: 'México360Noticias',  bg: '#1B2A4A', pri: '#1B2A4A' },
    { slug: 'capitalpress',      name: 'CapitalPress',       bg: '#2C2C2C', pri: '#2C2C2C' },
    { slug: 'boominformativo',   name: 'BoomInformativo',    bg: '#0A192F', pri: '#FF6B9D' },
    { slug: 'puntonoticias',     name: 'PuntoNoticias',      bg: '#1a1a2e', pri: '#e94560' },
    { slug: 'reportediario',     name: 'ReporteDiario',      bg: '#1C1C1C', pri: '#8B1A2B' },
    { slug: 'pulsodiario',       name: 'PulsoDiario',        bg: '#1C1E21', pri: '#00FF66' },
    { slug: 'radarinformativo',  name: 'RadarInformativo',   bg: '#121212', pri: '#8B5CF6' },
    { slug: 'formulacdmx',       name: 'FormulaCDMX',        bg: '#0f172a', pri: '#38bdf8' },
    { slug: 'enfoquecapital',    name: 'EnfoqueCapital',     bg: '#111111', pri: '#1a73e8' },
    { slug: 'mexicantimes',      name: 'MexicanTimes',       bg: '#111111', pri: '#1a73e8' },
    { slug: 'elpulsomexicano',   name: 'ElPulsoMexicano',    bg: '#111111', pri: '#1a73e8' },
    { slug: 'mradio',            name: 'MRadio',             bg: '#111111', pri: '#1a73e8' },
    { slug: 'televisionabc',     name: 'TelevisiónABC',      bg: '#111111', pri: '#1a73e8' },
];

// Try to extract actual colors from existing file
function tryExtractColors(filePath) {
    try {
        const c = fs.readFileSync(filePath, 'utf8');
        const m = c.match(/background:([^;]+);border-bottom:3px solid ([^;]+);/);
        if (m) return { bg: m[1].trim(), pri: m[2].trim() };
    } catch(e) {}
    return null;
}

function gen(site) {
    const n = site.name;
    const bg = site.bg;
    const pri = site.pri;
    
    return `(function(){
    var p=window.location.pathname;
    var isSubdir=/\\/(categoria|articulo|admin)\\//.test(p);
    var base=isSubdir?"../":"./";

    // PRELOADER
    var PRE='<div class="site-preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;background:${bg};display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:99999;gap:20px;transition:opacity 0.6s;">'+
        '<img src="'+base+'logo.png" alt="${n}" style="height:80px;width:auto;object-fit:contain;">'+
        '<p style="font-family:sans-serif;color:rgba(255,255,255,0.7);font-size:1rem;letter-spacing:2px;text-transform:uppercase;">${n}</p></div>';

    // HEADER
    var HDR='<header class="injected-header" style="background:${bg};border-bottom:3px solid ${pri};position:sticky;top:0;z-index:1000;box-shadow:0 4px 20px rgba(0,0,0,0.3);">'+
        '<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 24px;max-width:1400px;margin:0 auto;">'+
        '<a href="'+base+'index.html" style="display:flex;align-items:center;"><img src="'+base+'logo.png" alt="${n}" style="height:48px;width:auto;object-fit:contain;"></a>'+
        '<nav style="display:flex;flex-wrap:wrap;gap:0;">'+
        '<a href="'+base+'categoria/nacional.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Nacional</a>'+
        '<a href="'+base+'categoria/politica.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Política</a>'+
        '<a href="'+base+'categoria/economia.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Economía</a>'+
        '<a href="'+base+'categoria/deportes.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Deportes</a>'+
        '<a href="'+base+'categoria/cultura.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Cultura</a>'+
        '<a href="'+base+'categoria/tecnologia.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;font-size:0.9rem;padding:10px 14px;color:#fff;opacity:0.8;text-decoration:none;">Tecnología</a>'+
        '</nav></div></header>';

    // FOOTER with logo.png
    var FTR='<footer style="background:${bg};color:rgba(255,255,255,0.6);padding:50px 24px 30px;margin-top:60px;">'+
        '<div style="max-width:1400px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:40px;align-items:start;">'+

        '<div style="display:flex;flex-direction:column;gap:12px;">'+
        '<img src="'+base+'logo.png" alt="${n}" style="height:50px;width:auto;object-fit:contain;margin-bottom:8px;">'+
        '<p style="font-size:0.95rem;line-height:1.5;max-width:280px;">Noticias digitales en tiempo real. Información verificada las 24 horas.</p>'+
        '</div>'+

        '<div style="display:flex;flex-direction:column;gap:10px;">'+
        '<h4 style="color:#fff;margin-bottom:5px;font-family:sans-serif;font-size:1rem;">Secciones</h4>'+
        '<a href="'+base+'categoria/nacional.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Nacional</a>'+
        '<a href="'+base+'categoria/politica.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Política</a>'+
        '<a href="'+base+'categoria/economia.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Economía</a>'+
        '<a href="'+base+'categoria/deportes.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Deportes</a>'+
        '</div>'+

        '<div style="display:flex;flex-direction:column;gap:10px;">'+
        '<h4 style="color:#fff;margin-bottom:5px;font-family:sans-serif;font-size:1rem;">Legal</h4>'+
        '<a href="'+base+'acerca-de.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Acerca de</a>'+
        '<a href="'+base+'privacidad.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Privacidad</a>'+
        '<a href="'+base+'terminos.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Términos</a>'+
        '<a href="'+base+'contacto.html" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:0.95rem;">Contacto</a>'+
        '</div>'+

        '</div>'+
        '<div style="border-top:1px solid rgba(255,255,255,0.1);margin-top:40px;padding-top:20px;text-align:center;font-size:0.9rem;max-width:1400px;margin-left:auto;margin-right:auto;">© 2026 ${n}. Todos los derechos reservados.</div>'+
        '</footer>';

    function init(){
        var pre=document.getElementById("site-preloader");if(pre)pre.outerHTML=PRE;
        var hdr=document.getElementById("site-header");if(hdr)hdr.outerHTML=HDR;
        var ftr=document.getElementById("site-footer");if(ftr)ftr.outerHTML=FTR;
        setTimeout(function(){
            var p=document.querySelector(".site-preloader");
            if(p){p.style.opacity="0";setTimeout(function(){p.style.display="none";},600);}
        },800);
        document.querySelectorAll("img").forEach(function(i){
            i.addEventListener("error",function(){this.src=base+"logo.png";});
        });
    }

    if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);
    else init();
})();`;
}

const sitesDir = path.join(__dirname, 'sites');
let count = 0;

SITES.forEach(function(site) {
    const compPath = path.join(sitesDir, site.slug, 'components.js');
    
    // Try to get real colors from existing file
    const extracted = tryExtractColors(compPath);
    if (extracted) {
        site.bg = extracted.bg;
        site.pri = extracted.pri;
    }
    
    const content = gen(site);
    
    try {
        fs.writeFileSync(compPath, content, 'utf8');
        console.log('[OK] ' + site.slug + ' (bg:' + site.bg + ' pri:' + site.pri + ')');
        count++;
    } catch(e) {
        console.log('[ERR] ' + site.slug + ': ' + e.message);
    }
});

console.log('\nDone: ' + count + '/17 files updated');
