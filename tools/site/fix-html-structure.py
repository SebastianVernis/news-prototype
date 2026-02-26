#!/usr/bin/env python3
"""
Script para validar y corregir HTML de los 10 sitios
- Cierra etiquetas abiertas
- Corrige enlaces
- Elimina clases que aparecen como texto
- Valida estructura HTML
"""

import os
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))

def fix_html_structure(site_num):
    """Corrige la estructura HTML de un sitio"""
    site_file = SITES_DIR / f'site{site_num}.html'
    
    if not site_file.exists():
        print(f"⚠️ Archivo no encontrado: {site_file}")
        return False
    
    with open(site_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Corregir etiquetas <style> mal cerradas
    content = re.sub(r'</style\s+id="[^"]*">', '</style>', content)
    
    # 2. Corregir enlaces vacíos o #
    content = re.sub(r'href="#"', 'href="index.html"', content)
    
    # 3. Corregir saltos de línea en atributos class
    content = re.sub(r'\n\s*class="', ' class="', content)
    
    # 4. Corregir etiquetas <div> sin cerrar en secciones inyectadas
    # Contar divs abiertos vs cerrados
    open_divs = len(re.findall(r'<div[^>]*>', content))
    close_divs = len(re.findall(r'</div>', content))
    
    if open_divs > close_divs:
        missing_divs = open_divs - close_divs
        # Agregar divs de cierre antes del </main>
        closing_divs = '</div>\n' * missing_divs
        if '</main>' in content:
            content = content.replace('</main>', closing_divs + '</main>')
        elif '</body>' in content:
            content = content.replace('</body>', closing_divs + '</body>')
    
    # 5. Corregir etiquetas <p> sin cerrar
    content = re.sub(r'<p([^>]*)(?=<[^>]+>)', r'<p\1>', content)
    
    # 6. Asegurar que todos los <article> tengan cierre
    open_articles = len(re.findall(r'<article[^>]*>', content))
    close_articles = len(re.findall(r'</article>', content))
    
    if open_articles > close_articles:
        missing_articles = open_articles - close_articles
        closing_articles = '</article>\n' * missing_articles
        content = content.replace('</section>', closing_articles + '</section>')
    
    # 7. Corregir enlaces de categorías (asegurar que existen las rutas)
    content = re.sub(r'href="categoria/([^"]+)"', r'href="#\1"', content)
    
    # 8. Corregir enlaces de artículos
    content = re.sub(r'href="articulo/(\d+)\.html"', r'href="#article-\1"', content)
    
    # 9. Eliminar caracteres raros o clases que aparecen como texto
    content = re.sub(r'\\n', '', content)
    content = re.sub(r'\\t', '', content)
    
    # 10. Asegurar estructura básica HTML
    if not content.strip().startswith('<!DOCTYPE'):
        content = '<!DOCTYPE html>\n' + content
    
    if '<html' not in content:
        content = '<html lang="es">\n' + content
    
    if '</html>' not in content:
        content = content + '\n</html>'
    
    if '<head>' not in content:
        if '<meta' in content:
            content = content.replace('<meta', '<head>\n<meta', 1)
        if '</head>' not in content:
            content = content.replace('</html>', '</head>\n</html>', 1)
    
    if '<body>' not in content:
        content = content.replace('</head>', '</head>\n<body>', 1)
    
    # 11. Validar y corregir script tags
    open_scripts = len(re.findall(r'<script[^>]*>', content))
    close_scripts = len(re.findall(r'</script>', content))
    
    if open_scripts > close_scripts:
        content = content + '</script>\n' * (open_scripts - close_scripts)
    
    # 12. Corregir estilos en línea con comillas mal cerradas
    content = re.sub(r'style="([^"]*?)"([^>]*>)', r'style="\1"\2', content)
    
    # Guardar archivo corregido
    with open(site_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Sitio {site_num} corregido: {open_divs} divs, {close_divs} cierres, {open_articles} artículos")
    return True

def validate_html(site_num):
    """Valida la estructura HTML de un sitio"""
    site_file = SITES_DIR / f'site{site_num}.html'
    
    with open(site_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Verificar etiquetas básicas
    if '<!DOCTYPE html>' not in content:
        issues.append("Falta DOCTYPE")
    
    if '<html' not in content:
        issues.append("Falta <html>")
    
    if '</html>' not in content:
        issues.append("Falta </html>")
    
    if '<head>' not in content:
        issues.append("Falta <head>")
    
    if '</head>' not in content:
        issues.append("Falta </head>")
    
    if '<body>' not in content:
        issues.append("Falta <body>")
    
    if '</body>' not in content:
        issues.append("Falta </body>")
    
    # Contar etiquetas
    open_divs = len(re.findall(r'<div[^>]*>', content))
    close_divs = len(re.findall(r'</div>', content))
    
    if open_divs != close_divs:
        issues.append(f"Divs sin cerrar: {open_divs - close_divs}")
    
    open_articles = len(re.findall(r'<article[^>]*>', content))
    close_articles = len(re.findall(r'</article>', content))
    
    if open_articles != close_articles:
        issues.append(f"Artículos sin cerrar: {open_articles - close_articles}")
    
    open_sections = len(re.findall(r'<section[^>]*>', content))
    close_sections = len(re.findall(r'</section>', content))
    
    if open_sections != close_sections:
        issues.append(f"Secciones sin cerrar: {open_sections - close_sections}")
    
    if issues:
        print(f"⚠️ Sitio {site_num} - Issues: {', '.join(issues)}")
        return False
    else:
        print(f"✅ Sitio {site_num} - HTML válido")
        return True

def main():
    print("🔧 Validando y corrigiendo HTML de los 10 sitios...")
    print("="*60)
    
    # Corregir los 10 sitios
    for i in range(1, 11):
        fix_html_structure(i)
    
    print("="*60)
    print("📋 Validación de HTML:")
    
    # Validar los 10 sitios
    valid_count = 0
    for i in range(1, 11):
        if validate_html(i):
            valid_count += 1
    
    print("="*60)
    print(f"✅ {valid_count}/10 sitios con HTML válido")

if __name__ == "__main__":
    main()
