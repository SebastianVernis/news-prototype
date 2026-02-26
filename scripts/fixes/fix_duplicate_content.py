#!/usr/bin/env python3
"""
Limpia el contenido duplicado en los index.html de los sitios.
Extrae solo la primera parte válida del documento HTML.
"""

import os
import re

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

def clean_index(site_slug):
    site_dir = os.path.join('sites', site_slug)
    path = os.path.join(site_dir, 'index.html')
    
    if not os.path.exists(path):
        print(f'  [SKIP] No existe: {site_slug}')
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar el primer <!DOCTYPE html> completo hasta </html>
    # Pero ignorar el segundo <!DOCTYPE que aparece como duplicado
    match = re.search(r'(<!DOCTYPE html>.*?</html>)', content, re.DOTALL | re.IGNORECASE)
    if not match:
        print(f'  [SKIP] No se encontró HTML válido: {site_slug}')
        return
    
    first_html = match.group(1)
    
    # Verificar si hay contenido duplicado (segundo <!DOCTYPE)
    if content.count('<!DOCTYPE html>') > 1:
        print(f'  [FIX] Limpiando duplicado: {site_slug}')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(first_html)
        print(f'  [OK] Limpiado: {site_slug}')
    else:
        print(f'  [--] Sin duplicados: {site_slug}')

def main():
    print('=' * 60)
    print('Limpiando contenido duplicado en index.html')
    print('=' * 60)
    
    for site_slug in SITES:
        try:
            clean_index(site_slug)
        except Exception as e:
            print(f'  [ERROR] {site_slug}: {e}')
    
    print('\n' + '=' * 60)
    print('¡Limpieza completada!')
    print('=' * 60)

if __name__ == '__main__':
    main()
