(function () {
    const HEADER_HTML = '<header class="site-header">' +
        '<div class="header-container">' +
            '<div class="logo-section">' +
                '<a href="/"><img src="https://placehold.co/400x100/000080/ffffff?text=RadioABC" alt="RadioABC"></a>' +
            '</div>' +
            '<nav class="main-nav">' +
                '<a href="/">Inicio</a>' +
                '<a href="/categoria/nacional.html">Nacional</a>' +
                '<a href="/categoria/politica.html">Política</a>' +
                '<a href="/categoria/economia.html">Economía</a>' +
                '<a href="/categoria/deportes.html">Deportes</a>' +
                '<a href="/categoria/espectaculos.html">Espectáculos</a>' +
            '</nav>' +
        '</div>' +
    '</header>';
    const FOOTER_HTML = '<footer class="site-footer">' +
        '<div class="footer-logo">' +
            '<img src="https://placehold.co/400x100/000080/ffffff?text=RadioABC" alt="RadioABC">' +
        '</div>' +
        '<div class="footer-links">' +
            '<a href="/acerca-de.html">Acerca de</a>' +
            '<a href="/contacto.html">Contacto</a>' +
            '<a href="/privacidad.html">Privacidad</a>' +
        '</div>' +
        '<p>&copy; ' + new Date().getFullYear() + ' RadioABC. Todos los derechos reservados.</p>' +
    '</footer>';
    document.addEventListener("DOMContentLoaded", () => {
        const preloader = document.getElementById("site-preloader");
        if(preloader) setTimeout(() => { preloader.classList.add("hidden"); setTimeout(() => preloader.style.display="none", 500); }, 800);

        const headerEl = document.getElementById('site-header');
        if(headerEl) headerEl.innerHTML = HEADER_HTML;
        const footerEl = document.getElementById('site-footer');
        if(footerEl) footerEl.innerHTML = FOOTER_HTML;
    });
})();
