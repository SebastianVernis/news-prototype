#!/usr/bin/env python3
"""
Fix API URLs in all articulo/index.html files to use full worker URL
"""

import os

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

OLD_URL = "await fetch('/api/articles/'"
NEW_URL = "await fetch('https://news-api.sebastianvernis.workers.dev/api/articles/'"

def fix_articulo(site):
    path = f'sites/{site}/articulo/index.html'
    if not os.path.exists(path):
        print(f'[SKIP] {site}: articulo/index.html not found')
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if OLD_URL in content:
        new_content = content.replace(OLD_URL, NEW_URL)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'[OK] {site}: articulo API URL updated')
    else:
        # Check if already has full URL
        if 'news-api.sebastianvernis.workers.dev' in content:
            print(f'[--] {site}: already has full URL')
        else:
            print(f'[WARN] {site}: pattern not found')

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
