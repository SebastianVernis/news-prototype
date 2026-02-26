#!/usr/bin/env python3
"""
Fix 3 UI issues across all 10 sites:
1. Footer logo broken (wrong src / wrong h3 text)
2. Hero card size (fixed height conflicts with aspect-ratio)
3. Header nav categories cut off (no flex-wrap)
"""
import os
import re

SITES = {
    'bitacoraurbana':    'Bitácora Urbana',
    'cbnnoticias':       'CBN Noticias',
    'centralmexico':     'Central México',
    'mexicoinformado':   'México Informado',
    'nodoinformativo':   'Nodo Informativo',
    'noticiasobjetivo':  'Noticias Objetivo',
    'radiocinconoticias':'Radio Cinco Noticias',
    'reportecentralmx':  'Reporte Central MX',
    'tvmexico':          'TV México',
    'verticenoticias':   'Vértice Noticias',
}

# ─────────────────────────────────────────────
# 1. FIX FOOTER LOGO
# ─────────────────────────────────────────────
def fix_footer_logo(content: str, site_name: str, logo_path: str) -> str:
    """Replace the footer-logo div with correct logo.png and site name."""
    # Match the entire footer-logo div (img + h3, possibly with whitespace/newlines)
    pattern = r'<div class="footer-logo">\s*<img[^>]*?>\s*<h3[^>]*>[^<]*</h3>\s*</div>'
    replacement = (
        f'<div class="footer-logo">'
        f'<img alt="{site_name}" src="{logo_path}" style="height:40px;width:auto;object-fit:contain;"/>'
        f'<h3>{site_name}</h3>'
        f'</div>'
    )
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if new_content == content:
        # Try alternate pattern (pretty-printed HTML with indentation)
        pattern2 = r'<div class="footer-logo">[\s\S]*?</div>'
        # Only replace if it contains an img tag (to avoid false positives)
        def replace_if_logo(m):
            block = m.group(0)
            if '<img' in block and ('footer-logo' in block or 'logo' in block.lower()):
                return replacement
            return block
        new_content = re.sub(pattern2, replace_if_logo, content, flags=re.DOTALL)
    return new_content

# ─────────────────────────────────────────────
# 2. FIX CSS: HERO SIZE + NAV WRAP
# ─────────────────────────────────────────────
def fix_css(content: str) -> str:
    """
    - Remove fixed height from .card-hero (use aspect-ratio on img instead)
    - Add flex-wrap: wrap to .main-nav so categories don't get cut off
    """
    # --- Hero: remove height:500px from .card-hero ---
    # Pattern: .card-hero { ... height: 500px; ... }
    content = re.sub(
        r'(\.card-hero\s*\{[^}]*?)height\s*:\s*\d+px\s*;',
        r'\1',
        content
    )
    # --- Hero img: replace height:100% with height:auto + aspect-ratio ---
    content = re.sub(
        r'(\.card-hero\s+img\s*\{[^}]*?)height\s*:\s*100%\s*;',
        r'\1height: auto; aspect-ratio: 16/9;',
        content
    )
    # --- Nav: add flex-wrap: wrap if not already present ---
    def add_flex_wrap(m):
        block = m.group(0)
        if 'flex-wrap' not in block:
            # Insert before closing brace
            block = block.rstrip('}').rstrip() + '; flex-wrap: wrap; }'
        return block
    content = re.sub(r'\.main-nav\s*\{[^}]+\}', add_flex_wrap, content)
    return content

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def process_html_file(filepath: str, site_name: str, logo_path: str):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = fix_footer_logo(content, site_name, logo_path)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'  ✓ Footer logo fixed: {filepath}')
        else:
            print(f'  - No footer-logo found: {filepath}')
    except Exception as e:
        print(f'  ✗ Error processing {filepath}: {e}')

def process_css_file(filepath: str):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = fix_css(content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'  ✓ CSS fixed: {filepath}')
        else:
            print(f'  - CSS already OK: {filepath}')
    except Exception as e:
        print(f'  ✗ Error processing {filepath}: {e}')

def main():
    for site_slug, site_name in SITES.items():
        site_dir = f'sites/{site_slug}'
        if not os.path.isdir(site_dir):
            print(f'[SKIP] {site_dir} not found')
            continue

        print(f'\n[{site_slug}] {site_name}')

        # Root-level HTML files → logo path = "logo.png"
        root_files = [
            'index.html', 'acerca-de.html', 'contacto.html',
            'privacidad.html', 'terminos.html'
        ]
        for fname in root_files:
            fpath = os.path.join(site_dir, fname)
            if os.path.exists(fpath):
                process_html_file(fpath, site_name, 'logo.png')

        # Subdirectory HTML files → logo path = "../logo.png"
        for subdir in ['categoria', 'articulo']:
            subdir_path = os.path.join(site_dir, subdir)
            if os.path.isdir(subdir_path):
                for fname in os.listdir(subdir_path):
                    if fname.endswith('.html'):
                        fpath = os.path.join(subdir_path, fname)
                        process_html_file(fpath, site_name, '../logo.png')

        # CSS fix
        css_path = os.path.join(site_dir, 'style.css')
        if os.path.exists(css_path):
            process_css_file(css_path)

    print('\n✅ Done!')

if __name__ == '__main__':
    main()
