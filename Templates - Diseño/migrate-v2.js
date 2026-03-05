/**
 * migrate-v2.js — Preserves original Titulares layouts, only adds API integration
 * Run: node migrate-v2.js
 */
const fs = require('fs');
const path = require('path');

// ── CONFIG ──
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

const BASE_DIR = __dirname;
const TITULARES = path.join(BASE_DIR, 'Titulares');
const SITES_DIR = path.join(BASE_DIR, 'sites');
const META_DIR  = path.join(BASE_DIR, 'data', 'sites_metadata');
const API_BASE  = 'https://news-api.sebastianvernis.workers.dev';
const CATS = ['nacional','politica','economia','deportes','cultura','tecnologia'];

// ── HELPERS ──
function mkdirp(p) { fs.mkdirSync(p, { recursive: true }); }
function write(fp, content) { fs.writeFileSync(fp, content, 'utf8'); }
function copy(src, dst) {
    if (fs.existsSync(src)) fs.copyFileSync(src, dst);
    else console.log('    WARN: no existe ' + src);
}

function extractStyle(html) {
    var m = html.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
    return m ? m[1].trim() : '';
}

function extractMain(html) {
    // Get body content
    var bodyM = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    if (!bodyM) return '';
    var body = bodyM[1];
    // Try to get <main>...</main>
    var mainM = body.match(/<main[\s\S]*?<\/main>/i);
    if (mainM) return mainM[0];
    // Otherwise get everything between header and footer
    body = body.replace(/<header[\s\S]*?<\/header>/i, '');
    body = body.replace(/<footer[\s\S]*?<\/footer>/i, '');
    return '<main>\n' + body.trim() + '\n</main>';
}

function extractVars(css) {
    var vars = {};
    var rootM = css.match(/:root\s*\{([^}]+)\}/);
    if (!rootM) return vars;
    rootM[1].split('\n').forEach(function(line) {
        var m = line.match(/--([\w-]+)\s*:\s*([^;]+)/);
        if (m) vars[m[1].trim()] = m[2].trim();
    });
    return vars;
}

function findColor(vars, keywords) {
    for (var i = 0; i < keywords.length; i++) {
        var keys = Object.keys(vars);
        for (var j = 0; j < keys.length; j++) {
            if (keys[j].toLowerCase().indexOf(keywords[i]) !== -1) {
                var v = vars[keys[j]];
                if (v.match(/#[0-9a-fA-F]{3,8}/)) return v.split('/')[0].split('*')[0].trim();
            }
        }
    }
    return null;
}

function getColors(vars) {
    return {
        primary: findColor(vars, ['accent','brand','primary','glow','neon']) || '#1a73e8',
        bg: findColor(vars, ['bg','surface','paper','bone','sand','base','navy','dark']) || '#ffffff',
        text: findColor(vars, ['text-dark','text-ink','text-main','text-primary','text-color']) || '#111111',
    };
}

function isDarkTheme(bgColor) {
    if (!bgColor) return false;
    var hex = bgColor.replace('#', '');
    if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
    var r = parseInt(hex.substr(0,2),16);
    var g = parseInt(hex.substr(2,2),16);
    var b = parseInt(hex.substr(4,2),16);
    return (r + g + b) / 3 < 128;
}

// ── GENERATE INDEX.HTML ──
// Preserves original <main> layout, adds API integration
function genIndex(site, mainHTML, origCSS) {
    var s = site.slug, n = site.name;
    return [
        '<!DOCTYPE html>',
        '<html lang="es">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <title>' + n + ' - Noticias en Tiempo Real</title>',
        '    <meta name="description" content="' + n + ' - Noticias digitales en tiempo real.">',
        '    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">',
        '    <link href="style-custom.css" rel="stylesheet">',
        '    <link rel="alternate" type="application/rss+xml" title="' + n + ' RSS" href="/rss.xml">',
        '</head>',
        '<body>',
        '',
        '<div id="site-preloader"></div>',
        '<div id="site-header"></div>',
        '',
        mainHTML,
        '',
        '<div id="site-footer"></div>',
        '',
        '<script src="components.js"></script>',
        '<script src="script.js"></script>',
        '<script>',
        genAPIScript(s),
        '</script>',
        '',
        '</body>',
        '</html>'
    ].join('\n');
}

// ── API INTEGRATION SCRIPT ──
// Generic script that populates the original layout with API data
function genAPIScript(slug) {
    return [
        '(function() {',
        '    var API = "' + API_BASE + '/api/articles?site=' + slug + '&limit=20";',
        '    function esc(t){if(!t)return"";return String(t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");}',
        '    function enc(t){return encodeURIComponent(t||"");}',
        '',
        '    async function load(){',
        '        try{',
        '            var r=await fetch(API);if(!r.ok)throw new Error("err");',
        '            var d=await r.json();var arts=d.articles;',
        '            if(!arts||!arts.length)return;',
        '            populate(arts);',
        '        }catch(e){console.error("Error:",e);}',
        '    }',
        '',
        '    function populate(arts){',
        '        var main=document.querySelector("main");if(!main)return;',
        '        var ai=0;',
        '',
        '        // 1. Populate background-image placeholders (divs used as images)',
        '        var imgDivs=main.querySelectorAll("[class*=img],[class*=image],[class*=thumb],[class*=placeholder]");',
        '        imgDivs.forEach(function(el){',
        '            if(ai>=arts.length)return;',
        '            // Only target divs without text content (image placeholders)',
        '            if(el.tagName==="DIV"&&el.children.length<=1&&el.textContent.trim().length<20){',
        '                if(arts[ai].imageUrl){',
        '                    el.style.backgroundImage="url("+arts[ai].imageUrl+")";',
        '                    el.style.backgroundSize="cover";',
        '                    el.style.backgroundPosition="center";',
        '                }',
        '            }',
        '            ai++;',
        '        });',
        '',
        '        // 2. Populate titles - find all article-like containers',
        '        ai=0;',
        '        var containers=main.querySelectorAll("article,.hero,.hero-content,.hero-text,.hero-text-box,.hero-headline,.z-content,.focus-section,.side-item,.side-article,.grid-item,.scroll-content,.video-card,.minimal-card,.gallery-card,.classic-card,.card,.card-body,.brief-card,.tech-card,.grid-card,.scroll-card");',
        '        containers.forEach(function(el){',
        '            if(ai>=arts.length)return;',
        '            var a=arts[ai];',
        '            // Find the first heading in this container',
        '            var heading=el.querySelector("h1,h2,h3,h4");',
        '            if(heading){',
        '                var link="articulo/index.html?slug="+enc(a.slug);',
        '                heading.innerHTML=\'<a href="\'+link+\'" style="color:inherit;text-decoration:none;">\'+esc(a.title)+\'</a>\';',
        '            }',
        '            // Find excerpt paragraph',
        '            var para=el.querySelector("p");',
        '            if(para&&!para.closest(".author-meta,.author-info,.img-caption")){',
        '                if(a.excerpt)para.textContent=a.excerpt;',
        '            }',
        '            // Find category tag',
        '            var tag=el.querySelector(".tag,.tag-pill,.category-tag,.category,.category-label,.category-pill,.hero-tag,.card-meta");',
        '            if(tag&&a.category)tag.textContent=a.category;',
        '            // Find image placeholder div',
        '            var imgDiv=el.querySelector("[class*=img],[class*=image],[class*=thumb],[class*=placeholder]");',
        '            if(imgDiv&&imgDiv.tagName==="DIV"&&a.imageUrl){',
        '                imgDiv.style.backgroundImage="url("+a.imageUrl+")";',
        '                imgDiv.style.backgroundSize="cover";',
        '                imgDiv.style.backgroundPosition="center";',
        '            }',
        '            // Find read-more link',
        '            var rm=el.querySelector("a.read-more,a.read-link,a.btn-outline,a.read-btn,a[href=\'#\']");',
        '            if(rm)rm.href="articulo/index.html?slug="+enc(a.slug);',
        '            ai++;',
        '        });',
        '',
        '        // 3. Populate numbered lists',
        '        var listItems=main.querySelectorAll(".numbered-list li,.trending-list li span");',
        '        listItems.forEach(function(el,i){if(arts[i])el.textContent=arts[i].title;});',
        '',
        '        // 4. Populate marquee/ticker',
        '        var marquee=main.querySelector(".marquee,marquee");',
        '        if(marquee)marquee.textContent=arts.slice(0,5).map(function(a){return"+++ "+a.title.toUpperCase();}).join(" ");',
        '',
        '        // 5. Populate newspaper columns',
        '        var cols=main.querySelector(".newspaper-columns");',
        '        if(cols&&arts[0]){',
        '            var credit=cols.querySelector(".author-credit");',
        '            if(credit&&arts[0].author)credit.textContent="Por "+arts[0].author;',
        '            var paras=cols.querySelectorAll("p");',
        '            paras.forEach(function(p,i){if(arts[i]&&arts[i].excerpt)p.textContent=arts[i].excerpt;});',
        '        }',
        '    }',
        '',
        '    if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",load);',
        '    else load();',
        '})();'
    ].join('\n');
}

// ── GENERATE COMPONENTS.JS ──
function genComponents(site, colors) {
    var n = site.name, dark = isDarkTheme(colors.bg);
    var hdrBg = dark ? colors.bg : (colors.text || '#111');
    var pri = colors.primary;
    var logoFilter = dark ? '' : 'filter:brightness(0) invert(1);';

    return [
        '(function(){',
        '    var p=window.location.pathname;',
        '    var isSubdir=/\\/(categoria|articulo|admin)\\//.test(p);',
        '    var base=isSubdir?"../":"./";',
        '',
        '    var PRE=\'<div class="site-preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;background:' + hdrBg + ';display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:99999;gap:20px;transition:opacity 0.6s;">\'+',
        '        \'<img src="\'+base+\'logo-header.png" alt="' + n + '" style="height:75px;width:auto;object-fit:contain;' + logoFilter + 'animation:pulse 2s ease-in-out infinite;">\'+',
        '        \'<p style="font-family:sans-serif;color:rgba(255,255,255,0.7);font-size:0.85rem;letter-spacing:2px;text-transform:uppercase;">' + n + '</p></div>\';',
        '',
        '    var HDR=\'<header class="injected-header" style="background:' + hdrBg + ';border-bottom:3px solid ' + pri + ';position:sticky;top:0;z-index:1000;box-shadow:0 4px 20px rgba(0,0,0,0.3);">\'+',
        '        \'<div style="display:flex;align-items:center;justify-content:space-between;padding:4px 24px;max-width:1400px;margin:0 auto;">\'+',
        '        \'<a href="\'+base+\'index.html" style="display:flex;align-items:center;"><img src="\'+base+\'logo-header.png" alt="' + n + '" style="height:50px;width:auto;object-fit:contain;' + logoFilter + '"></a>\'+',
        '        \'<nav style="display:flex;flex-wrap:wrap;gap:0;">\'+',
        '        \'<a href="\'+base+\'categoria/nacional.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:1px;font-size:0.77rem;padding:10px 12px;color:#fff;opacity:0.7;text-decoration:none;">Nacional</a>\'+',
        '        \'<a href="\'+base+\'categoria/politica.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:1px;font-size:0.77rem;padding:10px 12px;color:#fff;opacity:0.7;text-decoration:none;">Política</a>\'+',
        '        \'<a href="\'+base+\'categoria/economia.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:1px;font-size:0.77rem;padding:10px 12px;color:#fff;opacity:0.7;text-decoration:none;">Economía</a>\'+',
        '        \'<a href="\'+base+\'categoria/deportes.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:1px;font-size:0.77rem;padding:10px 12px;color:#fff;opacity:0.7;text-decoration:none;">Deportes</a>\'+',
        '        \'<a href="\'+base+\'categoria/cultura.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:1px;font-size:0.77rem;padding:10px 12px;color:#fff;opacity:0.7;text-decoration:none;">Cultura</a>\'+',
        '        \'<a href="\'+base+\'categoria/tecnologia.html" style="font-family:sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:1px;font-size:0.77rem;padding:10px 12px;color:#fff;opacity:0.7;text-decoration:none;">Tecnología</a>\'+',
        '        \'</nav></div></header>\';',
        '',
        '    var FTR=\'<footer style="background:' + hdrBg + ';color:rgba(255,255,255,0.6);padding:40px 24px;margin-top:60px;">\'+',
        '        \'<div style="max-width:1400px;margin:0 auto;display:flex;flex-wrap:wrap;justify-content:space-between;gap:30px;">\'+',
        '        \'<div><h4 style="color:#fff;margin-bottom:10px;font-family:sans-serif;">' + n + '</h4><p style="font-size:0.9rem;max-width:300px;">Noticias digitales en tiempo real.</p></div>\'+',
        '        \'<div style="display:flex;gap:20px;flex-wrap:wrap;font-size:0.88rem;">\'+',
        '        \'<a href="\'+base+\'acerca-de.html" style="color:rgba(255,255,255,0.6);text-decoration:none;">Acerca de</a>\'+',
        '        \'<a href="\'+base+\'privacidad.html" style="color:rgba(255,255,255,0.6);text-decoration:none;">Privacidad</a>\'+',
        '        \'<a href="\'+base+\'terminos.html" style="color:rgba(255,255,255,0.6);text-decoration:none;">Términos</a>\'+',
        '        \'<a href="\'+base+\'contacto.html" style="color:rgba(255,255,255,0.6);text-decoration:none;">Contacto</a>\'+',
        '        \'</div></div>\'+',
        '        \'<div style="border-top:1px solid rgba(255,255,255,0.1);margin-top:30px;padding-top:20px;text-align:center;font-size:0.82rem;">© 2026 ' + n + '. Todos los derechos reservados.</div></footer>\';',
        '',
        '    function init(){',
        '        var pre=document.getElementById("site-preloader");if(pre)pre.outerHTML=PRE;',
        '        var hdr=document.getElementById("site-header");if(hdr)hdr.outerHTML=HDR;',
        '        var ftr=document.getElementById("site-footer");if(ftr)ftr.outerHTML=FTR;',
        '        setTimeout(function(){var p=document.querySelector(".site-preloader");if(p){p.style.opacity="0";setTimeout(function(){p.style.display="none";},600);}},800);',
        '        document.querySelectorAll("img").forEach(function(i){i.addEventListener("error",function(){this.src=base+"logo.png";});});',
        '    }',
        '',
        '    if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);',
        '    else init();',
        '})();'
    ].join('\n');
}

// ── GENERATE LEGAL PAGES ──
function genLegal(site, type) {
    var n = site.name;
    var titles = { 'acerca-de': 'Acerca de', 'contacto': 'Contacto', 'privacidad': 'Aviso de Privacidad', 'terminos': 'Términos y Condiciones' };
    var contents = {
        'acerca-de': '<h2>Nuestra Misión</h2><p>En ' + n + ' nos dedicamos a proporcionar información veraz, oportuna y objetiva.</p><h2>Nuestros Valores</h2><ul><li><strong>Veracidad:</strong> Compromiso con la información verificada</li><li><strong>Objetividad:</strong> Presentamos los hechos sin sesgos</li><li><strong>Responsabilidad:</strong> Asumimos la responsabilidad de nuestro contenido</li></ul>',
        'contacto': '<h2>Contacto</h2><p>Email: contacto@' + site.slug + '.lat</p><p>Para consultas editoriales, colaboraciones o reportar errores en nuestro contenido, no dude en comunicarse con nosotros.</p>',
        'privacidad': '<h2>Recopilación de Datos</h2><p>' + n + ' recopila información limitada para mejorar la experiencia del usuario.</p><h2>Uso de Cookies</h2><p>Utilizamos cookies esenciales para el funcionamiento del sitio.</p><h2>Derechos del Usuario</h2><p>Puede solicitar la eliminación de sus datos en cualquier momento.</p>',
        'terminos': '<h2>Uso del Sitio</h2><p>Al acceder a ' + n + ', acepta estos términos y condiciones.</p><h2>Propiedad Intelectual</h2><p>Todo el contenido es propiedad de ' + n + ' o sus respectivos autores.</p><h2>Limitación de Responsabilidad</h2><p>' + n + ' no se hace responsable por decisiones tomadas con base en la información publicada.</p>'
    };
    return [
        '<!DOCTYPE html><html lang="es"><head>',
        '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>' + titles[type] + ' - ' + n + '</title>',
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">',
        '<link href="style-custom.css" rel="stylesheet">',
        '<style>.legal-page{max-width:800px;margin:40px auto;padding:0 24px;font-family:sans-serif;line-height:1.8;}.legal-page h1{font-size:2rem;margin-bottom:10px;}.legal-page h2{font-size:1.3rem;margin:25px 0 10px;}.legal-page p,.legal-page li{color:#555;font-size:1rem;}.legal-page ul{padding-left:20px;}</style>',
        '</head><body>',
        '<div id="site-preloader"></div><div id="site-header"></div>',
        '<main class="legal-page"><h1>' + titles[type] + ' - ' + n + '</h1>' + contents[type] + '</main>',
        '<div id="site-footer"></div>',
        '<script src="components.js"></script>',
        '</body></html>'
    ].join('\n');
}

// ── GENERATE ARTICULO PAGE ──
function genArticulo(site) {
    var s = site.slug, n = site.name;
    return [
        '<!DOCTYPE html><html lang="es"><head>',
        '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>Artículo - ' + n + '</title>',
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">',
        '<link href="../style-custom.css" rel="stylesheet">',
        '<style>.article-page{max-width:800px;margin:40px auto;padding:0 24px;font-family:sans-serif;line-height:1.8;}.article-page h1{font-size:2.2rem;margin-bottom:15px;}.article-page .meta{color:#888;font-size:0.9rem;margin-bottom:20px;}.article-page .feat-img{width:100%;max-height:450px;object-fit:cover;border-radius:8px;margin-bottom:25px;}.article-page .content{font-size:1.05rem;color:#333;}.article-page .content p{margin-bottom:15px;}</style>',
        '</head><body>',
        '<div id="site-preloader"></div><div id="site-header"></div>',
        '<main class="article-page"><div id="article-content"><p style="text-align:center;padding:60px;">Cargando artículo...</p></div></main>',
        '<div id="site-footer"></div>',
        '<script src="../components.js"></script>',
        '<script>',
        '(function(){',
        '    var params=new URLSearchParams(window.location.search);',
        '    var slug=params.get("slug");if(!slug)return;',
        '    fetch("' + API_BASE + '/api/articles/"+encodeURIComponent(slug)+"?site=' + s + '")',
        '    .then(function(r){return r.json();})',
        '    .then(function(d){',
        '        var a=d.article||d;if(!a||!a.title)return;',
        '        document.title=a.title+" - ' + n + '";',
        '        var h=\'<h1>\'+a.title+\'</h1>\';',
        '        h+=\'<div class="meta"><span><i class="far fa-user"></i> \'+(a.author||"Redacción")+\'</span> &bull; <span><i class="far fa-calendar"></i> \'+(a.publishedAt?new Date(a.publishedAt).toLocaleDateString("es-MX"):"")+\'</span> &bull; <span>\'+(a.category||"General")+\'</span></div>\';',
        '        if(a.imageUrl)h+=\'<img class="feat-img" src="\'+a.imageUrl+\'" alt="">\';',
        '        h+=\'<div class="content">\'+(a.content||a.excerpt||"")+\'</div>\';',
        '        document.getElementById("article-content").innerHTML=h;',
        '    }).catch(function(e){console.error(e);});',
        '})();',
        '</script>',
        '</body></html>'
    ].join('\n');
}

// ── GENERATE CATEGORIA PAGE ──
function genCategoria(site, cat) {
    var s = site.slug, n = site.name;
    var catLabel = cat.charAt(0).toUpperCase() + cat.slice(1);
    return [
        '<!DOCTYPE html><html lang="es"><head>',
        '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>' + catLabel + ' - ' + n + '</title>',
        '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">',
        '<link href="../style-custom.css" rel="stylesheet">',
        '<style>.cat-page{max-width:1200px;margin:40px auto;padding:0 24px;font-family:sans-serif;}.cat-page h1{font-size:2rem;margin-bottom:30px;}.cat-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px;}.cat-card{background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.1);transition:transform 0.2s;}.cat-card:hover{transform:translateY(-4px);}.cat-card img{width:100%;height:200px;object-fit:cover;}.cat-card-body{padding:16px;}.cat-card-body h3{font-size:1.1rem;margin-bottom:8px;}.cat-card-body h3 a{color:inherit;text-decoration:none;}.cat-card-body p{color:#666;font-size:0.9rem;}</style>',
        '</head><body>',
        '<div id="site-preloader"></div><div id="site-header"></div>',
        '<main class="cat-page"><h1>' + catLabel + '</h1><div id="cat-grid" class="cat-grid"><p>Cargando...</p></div></main>',
        '<div id="site-footer"></div>',
        '<script src="../components.js"></script>',
        '<script>',
        '(function(){',
        '    fetch("' + API_BASE + '/api/articles?site=' + s + '&category=' + cat + '&limit=20")',
        '    .then(function(r){return r.json();})',
        '    .then(function(d){',
        '        var arts=d.articles;if(!arts||!arts.length){document.getElementById("cat-grid").innerHTML="<p>No hay noticias.</p>";return;}',
        '        document.getElementById("cat-grid").innerHTML=arts.map(function(a){',
        '            return \'<article class="cat-card">\'+',
        '                (a.
