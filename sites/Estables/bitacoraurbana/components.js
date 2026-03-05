/**
 * Bitácora Urbana - Componentes Compartidos
 * Header, Footer y Preloader inyectados dinámicamente en todas las páginas
 */
(function () {
    // ── Detectar ruta base según profundidad de la URL ──────────────────────
    const path = window.location.pathname;
    const isSubdir = /\/(categoria|articulo|admin)\//.test(path);
    const base = isSubdir ? '../' : './';

    // ── Detectar página activa para el nav ──────────────────────────────────
    const p = path.toLowerCase();
    const isNacional   = p.includes('nacional');
    const isPolitica   = p.includes('politica');
    const isEconomia   = p.includes('economia');
    const isDeportes   = p.includes('deportes');
    const isCultura    = p.includes('cultura');
    const isTecnologia = p.includes('tecnologia');
    const isHome       = !isNacional && !isPolitica && !isEconomia && !isDeportes && !isCultura && !isTecnologia;

    function cls(cond) { return cond ? ' active' : ''; }

    // ── PRELOADER ────────────────────────────────────────────────────────────
    const PRELOADER_HTML = `
<div id="preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:999999;display:flex;flex-direction:column;justify-content:center;align-items:center;background:linear-gradient(135deg,#1A1A1A 0%,#2D2D2D 40%,#1A1A1A 100%);">
    <div style="text-align:center;">
        <div style="margin-bottom:25px;animation:bu-spin3D 2s ease-in-out infinite;">
            <img src="${base}logo-header.png" alt="Bitácora Urbana" style="height:110px;width:auto;filter:brightness(0) invert(1);">
        </div>
        <div style="width:40px;height:40px;border:4px solid rgba(255,215,0,0.3);border-top:4px solid #FFD700;border-radius:50%;animation:bu-spin 1s linear infinite;margin:0 auto 20px;"></div>
        <p style="font-family:'Inter',Arial,sans-serif;color:#FFD700;font-weight:700;letter-spacing:3px;text-transform:uppercase;font-size:0.85rem;">Cargando...</p>
    </div>
</div>
<style>
    @keyframes bu-spin    { 0%{transform:rotate(0deg)}   100%{transform:rotate(360deg)} }
    @keyframes bu-spin3D  { 0%{transform:rotateY(0deg) scale(1)} 50%{transform:rotateY(180deg) scale(1.1)} 100%{transform:rotateY(360deg) scale(1)} }
</style>`;

    // ── HEADER ───────────────────────────────────────────────────────────────
    const HEADER_HTML = `
<header class="header">
    <div class="container header-container">
        <div class="logo-section">
            <a href="/" style="display:block;line-height:0;">
                <img src="${base}logo-header.png" alt="Bitácora Urbana" class="site-logo">
            </a>
        </div>
        <nav class="main-nav">
            <a href="/"                    class="nav-link${cls(isHome)}">Inicio</a>
            <a href="/categoria/nacional.html"       class="nav-link${cls(isNacional)}">Nacional</a>
            <a href="/categoria/politica.html"       class="nav-link${cls(isPolitica)}">Política</a>
            <a href="/categoria/economia.html"       class="nav-link${cls(isEconomia)}">Economía</a>
            <a href="/categoria/deportes.html"       class="nav-link${cls(isDeportes)}">Deportes</a>
            <a href="/categoria/cultura.html"        class="nav-link${cls(isCultura)}">Cultura</a>
            <a href="/categoria/tecnologia.html"     class="nav-link${cls(isTecnologia)}">Tecnología</a>
        </nav>
    </div>
</header>`;

    // ── TICKER (separado del header para quedar fijo) ─────────────────────
    const TICKER_HTML = `
<section class="breaking-news">
    <div class="breaking-weather" id="ticker-weather">
        <span id="weather-icon">🌤</span>
        <span id="weather-city">CDMX</span>
        <span id="weather-temp">--°</span>
    </div>
    <div class="breaking-ticker">
        <marquee behavior="scroll" direction="left" onmouseover="this.stop();" onmouseout="this.start();">
            <span class="ticker-item">Bienvenido a Bitácora Urbana &mdash; Información verificada las 24 horas</span>
            <span class="ticker-item">&nbsp;&bull;&nbsp;</span>
            <span class="ticker-item">Síguenos en redes sociales para más actualizaciones</span>
        </marquee>
    </div>
</section>
<style>
.breaking-weather{display:flex;align-items:center;gap:5px;padding:0 12px 0 8px;
border-right:1px solid rgba(255,255,255,0.18);flex-shrink:0;
font-family:'Noto Sans',Arial,sans-serif;font-size:0.74rem;white-space:nowrap;}
.breaking-weather #weather-icon{font-size:0.9rem;line-height:1;}
.breaking-weather #weather-city{font-weight:700;color:#fff;letter-spacing:0.5px;}
.breaking-weather #weather-temp{color:rgba(255,255,255,0.75);}
</style>`;

    // ── FOOTER ───────────────────────────────────────────────────────────────
    const FOOTER_HTML = `
<footer class="footer" style="padding:24px 0 12px;">
    <div class="container">
        <div class="footer-grid cols-3" style="gap:16px;">
            <div class="footer-column">
                <div class="footer-logo">
                    <img src="${base}logo-header.png" alt="Bitácora Urbana">
                    <h3>Bitácora Urbana</h3>
                </div>
                <p class="footer-about" style="font-size:0.82rem;line-height:1.5;margin:8px 0 10px;">Crónicas de la ciudad. Información veraz y oportuna.</p>
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
                    <li><a href="/categoria/nacional.html">Nacional</a></li>
                    <li><a href="/categoria/politica.html">Política</a></li>
                    <li><a href="/categoria/economia.html">Economía</a></li>
                    <li><a href="/categoria/deportes.html">Deportes</a></li>
                    <li><a href="/categoria/cultura.html">Cultura</a></li>
                    <li><a href="/categoria/tecnologia.html">Tecnología</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h4 style="margin-bottom:8px;font-size:0.85rem;">Información</h4>
                <ul class="footer-links">
                    <li><a href="/acerca-de.html">Acerca de</a></li>
                    <li><a href="/contacto.html">Contacto</a></li>
                    <li><a href="/privacidad.html">Privacidad</a></li>
                    <li><a href="/terminos.html">Términos</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom" style="padding-top:10px;margin-top:0;">
            <p>&copy; 2026 Bitácora Urbana. Todos los derechos reservados.</p>
            <p class="disclaimer">Este sitio publica contenidos con fines informativos. Las opiniones expresadas pertenecen a sus autores.</p>
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
            '.breaking-news,.radio-bar{position:fixed!important;left:0;right:0;z-index:8999;}' +
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
            var tickerEl = document.querySelector('.breaking-news') || document.querySelector('.radio-bar');
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
                this.style.background = 'linear-gradient(160deg,#1A1A1A 0%,#2D2D2D 100%)';
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

    // ── INYECCIÓN ────────────────────────────────────────────────────────────
    function replaceOrInject(id, html, fallbackFn) {
        const placeholder = document.getElementById(id);
        if (placeholder) {
            placeholder.outerHTML = html;
        } else {
            fallbackFn(html);
        }
    }

    function init() {
        // Preloader
        replaceOrInject('site-preloader', PRELOADER_HTML, function(html) {
            document.body.insertAdjacentHTML('afterbegin', html);
        });

        // Header
        replaceOrInject('site-header', HEADER_HTML, function(html) {
            const main = document.querySelector('main');
            if (main) main.insertAdjacentHTML('beforebegin', html);
            else document.body.insertAdjacentHTML('afterbegin', html);
        });

        // Ticker fijo (separado del header)
        document.body.insertAdjacentHTML('afterbegin', TICKER_HTML);

        // Footer
        replaceOrInject('site-footer', FOOTER_HTML, function(html) {
            const main = document.querySelector('main');
            if (main) main.insertAdjacentHTML('afterend', html);
            else document.body.insertAdjacentHTML('beforeend', html);
        });

        // Breaking news ticker dinámico + weather
        initBreakingTicker();
        initWeatherWidget();

        // Header fijo siempre visible
        initFixedHeader();

        // Image fallbacks (logo cuando imagen falla)
        initImageFallbacks();

        // Preloader: ocultar al cargar
        window.addEventListener('load', function () {
            setTimeout(function () {
                var pre = document.getElementById('preloader');
                if (pre) {
                    pre.style.transition = 'opacity 0.5s ease';
                    pre.style.opacity = '0';
                    setTimeout(function () { pre.style.display = 'none'; }, 500);
                }
            }, 800);
        });
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

    function initBreakingTicker() {
        fetch('https://news-api.sebastianvernis.workers.dev/api/ticker/headlines?limit=10')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (!Array.isArray(data) || data.length === 0) return;
                var marquee = document.querySelector('.breaking-ticker marquee') ||
                              document.querySelector('.radio-bar marquee');
                if (!marquee) return;
                marquee.innerHTML = data.map(function(h) {
                    var t = h.TITULO.replace(/&/g,'&amp;').replace(/</g,'<').replace(/>/g,'>');
                    return '<span class="ticker-item">' + t + '</span>' +
                           '<span class="ticker-item">&nbsp;&bull;&nbsp;</span>';
                }).join('');
            })
            .catch(function() {});
    }

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
