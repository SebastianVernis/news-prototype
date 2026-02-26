
#!/usr/bin/env python3
"""
Fix index.html API URLs to use full worker URL
"""

import os
import re

SITES_DIR = 'sites'
WORKER_URL = 'https://news-api.sebastianvernis.workers.dev'

SITES = [
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

def fix_index_html(site_dir, site_slug):
    path = os.path.join(site_dir, 'index.html')
    if not os.path.exists(path):
        print(f'  [SKIP] index.html not found: {site_slug}')
        return False

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix data-api attribute
    content = re.sub(
        r'data-api="/api/articles\?site=' + site_slug + r'(&[^"]*)?"',
        f'data-api="{WORKER_URL}/api/articles?site={site_slug}\\1"',
        content
    )

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [OK] Fixed index.html API URL: {site_slug}')
        return True
    else:
        print(f'  [--] No changes needed: {site_slug}')
        return False

def main():
    print('=' * 60)
    print('Fixing index.html API URLs')
    print('=' * 60)

    fixed_count = 0
    for site_slug in SITES:
        site_dir = os.path.join(SITES_DIR, site_slug)
        if not os.path.isdir(site_dir):
            print(f'\n[SKIP] Directory not found: {site_dir}')
            continue

        print(f'\n--- {site_slug} ---')
        if fix_index_html(site_dir, site_slug):
            fixed_count += 1

    print('\n' + '=' * 60)
    print(f'Done! Fixed {fixed_count} sites.')
    print('=' * 60)


if __name__ == '__main__':
    main()
