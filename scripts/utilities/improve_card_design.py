#!/usr/bin/env python3
"""
Improve card design across all sites:
- Rounded borders (border-radius: 12px)
- 3D shadow effects with hover
- Proper padding
- Responsive grid for categories (4 cols -> 3 -> 2 -> 1)
"""

import os
import re

SITES_DIR = 'sites'

SITES = [
    'bitacoraurbana',
    'cbnnoticias',
    'centralmexico',
    'mexicoinformado',
    'nodoinformativo',
    'noticiasobjetivo',
    'radiocinconoticias',
    'reportecentralmx',
    'tvmexico',
    'verticenoticias',
]

# CSS to add for improved card design
CARD_CSS = '''
/* Improved Card Design - 3D Effects */
.card-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
    padding: 20px 0;
}

@media (max-width: 1200px) {
    .card-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 900px) {
    .card-grid { grid-template-columns: repeat(2, 1fr); gap: 20px; }
}

@media (max-width: 600px) {
    .card-grid { grid-template-columns: 1fr; gap: 16px; }
}

/* Article Card Base Styles */
.article-card {
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.06);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    display: flex;
    flex-direction: column;
}

.article-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15), 0 8px 16px rgba(0,0,0,0.1);
}

.article-card .card-image-wrapper {
    position: relative;
    overflow: hidden;
    border-radius: 12px 12px 0 0;
}

.article-card .card-image-wrapper img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.article-card:hover .card-image-wrapper img {
    transform: scale(1.05);
}

.article-card .card-content {
    padding: 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
}

.article-card .card-category-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    width: fit-content;
}

.article-card .card-title {
    font-size: 1.1rem;
    font-weight: 700;
    line-height: 1.4;
    margin: 0 0 12px 0;
    color: #1a1a1a;
}

.article-card .card-title a {
    color: inherit;
    text-decoration: none;
    transition: color 0.2s;
}

.article-card .card-title a:hover {
    color: #0066cc;
}

.article-card .card-excerpt {
    font-size: 0.9rem;
    line-height: 1.6;
    color: #555;
    margin: 0 0 16px 0;
    flex: 1;
}

.article-card .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 16px;
    border-top: 1px solid #eee;
    font-size: 0.8rem;
    color: #777;
}

.article-card .card-author {
    font-weight: 500;
}

.article-card .card-date {
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Horizontal Card Variant */
.horizontal-card {
    display: flex;
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0,0,0,0.07), 0 1px 3px rgba(0,0,0,0.06);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 20px;
}

.horizontal-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 32px rgba(0,0,0,0.12), 0 6px 12px rgba(0,0,0,0.08);
}

.horizontal-card > a {
    flex: 0 0 280px;
    overflow: hidden;
}

.horizontal-card img {
    width: 280px;
    height: 180px;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.horizontal-card:hover img {
    transform: scale(1.05);
}

.horizontal-card-content {
    padding: 20px;
    flex: 1;
    display: flex;
    flex-direction: column;
}

@media (max-width: 768px) {
    .horizontal-card { flex-direction: column; }
    .horizontal-card > a { flex: none; }
    .horizontal-card img { width: 100%; height: 200px; }
}

/* Hero Card */
.hero-card {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    transition: all 0.3s ease;
}

.hero-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 50px rgba(0,0,0,0.2);
}

.hero-card img {
    width: 100%;
    aspect-ratio: 16/9;
    object-fit: cover;
}

.hero-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 40px;
    background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
    color: white;
}

.hero-overlay .hero-title {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 12px 0;
    line-height: 1.2;
}

.hero-overlay .hero-excerpt {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0;
}

/* Category Badge Colors */
.cat-nacional { background: #e3f2fd; color: #1565c0; }
.cat-politica { background: #fce4ec; color: #c2185b; }
.cat-economia { background: #e8f5e9; color: #2e7d32; }
.cat-deportes { background: #fff3e0; color: #ef6c00; }
.cat-internacional { background: #f3e5f5; color: #7b1fa2; }
.cat-cultura { background: #e0f2f1; color: #00695c; }
.cat-tecnologia { background: #e8eaf6; color: #283593; }
.cat-salud { background: #fce4ec; color: #ad1457; }
.cat-general { background: #f5f5f5; color: #616161; }
'''

def add_card_css_to_style(site_dir, site_slug):
    """Add card CSS to style.css"""
    style_path = os.path.join(site_dir, 'style.css')
    if not os.path.exists(style_path):
        print(f'  [SKIP] style.css not found: {site_slug}')
        return False

    with open(style_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already has card styles
    if '.article-card' in content:
        print(f'  [--] Card styles already exist: {site_slug}')
        return False

    # Add card CSS at the end
    with open(style_path, 'a', encoding='utf-8') as f:
        f.write('\n\n/* ===== IMPROVED CARD DESIGN ===== */\n')
        f.write(CARD_CSS)

    print(f'  [OK] Added card CSS: {site_slug}')
    return True

def update_index_html(site_dir, site_slug):
    """Update index.html to use new card classes"""
    index_path = os.path.join(site_dir, 'index.html')
    if not os.path.exists(index_path):
        return False

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Update render functions to use new card classes
    # Replace horizontal-card with improved version
    content = re.sub(
        r'class="horizontal-card"',
        'class="article-card"',
        content
    )

    # Update category badge classes
    content = re.sub(
        r'class="category-badge cat-',
        'class="card-category-badge cat-',
        content
    )

    # Update news container to use card-grid
    content = re.sub(
        r'id="news-container" class="horizontal-list"',
        'id="news-container" class="card-grid"',
        content
    )

    if content != original:
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [OK] Updated index.html: {site_slug}')
        return True
    else:
        print(f'  [--] No changes needed: {site_slug}')
        return False

def update_category_html(site_dir, site_slug):
    """Update category pages to use card-grid"""
    updated = 0
    categoria_dir = os.path.join(site_dir, 'categoria')
    if not os.path.exists(categoria_dir):
        return 0

    for filename in os.listdir(categoria_dir):
        if not filename.endswith('.html'):
            continue

        filepath = os.path.join(categoria_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Update to use card-grid and article-card classes
        content = re.sub(
            r'class="news-grid"',
            'class="card-grid"',
            content
        )
        content = re.sub(
            r'class="news-card"',
            'class="article-card"',
            content
        )
        content = re.sub(
            r'class="card-category-badge ',
            'class="card-category-badge ',
            content
        )

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1

    if updated:
        print(f'  [OK] Updated {updated} category pages: {site_slug}')
    return updated

def main():
    print('=' * 60)
    print('Improving card design across all sites')
    print('=' * 60)

    total_css = 0
    total_index = 0
    total_category = 0

    for site_slug in SITES:
        site_dir = os.path.join(SITES_DIR, site_slug)
        if not os.path.isdir(site_dir):
            print(f'\n[SKIP] Directory not found: {site_dir}')
            continue

        print(f'\n--- {site_slug} ---')

        if add_card_css_to_style(site_dir, site_slug):
            total_css += 1

        if update_index_html(site_dir, site_slug):
            total_index += 1

        cat_updated = update_category_html(site_dir, site_slug)
        total_category += cat_updated

    print('\n' + '=' * 60)
    print(f'Summary:')
    print(f'  - CSS files updated: {total_css}')
    print(f'  - Index files updated: {total_index}')
    print(f'  - Category pages updated: {total_category}')
    print('=' * 60)


if __name__ == '__main__':
    main()
