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
    const SITE_SLUG = 'mexico360noticias';
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
        
        let articleIndex = 0;
        
        // Actualizar hero image si existe
        const heroImgBox = main.querySelector('.hero-img-box');
        if (heroImgBox && articles[0] && articles[0].imageUrl) {
            heroImgBox.style.backgroundImage = `url(${articles[0].imageUrl})`;
            heroImgBox.style.backgroundSize = 'cover';
            heroImgBox.style.backgroundPosition = 'center';
        }
        
        // Buscar contenedores de artículos en el HTML
        const containers = main.querySelectorAll(
            'article, .hero, .hero-content, .hero-text, .hero-text-box, .hero-headline,' +
            '.z-content, .focus-section, .side-item, .side-article, .grid-item,' +
            '.scroll-content, .video-card, .minimal-card, .gallery-card, .classic-card,' +
            '.card, .card-body, .brief-card, .tech-card, .grid-card, .scroll-card,' +
            '.hero-card > .hero-content, .hero-section .hero-content'
        );
        
        // Deduplicar contenedores
        const seen = new Set();
        const unique = [];
        containers.forEach(function(el) {
            let dominated = false;
            seen.forEach(function(s) {
                if (s.contains(el) && s !== el) dominated = true;
            });
            if (!dominated) {
                unique.push(el);
                seen.add(el);
            }
        });
        
        // Llenar cada contenedor con datos del artículo
        unique.forEach(function(el) {
            if (articleIndex >= articles.length) return;
            
            const a = articles[articleIndex];
            const link = `articulo/index.html?slug=${enc(a.slug)}`;
            
            // Título
            const heading = el.querySelector('h1,h2,h3,h4');
            if (heading) {
                heading.innerHTML = `<a href="${link}" style="color:inherit;text-decoration:none;">${esc(a.title)}</a>`;
            }
            
            // Extracto
            const para = el.querySelector('p:not(.author-meta):not(.img-caption)');
            if (para && a.excerpt) {
                para.textContent = a.excerpt;
            }
            
            // Categoría
            const tag = el.querySelector('.tag,.tag-pill,.category-tag,.category,.category-label,.category-pill,.hero-tag,.card-meta');
            if (tag && a.category) {
                tag.textContent = a.category;
            }
            
            // Imagen
            const imgDiv = el.querySelector('div[class*=img],div[class*=image],div[class*=thumb],div[class*=placeholder]');
            if (imgDiv && a.imageUrl) {
                imgDiv.style.backgroundImage = `url(${a.imageUrl})`;
                imgDiv.style.backgroundSize = 'cover';
                imgDiv.style.backgroundPosition = 'center';
            }
            
            // Background en grid-items
            if (!imgDiv && a.imageUrl && el.classList.contains('grid-item')) {
                el.style.backgroundImage = `linear-gradient(to bottom, transparent 30%, rgba(10,25,47,0.9)), url(${a.imageUrl})`;
                el.style.backgroundSize = 'cover';
                el.style.backgroundPosition = 'center';
            }
            
            // Link read-more
            const rm = el.querySelector('a.read-more,a.read-link,a.btn-outline,a.read-btn,a[href="#"]');
            if (rm) rm.href = link;
            
            articleIndex++;
        });
        
        console.log(`Artículos cargados: ${articleIndex}`);
    }
    
    // Iniciar carga cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadArticles);
    } else {
        loadArticles();
    }
})();