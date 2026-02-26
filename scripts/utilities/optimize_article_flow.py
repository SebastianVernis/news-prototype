#!/usr/bin/env python3
"""
Optimize article flow for all 10 sites:
1. Fix index.html fetch bug (wrong response parsing + field mapping)
2. Create dynamic articulo/index.html template per site
3. Fix categoria/*.html pages to load dynamically
4. Delete static article HTML files
"""

import os
import re
import glob

SITES_DIR = 'sites'

SITES = [
    ('bitacoraurbana',      'Bitácora Urbana'),
    ('cbnnoticias',         'CBN Noticias'),
    ('centralmexico',       'Central México'),
    ('mexicoinformado',     'México Informado'),
    ('nodoinformativo',     'Nodo Informativo'),
    ('noticiasobjetivo',    'Noticias Objetivo'),
    ('radiocinconoticias',  'Radio Cinco Noticias'),
    ('reportecentralmx',    'Reporte Central MX'),
    ('tvmexico',            'TV México News'),
    ('verticenoticias',     'Vértice Noticias'),
]

CATEGORIES = [
    ('nacional',       'Nacional'),
    ('politica',       'Política'),
    ('economia',       'Economía'),
    ('deportes',       'Deportes'),
    ('internacional',  'Internacional'),
    ('cultura',        'Cultura'),
    ('tecnologia',     'Tecnología'),
    ('salud',          'Salud'),
]

# ─────────────────────────────────────────────
# 1. FIX index.html
# ─────────────────────────────────────────────

def fix_index_html(site_dir, site_slug):
    path = os.path.join(site_dir, 'index.html')
    if not os.path.exists(path):
        print(f'  [SKIP] index.html not found: {site_slug}')
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix broken response parsing (multiple variants)
    content = re.sub(
        r'const articles\s*=\s*await res\.json\(\);\s*if\s*\(\s*!Array\.isArray\(articles\)\s*\)\s*return;',
        'const {articles} = await res.json(); if(!articles?.length) return;',
        content
    )
    content = re.sub(
        r'const articles=await res\.json\(\);\s*if\s*\(\s*!Array\.isArray\(articles\)\s*\)\s*return;',
        'const {articles} = await res.json(); if(!articles?.length) return;',
        content
    )

    # Fix field mapping: image
    for old in ['a.image || a.hero || a.thumbnail', 'a.image||a.hero||a.thumbnail',
                'a.image || a.thumbnail', 'a.image||a.thumbnail']:
        content = content.replace(old, "a.imageUrl || 'assets/images/article_placeholder.jpg'")

    # Fix field mapping: date (timestamp spans)
    for old in ['a.time_ago || a.date', 'a.time_ago||a.date']:
        content = content.replace(old, '(a.publishedAt ? new Date(a.publishedAt).toLocaleDateString("es-MX") : "")')

    # Fix a.date standalone (in renderHero meta, renderNewsCard footer)
    content = content.replace("+(a.date||'')+", '+(a.publishedAt ? new Date(a.publishedAt).toLocaleDateString("es-MX") : "")+')
    content = content.replace("a.date||''", 'a.publishedAt ? new Date(a.publishedAt).toLocaleDateString("es-MX") : ""')
    content = content.replace('a.date||""', 'a.publishedAt ? new Date(a.publishedAt).toLocaleDateString("es-MX") : ""')

    # Fix field mapping: excerpt/summary
    for old in ['a.summary || a.excerpt', 'a.summary||a.excerpt', "a.excerpt || a.summary", "a.excerpt||a.summary"]:
        content = content.replace(old, 'a.excerpt')

    # Fix article URL to point to dynamic template
    for old in [
        "a.url || a.path || ('articulo/'+(a.slug||''))",
        "a.url||a.path||('articulo/'+(a.slug||''))",
        "a.url || a.path || ('articulo/' + (a.slug || ''))",
    ]:
        content = content.replace(old, "'articulo/index.html?slug='+(a.slug||'')")

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [OK] Fixed index.html: {site_slug}')
    else:
        print(f'  [--] index.html unchanged (pattern not matched): {site_slug}')


# ─────────────────────────────────────────────
# 2. CREATE articulo/index.html
# ─────────────────────────────────────────────

def extract_header_footer_from_article(site_dir):
    """Read an existing article page and extract <header> and <footer> blocks."""
    articulo_dir = os.path.join(site_dir, 'articulo')
    candidates = [f for f in glob.glob(os.path.join(articulo_dir, '*.html'))
                  if os.path.basename(f) != 'index.html']

    if not candidates:
        # Fall back to index.html
        candidates = [os.path.join(site_dir, 'index.html')]

    with open(candidates[0], 'r', encoding='utf-8') as f:
        src = f.read()

    header_m = re.search(r'(<header[\s\S]*?</header>)', src, re.IGNORECASE)
    footer_m = re.search(r'(<footer[\s\S]*?</footer>)', src, re.IGNORECASE)

    header = header_m.group(1) if header_m else ''
    footer = footer_m.group(1) if footer_m else ''

    return header, footer


def create_article_template(site_dir, site_slug, site_name):
    articulo_dir = os.path.join(site_dir, 'articulo')
    os.makedirs(articulo_dir, exist_ok=True)

    out_path = os.path.join(articulo_dir, 'index.html')

    has_article_css = os.path.exists(os.path.join(site_dir, 'article.css'))
    header_html, footer_html = extract_header_footer_from_article(site_dir)

    # Preloader color from style.css (best-effort)
    preloader_color = '#1a1a2e'
    style_path = os.path.join(site_dir, 'style.css')
    if os.path.exists(style_path):
        with open(style_path, 'r', encoding='utf-8') as f:
            css = f.read()
        m = re.search(r'--primary-color\s*:\s*(#[0-9a-fA-F]{3,6})', css)
        if m:
            preloader_color = m.group(1)

    article_css_tag = '<link rel="stylesheet" href="../article.css">' if has_article_css else ''

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title id="page-title">Cargando... - {site_name}</title>
    <meta name="description" id="page-desc" content="">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;800&family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../style.css">
    {article_css_tag}
</head>
<body>

<!-- Preloader -->
<div id="preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;background:{preloader_color};z-index:999999;display:flex;flex-direction:column;justify-content:center;align-items:center;">
    <div style="text-align:center;">
        <div style="margin-bottom:25px;animation:spin3D 2s ease-in-out infinite;">
            <img src="../logo.png" alt="Logo" style="height:80px;width:auto;filter:brightness(0) invert(1);">
        </div>
        <div style="width:40px;height:40px;border:4px solid rgba(255,255,255,0.2);border-top:4px solid white;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 20px;"></div>
        <p style="font-family:Arial,sans-serif;color:white;font-weight:bold;letter-spacing:2px;text-transform:uppercase;font-size:0.9rem;">Cargando...</p>
    </div>
</div>
<style>
    @keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
    @keyframes spin3D{{0%{{transform:rotateY(0deg) scale(1)}}50%{{transform:rotateY(180deg) scale(1.1)}}100%{{transform:rotateY(360deg) scale(1)}}}}
</style>
<script>
    window.addEventListener('load', function() {{
        setTimeout(function() {{
            var p = document.getElementById('preloader');
            if(p) {{ p.style.transition='opacity 0.5s ease'; p.style.opacity='0'; setTimeout(function(){{p.style.display='none';}},500); }}
        }}, 1200);
    }});
</script>

{header_html}

<main class="main-content article-page">
    <div class="container">
        <!-- Estado de carga -->
        <div id="article-loading" style="text-align:center;padding:60px 20px;">
            <p style="font-size:1.1rem;color:#666;">Cargando artículo...</p>
        </div>

        <!-- Error -->
        <div id="article-error" style="display:none;text-align:center;padding:60px 20px;">
            <h2>Artículo no encontrado</h2>
            <p style="color:#666;margin:20px 0;">El artículo que buscas no está disponible.</p>
            <a href="../index.html" class="back-link" style="color:var(--primary-color,#00897B);font-weight:bold;">
                <i class="fas fa-arrow-left"></i> Volver al inicio
            </a>
        </div>

        <!-- Contenido del artículo -->
        <article id="article-content" class="article-full" style="display:none;">
            <div class="article-header">
                <div class="breadcrumb" style="margin-bottom:12px;">
                    <a href="../index.html">Inicio</a>
                    <span style="margin:0 6px;color:#999;">/</span>
                    <span id="art-category-breadcrumb"></span>
                </div>
                <span id="art-category-badge" class="article-category-badge"></span>
                <h1 id="art-title" class="article-title"></h1>
                <div class="article-meta">
                    <span class="author"><i class="far fa-user"></i> Por <span id="art-author"></span></span>
                    <span class="separator">•</span>
                    <span class="date"><i class="far fa-calendar"></i> <span id="art-date"></span></span>
                </div>
            </div>

            <div class="article-image-wrapper" id="art-image-wrapper">
                <img id="art-image" class="article-image" src="" alt="" loading="lazy"
                     style="width:100%;max-height:500px;object-fit:cover;border-radius:8px;margin:20px 0;">
            </div>

            <div id="art-body" class="article-content"></div>

            <div class="article-footer" style="margin-top:30px;padding-top:20px;border-top:1px solid #eee;">
                <div class="article-share">
                    <span class="share-label" style="font-weight:bold;margin-right:10px;">Compartir:</span>
                    <a id="share-fb" href="#" class="share-link facebook" target="_blank" rel="noopener"
                       style="margin-right:8px;"><i class="fab fa-facebook-f"></i></a>
                    <a id="share-tw" href="#" class="share-link twitter" target="_blank" rel="noopener"
                       style="margin-right:8px;"><i class="fab fa-twitter"></i></a>
                    <a id="share-wa" href="#" class="share-link whatsapp" target="_blank" rel="noopener">
                       <i class="fab fa-whatsapp"></i></a>
                </div>
            </div>

            <div class="article-nav" style="margin-top:30px;">
                <a href="../index.html" class="back-link">
                    <i class="fas fa-arrow-left"></i> Volver al inicio
                </a>
            </div>
        </article>
    </div>
</main>

{footer_html}

<script src="../script.js"></script>
<script>
(async function() {{
    const params = new URLSearchParams(location.search);
    const slug = params.get('slug');

    if (!slug) {{
        showError();
        return;
    }}

    try {{
        const res = await fetch('/api/articles/' + encodeURIComponent(slug));
        if (!res.ok) throw new Error('not found');
        const data = await res.json();
        const a = data.article;
        if (!a) throw new Error('empty');
        renderArticle(a);
    }} catch(e) {{
        console.error('Error loading article:', e);
        showError();
    }}

    function renderArticle(a) {{
        // Meta
        document.title = (a.title || 'Artículo') + ' - {site_name}';
        const desc = document.getElementById('page-desc');
        if (desc) desc.content = a.excerpt || '';

        // Category
        const cat = a.category || '';
        const catSlug = cat.toLowerCase().replace(/\\s+/g, '-');
        const badge = document.getElementById('art-category-badge');
        if (badge) {{ badge.textContent = cat; badge.className = 'article-category-badge cat-' + catSlug; }}
        const breadCat = document.getElementById('art-category-breadcrumb');
        if (breadCat) breadCat.textContent = cat;

        // Title
        const title = document.getElementById('art-title');
        if (title) title.textContent = a.title || '';

        // Author & date
        const author = document.getElementById('art-author');
        if (author) author.textContent = a.author || 'Redacción';
        const date = document.getElementById('art-date');
        if (date) date.textContent = a.publishedAt ? new Date(a.publishedAt).toLocaleDateString('es-MX', {{year:'numeric',month:'long',day:'numeric'}}) : '';

        // Image
        const imgWrapper = document.getElementById('art-image-wrapper');
        const img = document.getElementById('art-image');
        if (a.imageUrl && img) {{
            img.src = a.imageUrl;
            img.alt = a.title || '';
        }} else if (imgWrapper) {{
            imgWrapper.style.display = 'none';
        }}

        // Body
        const body = document.getElementById('art-body');
        if (body) body.innerHTML = a.content || '<p>' + (a.excerpt || '') + '</p>';

        // Share links
        const url = encodeURIComponent(location.href);
        const text = encodeURIComponent(a.title || '');
        const fbLink = document.getElementById('share-fb');
        const twLink = document.getElementById('share-tw');
        const waLink = document.getElementById('share-wa');
        if (fbLink) fbLink.href = 'https://www.facebook.com/sharer/sharer.php?u=' + url;
        if (twLink) twLink.href = 'https://twitter.com/intent/tweet?url=' + url + '&text=' + text;
        if (waLink) waLink.href = 'https://wa.me/?text=' + text + '%20' + url;

        // Show article, hide loading
        document.getElementById('article-loading').style.display = 'none';
        document.getElementById('article-content').style.display = 'block';
    }}

    function showError() {{
        document.getElementById('article-loading').style.display = 'none';
        document.getElementById('article-error').style.display = 'block';
    }}
}})();
</script>
</body>
</html>
'''

    # Fix relative paths in footer: assets/ → ../assets/ (since we're in articulo/)
    html = re.sub(r'src="assets/', 'src="../assets/', html)
    html = re.sub(r"src='assets/", "src='../assets/", html)
    # Fix category links in footer that lack ../
    html = re.sub(r'href="categoria/', 'href="../categoria/', html)
    html = re.sub(r"href='categoria/", "href='../categoria/", html)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  [OK] Created articulo/index.html: {site_slug}')


# ─────────────────────────────────────────────
# 3. FIX categoria/*.html
# ─────────────────────────────────────────────

def fix_category_pages(site_dir, site_slug, site_name):
    cat_dir = os.path.join(site_dir, 'categoria')
    if not os.path.exists(cat_dir):
        print(f'  [SKIP] categoria/ not found: {site_slug}')
        return

    cat_files = glob.glob(os.path.join(cat_dir, '*.html'))
    if not cat_files:
        print(f'  [SKIP] No category pages: {site_slug}')
        return

    # Extract header/footer from first category page
    with open(cat_files[0], 'r', encoding='utf-8') as f:
        src = f.read()

    header_m = re.search(r'(<header[\s\S]*?</header>)', src, re.IGNORECASE)
    footer_m = re.search(r'(<footer[\s\S]*?</footer>)', src, re.IGNORECASE)
    header_html = header_m.group(1) if header_m else ''
    footer_html = footer_m.group(1) if footer_m else ''

    # Preloader color
    preloader_color = '#1a1a2e'
    style_path = os.path.join(site_dir, 'style.css')
    if os.path.exists(style_path):
        with open(style_path, 'r', encoding='utf-8') as f:
            css = f.read()
        m = re.search(r'--primary-color\s*:\s*(#[0-9a-fA-F]{3,6})', css)
        if m:
            preloader_color = m.group(1)

    for cat_slug, cat_name in CATEGORIES:
        cat_file = os.path.join(cat_dir, f'{cat_slug}.html')
        if not os.path.exists(cat_file):
            continue

        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_name} - {site_name}</title>
    <meta name="description" content="Noticias de {cat_name} en {site_name}.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;800&family=Noto+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../style.css">
</head>
<body>

<!-- Preloader -->
<div id="preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;background:{preloader_color};z-index:999999;display:flex;flex-direction:column;justify-content:center;align-items:center;">
    <div style="text-align:center;">
        <div style="margin-bottom:25px;animation:spin3D 2s ease-in-out infinite;">
            <img src="../logo.png" alt="Logo" style="height:80px;width:auto;filter:brightness(0) invert(1);">
        </div>
        <div style="width:40px;height:40px;border:4px solid rgba(255,255,255,0.2);border-top:4px solid white;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 20px;"></div>
        <p style="font-family:Arial,sans-serif;color:white;font-weight:bold;letter-spacing:2px;text-transform:uppercase;font-size:0.9rem;">Cargando...</p>
    </div>
</div>
<style>
    @keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
    @keyframes spin3D{{0%{{transform:rotateY(0deg) scale(1)}}50%{{transform:rotateY(180deg) scale(1.1)}}100%{{transform:rotateY(360deg) scale(1)}}}}
</style>
<script>
    window.addEventListener('load', function() {{
        setTimeout(function() {{
            var p = document.getElementById('preloader');
            if(p) {{ p.style.transition='opacity 0.5s ease'; p.style.opacity='0'; setTimeout(function(){{p.style.display='none';}},500); }}
        }}, 1200);
    }});
</script>

{header_html}

<main class="main-content">
    <div class="container">
        <div class="category-header" style="margin:30px 0 20px;">
            <span class="category-badge-large cat-{cat_slug}">{cat_name}</span>
            <h1 class="category-title">Noticias de {cat_name}</h1>
            <p class="category-description">Todas las noticias actualizadas sobre {cat_name}.</p>
        </div>

        <div id="cat-loading" style="text-align:center;padding:40px;">
            <p style="color:#666;">Cargando noticias...</p>
        </div>

        <div id="cat-empty" style="display:none;text-align:center;padding:40px;">
            <p style="color:#666;">No hay noticias disponibles en esta categoría por el momento.</p>
            <a href="../index.html" style="color:var(--primary-color,#00897B);font-weight:bold;">← Volver al inicio</a>
        </div>

        <div id="cat-grid" class="news-grid news-grid-3" style="display:none;"></div>
    </div>
</main>

{footer_html}

<script src="../script.js"></script>
<script>
(async function() {{
    const site = '{site_slug}';
    const category = '{cat_slug}';
    try {{
        const res = await fetch('/api/articles?site=' + site + '&category=' + category + '&limit=30');
        if (!res.ok) throw new Error('fetch error');
        const {{articles}} = await res.json();
        if (!articles?.length) {{
            document.getElementById('cat-loading').style.display = 'none';
            document.getElementById('cat-empty').style.display = 'block';
            return;
        }}
        const grid = document.getElementById('cat-grid');
        grid.innerHTML = articles.map(a => renderCard(a)).join('');
        document.getElementById('cat-loading').style.display = 'none';
        grid.style.display = '';
    }} catch(e) {{
        console.error('Category load error:', e);
        document.getElementById('cat-loading').style.display = 'none';
        document.getElementById('cat-empty').style.display = 'block';
    }}

    function renderCard(a) {{
        const slug = a.slug || '';
        const img = a.imageUrl || '../assets/images/article_placeholder.jpg';
        const cat = a.category || '{cat_name}';
        const catSlug = cat.toLowerCase().replace(/\\s+/g, '-');
        const title = escHtml(a.title || '');
        const excerpt = escHtml(a.excerpt || '');
        const author = escHtml(a.author || 'Redacción');
        const date = a.publishedAt ? new Date(a.publishedAt).toLocaleDateString('es-MX') : '';
        const url = '../articulo/index.html?slug=' + encodeURIComponent(slug);
        return `<article class="news-card">
            <div class="card-image-wrapper">
                <a href="${{url}}"><img src="${{img}}" alt="${{title}}" loading="lazy"></a>
                <span class="card-category-badge cat-${{catSlug}}">${{cat}}</span>
            </div>
            <div class="card-content">
                <h3 class="card-title"><a href="${{url}}">${{title}}</a></h3>
                <p class="card-excerpt">${{excerpt}}</p>
                <div class="card-footer">
                    <span class="card-author">Por ${{author}}</span>
                    <span class="card-date">${{date}}</span>
                </div>
            </div>
        </article>`;
    }}

    function escHtml(s) {{
        return String(s).replace(/&/g,'&amp;').replace(/</g,'<').replace(/>/g,'>').replace(/"/g,'"');
    }}
}})();
</script>
</body>
</html>
'''
        with open(cat_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  [OK] Fixed categoria/{cat_slug}.html: {site_slug}')


# ─────────────────────────────────────────────
# 4. DELETE static article HTML files
# ─────────────────────────────────────────────

def delete_static_articles(site_dir, site_slug):
    articulo_dir = os.path.join(site_dir, 'articulo')
    if not os.path.exists(articulo_dir):
        return
    deleted = 0
    for html_file in glob.glob(os.path.join(articulo_dir, '*.html')):
        if os.path.basename(html_file) != 'index.html':
            os.remove(html_file)
            deleted += 1
    if deleted:
        print(f'  [OK] Deleted {deleted} static article files: {site_slug}')
    else:
        print(f'  [--] No static articles to delete: {site_slug}')


# ─────────────────────────────────────────────
# 5. CLEANUP accidental files
# ─────────────────────────────────────────────

def cleanup_root():
    """Remove accidental files created by Windows shell redirects."""
    for f in ['nul']:
        if os.path.isfile(f):
            os.remove(f)
            print(f'  [OK] Removed accidental file: {f}')


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print('=' * 60)
    print('Optimizing article flow for all sites')
    print('=' * 60)

    for site_slug, site_name in SITES:
        site_dir = os.path.join(SITES_DIR, site_slug)
        if not os.path.isdir(site_dir):
            print(f'\n[SKIP] Directory not found: {site_dir}')
            continue

        print(f'\n--- {site_slug} ({site_name}) ---')
        fix_index_html(site_dir, site_slug)
        create_article_template(site_dir, site_slug, site_name)
        fix_category_pages(site_dir, site_slug, site_name)
        delete_static_articles(site_dir, site_slug)

    print('\n--- Cleanup ---')
    cleanup_root()

    print('\n' + '=' * 60)
    print('Done!')
    print('=' * 60)


if __name__ == '__main__':
    main()
