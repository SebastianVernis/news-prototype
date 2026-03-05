var { API_BASE } = require('./config');

// ── SCRIPT.JS ──
function genScriptJS() {
    return [
        '/* Carousel + Interaction Functionality */',
        'let currentSlide = 0;',
        'let autoPlayInterval;',
        '',
        'function initCarousel() {',
        '    const slides = document.querySelectorAll(".carousel-slide");',
        '    if (slides.length === 0) return;',
        '    showSlide(0);',
        '    startAutoPlay();',
        '    document.querySelector(".carousel-btn.prev")?.addEventListener("click", () => {',
        '        currentSlide = (currentSlide - 1 + slides.length) % slides.length;',
        '        showSlide(currentSlide); resetAutoPlay();',
        '    });',
        '    document.querySelector(".carousel-btn.next")?.addEventListener("click", () => {',
        '        currentSlide = (currentSlide + 1) % slides.length;',
        '        showSlide(currentSlide); resetAutoPlay();',
        '    });',
        '}',
        '',
        'function showSlide(index) {',
        '    const slides = document.querySelectorAll(".carousel-slide");',
        '    const dots = document.querySelectorAll(".carousel-dot");',
        '    slides.forEach(s => s.classList.remove("active"));',
        '    dots.forEach(d => d.classList.remove("active"));',
        '    if (slides[index]) slides[index].classList.add("active");',
        '    if (dots[index]) dots[index].classList.add("active");',
        '    currentSlide = index;',
        '}',
        '',
        'function startAutoPlay() {',
        '    autoPlayInterval = setInterval(() => {',
        '        const slides = document.querySelectorAll(".carousel-slide");',
        '        if (slides.length === 0) return;',
        '        currentSlide = (currentSlide + 1) % slides.length;',
        '        showSlide(currentSlide);',
        '    }, 5000);',
        '}',
        '',
        'function resetAutoPlay() { clearInterval(autoPlayInterval); startAutoPlay(); }',
        '',
        'document.querySelector(".carousel-main")?.addEventListener("mouseenter", () => clearInterval(autoPlayInterval));',
        'document.querySelector(".carousel-main")?.addEventListener("mouseleave", () => startAutoPlay());',
        '',
        'document.addEventListener("DOMContentLoaded", initCarousel);',
    ].join('\n');
}

// ── _REDIRECTS ──
function genRedirects(slug) {
    return [
        '# Proxy /api/* al worker de noticias',
        '/api/* ' + API_BASE + '/api/:splat 200',
        '',
        '# RSS Feed',
        '/rss.xml  /api/rss/' + slug + '  200',
        '/feed.xml /api/rss/' + slug + '  200',
    ].join('\n');
}

// ── WRANGLER.TOML ──
function genWrangler(slug) {
    return [
        'name = "' + slug + '"',
        'pages_build_output_dir = "."',
        'compatibility_date = "2024-01-01"',
        '',
        '[[d1_databases]]',
        'binding = "DB"',
        'database_name = "news_db"',
        'database_id = "039ec6ab-8f14-4e79-8f02-021df67a6c18"',
    ].join('\n');
}

// ── METADATA JSON ──
function genMetadata(site, colors) {
    return JSON.stringify({
        id: site.slug,
        name: site.name,
        category_default: 'General',
        facebook_page_id: '',
        theme: {
            primary: colors.primary,
            secondary: colors.bg,
            accent: colors.primary,
        },
        selectors: {
            container: '#news-container',
            template: 'card-modern'
        }
    }, null, 2);
}

module.exports = { genScriptJS, genRedirects, genWrangler, genMetadata };
