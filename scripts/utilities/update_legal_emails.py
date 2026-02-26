#!/usr/bin/env python3
"""
Update legal pages with correct domain emails
"""

import os
import re

# Get root directory from script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../../'))
SITES_DIR = os.path.join(ROOT_DIR, 'sites')

# Site slug -> domain mapping
SITE_DOMAINS = {
    'bitacoraurbana': 'bitacoraurbana.lat',
    'cbnnoticias': 'cbnnoticias.click',
    'centralmexico': 'centralmexico.online',
    'mexicoinformado': 'mexicoinformado.lat',
    'nodoinformativo': 'nodoinformativo.lat',
    'noticiasobjetivo': 'noticiasobjetivo.click',
    'radiocinconoticias': 'radiocinconoticias.click',
    'reportecentralmx': 'reportecentral.site',
    'tvmexico': 'tvmexiconews.site',
    'verticenoticias': 'verticenoticias.today',
}

LEGAL_FILES = ['privacidad.html', 'terminos.html', 'contacto.html', 'acerca-de.html']

def update_legal_emails(site_dir, site_slug, domain):
    updated = 0
    for filename in LEGAL_FILES:
        filepath = os.path.join(site_dir, filename)
        if not os.path.exists(filepath):
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Replace generic emails with domain-specific ones
        # Pattern: word@anything.com -> word@domain
        content = re.sub(
            r'([a-zA-Z0-9._%+-]+)@[a-zA-Z0-9.-]+\.(com|mx|org|net)',
            r'\1@' + domain,
            content
        )

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'  [OK] Updated {filename}: {site_slug} -> {domain}')
            updated += 1
        else:
            print(f'  [--] No changes: {filename}: {site_slug}')

    return updated

def main():
    print('=' * 60)
    print('Updating legal emails with real domains')
    print('=' * 60)

    total_updated = 0
    for site_slug, domain in SITE_DOMAINS.items():
        site_dir = os.path.join(SITES_DIR, site_slug)
        if not os.path.isdir(site_dir):
            print(f'\n[SKIP] Directory not found: {site_dir}')
            continue

        print(f'\n--- {site_slug} ({domain}) ---')
        updated = update_legal_emails(site_dir, site_slug, domain)
        total_updated += updated

    print('\n' + '=' * 60)
    print(f'Done! Updated {total_updated} files.')
    print('=' * 60)


if __name__ == '__main__':
    main()
