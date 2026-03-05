// Generates style-custom.css (full visual theme)
function genStyleCustomCSS(site, origCSS, colors) {
    var theme = origCSS
        .replace(/:root\s*\{[^}]+\}/g, '')
        .replace(/\*\s*\{[^}]*\}/g, '')
        .replace(/body\s*\{[^}]*\}/g, '')
        .trim();

    var c = colors;
    var L = [];

    L.push('/* ' + site.name.toUpperCase() + ' - Estilo Personalizado */');
    L.push('/* Style: ' + site.style + ' */');
    L.push('');
    L.push("@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;800&family=Noto+Sans:wght@400;600;700&display=swap');");
    L.push('');

    // HEADER
    L.push('/* ===== HEADER ===== */');
    L.push('.header { background: ' + c.dark + '; border-bottom: 3px solid ' + c.primary + '; position: sticky; top: 0; z-index: 1000; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }');
    L.push('.header-container { display: flex; align-items: center; justify-content: space-between; padding: 4px 24px; gap: 24px; max-width: 1400px; margin: 0 auto; }');
    L.push('.logo-section { display: flex; align-items: center; flex-shrink: 0; }');
    L.push('.site-logo { height: 64px; width: auto; object-fit: contain; display: block; filter: brightness(0) invert(1); }');
    L.push('');

    // NAV
    L.push('/* ===== NAV ===== */');
    L.push('.main-nav { display: flex; align-items: center; flex-wrap: wrap; gap: 0; }');
    L.push(".nav-link { font-family: 'Noto Sans', sans-serif; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-size: 0.77rem; padding: 10px 15px; color: rgba(255,255,255,0.6); opacity: 0.7; transition: all 0.3s ease; border-bottom: 2px solid transparent; display: inline-block; }");
    L.push('.nav-link:hover, .nav-link.active { color: #fff; border-bottom-color: ' + c.primary + '; opacity: 1; }');
    L.push('');

    // TICKER
    L.push('/* ===== TICKER ===== */');
    L.push('.radio-bar { background: ' + c.primary + '; padding: 6px 0; }');
    L.push('.radio-bar-inner { display: flex; align-items: center; gap: 16px; max-width: 1400px; margin: 0 auto; padding: 0 24px; }');
    L.push('.radio-bar marquee { color: rgba(255,255,255,0.85); font-size: 0.82rem; flex: 1; }');
    L.push('.ticker-item { color: rgba(255,255,255,0.85); }');
    L.push('');

    // FEATURED
    L.push('/* ===== FEATURED ===== */');
    L.push('.featured-section { padding: var(--space-2xl) 0 var(--space-md); }');
    L.push('.sidebar-layout { display: grid; grid-template-columns: 1fr 360px; gap: 28px; margin-bottom: 40px; align-items: start; }');
    L.push('');

    // MAIN ARTICLE
    L.push('/* ===== MAIN ARTICLE ===== */');
    L.push('.rc-main-article { background: #fff; border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-lg); cursor: pointer; }');
    L.push('.rc-main-article .main-img-wrapper { position: relative; overflow: hidden; }');
    L.push('.rc-main-article .main-img-wrapper img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; transition: transform 0.5s ease; }');
    L.push('.rc-main-article:hover .main-img-wrapper img { transform: scale(1.04); }');
    L.push('.rc-main-article .main-content-body { padding: 28px; }');
    L.push('.rc-main-article .main-content-body .category-badge { margin-bottom: 12px; }');
    L.push(".rc-main-article .main-content-body h2 { font-family: 'Playfair Display', Georgia, serif; font-size: clamp(1.4rem, 2.5vw, 2rem); font-weight: 800; line-height: 1.2; color: " + c.text + "; margin-bottom: 14px; }");
    L.push('.rc-main-article .main-content-body h2 a { color: inherit; text-decoration: none; }');
    L.push('.rc-main-article .main-content-body h2 a:hover { color: ' + c.primary + '; }');
    L.push('.rc-main-article .main-content-body p { font-size: 1rem; line-height: 1.7; color: ' + c.textLight + '; margin-bottom: 18px; display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }');
    L.push('.rc-main-article .main-meta { display: flex; gap: 20px; font-size: 0.82rem; color: ' + c.textLight + '; padding-top: 16px; border-top: 1px solid rgba(0,0,0,0.08); }');
    L.push('.rc-main-article .main-meta i { color: ' + c.primary + '; margin-right: 4px; }');
    L.push('.rc-read-more { display: inline-block; background: ' + c.primary + '; color: #fff; padding: 10px 22px; border-radius: var(--radius-sm); font-weight: 700; font-size: 0.82rem; text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s; margin-top: 16px; }');
    L.push('.rc-read-more:hover { background: ' + c.secondary + '; transform: translateX(4px); }');
    L.push('');

    // SIDEBAR
    L.push('/* ===== SIDEBAR ===== */');
    L.push('.rc-sidebar-list { display: flex; flex-direction: column; gap: 0; background: #fff; border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-md); }');
    L.push('.rc-sidebar-header { background: ' + c.primary + '; padding: 12px 18px; display: flex; align-items: center; gap: 10px; }');
    L.push(".rc-sidebar-header h3 { font-family: 'Noto Sans', sans-serif; font-weight: 800; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 2px; color: #fff; margin: 0; }");
    L.push('.rc-list-item { display: flex; gap: 0; border-bottom: 1px solid rgba(0,0,0,0.06); cursor: pointer; transition: background 0.2s; overflow: hidden; }');
    L.push('.rc-list-item:last-child { border-bottom: none; }');
    L.push('.rc-list-item:hover { background: rgba(0,0,0,0.03); }');
    L.push('.rc-list-item img { width: 95px; height: 80px; object-fit: cover; flex-shrink: 0; transition: transform 0.4s ease; }');
    L.push('.rc-list-item:hover img { transform: scale(1.06); }');
    L.push('.rc-list-content { padding: 12px 14px; display: flex; flex-direction: column; justify-content: center; gap: 5px; flex: 1; }');
    L.push(".rc-list-content h4 { font-family: 'Playfair Display', Georgia, serif; font-size: 0.85rem; font-weight: 700; line-height: 1.3; color: " + c.text + "; }");
    L.push('.rc-list-content h4 a { color: inherit; text-decoration: none; }');
    L.push('.rc-list-content h4 a:hover { color: ' + c.primary + '; }');
    L.push('.rc-list-content .card-meta { font-size: 0.7rem; color: ' + c.textLight + '; display: flex; gap: 8px; }');
    L.push('');

    // NEWS SECTION + CARDS
    L.push('/* ===== NEWS SECTION ===== */');
    L.push('.news-section { padding: 20px 0 60px; }');
    L.push(".section-title { font-family: 'Playfair Display', Georgia, serif; font-size: 1.7rem; color: " + c.text + "; margin: 0 0 28px; position: relative; padding-bottom: 14px; }");
    L.push(".section-title::after { content: ''; position: absolute; bottom: 0; left: 0; width: 60px; height: 3px; background: linear-gradient(90deg, " + c.primary + ", " + c.accent + "); }");
    L.push('.card-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 22px; }');
    L.push('@media (max-width: 1200px) { .card-grid { grid-template-columns: repeat(3, 1fr); } }');
    L.push('@media (max-width: 900px)  { .card-grid { grid-template-columns: repeat(2, 1fr); } }');
    L.push('@media (max-width: 560px)  { .card-grid { grid-template-columns: 1fr; } }');
    L.push('');

    // ARTICLE CARD
    L.push('/* ===== ARTICLE CARD ===== */');
    L.push('.article-card { background: #fff; border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-sm); transition: all 0.3s ease; display: flex; flex-direction: column; height: 100%; border-top: 3px solid transparent; }');
    L.push('.article-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-lg); border-top-color: ' + c.primary + '; }');
    L.push('.article-card .card-image-wrapper { overflow: hidden; aspect-ratio: 16/9; height: auto; flex-shrink: 0; }');
    L.push('.article-card .card-image-wrapper img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; display: block; }');
    L.push('.article-card:hover .card-image-wrapper img { transform: scale(1.06); }');
    L.push('.article-card .card-content { padding: 16px; flex: 1; display: flex; flex-direction: column; }');
    L.push(".article-card .card-title { font-family: 'Playfair Display', Georgia, serif; font-size: 0.95rem; font-weight: 700; line-height: 1.35; margin: 0 0 8px; color: " + c.text + "; }");
    L.push('.article-card .card-title a { color: inherit; text-decoration: none; }');
    L.push('.article-card .card-title a:hover { color: ' + c.primary + '; }');
    L.push('.article-card .card-excerpt { font-size: 0.83rem; line-height: 1.6; color: ' + c.textLight + '; flex: 1; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; margin-bottom: 10px; }');
    L.push('.article-card .card-footer { display: flex; justify-content: space-between; font-size: 0.73rem; color: ' + c.textLight + '; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.08); margin-top: auto; }');
    L.push('');

    // BADGES
    L.push('/* ===== BADGES ===== */');
    L.push('.category-badge, .card-category-badge { display: inline-block; padding: 3px 9px; border-radius: 3px; font-size: 0.67rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; width: fit-content; }');
    L.push('.cat-nacional { background: #1565C0 !important; color: white !important; }');
    L.push('.cat-politica { background: #C2185B !important; color: white !important; }');
    L.push('.cat-economia { background: #2E7D32 !important; color: white !important; }');
    L.push('.cat-deportes { background: #EF6C00 !important; color: white !important; }');
    L.push('.cat-internacional { background: #7B1FA2 !important; color: white !important; }');
    L.push('.cat-cultura { background: #00695C !important; color: white !important; }');
    L.push('.cat-tecnologia { background: #283593 !important; color: white !important; }');
    L.push('.cat-salud { background: #AD1457 !important; color: white !important; }');
    L.push('.cat-general { background: ' + c.primary + ' !important; color: white !important; }');
    L.push('.cat-destacado { background: ' + c.secondary + ' !important; color: white !important; }');
    L.push('');

    // FOOTER
    L.push('/* ===== FOOTER ===== */');
    L.push('.footer { background: ' + c.dark + '; border-top: 4px solid ' + c.primary + '; padding: 60px 0 30px; margin-top: var(--space-2xl); }');
    L.push('.footer-grid { display: grid; gap: 40px; max-width: 1400px; margin: 0 auto; padding: 0 24px; }');
    L.push('.footer-grid.cols-3 { grid-template-columns: 2fr 1fr 1fr; }');
    L.push('.footer-column { display: flex; flex-direction: column; gap: 14px; }');
    L.push('.footer-logo { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }');
    L.push('.footer-logo img { height: 40px; width: auto; object-fit: contain; filter: brightness(0) invert(1); }');
    L.push(".footer-logo h3 { font-family: 'Playfair Display', Georgia, serif; color: rgba(255,255,255,0.7); font-size: 1.2rem; margin: 0; }");
    L.push('.footer-about { color: rgba(255,255,255,0.5); font-size: 0.9rem; line-height: 1.7; margin: 0; }');
    L.push(".footer-column h4 { color: rgba(255,255,255,0.7); font-family: 'Noto Sans', sans-serif; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; font-size: 0.72rem; margin: 0 0 6px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.15); }");
    L.push('.footer-links { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }');
    L.push('.footer-links li a { color: rgba(255,255,255,0.5); transition: all 0.3s; font-size: 0.88rem; display: inline-block; }');
    L.push('.footer-links li a:hover { color: rgba(255,255,255,0.8); padding-left: 5px; }');
    L.push('.social-links { display: flex; gap: 10px; flex-wrap: wrap; }');
    L.push('.social-link { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: var(--radius-sm); background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); color: rgba(255,255,255,0.6); transition: all 0.3s; font-size: 0.85rem; }');
    L.push('.social-link:hover { background: ' + c.primary + '; border-color: ' + c.primary + '; color: #fff; transform: translateY(-3px); }');
    L.push('.footer-bottom { border-top: 1px solid rgba(255,255,255,0.1); margin-top: 40px; padding: 24px 24px 0; max-width: 1400px; margin-left: auto; margin-right: auto; color: rgba(255,255,255,0.35); font-size: 0.82rem; text-align: center; display: flex; flex-direction: column; gap: 6px; }');
    L.push('');

    // RESPONSIVE
    L.push('/* ===== RESPONSIVE ===== */');
    L.push('@media (max-width: 1024px) { .sidebar-layout { grid-template-columns: 1fr; } .rc-sidebar-list { display: grid; grid-template-columns: repeat(2, 1fr); } .rc-sidebar-header { grid-column: 1 / -1; } }');
    L.push('@media (max-width: 600px) { .rc-sidebar-list { grid-template-columns: 1fr; } .footer-grid.cols-3 { grid-template-columns: 1fr; } }');
    L.push('');

    // ANIMATIONS
    L.push('/* ===== ANIMATIONS ===== */');
    L.push('@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }');
    L.push('.article-card { animation: fadeInUp 0.5s ease forwards; }');
    L.push('::-webkit-scrollbar { width: 8px; }');
    L.push('::-webkit-scrollbar-track { background: ' + c.light + '; }');
    L.push('::-webkit-scrollbar-thumb { background: ' + c.textLight + '; border-radius: 4px; }');
    L.push('::-webkit-scrollbar-thumb:hover { background: ' + c.primary + '; }');
    L.push('');

    // ORIGINAL THEME
    if (theme.length > 10) {
        L.push('/* ===== ORIGINAL THEME (' + site.style + ') ===== */');
        L.push(theme);
    }

    return L.join('\n');
}

module.exports = genStyleCustomCSS;
