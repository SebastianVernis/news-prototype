/* Carousel + Interaction Functionality */
let currentSlide = 0;
let autoPlayInterval;

function initCarousel() {
    const slides = document.querySelectorAll(".carousel-slide");
    if (slides.length === 0) return;
    showSlide(0);
    startAutoPlay();
    document.querySelector(".carousel-btn.prev")?.addEventListener("click", () => {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide); resetAutoPlay();
    });
    document.querySelector(".carousel-btn.next")?.addEventListener("click", () => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide); resetAutoPlay();
    });
}

function showSlide(index) {
    const slides = document.querySelectorAll(".carousel-slide");
    const dots = document.querySelectorAll(".carousel-dot");
    slides.forEach(s => s.classList.remove("active"));
    dots.forEach(d => d.classList.remove("active"));
    if (slides[index]) slides[index].classList.add("active");
    if (dots[index]) dots[index].classList.add("active");
    currentSlide = index;
}

function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
        const slides = document.querySelectorAll(".carousel-slide");
        if (slides.length === 0) return;
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }, 5000);
}

function resetAutoPlay() { clearInterval(autoPlayInterval); startAutoPlay(); }

document.querySelector(".carousel-main")?.addEventListener("mouseenter", () => clearInterval(autoPlayInterval));
document.querySelector(".carousel-main")?.addEventListener("mouseleave", () => startAutoPlay());

document.addEventListener("DOMContentLoaded", initCarousel);

/* ========================================
   Carga de Artículos desde API
   ======================================== */
(function() {
    const SITE_SLUG = 'formulacdmx';
    const API_URL = `https://news-api.sebastianvernis.workers.dev/api/articles?site=${SITE_SLUG}&limit=20`;
    
    // Función para escapar HTML
    function esc(t) {
        if (!t) return '';
        return String(t)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }
    
    // Función para codificar URLs
    function enc(t) {
        return encodeURIComponent(t || '');
    }
    const HERO_CONFIG = {
        boominformativo: {
            root: '.hero-section',
            title: '.hero-text-box h1',
            excerpt: '.hero-text-box p',
            image: '.hero-img-box'
        },
        capitalpress: {
            root: '.focus-section',
            title: 'h1',
            excerpt: 'p',
            category: '.category-label',
            image: '.hero-image'
        },
        diarioexpress: {
            root: '.hero-section',
            title: '.hero-text h1',
            excerpt: '.hero-text p',
            category: '.hero-tag',
            image: '.hero-image'
        },
        elpulsomexicano: {
            root: '.hero-max',
            title: '.hero-text-block h1',
            excerpt: '.hero-text-block p',
            image: '.hero-max-img'
        },
        enfoquecapital: {
            root: '.left-pane .hero-content',
            title: 'h1',
            excerpt: 'p',
            category: '.category-label',
            image: '.portrait-img'
        },
        enfoquedirecto: {
            root: '.hero-cinematic',
            title: '.hero-content h1',
            category: '.category-tag',
            image: '.hero-image'
        },
        formulacdmx: {
            root: '.glass-panel.hero-card',
            title: '.hero-content h1',
            excerpt: '.hero-content p',
            category: '.category-pill',
            image: '.hero-img'
        },
        mexicantimes: {
            root: '.timeline-item.left',
            title: '.timeline-content h2',
            excerpt: '.timeline-content p',
            category: '.category-name',
            image: '.timeline-img'
        },
        mexico360noticias: {
            root: '.hero-article',
            title: 'h1',
            excerpt: '.hero-summary',
            image: '.corp-img'
        },
        mradio: {
            root: '.hero-section .neu-card.hero-content',
            title: 'h1',
            excerpt: 'p',
            category: '.category-neu',
            link: '.btn-neu'
        },
        noticiashorizonte: {
            root: '.z-pattern-section .z-row:first-child',
            title: '.z-content h1',
            excerpt: '.z-content p',
            category: '.z-content .category',
            image: '.z-image',
            link: '.btn-outline'
        },
        pulsodiario: {
            root: '.hero-article',
            title: '.hero-content h1',
            excerpt: '.hero-content p',
            image: '.hero-img'
        },
        puntoclave: {
            root: '.top-section .hero',
            title: 'h1',
            excerpt: 'p',
            image: '.hero-img'
        },
        puntonoticias: {
            root: '.hero-card',
            title: '.hero-content h1',
            excerpt: '.hero-content p',
            category: '.hero-content .tag',
            image: '.hero-img'
        },
        radarinformativo: {
            root: '.hero-tech',
            title: '.hero-content h1',
            excerpt: '.hero-content p',
            category: '.hero-content .tag',
            image: '.hero-img-container'
        },
        reportediario: {
            root: '.broadsheet-hero',
            title: '.hero-headline h1',
            excerpt: '.hero-headline h2',
            image: '.broadsheet-img'
        },
        televisionabc: {
            root: '.hero-fin > article',
            title: 'h1',
            excerpt: 'p',
            category: '.section-label',
            image: '.fin-img'
        }
    };

    const SITE_SLOTS = {
        formulacdmx: [
            { root: '.glass-grid .grid-card:nth-of-type(1)', title: 'h2', excerpt: 'p', image: '.card-img-placeholder' },
            { root: '.glass-grid .grid-card:nth-of-type(2)', title: 'h2', excerpt: 'p', image: '.card-img-placeholder' },
            { root: '.glass-grid .grid-card:nth-of-type(3)', title: 'h2', excerpt: 'p', image: '.card-img-placeholder' }
        ]
    };

    function setBackgroundImage(el, imageUrl) {
        if (!el || !imageUrl) return;
        el.style.backgroundImage = `url(${imageUrl})`;
        el.style.backgroundSize = 'cover';
        el.style.backgroundPosition = 'center';
    }

    function getHeroRoot(main) {
        const config = HERO_CONFIG[SITE_SLUG];
        if (!config || !config.root) return null;
        return main.querySelector(config.root) || document.querySelector(config.root);
    }

    function populateHero(main, article) {
        const config = HERO_CONFIG[SITE_SLUG];
        if (!config || !article) return false;

        const root = getHeroRoot(main);
        if (!root) return false;

        const link = `articulo/index.html?slug=${enc(article.slug)}`;

        const title = config.title ? root.querySelector(config.title) : null;
        if (title) {
            title.innerHTML = `<a href="${link}" style="color:inherit;text-decoration:none;">${esc(article.title)}</a>`;
        }

        const excerpt = config.excerpt ? root.querySelector(config.excerpt) : null;
        if (excerpt && article.excerpt) {
            excerpt.textContent = article.excerpt;
        }

        const category = config.category ? root.querySelector(config.category) : null;
        if (category && article.category) {
            category.textContent = article.category;
        }

        const image = config.image ? root.querySelector(config.image) : null;
        if (image) {
            setBackgroundImage(image, article.imageUrl);
            if (SITE_SLUG === 'elpulsomexicano' && article.imageUrl) {
                image.style.backgroundColor = 'transparent';
                image.classList.add('has-image');
            }
        }

        const heroLink = config.link ? root.querySelector(config.link) : null;
        if (heroLink) {
            heroLink.href = link;
        }

        return true;
    }

    function getSiteSlots(main) {
        const defs = SITE_SLOTS[SITE_SLUG] || [];
        return defs
            .map(function(def) {
                const root = main.querySelector(def.root) || document.querySelector(def.root);
                return root ? { root, def } : null;
            })
            .filter(Boolean);
    }

    function applyArticleToSlot(slotRoot, slotDef, article) {
        if (!slotRoot || !article) return;

        const link = `articulo/index.html?slug=${enc(article.slug)}`;

        const heading = slotDef.title ? slotRoot.querySelector(slotDef.title) : null;
        if (heading) {
            heading.innerHTML = `<a href="${link}" style="color:inherit;text-decoration:none;">${esc(article.title)}</a>`;
        }

        const para = slotDef.excerpt ? slotRoot.querySelector(slotDef.excerpt) : null;
        if (para && article.excerpt) {
            para.textContent = article.excerpt;
        }

        const tag = slotDef.category ? slotRoot.querySelector(slotDef.category) : null;
        if (tag && article.category) {
            tag.textContent = article.category;
        }

        const imgDiv = slotDef.image ? slotRoot.querySelector(slotDef.image) : null;
        if (imgDiv) {
            setBackgroundImage(imgDiv, article.imageUrl);
        }

        const linkEl = slotDef.link ? slotRoot.querySelector(slotDef.link) : null;
        if (linkEl) {
            linkEl.href = link;
        }

        const fallbackLink = slotRoot.querySelector('a.read-more,a.read-link,a.btn-outline,a.read-btn,a[href="#"],a.btn-neu,a.btn-subscribe');
        if (fallbackLink) {
            fallbackLink.href = link;
        }
    }

    // Cargar artículos
    async function loadArticles() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Error en API');
            
            const data = await response.json();
            const articles = data.articles;
            
            if (!articles || articles.length === 0) {
                console.log('No hay artículos para cargar');
                return;
            }
            
            populateArticles(articles);
        } catch (e) {
            console.error('Error cargando artículos:', e);
        }
    }

    // Poblar artículos en el DOM
    function populateArticles(articles) {
        const main = document.querySelector('main');
        if (!main) return;

        let articleIndex = populateHero(main, articles[0]) ? 1 : 0;

        const slots = getSiteSlots(main);
        slots.forEach(function(slot) {
            if (articleIndex >= articles.length) return;
            applyArticleToSlot(slot.root, slot.def, articles[articleIndex]);
            articleIndex++;
        });

        const listItems = main.querySelectorAll('.numbered-list li,.trending-list li');
        listItems.forEach(function(el, i) {
            if (!articles[i]) return;
            const span = el.querySelector('span');
            if (span) span.textContent = articles[i].title;
            else el.textContent = articles[i].title;
        });

        const marquee = main.querySelector('.marquee,marquee');
        if (marquee) {
            marquee.textContent = articles.slice(0, 5).map(function(article) {
                return '+++ ' + article.title.toUpperCase();
            }).join(' ');
        }

        const cols = main.querySelector('.newspaper-columns');
        if (cols && articles[0]) {
            const credit = cols.querySelector('.author-credit');
            if (credit && articles[0].author) credit.textContent = 'Por ' + articles[0].author;

            const paras = cols.querySelectorAll('p');
            paras.forEach(function(p, i) {
                if (articles[i] && articles[i].excerpt) p.textContent = articles[i].excerpt;
            });
        }

        console.log(`Articulos cargados: ${articleIndex}`);
    }

    // Iniciar carga cuando el DOM este listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadArticles);
    } else {
        loadArticles();
    }
})();