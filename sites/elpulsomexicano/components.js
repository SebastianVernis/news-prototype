/**
 * UNIFIED COMPONENTS - DEFINITIVE VERSION
 * Managed by Gemini CLI
 */
(function () {
    const siteConfig = {
        name: 'El Pulso Mexicano',
        accentColor: '#EAFF00',
        slug: 'elpulsomexicano'
    };

    const path = window.location.pathname;
    const isSubdir = /\/(categoria|articulo|admin)\//.test(path);
    const base = isSubdir ? '../' : './';

    const TICKER_VARIANT = 'sidebar';

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
<div id="preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:999999;display:flex;flex-direction:column;justify-content:center;align-items:center;background:#000;">
    <div style="text-align:center;">
        <div style="margin-bottom:25px;position:relative;width:120px;height:120px;margin:0 auto 30px;background:#FF00FF;padding:10px;transform:rotate(5deg);border:4px solid #000;">
            <div style="position:absolute;top:0;left:0;width:100%;height:100%;border:4px solid #000;border-top:4px solid #fff;animation:uni-spin 0.5s steps(4) infinite;"></div>
            <img src="${base}logo-header.png" alt="${siteConfig.name}" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);height:60px;width:auto;">
        </div>
        <h2 style="font-family:'Impact',Arial,sans-serif;color:#EAFF00;font-weight:900;letter-spacing:2px;text-transform:uppercase;font-size:2rem;margin:0;text-shadow:4px 4px 0px #000;">${siteConfig.name}</h2>
    </div>
</div>
<style>
    @keyframes uni-spin { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }
</style>`;

    // ── TICKER BAR (UNIFIED) ─────────────────────────────────────────────────
    const TICKER_HTML = `
<div id="unified-ticker-container" style="position:fixed;bottom:0;left:0;right:0;height:45px;background:#000;color:#fff;z-index:10001;display:flex;align-items:center;font-family:'Impact',sans-serif;border-top:4px solid ${siteConfig.accentColor};">
    <div style="background:${siteConfig.accentColor};color:#000;height:100%;display:flex;align-items:center;padding:0 20px;font-weight:900;font-size:1.1rem;text-transform:uppercase;letter-spacing:1px;flex-shrink:0;transform:skewX(-10deg);margin-left:-10px;">
        <span style="transform:skewX(10deg);padding-left:10px;">AL MOMENTO</span>
    </div>
    <div id="unified-ticker" style="flex:1;overflow:hidden;white-space:nowrap;display:flex;align-items:center;position:relative;height:100%;">
        <div class="ticker-scroll" style="display:inline-block;padding-left:100%;animation:ticker-swipe 240s linear infinite;white-space:nowrap;position:absolute;will-change:transform;">
            <span id="ticker-content">Cargando noticias y finanzas...</span>
        </div>
    </div>
    <div id="weather-widget" style="padding:0 20px;border-left:4px solid #fff;display:flex;align-items:center;gap:10px;font-size:1rem;background:#000;height:100%;flex-shrink:0;font-weight:900;">
        <span id="weather-icon"></span>
        <span id="weather-city" style="color:${siteConfig.accentColor};"></span>
        <span id="weather-temp"></span>
    </div>
</div>
<style>
    @keyframes ticker-swipe {
        0% { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    .ticker-item-fin { margin-right: 60px; font-weight: 300; letter-spacing: 4px; font-size: 1rem; color: #fff; }
    .ticker-item-news { margin-right: 60px; font-weight: 300; letter-spacing: 4px; font-size: 1rem; color: ${siteConfig.accentColor}; text-transform: uppercase; }
    .up { color: #0f0 !important; }
    .down { color: #f00 !important; }
    #unified-ticker:hover .ticker-scroll { animation-play-state: paused; }
    @media (max-width: 700px) {
        #weather-widget { display: none !important; }
    }
</style>`;

    // ── HEADER ───────────────────────────────────────────────────────────────
    const HEADER_HTML = `
<header class="header" style="margin-top:0;background:#FF00FF;border-bottom:6px solid #000;position:sticky;top:0;z-index:10000;padding:15px 20px;">
    <div class="container" style="display:flex;align-items:center;justify-content:space-between;max-width:1400px;margin:0 auto;position:relative;">
        <a href="${base}" style="display:block;z-index:1001;background:#000;padding:10px;transform:rotate(-2deg);box-shadow:8px 8px 0px #fff;">
            <img src="${base}logo.png" alt="${siteConfig.name}" style="scale:2;height:45px;width:auto;">
        </a>

        <!-- Mobile Toggle -->
        <button id="mobile-toggle" style="display:none;background:#000;border:none;color:#fff;padding:10px 15px;font-size:1.5rem;cursor:pointer;z-index:1001;box-shadow:4px 4px 0px #fff;">
            <i class="fas fa-bars"></i>
        </button>

        <nav class="main-nav">
            <ul style="display:flex;gap:25px;list-style:none;margin:0;padding:0;">
                <li><a href="${base}" class="nav-link${cls(isHome)}" style="text-decoration:none;color:#000;font-weight:900;font-size:1.4rem;text-transform:uppercase;text-shadow:2px 2px 0px #fff;">Inicio</a></li>
                <li><a href="${base}categoria/nacional.html" class="nav-link${cls(isNacional)}" style="text-decoration:none;color:#000;font-weight:900;font-size:1.4rem;text-transform:uppercase;text-shadow:2px 2px 0px #fff;">Nacional</a></li>
                <li><a href="${base}categoria/politica.html" class="nav-link${cls(isPolitica)}" style="text-decoration:none;color:#000;font-weight:900;font-size:1.4rem;text-transform:uppercase;text-shadow:2px 2px 0px #fff;">Política</a></li>
                <li><a href="${base}categoria/economia.html" class="nav-link${cls(isEconomia)}" style="text-decoration:none;color:#000;font-weight:900;font-size:1.4rem;text-transform:uppercase;text-shadow:2px 2px 0px #fff;">Economía</a></li>
                <li><a href="${base}categoria/deportes.html" class="nav-link${cls(isDeportes)}" style="text-decoration:none;color:#000;font-weight:900;font-size:1.4rem;text-transform:uppercase;text-shadow:2px 2px 0px #fff;">Deportes</a></li>
            </ul>
        </nav>
    </div>
</header>
<style>
    @media (max-width: 950px) {
        #mobile-toggle { display: block !important; }
        .main-nav {
            position: fixed;
            top: 0;
            right: -100%;
            width: 100%;
            height: 100vh;
            background: #EAFF00;
            padding: 120px 40px;
            transition: right 0.3s steps(4);
            z-index: 1000;
            border-left: 10px solid #000;
        }
        .main-nav.active { right: 0; }
        .main-nav ul { flex-direction: column; gap: 30px !important; }
        .main-nav ul li a { font-size: 2.5rem !important; }
    }
</style>`;

    // ── FOOTER ───────────────────────────────────────────────────────────────
    const FOOTER_HTML = `
<footer class="footer" style="background:#000;color:#EAFF00;padding:80px 20px;margin-top:100px;border-top:10px solid #FF00FF;">
    <div class="container" style="max-width:1400px;margin:0 auto;display:grid;grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));gap:60px;">
        <div class="footer-column">
            <img src="${base}logo-header.png" alt="${siteConfig.name}" style="height:60px;margin-bottom:30px;background:#fff;padding:10px;transform:rotate(3deg);">
            <p style="font-size:1.5rem;line-height:1.2;font-weight:900;text-transform:uppercase;">LA VERDAD SIN FILTROS. EL PULSO DE MÉXICO EN TUS MANOS.</p>
        </div>
        <div class="footer-column">
            <h4 style="text-transform:uppercase;margin-bottom:30px;font-size:2rem;font-weight:900;background:#EAFF00;color:#000;display:inline-block;padding:5px 15px;">Secciones</h4>
            <ul style="list-style:none;padding:0;margin:0;display:grid;grid-template-columns: 1fr;gap:15px;">
                <li><a href="${base}categoria/nacional.html" style="color:#EAFF00;text-decoration:none;font-size:1.4rem;font-weight:900;text-transform:uppercase;">> Nacional</a></li>
                <li><a href="${base}categoria/politica.html" style="color:#EAFF00;text-decoration:none;font-size:1.4rem;font-weight:900;text-transform:uppercase;">> Política</a></li>
                <li><a href="${base}categoria/economia.html" style="color:#EAFF00;text-decoration:none;font-size:1.4rem;font-weight:900;text-transform:uppercase;">> Economía</a></li>
                <li><a href="${base}categoria/deportes.html" style="color:#EAFF00;text-decoration:none;font-size:1.4rem;font-weight:900;text-transform:uppercase;">> Deportes</a></li>
            </ul>
        </div>
        <div class="footer-column">
            <h4 style="text-transform:uppercase;margin-bottom:30px;font-size:2rem;font-weight:900;background:#fff;color:#000;display:inline-block;padding:5px 15px;">Legal</h4>
            <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:15px;">
                <li><a href="${base}acerca-de.html" style="color:#EAFF00;text-decoration:none;font-size:1.2rem;font-weight:900;text-transform:uppercase;">Acerca de</a></li>
                <li><a href="${base}contacto.html" style="color:#EAFF00;text-decoration:none;font-size:1.2rem;font-weight:900;text-transform:uppercase;">Contacto</a></li>
                <li><a href="${base}privacidad.html" style="color:#EAFF00;text-decoration:none;font-size:1.2rem;font-weight:900;text-transform:uppercase;">Privacidad</a></li>
                <li><a href="${base}terminos.html" style="color:#EAFF00;text-decoration:none;font-size:1.2rem;font-weight:900;text-transform:uppercase;">Términos</a></li>
            </ul>
        </div>
    </div>
    <div style="margin-top:80px;text-align:center;font-size:1.2rem;font-weight:900;text-transform:uppercase;letter-spacing:4px;background:#EAFF00;color:#000;padding:10px;">
        &copy; ${new Date().getFullYear()} ${siteConfig.name}. BRUTAL NEWS.
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
                fetch('https://cms-nuevos.sebastianvernis.workers.dev/api/ticker/financials'),
                fetch('https://cms-nuevos.sebastianvernis.workers.dev/api/ticker/headlines?limit=10')
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
            const res = await fetch('https://cms-nuevos.sebastianvernis.workers.dev/api/weather');
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
