#!/usr/bin/env python3
"""
Fix API URLs in all site index.html files to use full worker URL
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

def fix_site(site):
    path = f'sites/{site}/index.html'
    if not os.path.exists(path):
        print(f'[SKIP] {site}: file not found')
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the apiUrl line
    pattern = r"const apiUrl = document\.querySelector\('#featured-container'\)\?\.dataset\.api \|\| '/api/articles\?site=[^']+&limit=\d+';"
    
    # Replacement with full worker URL
    replacement = f"const apiUrl = '{WORKER_URL}/api/articles?site={site}&limit=20';"
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'[OK] {site}: API URL updated')
    else:
        print(f'[--] {site}: no changes needed')

def main():
    print('=' * 60)
    print('Fixing API URLs in all sites')
    print('=' * 60)
    
    for site in SITES:
        fix_site(site)
    
    print('\n' + '=' * 60)
    print('Done!')
    print('=' * 60)

if __name__ == '__main__':
    main()
