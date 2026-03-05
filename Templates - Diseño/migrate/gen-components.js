// Generates components.js (header, footer, preloader, ticker, weather)
var { API_BASE, CATEGORIES, CAT_LABELS } = require('./config');

function genComponentsJS(site, colors) {
    var c = colors;
    var s = '';

    s += '/**\n * ' + site.name + ' - Componentes Compartidos\n';
    s += ' * Header, Footer y Preloader inyectados dinamicamente\n */\n';
    s += '(function () {\n';
    s += '    var path = window.location.pathname;\n';
    s += '    var isSubdir = /\\/(categoria|articulo|admin)\\//.test(path);\n';
    s += "    var base = isSubdir ? '../' : './';\n\n";

    // Active nav detection
    s += '    var p = path.toLowerCase();\n';
    CATEGORIES.forEach(function(cat) {
        s += "    var is" + cap(cat) + " = p.includes('" + cat + "');\n";
    });
    s += '    var isHome = !' + CATEGORIES.map(function(cat) { return 'is' + cap(cat); }).join(' && !') + ';\n';
    s += "    function cls(cond) { return cond ? ' active' : ''; }\n\n";

    // PRELOADER
    s += '    var PRELOADER_HTML = \'<div id="site-preloader" class="rc-preloader">\' +\n';
    s += '        \'<div class="rc-circle-expand"></div>\' +\n';
    s += '        \'<div class="rc-circle-expand rc-circle-2"></div>\' +\n';
    s += '        \'<img src="\' + base + \'logo-header.png" alt="' + site.name + '" class="rc-preloader-logo">\' +\n';
    s += "        '<p class=\"rc-preloader-text\">" + site.name + "</p>' +\n";
    s += "        '</div>' +\n";
    s += "        '<style>' +\n";
    s += "        '.rc-preloader{position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(135deg," + c.dark + " 0%," + c.primary + " 100%);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:99999;gap:20px;transition:opacity 0.6s ease;}' +\n";
    s += "        '.rc-preloader.loaded{opacity:0;pointer-events:none;}' +\n";
    s += "        '.rc-circle-expand{position:absolute;width:60px;height:60px;border:3px solid rgba(255,255,255,0.3);border-radius:50%;animation:rc-expand 1.8s ease-out infinite;}' +\n";
    s += "        '.rc-circle-2{animation-delay:0.9s;border-color:rgba(255,255,255,0.15);}' +\n";
    s += "        '@keyframes rc-expand{0%{transform:scale(1);opacity:1;}100%{transform:scale(5);opacity:0;}}' +\n";
    s += "        '.rc-preloader-logo{position:relative;z-index:1;height:75px;width:auto;object-fit:contain;filter:brightness(0) invert(1);animation:rc-pulse 2s ease-in-out infinite;}' +\n";
    s += "        '@keyframes rc-pulse{0%,100%{opacity:1;}50%{opacity:0.7;}}' +\n";
    s += "        '.rc-preloader-text{position:relative;z-index:1;font-family:Noto Sans,Arial,sans-serif;color:rgba(255,255,255,0.6);font-size:0.85rem;letter-spacing:3px;text-transform:uppercase;}' +\n";
    s += "        '</style>';\n\n";

    // HEADER
    s += '    var HEADER_HTML = \'<header class="header">\' +\n';
    s += "        '<div class=\"header-container\">' +\n";
    s += "        '<div class=\"logo-section\"><a href=\"' + base + 'index.html\"><img src=\"' + base + 'logo-header.png\" alt=\"" + site.name + "\" class=\"site-logo\"></a></div>' +\n";
    s += "        '<nav class=\"main-nav\">' +\n";
    s += "        '<a href=\"' + base + 'index.html\" class=\"nav-link' + cls(isHome) + '\">Inicio</a>' +\n";
    CATEGORIES.forEach(function(cat) {
        var label = CAT_LABELS[cat] || cat;
        s += "        '<a href=\"' + base + 'categoria/" + cat + ".html\" class=\"nav-link' + cls(is" + cap(cat) + ") + '\">" + label + "</a>' +\n";
    });
    s += "        '</nav>' +\n";
    s += "        '</div>' +\n";
    s += "        '</header>' +\n";

    // TICKER BAR
    s += "        '<div class=\"radio-bar\"><div class=\"radio-bar-inner\">' +\n";
    s += "        '<div style=\"background:rgba(0,0,0,0.3);color:#fff;font-family:Noto Sans,sans-serif;font-weight:800;font-size:0.68rem;letter-spacing:2px;padding:4px 10px;border-radius:3px;flex-shrink:0;display:flex;align-items:center;gap:6px;\"><i class=\"fas fa-bolt\" style=\"color:#FF6B6B;\"></i> AHORA</div>' +\n";
    s += "        '<marquee scrollamount=\"4\"><span class=\"ticker-item\">Cargando titulares...</span></marquee>' +\n";
    s += "        '<div id=\"weather-widget\" style=\"display:flex;align-items:center;gap:6px;flex-shrink:0;color:rgba(255,255,255,0.85);font-size:0.82rem;\"><span id=\"weather-icon\"></span><span id=\"weather-city\">CDMX</span><span id=\"weather-temp\">--</span></div>' +\n";
    s += "        '</div></div>';\n\n";

    // FOOTER
    s += '    var FOOTER_HTML = \'<footer class="footer">\' +\n';
    s += "        '<div class=\"footer-grid cols-3\">' +\n";
    s += "        '<div class=\"footer-column\">' +\n";
    s += "        '<div class=\"footer-logo\"><img src=\"' + base + 'logo-header.png\" alt=\"" + site.name + "\"><h3>" + site.name + "</h3></div>' +\n";
    s += "        '<p class=\"footer-about\">Noticias digitales en tiempo real. Informacion veraz y oportuna las 24 horas.</p>' +\n";
    s += "        '<div class=\"social-links\">' +\n";
    s += "        '<a href=\"#\" class=\"social-link\"><i class=\"fab fa-facebook-f\"></i></a>' +\n";
    s += "        '<a href=\"#\" class=\"social-link\"><i class=\"fab fa-twitter\"></i></a>' +\n";
    s += "        '<a href=\"#\" class=\"social-link\"><i class=\"fab fa-instagram\"></i></a>' +\n";
    s += "        '</div></div>' +\n";
    s += "        '<div class=\"footer-column\"><h4>Secciones</h4><ul class=\"footer-links\">' +\n";
    CATEGORIES.forEach(function(cat) {
        var label = CAT_LABELS[cat] || cat;
        s += "        '<li><a href=\"' + base + 'categoria/" + cat + ".html\">" + label + "</a></li>' +\n";
    });
    s += "        '</ul></div>' +\n";
    s += "        '<div class=\"footer-column\"><h4>Legal</h4><ul class=\"footer-links\">' +\n";
    s += "        '<li><a href=\"' + base + 'acerca-de.html\">Acerca de</a></li>' +\n";
    s += "        '<li><a href=\"' + base + 'contacto.html\">Contacto</a></li>' +\n";
    s += "        '<li><a href=\"' + base + 'privacidad.html\">Privacidad</a></li>' +\n";
    s += "        '<li><a href=\"' + base + 'terminos.html\">Terminos</a></li>' +\n";
    s += "        '</ul></div></div>' +\n";
    s += "        '<div class=\"footer-bottom\"><span>&copy; ' + new Date().getFullYear() + ' " + site.name + ". Todos los derechos reservados.</span></div>' +\n";
    s += "        '</footer>';\n\n";

    // INIT
    s += '    function init() {\n';
    s += "        var pre = document.getElementById('site-preloader');\n";
    s += '        if (pre) { pre.outerHTML = PRELOADER_HTML; }\n';
    s += "        var hdr = document.getElementById('site-header');\n";
    s += '        if (hdr) { hdr.outerHTML = HEADER_HTML; }\n';
    s += "        var ftr = document.getElementById('site-footer');\n";
    s += '        if (ftr) { ftr.outerHTML = FOOTER_HTML; }\n\n';
    s += '        setTimeout(function() {\n';
    s += "            var loader = document.querySelector('.rc-preloader');\n";
    s += "            if (loader) loader.classList.add('loaded');\n";
    s += '            setTimeout(function() { if (loader) loader.remove(); }, 700);\n';
    s += '        }, 800);\n\n';
    s += '        initFixedHeader();\n';
    s += '        initImageFallbacks();\n';
    s += '        initBreakingTicker();\n';
    s += '        initWeatherWidget();\n';
    s += '    }\n\n';

    // FIXED HEADER
    s += '    function initFixedHeader() {\n';
    s += "        var header = document.querySelector('.header');\n";
    s += '        if (!header) return;\n';
    s += '        var lastY = 0;\n';
    s += "        window.addEventListener('scroll', function() {\n";
    s += '            var y = window.scrollY;\n';
    s += "            if (y > 100) header.classList.add('scrolled');\n";
    s += "            else header.classList.remove('scrolled');\n";
    s += '            lastY = y;\n';
    s += '        });\n';
    s += '    }\n\n';

    // IMAGE FALLBACKS
    s += '    function initImageFallbacks() {\n';
    s += "        document.querySelectorAll('img').forEach(function(img) {\n";
    s += "            img.addEventListener('error', function() {\n";
    s += "                this.src = base + 'logo.png';\n";
    s += "                this.style.objectFit = 'contain';\n";
    s += "                this.style.padding = '20px';\n";
    s += '            });\n';
    s += '        });\n';
    s += '    }\n\n';

    // WEATHER
    s += '    function initWeatherWidget() {\n';
    s += "        var iconEl = document.getElementById('weather-icon');\n";
    s += "        var cityEl = document.getElementById('weather-city');\n";
    s += "        var tempEl = document.getElementById('weather-temp');\n";
    s += '        if (!iconEl && !tempEl) return;\n\n';
    s += '        function toEmoji(code) {\n';
    s += "            if (!code) return '\\u{1F324}';\n";
    s += '            var c = String(code).toLowerCase();\n';
    s += "            if (c.includes('clear') || c.includes('sunny') || c==='01d' || c==='01n') return '\\u2600\\uFE0F';\n";
    s += "            if (c.includes('cloud') || c==='03d' || c==='04d') return '\\u26C5';\n";
    s += "            if (c.includes('rain') || c==='10d') return '\\u{1F327}';\n";
    s += "            if (c.includes('thunder') || c==='11d') return '\\u26C8';\n";
    s += "            if (c.includes('snow') || c==='13d') return '\\u{1F328}';\n";
    s += "            if (c.includes('mist') || c.includes('fog') || c==='50d') return '\\u{1F32B}';\n";
    s += "            return '\\u{1F324}';\n";
    s += '        }\n\n';
    s += "        fetch('" + API_BASE + "/api/weather')\n";
    s += '            .then(function(r) { return r.json(); })\n';
    s += '            .then(function(data) {\n';
    s += '                if (!data) return;\n';
    s += "                if (iconEl) iconEl.textContent = toEmoji(data.icon || data.condition || '');\n";
    s += "                if (cityEl) cityEl.textContent = data.city || data.name || 'CDMX';\n";
    s += "                if (tempEl) tempEl.textContent = (data.temp !== undefined ? Math.round(data.temp) : '--') + '\\u00B0';\n";
    s += '            }).catch(function() {});\n';
    s += '    }\n\n';

    // TICKER
    s += '    function initBreakingTicker() {\n';
    s += "        fetch('" + API_BASE + "/api/ticker/headlines?limit=10')\n";
    s += '            .then(function(r) { return r.json(); })\n';
    s += '            .then(function(data) {\n';
    s += '                if (!Array.isArray(data) || data.length === 0) return;\n';
    s += "                var marquee = document.querySelector('.radio-bar marquee');\n";
    s += '                if (!marquee) return;\n';
    s += '                marquee.innerHTML = data.map(function(h) {\n';
    s += "                    var t = (h.TITULO||h.titulo||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');\n";
    s += "                    return '<span class=\"ticker-item\">' + t + '</span><span class=\"ticker-item\">&nbsp;\\u2022&nbsp;</span>';\n";
    s += "                }).join('');\n";
    s += '            }).catch(function() {});\n';
    s += '    }\n\n';

    // BOOT
    s += "    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);\n";
    s += '    else init();\n';
    s += '})();\n';

    return s;
}

function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

module.exports = genComponentsJS;
