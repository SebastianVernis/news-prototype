// Generates script.js, _redirects, wrangler.toml, legal.css, article.css, metadata JSON

function genScriptJS() {
    var s = '';
    s += '/* Carousel + Sidebar Functionality */\n';
    s += 'var currentSlide = 0;\n';
    s += 'var autoPlayInterval;\n\n';
    s += 'function initCarousel() {\n';
    s += "    var slides = document.querySelectorAll('.carousel-slide');\n";
    s += "    var sidebarItems = document.querySelectorAll('.sidebar-item');\n";
    s += "    var dots = document.querySelectorAll('.carousel-dot');\n";
    s += '    if (slides.length === 0) return;\n';
    s += '    showSlide(0);\n';
    s += '    startAutoPlay();\n\n';
    s += "    var prevBtn = document.querySelector('.carousel-btn.prev');\n";
    s += "    var nextBtn = document.querySelector('.carousel-btn.next');\n";
    s += '    if (prevBtn) prevBtn.addEventListener("click", function() {\n';
    s += '        currentSlide = (currentSlide - 1 + slides.length) % slides.length;\n';
    s += '        showSlide(currentSlide); resetAutoPlay();\n';
    s += '    });\n';
    s += '    if (nextBtn) nextBtn.addEventListener("click", function() {\n';
    s += '        currentSlide = (currentSlide + 1) % slides.length;\n';
    s += '        showSlide(currentSlide); resetAutoPlay();\n';
    s += '    });\n\n';
    s += '    dots.forEach(function(dot, index) {\n';
    s += '        dot.addEventListener("click", function() {\n';
    s += '            currentSlide = index; showSlide(currentSlide); resetAutoPlay();\n';
    s += '        });\n    });\n';
    s += '    sidebarItems.forEach(function(item, index) {\n';
    s += '        item.addEventListener("click", function() {\n';
    s += '            currentSlide = index; showSlide(currentSlide); resetAutoPlay();\n';
    s += '        });\n    });\n';
    s += '}\n\n';
    s += 'function showSlide(index) {\n';
    s += "    var slides = document.querySelectorAll('.carousel-slide');\n";
    s += "    var sidebarItems = document.querySelectorAll('.sidebar-item');\n";
    s += "    var dots = document.querySelectorAll('.carousel-dot');\n";
    s += "    slides.forEach(function(sl) { sl.classList.remove('active'); });\n";
    s += "    sidebarItems.forEach(function(it) { it.classList.remove('active'); });\n";
    s += "    dots.forEach(function(d) { d.classList.remove('active'); });\n";
    s += "    if (slides[index]) slides[index].classList.add('active');\n";
    s += "    if (sidebarItems[index]) sidebarItems[index].classList.add('active');\n";
    s += "    if (dots[index]) dots[index].classList.add('active');\n";
    s += '    currentSlide = index;\n';
    s += '}\n\n';
    s += 'function startAutoPlay() {\n';
    s += '    autoPlayInterval = setInterval(function() {\n';
    s += "        currentSlide = (currentSlide + 1) % document.querySelectorAll('.carousel-slide').length;\n";
    s += '        showSlide(currentSlide);\n';
    s += '    }, 5000);\n}\n\n';
    s += 'function resetAutoPlay() { clearInterval(autoPlayInterval); startAutoPlay(); }\n\n';
    s += "var cm = document.querySelector('.carousel-main');\n";
    s += 'if (cm) {\n';
    s += "    cm.addEventListener('mouseenter', function() { clearInterval(autoPlayInterval); });\n";
    s += "    cm.addEventListener('mouseleave', function() { startAutoPlay(); });\n";
    s += '}\n\n';
    s += "document.addEventListener('DOMContentLoaded', initCarousel);\n";
    return s;
}

function genRedirects(slug) {
    var s = '';
    s += '# Proxy /api/* al worker de noticias\n';
    s += '/api/* https://news-api.sebastianvernis.workers.dev/api/:splat 200\n\n';
    s += '# RSS Feed\n';
    s += '/rss.xml  /api/rss/' + slug + '  200\n';
    s += '/feed.xml /api/rss/' + slug + '  200\n';
    return s;
}

function genWranglerToml(slug) {
    var s = '';
    s += 'name = "' + slug + '"\n';
    s += 'pages_build_output_dir = "."\n';
    s += 'compatibility_date = "2024-01-01"\n\n';
    s += '[[d1_databases]]\n';
    s += 'binding = "DB"\n';
    s += 'database_name = "news_db"\n';
    s += 'database_id = "039ec6ab-8f14-4e79-8f02-021df67a6c18"\n';
    return s;
}

function genLegalCSS() {
    var s = '';
    s += '/* Legal Pages Styles */\n';
    s += '.legal-page { padding: var(--space-2xl) 0; background: var(--background-color); min-height: 70vh; }\n';
    s += '.legal-content { max-width: 900px; margin: 0 auto; background: var(--card-bg); padding: var(--space-2xl); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); }\n';
    s += '.legal-content h1 { font-family: var(--font-primary); font-size: 2.5rem; margin-bottom: var(--space-md); color: var(--text-color); }\n';
    s += '.last-updated { color: var(--text-muted); font-size: 0.9rem; margin-bottom: var(--space-2xl); padding-bottom: var(--space-md); border-bottom: 1px solid var(--border-color); }\n';
    s += '.legal-section { margin-bottom: var(--space-2xl); }\n';
    s += '.legal-section h2 { font-family: var(--font-primary); font-size: 1.5rem; margin-top: var(--space-xl); margin-bottom: var(--space-md); color: var(--text-color); }\n';
    s += '.legal-section p { line-height: 1.8; margin-bottom: var(--space-md); color: var(--text-color); }\n';
    s += '.legal-section ul, .legal-section ol { margin-left: var(--space-xl); margin-bottom: var(--space-md); }\n';
    s += '.legal-section li { line-height: 1.8; margin-bottom: var(--space-sm); color: var(--text-color); }\n';
    s += '@media (max-width: 768px) { .legal-content { padding: var(--space-lg); } .legal-content h1 { font-size: 1.8rem; } }\n';
    return s;
}

function genArticleCSS() {
    var s = '';
    s += '/* Article Page Styles */\n';
    s += '.article-page { padding: 3rem 0; background: var(--background-color); }\n';
    s += '.article-full { max-width: 900px; margin: 0 auto; background: var(--card-bg); border-radius: 12px; padding: 3rem; box-shadow: var(--shadow-md); }\n';
    s += '.article-header { margin-bottom: 2rem; }\n';
    s += '.article-category-badge { display: inline-block; padding: 4px 12px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; border-radius: 4px; color: white; margin-bottom: 1rem; }\n';
    s += '.article-title { font-family: var(--font-primary); font-size: 2.5rem; font-weight: 800; line-height: 1.2; margin-bottom: 1rem; color: var(--text-color); }\n';
    s += '.article-meta { display: flex; align-items: center; gap: 1rem; font-size: 0.9rem; color: var(--text-muted); flex-wrap: wrap; }\n';
    s += '.article-meta .author { font-weight: 600; color: var(--primary-color); }\n';
    s += '.article-image-wrapper { margin: 2rem 0; }\n';
    s += '.article-image { width: 100%; height: auto; border-radius: 8px; }\n';
    s += '.image-caption { font-size: 0.85rem; color: var(--text-muted); text-align: center; margin-top: 0.5rem; font-style: italic; }\n';
    s += '.article-content { font-size: 1.1rem; line-height: 1.8; color: var(--text-color); }\n';
    s += '.article-content .lead { font-size: 1.25rem; font-weight: 500; color: var(--primary-color); margin-bottom: 1.5rem; }\n';
    s += '.article-content p { margin-bottom: 1.5rem; }\n';
    s += '.article-content h2 { font-family: var(--font-primary); font-size: 1.75rem; margin-top: 2.5rem; margin-bottom: 1rem; color: var(--primary-color); }\n';
    s += '.article-content h3 { font-family: var(--font-primary); font-size: 1.4rem; margin-top: 2rem; margin-bottom: 0.75rem; color: var(--text-color); }\n';
    s += '.article-content ul, .article-content ol { margin-left: 2rem; margin-bottom: 1.5rem; }\n';
    s += '.article-content li { margin-bottom: 0.5rem; line-height: 1.7; }\n';
    s += '.article-quote { border-left: 4px solid var(--accent-color); padding-left: 1.5rem; margin: 2rem 0; font-style: italic; font-size: 1.2rem; color: var(--text-muted); }\n';
    s += '.article-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color); align-items: center; }\n';
    s += '.article-footer { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }\n';
    s += '.article-share { display: flex; align-items: center; gap: 0.5rem; }\n';
    s += '.share-link { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: white; font-size: 1rem; transition: all 0.3s ease; }\n';
    s += '.share-link.facebook { background: #1877f2; } .share-link.twitter { background: #1da1f2; } .share-link.whatsapp { background: #25d366; }\n';
    s += '.share-link:hover { transform: translateY(-3px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }\n';
    s += '.back-link { display: inline-flex; align-items: center; gap: 0.5rem; color: var(--primary-color); font-weight: 600; transition: all 0.3s ease; }\n';
    s += '.back-link:hover { color: var(--secondary-color); }\n';
    s += '@media (max-width: 768px) { .article-full { padding: 1.5rem; } .article-title { font-size: 1.8rem; } .article-content { font-size: 1rem; } }\n';
    return s;
}

function genMetadataJSON(site, colors) {
    return JSON.stringify({
        id: site.slug,
        name: site.name,
        category_default: 'General',
        facebook_page_id: '',
        theme: {
            primary: colors.primary,
            secondary: colors.secondary,
            accent: colors.accent
        },
        selectors: {
            container: '#news-grid',
            template: 'card-modern'
        }
    }, null, 2);
}

module.exports = { genScriptJS, genRedirects, genWranglerToml, genLegalCSS, genArticleCSS, genMetadataJSON };
