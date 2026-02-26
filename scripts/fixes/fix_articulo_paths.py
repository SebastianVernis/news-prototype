#!/usr/bin/env python3
"""
Fix path bugs in sites/*/articulo/index.html for all 10 sites:
1. Header logo: src="logo.png" → src="../logo.png"
2. Footer links: href="acerca-de.html" → href="../acerca-de.html" etc.
"""
import os
import re

SITES = [
    'bitacoraurbana', 'cbnnoticias', 'centralmexico', 'mexicoinformado',
    'nodoinformativo', 'noticiasobjetivo', 'radiocinconoticias',
    'reportecentralmx', 'tvmexico', 'verticenoticias'
]

FOOTER_LINKS = ['acerca-de.html', 'contacto.html', 'privacidad.html', 'terminos.html']

fixed = 0
skipped = 0

for site in SITES:
    path = os.path.join('sites', site, 'articulo', 'index.html')
    if not os.path.exists(path):
        print(f'  SKIP (not found): {path}')
        skipped += 1
        continue

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Fix logo in header: src="logo.png" → src="../logo.png"
    #    Only fix if it's NOT already ../logo.png
    content = re.sub(r'src="logo\.png"', 'src="../logo.png"', content)

    # 2. Fix footer links: href="acerca-de.html" → href="../acerca-de.html"
    #    Only fix bare filenames (not already prefixed with ../)
    for link in FOOTER_LINKS:
        # Match href="acerca-de.html" but NOT href="../acerca-de.html"
        content = re.sub(
            r'href="(?!\.\./|https?://)' + re.escape(link) + r'"',
            f'href="../{link}"',
            content
        )

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  FIXED: {path}')
        fixed += 1
    else:
        print(f'  OK (no changes): {path}')

print(f'\nDone: {fixed} fixed, {skipped} skipped.')
