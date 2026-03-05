(function(){
    var p=window.location.pathname;
    var isSubdir=/\/(categoria|articulo|admin)\//.test(p);
    var base=isSubdir?"../":"./";

    var accentColor = "#DC2626";
    var siteName = "México360Noticias";

    // TICKER DATA
    async function initTicker() {
        const tickerContainer = document.getElementById('unified-ticker');
        if (!tickerContainer) return;

        try {
            const [fin, head, weath] = await Promise.all([
                fetch('https://news-api.sebastianvernis.workers.dev/api/ticker/financials').then(r => r.json()),
                fetch('https://news-api.sebastianvernis.workers.dev/api/ticker/headlines?limit=10').then(r => r.json()),
                fetch('https://news-api.sebastianvernis.workers.dev/api/weather').then(r => r.json())
            ]);

            let html = '<div class="ticker-wrapper">';
            
            // Financials
            fin.forEach(f => {
                const color = f.TENDENCIA === 'up' ? '#4ade80' : '#f87171';
                html += '<span class="ticker-item"><strong>' + f.SIMBOLO + '</strong> ' + f.VALOR + ' <span style="color:' + color + '">' + f.CAMBIO + '</span></span>';
            });

            // Headlines
            head.forEach(h => {
                html += '<span class="ticker-item">+++ ' + h.TITULO.toUpperCase() + '</span>';
            });

            html += '</div>';

            // Weather (Fixed at the end)
            if (weath) {
                html += '<div class="weather-item">' + weath.city + ': ' + weath.temp + '°C ' + weath.description + '</div>';
            }

            tickerContainer.innerHTML = html;
        } catch (e) {
            tickerContainer.innerHTML = '<span>Error al cargar noticias de última hora</span>';
        }
    }

    var style = document.createElement('style');
    style.textContent = '#unified-ticker-container { background: #000; color: #fff; height: 40px; display: flex; align-items: center; font-family: sans-serif; font-size: 13px; overflow: hidden; border-bottom: 1px solid ' + accentColor + '; position: relative; z-index: 1001; }' +
        '#unified-ticker { display: flex; align-items: center; width: 100%; padding: 0 20px; }' +
        '.ticker-wrapper { display: flex; white-space: nowrap; animation: ticker-scroll 60s linear infinite; flex-grow: 1; }' +
        '.ticker-item { margin-right: 40px; display: flex; align-items: center; gap: 5px; }' +
        '.weather-item { background: ' + accentColor + '; color: #fff; padding: 0 15px; height: 100%; display: flex; align-items: center; font-weight: bold; white-space: nowrap; position: relative; z-index: 2; }' +
        '@keyframes ticker-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }' +
        '.site-preloader { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 99999; transition: opacity 0.5s ease; }' +
        '.loader-ring { width: 80px; height: 80px; border: 4px solid #f3f3f3; border-top: 4px solid ' + accentColor + '; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px; }' +
        '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';
    document.head.appendChild(style);

    var PRE = '<div class="site-preloader" id="preloader-overlay">' +
        '<div class="loader-ring"></div>' +
        '<img src="' + base + 'logo.png" style="height:60px;margin-bottom:10px;">' +
        '<h2 style="color:#333;font-family:sans-serif;letter-spacing:2px;text-transform:uppercase;font-size:14px;">' + siteName + '</h2>' +
        '</div>';

    var HDR = '<div id="unified-ticker-container"><div id="unified-ticker">Cargando...</div></div>' +
        '<header style="background:#fff; border-bottom:2px solid ' + accentColor + '; position:sticky; top:0; z-index:1000; box-shadow:0 2px 10px rgba(0,0,0,0.1);">' +
        '<div style="max-width:1200px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; padding:10px 20px;">' +
        '<a href="' + base + 'index.html"><img src="' + base + 'logo.png" style="height:45px;"></a>' +
        '<nav style="display:flex; gap:15px;">' +
        ['Nacional', 'Política', 'Economía', 'Deportes', 'Cultura', 'Tecnología'].map(function(c) {
            return '<a href="' + base + 'categoria/' + c.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "") + '.html" style="text-decoration:none; color:#333; font-weight:bold; font-size:13px; text-transform:uppercase; font-family:sans-serif;">' + c + '</a>';
        }).join('') +
        '</nav></div></header>';

    var FTR = '<footer style="background:#111; color:#ccc; padding:50px 20px; font-family:sans-serif; font-size:14px;">' +
        '<div style="max-width:1200px; margin:0 auto; display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:40px;">' +
        '<div><img src="' + base + 'logo.png" style="height:50px; filter:brightness(0) invert(1); margin-bottom:20px;"><p>Tu conexión directa con la realidad. Información veraz y oportuna las 24 horas.</p></div>' +
        '<div><h4 style="color:#fff; margin-bottom:15px; text-transform:uppercase;">Secciones</h4>' +
        ['Nacional', 'Política', 'Economía', 'Deportes', 'Cultura', 'Tecnología'].map(function(c) {
            return '<a href="' + base + 'categoria/' + c.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "") + '.html" style="display:block; color:#999; text-decoration:none; margin-bottom:8px;">' + c + '</a>';
        }).join('') + '</div>' +
        '<div><h4 style="color:#fff; margin-bottom:15px; text-transform:uppercase;">Legal</h4>' +
        '<a href="'+base+'privacidad.html" style="display:block; color:#999; text-decoration:none; margin-bottom:8px;">Privacidad</a>' +
        '<a href="'+base+'terminos.html" style="display:block; color:#999; text-decoration:none; margin-bottom:8px;">Términos</a>' +
        '<a href="'+base+'contacto.html" style="display:block; color:#999; text-decoration:none; margin-bottom:8px;">Contacto</a></div>' +
        '</div><div style="text-align:center; margin-top:40px; padding-top:20px; border-top:1px solid #222;">© 2026 ' + siteName + '. Todos los derechos reservados.</div></footer>';

    function inject(){
        var p = document.getElementById('site-preloader'); if(p) p.outerHTML = PRE;
        var h = document.getElementById('site-header'); if(h) h.outerHTML = HDR;
        var f = document.getElementById('site-footer'); if(f) f.outerHTML = FTR;
        
        initTicker();

        setTimeout(function() {
            var over = document.getElementById('preloader-overlay');
            if(over) { over.style.opacity = '0'; setTimeout(function() { over.parentNode && over.parentNode.removeChild(over); }, 500); }
        }, 1200);

        var imgs = document.getElementsByTagName('img');
        for(var i=0; i<imgs.length; i++) {
            imgs[i].onerror = function() { if(this.src !== base + 'logo.png') this.src = base + 'logo.png'; };
        }
    }

    if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject);
    else inject();
})();