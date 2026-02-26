#!/usr/bin/env python3
"""
Fix category HTML API URLs to use full worker URL
"""

import os
import re
import glob

SITES_DIR = 'sites'
WORKER_URL = 'https://news-api.sebastianvernis.workers.dev'

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

CATEGORIES = ['nacional', 'politica', 'economia', 'deportes']

def fix_category_files(site_dir, site_slug):
    fixed = 0
    for cat in CATEGORIES:
        cat_file = os.path.join(site_dir, 'categoria', f'{cat}.html')
        if not os.path.exists(cat_file):
            continue

        with open(cat_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Fix fetch URL
        content = re.sub(
            r"await fetch\('/api/articles\?",
            f"await fetch('{WORKER_URL}/api/articles?",
            content
        )

        if content != original:
            with open(cat_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [OK] Fixed categoria/{cat}.html: {site_slug}')
            fixed += 1
        else:
            print(f'  [--] No changes: categoria/{cat}.html: {site_slug}')

    return fixed

def main():
    print('=' * 60)
    print('Fixing category HTML API URLs')
    print('=' * 60)

    total_fixed = 0
    for site_slug in SITES:
        site_dir = os.path.join(SITES_DIR, site_slug)
        if not os.path.isdir(site_dir):
            print(f'\n[SKIP] Directory not found: {site_dir}')
            continue

        print(f'\n--- {site_slug} ---')
        fixed = fix_category_files(site_dir, site_slug)
        total_fixed += fixed

    print('\n' + '=' * 60)
    print(f'Done! Fixed {total_fixed} category files.')
    print('=' * 60)


if __name__ == '__main__':
    main()
