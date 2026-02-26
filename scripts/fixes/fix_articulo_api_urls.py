#!/usr/bin/env python3
"""
Fix API URLs in all articulo/index.html files to use full worker URL
"""

import os
import re

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

WORKER_URL = 'https://news-api.sebastianvernis.workers.dev'

def fix_articulo(site):
    path = f'sites/{site}/articulo/index.html'
    if not os.path.exists(path):
        print(f'[SKIP] {site}: articulo/index.html not found')
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the fetch call with relative URL
    # Match: fetch('/api/articles/' + encodeURIComponent(slug))
    pattern = r"fetch\(['\"]/api/articles/\s*\+\s*encodeURIComponent\(([^)]+)\)['\"]\)"
    
    # Replacement with full worker URL
    replacement = f"fetch('{WORKER_URL}/api/articles/' + encodeURIComponent(\\1))"
    
    new_content = re.sub(pattern, replacement, content)
    
    # Also try alternative pattern without encodeURIComponent
    pattern2 = r"fetch\(['\"]/api/articles/([^'\"]+)['\"]\)"
    replacement2 = f"fetch('{WORKER_URL}/api/articles/\\1')"
    new_content = re.sub(pattern2, replacement2, new_content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'[OK] {site}: articulo API URL updated')
    else:
        print(f'[--] {site}: no changes needed (pattern not found)')

def main():
    print('=' * 60)
    print('Fixing articulo/index.html API URLs')
    print('=' * 60)
    
    for site in SITES:
        fix_articulo(site)
    
    print('\n' + '=' * 60)
    print('Done!')
    print('=' * 60)

if __name__ == '__main__':
    main()
