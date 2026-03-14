/**
 * Noticias Objetivo - Componentes Compartidos
 * Header, Footer y Preloader inyectados dinámicamente
 */
(function () {
    const path = window.location.pathname;
    const isSubdir = /\/(categoria|articulo|admin)\//.test(path);
    const base = isSubdir ? '../' : './';

    const p = path.toLowerCase();
    const isNacional   = p.includes('nacional');
    const isPolitica   = p.includes('politica');
    const isEconomia   = p.includes('economia');
    const isDeportes   = p.includes('deportes');
    const isCultura    = p.includes('cultura');
    const isTecnologia = p.includes('tecnologia');
    const isHome       = !isNacional && !isPolitica && !isEconomia && !isDeportes && !isCultura && !isTecnologia;
    function cls(cond) { return cond ? ' active' : ''; }

    // ── PRELOADER: slide-down (cortinas) ─────────────────────────────────────
    const PRELOADER_HTML = `
<div id="site-preloader" class="no-preloader">
    <div class="no-curtain no-curtain-top"></div>
    <div class="no-curtain no-curtain-bottom"></div>
    <div class="no-preloader-logo">
        <img src="${base}logo-header.png" alt="Noticias Objetivo">
    </div>
</div>
<style>
.no-preloader {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 99999;
    pointer-events: all;
}
.no-curtain {
    position: absolute;
    left: 0;
    width: 100%;
    height: 50%;
    background: linear-gradient(135deg, #010B1C 0%, #0D334D 100%);
    transition: transform 0.85s cubic-bezier(0.77, 0, 0.175, 1);
}
.no-curtain-top  { top: 0; }
.no-curtain-bottom { bottom: 0; }
.no-preloader.loaded .no-curtain-top    { transform: translateY(-100%); }
.no-preloader.loaded .no-curtain-bottom { transform: translateY(100%); }
.no-preloader-logo {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1;
    transition: opacity 0.3s ease;
    text-align: center;
}
.no-preloader.loaded .no-preloader-logo { opacity: 0; }
.no-preloader-logo img {
    height: 80px;
    width: auto;
    object-fit: contain;
    filter: brightness(0) invert(1);
    animation: no-pulse 1.5s ease-in-out infinite;
}
@keyframes no-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.7; transform: scale(1.05); }
}
</style>`;

    // ── FINANCE TICKER ───────────────────────────────────────────────────────
    const FINANCE_TICKER_HTML = `
<div class="finance-ticker" id="finance-ticker">
    <span class="finance-ticker-label"><i class="fas fa-chart-line"></i> MERCADOS</span>
    <div class="finance-ticker-display">
        <span class="finance-ticker-value" id="finance-ticker-value"></span>
    </div>
    <div class="ticker-weather" id="ticker-weather">
        <span id="weather-icon">🌤</span>
        <span id="weather-city">CDMX</span>
        <span id="weather-temp">--°</span>
    </div>
</div>
<style>
.finance-ticker{background:rgba(10,10,10,0.9);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);
display:flex;align-items:center;height:30px;padding:0 16px;gap:12px;
border-bottom:1px solid rgba(255,255,255,0.07);}
.finance-ticker-label{font-family:'Noto Sans',Arial,sans-serif;font-size:0.6rem;font-weight:800;
letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.45);white-space:nowrap;
flex-shrink:0;border-right:1px solid rgba(255,255,255,0.12);padding-right:12px;}
.finance-ticker-display{flex:1;overflow:hidden;display:flex;align-items:center;}
.finance-ticker-value{font-family:'Noto Sans',Arial,sans-serif;font-size:0.76rem;
color:rgba(255,255,255,0.85);transition:opacity 0.3s ease;white-space:nowrap;}
.finance-ticker-value strong{color:#fff;font-weight:700;}
.ft-up{color:#48bb78;font-size:0.7rem;margin-left:4px;}
.ft-down{color:#fc8181;font-size:0.7rem;margin-left:4px;}
.ticker-weather{display:flex;align-items:center;gap:5px;padding-left:12px;
border-left:1px solid rgba(255,255,255,0.12);flex-shrink:0;
font-family:'Noto Sans',Arial,sans-serif;font-size:0.74rem;white-space:nowrap;}
#weather-icon{font-size:0.9rem;line-height:1;}
#weather-city{font-weight:700;color:#fff;letter-spacing:0.5px;}
#weather-temp{color:rgba(255,255,255,0.7);}
</style>`;

    var STATIC_FINANCE_ITEMS = [
        { label: 'USD/MXN',      value: '$17.23',    change: '+0.12%', up: true  },
        { label: 'EUR/MXN',      value: '$18.91',    change: '-0.08%', up: false },
        { label: 'Oro',          value: '$2,345/oz', change: '+0.23%', up: true  },
        { label: 'IPC BMV',      value: '54,231 pts',change: '+0.67%', up: true  },
        { label: 'Petróleo WTI', value: '$78.50/bbl',change: '-0.31%', up: false },
        { label: 'Bitcoin',      value: '$67,450',   change: '+1.24%', up: true  },
    ];

    function startFinanceRotation(items) {
        var current = 0;
        var el = document.getElementById('finance-ticker-value');
        if (!el) return;
        function update() {
            var item = items[current];
            el.style.opacity = '0';
            setTimeout(function () {
                el.innerHTML = '<strong>' + item.label + '</strong>: ' + item.value +
                    ' <span class="' + (item.up ? 'ft-up' : 'ft-down') + '">' +
                    (item.up ? '▲' : '▼') + ' ' + item.change + '</span>';
                el.style.opacity = '1';
            }, 300);
            current = (current + 1) % items.length;
        }
        update();
        setInterval(update, 3500);
    }

    // ── WEATHER WIDGET ───────────────────────────────────────────────────────
    function initWeatherWidget() {
        var iconEl = document.getElementById('weather-icon');
        var cityEl = document.getElementById('weather-city');
        var tempEl = document.getElementById('weather-temp');
        if (!cityEl && !tempEl) return;

        function toEmoji(code) {
            if (!code) return '🌤';
            var c = String(code).toLowerCase();
            if (c === '01d' || c === '01n' || c.includes('clear') || c.includes('sunny')) return '☀️';
            if (c === '02d' || c === '02n' || c.includes('few')) return '🌤';
            if (c === '03d' || c === '04d' || c === '03n' || c === '04n' || c.includes('cloud')) return '⛅';
            if (c === '09d' || c === '09n' || c.includes('drizzle')) return '🌦';
            if (c === '10d' || c === '10n' || c.includes('rain')) return '🌧';
            if (c === '11d' || c === '11n' || c.includes('thunder')) return '⛈';
            if (c === '13d' || c === '13n' || c.includes('snow')) return '🌨';
            if (c === '50d' || c === '50n' || c.includes('mist') || c.includes('fog')) return '🌫';
            return '🌤';
        }

        fetch('https://news-api.sebastianvernis.workers.dev/api/weather')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (!data) return;
                if (iconEl) iconEl.textContent = toEmoji(data.icon || data.condition || data.weather_code || '');
                if (cityEl) cityEl.textContent = data.city || data.name || 'CDMX';
                if (tempEl) tempEl.textContent = (data.temp !== undefined ? Math.round(data.temp) : '--') + '°';
            })
            .catch(function() {});
    }

    function initFinanceTicker() {
        var el = document.getElementById('finance-ticker-value');
        if (!el) return;
        startFinanceRotation(STATIC_FINANCE_ITEMS);
        fetch('https://news-api.sebastianvernis.workers.dev/api/ticker/financials')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (!Array.isArray(data) || data.length === 0) return;
                var liveItems = data.map(function(d) {
                    return { label: d.NOMBRE, value: d.VALOR, change: d.CAMBIO || '0.00%', up: d.TENDENCIA !== 'down' };
                });
                startFinanceRotation(liveItems);
            })
            .catch(function() {});
    }

    // ── HEADER ───────────────────────────────────────────────────────────────
    const HEADER_HTML = `
<header class="header">
    <div class="container header-container">
        <div class="logo-section">
            <a href="${base}index.html" style="display:block;line-height:0;">
                <img src="${base}logo-header.png" alt="Noticias Objetivo" class="site-logo">
            </a>
        </div>
        <nav class="main-nav">
            <a href="${base}index.html"                    class="nav-link${cls(isHome)}">Inicio</a>
            <a href="${base}categoria/nacional.html"       class="nav-link${cls(isNacional)}">Nacional</a>
            <a href="${base}categoria/politica.html"       class="nav-link${cls(isPolitica)}">Política</a>
            <a href="${base}categoria/economia.html"       class="nav-link${cls(isEconomia)}">Economía</a>
            <a href="${base}categoria/deportes.html"       class="nav-link${cls(isDeportes)}">Deportes</a>
            <a href="${base}categoria/cultura.html"        class="nav-link${cls(isCultura)}">Cultura</a>
            <a href="${base}categoria/tecnologia.html"     class="nav-link${cls(isTecnologia)}">Tecnología</a>
        </nav>
    </div>
</header>`;

    // ── FOOTER ───────────────────────────────────────────────────────────────
    const FOOTER_HTML = `
<footer class="footer" style="padding:24px 0 12px;">
    <div class="container">
        <div class="footer-grid cols-3" style="gap:16px;">
            <div class="footer-column">
                <div class="footer-logo">
                    <img src="${base}logo-header.png" alt="Noticias Objetivo">
                    <h3>Noticias Objetivo</h3>
                </div>
                <p class="footer-about" style="font-size:0.82rem;line-height:1.5;margin:8px 0 10px;">Periodismo objetivo e imparcial. La verdad sin filtros desde México.</p>
                <div class="social-links">
                    <a href="#" class="social-link" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" class="social-link" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                    <a href="#" class="social-link" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                    <a href="#" class="social-link" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
                </div>
            </div>
            <div class="footer-column">
                <h4 style="margin-bottom:8px;font-size:0.85rem;">Secciones</h4>
                <ul class="footer-links" style="display:grid;grid-template-columns:1fr 1fr;gap:3px 12px;">
                    <li><a href="${base}categoria/nacional.html">Nacional</a></li>
                    <li><a href="${base}categoria/politica.html">Política</a></li>
                    <li><a href="${base}categoria/economia.html">Economía</a></li>
                    <li><a href="${base}categoria/deportes.html">Deportes</a></li>
                    <li><a href="${base}categoria/cultura.html">Cultura</a></li>
                    <li><a href="${base}categoria/tecnologia.html">Tecnología</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h4 style="margin-bottom:8px;font-size:0.85rem;">Información</h4>
                <ul class="footer-links">
                    <li><a href="${base}acerca-de.html">Acerca de</a></li>
                    <li><a href="${base}contacto.html">Contacto</a></li>
                    <li><a href="${base}privacidad.html">Privacidad</a></li>
                    <li><a href="${base}terminos.html">Términos</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom" style="padding-top:10px;margin-top:0;">
            <p>&copy; 2026 Noticias Objetivo. Todos los derechos reservados.</p>
            <p class="disclaimer">Este sitio publica contenidos con fines informativos.</p>
        </div>
    </div>
</footer>`;

    // ── FIXED HEADER (siempre visible) ──────────────────────────────────────
    function initFixedHeader() {
        var s = document.createElement('style');
        s.id = 'header-fixed-css';
        s.textContent =
            '.header{position:fixed!important;top:0;left:0;right:0;z-index:9000;' +
            'box-shadow:0 4px 24px rgba(0,0,0,0.35);}' +
            '.breaking-news,.radio-bar,.finance-ticker{position:fixed!important;left:0;right:0;z-index:8999;}' +
            '#layout-spacer{display:block;width:100%;}' +
            '#mobile-hamburger{display:none;position:fixed;top:10px;right:14px;z-index:9002;' +
            'background:rgba(0,0,0,0.82);border:none;border-radius:8px;width:44px;height:44px;' +
            'cursor:pointer;flex-direction:column;align-items:center;justify-content:center;gap:5px;' +
            'box-shadow:0 2px 12px rgba(0,0,0,0.35);padding:0;}' +
            '#mobile-hamburger span{display:block;width:22px;height:2px;background:#fff;border-radius:2px;' +
            'transition:transform 0.3s ease,opacity 0.3s ease;}' +
            '#mobile-hamburger.is-open span:nth-child(1){transform:rotate(45deg) translate(5px,5px);}' +
            '#mobile-hamburger.is-open span:nth-child(2){opacity:0;}' +
            '#mobile-hamburger.is-open span:nth-child(3){transform:rotate(-45deg) translate(5px,-5px);}' +
            '@media(max-width:768px){' +
            '#mobile-hamburger{display:flex;}' +
            '.header .main-nav{flex-direction:column!important;width:100%!important;' +
            'max-height:0;overflow:hidden;transition:max-height 0.35s ease;padding:0!important;}' +
            '.header.header-nav-open .main-nav{max-height:320px;padding:8px 0!important;}' +
            '.header.header-nav-open .nav-link{padding:10px 16px!important;' +
            'border-bottom:1px solid rgba(255,255,255,0.08)!important;width:100%!important;}' +
            '}';
        document.head.appendChild(s);

        var spacer = document.createElement('div');
        spacer.id = 'layout-spacer';
        var main = document.querySelector('main');
        if (main) main.insertAdjacentElement('beforebegin', spacer);
        else document.body.insertAdjacentElement('afterbegin', spacer);

        var hb = document.createElement('button');
        hb.id = 'mobile-hamburger';
        hb.setAttribute('aria-label', 'Menú');
        hb.innerHTML = '<span></span><span></span><span></span>';
        document.body.appendChild(hb);

        var header = document.querySelector('.header');
        if (!header) return;

        function updateLayout() {
            var tickerEl = document.querySelector('.breaking-news') || document.querySelector('.radio-bar') || document.querySelector('.finance-ticker');
            var headerH = header.offsetHeight;
            var tickerH = tickerEl ? tickerEl.offsetHeight : 0;
            if (tickerEl) tickerEl.style.top = headerH + 'px';
            var totalOffset = headerH + tickerH;
            spacer.style.height = totalOffset + 'px';
            document.documentElement.style.setProperty('--layout-offset', totalOffset + 'px');
            hb.style.top = (totalOffset > 0 ? totalOffset + 4 : 10) + 'px';
        }

        var hamburgerOpen = false;
        hb.addEventListener('click', function () {
            hamburgerOpen = !hamburgerOpen;
            hb.classList.toggle('is-open', hamburgerOpen);
            header.classList.toggle('header-nav-open', hamburgerOpen);
            updateLayout();
        });

        window.addEventListener('load', updateLayout);
        window.addEventListener('resize', updateLayout);
        setTimeout(updateLayout, 100);
    }

    // ── IMAGE FALLBACK ───────────────────────────────────────────────────────
    function initImageFallbacks() {
        var logoSrc = base + 'logo.png';

        function applyFallback(img) {
            if (img.dataset.fallbackSet) return;
            img.dataset.fallbackSet = '1';
            img.addEventListener('error', function () {
                if (this.dataset.fallbackApplied) return;
                this.dataset.fallbackApplied = '1';
                this.src = logoSrc;
                this.style.objectFit = 'contain';
                this.style.padding = '16px';
                this.style.background = 'linear-gradient(160deg,#1A1A2E 0%,#16213E 100%)';
                this.style.opacity = '0.75';
            });
        }

        document.querySelectorAll('img').forEach(applyFallback);

        var observer = new MutationObserver(function (mutations) {
            mutations.forEach(function (mutation) {
                mutation.addedNodes.forEach(function (node) {
                    if (!node || node.nodeType !== 1) return;
                    if (node.tagName === 'IMG') {
                        applyFallback(node);
                    } else if (node.querySelectorAll) {
                        node.querySelectorAll('img').forEach(applyFallback);
                    }
                });
            });
        });

        if (document.body) {
            observer.observe(document.body, { childList: true, subtree: true });
        }
    }

    function replaceOrInject(id, html, fallbackFn) {
        const placeholder = document.getElementById(id);
        if (placeholder) { placeholder.outerHTML = html; }
        else { fallbackFn(html); }
    }

    function init() {
        replaceOrInject('site-preloader', PRELOADER_HTML, function(html) {
            document.body.insertAdjacentHTML('afterbegin', html);
        });
        replaceOrInject('site-header', HEADER_HTML, function(html) {
            const main = document.querySelector('main');
            if (main) main.insertAdjacentHTML('beforebegin', html);
            else document.body.insertAdjacentHTML('afterbegin', html);
        });
        replaceOrInject('site-footer', FOOTER_HTML, function(html) {
            const main = document.querySelector('main');
            if (main) main.insertAdjacentHTML('afterend', html);
            else document.body.insertAdjacentHTML('beforeend', html);
        });

        // Finance ticker + weather
        document.body.insertAdjacentHTML('afterbegin', FINANCE_TICKER_HTML);
        initFinanceTicker();
        initWeatherWidget();

        // Header fijo siempre visible
        initFixedHeader();

        // Image fallbacks (logo cuando imagen falla)
        initImageFallbacks();

        window.addEventListener('load', function () {
            setTimeout(function () {
                var pre = document.getElementById('site-preloader');
                if (pre) {
                    pre.classList.add('loaded');
                    setTimeout(function () {
                        if (pre.parentNode) pre.parentNode.removeChild(pre);
                    }, 1000);
                }
            }, 500);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else { init(); }
})();
