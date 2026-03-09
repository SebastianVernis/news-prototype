/**
 * UNIFIED COMPONENTS - DEFINITIVE VERSION
 * Managed by Gemini CLI
 */
(function () {
    const siteConfig = {
        name: 'Capital Press',
        accentColor: '#A89F91',
        slug: 'capitalpress'
    };

    const path = window.location.pathname;
    const isSubdir = /\/(categoria|articulo|admin)\//.test(path);
    const base = isSubdir ? '../' : './';

    const TICKER_VARIANT = 'top';

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
<div id="preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:999999;display:flex;flex-direction:column;justify-content:center;align-items:center;background:#1A1A1A;">
    <div style="text-align:center;">
        <div style="margin-bottom:25px;position:relative;width:120px;height:120px;margin:0 auto 30px;">
            <div style="position:absolute;top:0;left:0;width:100%;height:100%;border:4px solid rgba(255,255,255,0.1);border-top:4px solid ${siteConfig.accentColor};border-radius:50%;animation:uni-spin 1s linear infinite;"></div>
            <img src="${base}logo-header.png" alt="${siteConfig.name}" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);height:60px;width:auto;filter:brightness(0) invert(1);">
        </div>
        <h2 style="font-family:'Inter',Arial,sans-serif;color:#fff;font-weight:700;letter-spacing:2px;text-transform:uppercase;font-size:1.2rem;margin:0;">${siteConfig.name}</h2>
        <p style="font-family:'Inter',Arial,sans-serif;color:${siteConfig.accentColor};font-weight:400;letter-spacing:4px;text-transform:uppercase;font-size:0.75rem;margin-top:10px;">Cargando contenido...</p>
    </div>
</div>
<style>
    @keyframes uni-spin { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
</style>`;

    // ── TICKER BAR (UNIFIED) ─────────────────────────────────────────────────
    const TICKER_HTML = `
<div id="unified-ticker-container" style="position:fixed;top:0;left:0;right:0;height:40px;background:#000;color:#fff;z-index:10001;display:flex;align-items:center;font-family:'Inter',sans-serif;border-bottom:1px solid ${siteConfig.accentColor};">
    <div style="background:${siteConfig.accentColor};color:#000;height:100%;display:flex;align-items:center;padding:0 15px;font-weight:800;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;flex-shrink:0;">
        AL MOMENTO
    </div>
    <div id="unified-ticker" style="flex:1;overflow:hidden;white-space:nowrap;display:flex;align-items:center;position:relative;height:100%;">
        <div class="ticker-scroll" style="display:inline-block;padding-left:100%;animation:ticker-swipe 180s linear infinite;white-space:nowrap;position:absolute;will-change:transform;">
            <span id="ticker-content">Cargando noticias y finanzas...</span>
        </div>
    </div>
    <div id="weather-widget" style="padding:0 15px;border-left:1px solid rgba(255,255,255,0.2);display:flex;align-items:center;gap:8px;font-size:0.8rem;background:#111;height:100%;flex-shrink:0;">
        <span id="weather-icon"></span>
        <span id="weather-city" style="font-weight:700;"></span>
        <span id="weather-temp"></span>
    </div>
</div>
<style>
    @keyframes ticker-swipe {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    .ticker-item-fin { margin-right: 30px; font-weight: 600; font-size: 0.8rem; }
    .ticker-item-news { margin-right: 30px; font-weight: 400; font-size: 0.8rem; }
    .up { color: #4CAF50; }
    .down { color: #F44336; }
    #unified-ticker:hover .ticker-scroll { animation-play-state: paused; }
    @media (max-width: 600px) {
        #weather-widget { display: none !important; }
    }
</style>`;

    // ── HEADER ───────────────────────────────────────────────────────────────
    const HEADER_HTML = `
<header class="header" style="margin-top:40px;background:linear-gradient(295deg, ${siteConfig.accentColor} 20%, #121826 100%);box-shadow:0 2px 10px rgba(0,0,0,0.18);position:sticky;top:40px;z-index:10000;">
    <div class="container" style="display:flex;align-items:center;justify-content:space-between;padding:10px 20px;max-width:1200px;margin:0 auto;position:relative;">
        <a href="${base}" style="display:block;z-index:1001;">
            <img src="${base}logo.png" alt="${siteConfig.name}" style="scale:2;height:50px;width:auto;filter:brightness(0) invert(1);">
        </a>

        <!-- Mobile Toggle -->
        <button id="mobile-toggle" style="display:none;background:none;border:none;color:#fff;font-size:1.5rem;cursor:pointer;z-index:1001;">
            <i class="fas fa-bars"></i>
        </button>

        <nav class="main-nav">
            <ul style="display:flex;gap:20px;list-style:none;margin:0;padding:0;">
                <li><a href="${base}" class="nav-link${cls(isHome)}" style="text-decoration:none;color:#f3f4f6;font-weight:700;font-size:0.82rem;text-transform:uppercase;letter-spacing:.5px;">Inicio</a></li>
                <li><a href="${base}categoria/nacional.html" class="nav-link${cls(isNacional)}" style="text-decoration:none;color:#f3f4f6;font-weight:700;font-size:0.82rem;text-transform:uppercase;letter-spacing:.5px;">Nacional</a></li>
                <li><a href="${base}categoria/politica.html" class="nav-link${cls(isPolitica)}" style="text-decoration:none;color:#f3f4f6;font-weight:700;font-size:0.82rem;text-transform:uppercase;letter-spacing:.5px;">Política</a></li>
                <li><a href="${base}categoria/economia.html" class="nav-link${cls(isEconomia)}" style="text-decoration:none;color:#f3f4f6;font-weight:700;font-size:0.82rem;text-transform:uppercase;letter-spacing:.5px;">Economía</a></li>
                <li><a href="${base}categoria/deportes.html" class="nav-link${cls(isDeportes)}" style="text-decoration:none;color:#f3f4f6;font-weight:700;font-size:0.82rem;text-transform:uppercase;letter-spacing:.5px;">Deportes</a></li>
            </ul>
        </nav>
    </div>
</header>
<style>
    @media (max-width: 900px) {
        #mobile-toggle { display: block !important; }
        .main-nav {
            position: fixed;
            top: 0;
            right: -100%;
            width: 250px;
            height: 100vh;
            background: #121826;
            padding: 80px 20px;
            transition: right 0.3s ease;
            box-shadow: -5px 0 15px rgba(0,0,0,0.5);
            z-index: 1000;
        }
        .main-nav.active { right: 0; }
        .main-nav ul { flex-direction: column; gap: 25px !important; }
        .main-nav ul li a { font-size: 1rem !important; }
    }
</style>`;

    // ── FOOTER ───────────────────────────────────────────────────────────────
    const FOOTER_HTML = `
<footer class="footer" style="background:#1a1a1a;color:#fff;padding:30px 0 15px;margin-top:40px;">
    <div class="container" style="max-width:1200px;margin:0 auto;padding:0 20px;display:grid;grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));gap:30px;">
        <div class="footer-column">
            <img src="${base}logo-header.png" alt="${siteConfig.name}" style="height:40px;filter:brightness(0) invert(1);margin-bottom:20px;">
            <p style="color:#aaa;font-size:0.9rem;line-height:1.6;">Líderes en información digital. Noticias de última hora, política, economía y más.</p>
        </div>
        <div class="footer-column">
            <h4 style="color:${siteConfig.accentColor};text-transform:uppercase;margin-bottom:20px;font-size:1rem;">Secciones</h4>
            <ul style="list-style:none;padding:0;margin:0;display:grid;grid-template-columns: 1fr 1fr;gap:10px;">
                <li><a href="${base}categoria/nacional.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Nacional</a></li>
                <li><a href="${base}categoria/politica.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Política</a></li>
                <li><a href="${base}categoria/economia.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Economía</a></li>
                <li><a href="${base}categoria/deportes.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Deportes</a></li>
                <li><a href="${base}categoria/cultura.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Cultura</a></li>
                <li><a href="${base}categoria/tecnologia.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Tecnología</a></li>
            </ul>
        </div>
        <div class="footer-column">
            <h4 style="color:${siteConfig.accentColor};text-transform:uppercase;margin-bottom:20px;font-size:1rem;">Legal</h4>
            <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px;">
                <li><a href="${base}acerca-de.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Acerca de</a></li>
                <li><a href="${base}contacto.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Contacto</a></li>
                <li><a href="${base}privacidad.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Privacidad</a></li>
                <li><a href="${base}terminos.html" style="color:#ccc;text-decoration:none;font-size:0.9rem;">Términos</a></li>
            </ul>
        </div>
    </div>
    <div style="max-width:1200px;margin:40px auto 0;padding:20px;border-top:1px solid rgba(255,255,255,0.1);text-align:center;color:#666;font-size:0.8rem;">
        &copy; ${new Date().getFullYear()} ${siteConfig.name}. Todos los derechos reservados.
    </div>
</footer>`;

    // ── INJECTION ────────────────────────────────────────────────────────────
    function inject() {
        // Preloader
        const preloaderPlaceholder = document.getElementById('site-preloader');
        if (preloaderPlaceholder) preloaderPlaceholder.outerHTML = PRELOADER_HTML;
        else document.body.insertAdjacentHTML('afterbegin', PRELOADER_HTML);

        // Ticker
        document.body.insertAdjacentHTML('afterbegin', TICKER_HTML);

        // Header
        const headerPlaceholder = document.getElementById('site-header');
        if (headerPlaceholder) headerPlaceholder.outerHTML = HEADER_HTML;
        else {
            const main = document.querySelector('main');
            if (main) main.insertAdjacentHTML('beforebegin', HEADER_HTML);
            else document.body.insertAdjacentHTML('afterbegin', HEADER_HTML);
        }

        // Footer
        const footerPlaceholder = document.getElementById('site-footer');
        if (footerPlaceholder) footerPlaceholder.outerHTML = FOOTER_HTML;
        else document.body.insertAdjacentHTML('beforeend', FOOTER_HTML);

        initTickerData();
        initWeatherData();
        initImageFallbacks();
        initMobileMenu();

        window.addEventListener('load', () => {
            setTimeout(() => {
                const pre = document.getElementById('preloader');
                if (pre) {
                    pre.style.transition = 'opacity 0.5s ease';
                    pre.style.opacity = '0';
                    setTimeout(() => pre.remove(), 600);
                }
            }, 1000);
        });
    }

    function initMobileMenu() {
        const toggle = document.getElementById('mobile-toggle');
        const nav = document.querySelector('.main-nav');
        if (toggle && nav) {
            toggle.addEventListener('click', () => {
                nav.classList.toggle('active');
                toggle.querySelector('i').classList.toggle('fa-bars');
                toggle.querySelector('i').classList.toggle('fa-times');
            });
        }
    }

    // ── DATA FETCHING ────────────────────────────────────────────────────────
    async function initTickerData() {
        const contentEl = document.getElementById('ticker-content');
        if (!contentEl) return;

        try {
            const [finRes, newsRes] = await Promise.all([
                fetch('https://news-api.sebastianvernis.workers.dev/api/ticker/financials'),
                fetch('https://news-api.sebastianvernis.workers.dev/api/ticker/headlines?limit=10')
            ]);

            const financials = await finRes.json();
            const headlines = await newsRes.json();

            let tickerHTML = '';

            // Mix Financials
            if (Array.isArray(financials)) {
                financials.forEach(f => {
                    const changeClass = parseFloat(f.CAMBIO) >= 0 ? 'up' : 'down';
                    const icon = parseFloat(f.CAMBIO) >= 0 ? '▲' : '▼';
                    tickerHTML += `<span class="ticker-item-fin">${f.SIMBOLO}: ${f.VALOR} <span class="${changeClass}">${icon} ${f.CAMBIO}</span></span>`;
                });
            }

            // Mix Headlines
            if (Array.isArray(headlines)) {
                headlines.forEach(h => {
                    tickerHTML += `<span class="ticker-item-news"><span style="color:${siteConfig.accentColor};">+++</span> ${h.TITULO}</span>`;
                });
            }

            contentEl.innerHTML = tickerHTML + tickerHTML; // Duplicate for seamless scroll
        } catch (e) {
            contentEl.textContent = 'Bienvenido a ' + siteConfig.name + ' - Información las 24 horas';
        }
    }

    async function initWeatherData() {
        const iconEl = document.getElementById('weather-icon');
        const cityEl = document.getElementById('weather-city');
        const tempEl = document.getElementById('weather-temp');
        if (!cityEl) return;

        try {
            const res = await fetch('https://news-api.sebastianvernis.workers.dev/api/weather');
            const data = await res.json();
            if (data) {
                cityEl.textContent = data.city || 'CDMX';
                tempEl.textContent = Math.round(data.temp || 0) + '°C';
                
                const desc = (data.description || '').toLowerCase();
                let icon = '🌤️';
                if (desc.includes('rain')) icon = '🌧️';
                else if (desc.includes('cloud')) icon = '☁️';
                else if (desc.includes('clear')) icon = '☀️';
                else if (desc.includes('storm')) icon = '⛈️';
                
                iconEl.textContent = icon;
                iconEl.title = data.description;
            }
        } catch (e) {}
    }

    // ── IMAGE FALLBACKS ──────────────────────────────────────────────────────
    function initImageFallbacks() {
        const logoSrc = base + 'logo.png';
        const apply = (img) => {
            img.onerror = () => {
                img.src = logoSrc;
                img.style.objectFit = 'contain';
                img.style.padding = '10px';
                img.style.background = '#f5f5f5';
                img.onerror = null;
            };
        };
        document.querySelectorAll('img').forEach(apply);
        new MutationObserver(muts => {
            muts.forEach(m => m.addedNodes.forEach(n => {
                if (n.tagName === 'IMG') apply(n);
                else if (n.querySelectorAll) n.querySelectorAll('img').forEach(apply);
            }));
        }).observe(document.body, { childList: true, subtree: true });
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject);
    else inject();
})();
