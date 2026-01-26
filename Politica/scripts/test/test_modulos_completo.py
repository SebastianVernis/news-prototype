#!/usr/bin/env python3
"""
Test de Verificación de 16 Módulos
Verifica que todos los componentes del sistema estén disponibles y funcionales
"""

import os
import sys
from pathlib import Path

# Colores ANSI
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def test_module(module_name: str, module_path: str, description: str) -> dict:
    """
    Verifica si un módulo existe y es importable
    
    Args:
        module_name: Nombre del módulo
        module_path: Ruta relativa al módulo
        description: Descripción del módulo
        
    Returns:
        Dict con resultado del test
    """
    result = {
        'name': module_name,
        'description': description,
        'path': module_path,
        'exists': False,
        'importable': False,
        'error': None
    }
    
    # Verificar si el archivo existe
    full_path = Path(__file__).parent.parent / module_path
    result['exists'] = full_path.exists()
    
    if not result['exists']:
        result['error'] = 'Archivo no encontrado'
        return result
    
    # Intentar importar el módulo
    try:
        # Agregar el directorio de scripts al path
        scripts_dir = str(Path(__file__).parent.parent)
        if scripts_dir not in sys.path:
            sys.path.insert(0, scripts_dir)
        
        # Intentar importar
        module_file = module_path.replace('/', '.').replace('.py', '')
        __import__(module_file)
        result['importable'] = True
    except Exception as e:
        result['error'] = str(e)
    
    return result

def print_module_result(result: dict, index: int):
    """Imprime el resultado de un test de módulo"""
    status = f"{Colors.GREEN}✅{Colors.ENDC}" if result['exists'] and result['importable'] else f"{Colors.RED}❌{Colors.ENDC}"
    
    print(f"\n{Colors.BOLD}{index}. {result['name']}{Colors.ENDC}")
    print(f"   {result['description']}")
    print(f"   Archivo: {status} {result['path']}")
    
    if result['exists']:
        import_status = f"{Colors.GREEN}✅{Colors.ENDC}" if result['importable'] else f"{Colors.RED}❌{Colors.ENDC}"
        print(f"   Importable: {import_status}")
        
        if result['error']:
            print(f"   {Colors.RED}Error: {result['error']}{Colors.ENDC}")
    else:
        print(f"   {Colors.RED}⚠️  Archivo no encontrado{Colors.ENDC}")

def main():
    """Ejecuta la verificación de todos los módulos"""
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🧪 VERIFICACIÓN DE 16 MÓDULOS DEL SISTEMA                       ║
║  Generador Automático de Sitios de Noticias                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
""")
    
    modules = [
        # Módulos principales de generación
        ('Master Orchestrator', 'master_orchestrator.py', 'Orquestador principal del flujo'),
        ('Site Pre-Creation', 'site_pre_creation.py', 'Generador de metadata de sitios'),
        ('Site Name Generator', 'site_name_generator.py', 'Generador de nombres de sitios'),
        ('Domain Verifier', 'domain_verifier.py', 'Verificador de dominios disponibles'),
        
        # Módulos de contenido
        ('NewsAPI', 'api/newsapi.py', 'API de NewsAPI.org'),
        ('Paraphrase', 'paraphrase.py', 'Motor de parafraseo con Blackbox AI'),
        ('Article Expander', 'article-expander.py', 'Expandidor de artículos'),
        
        # Módulos de diseño
        ('Logo Generator SVG', 'logo_generator_svg.py', 'Generador de logos SVG'),
        ('Color Palette Generator', 'color_palette_generator.py', 'Generador de paletas de colores'),
        ('Font Family Generator', 'font_family_generator.py', 'Generador de familias tipográficas'),
        ('Layout Generator', 'layout_generator.py', 'Generador de layouts'),
        ('Layout CSS Generator', 'layout_css_generator.py', 'Generador de CSS para layouts'),
        
        # Módulos de componentes HTML
        ('Header Generator', 'header_generator.py', 'Generador de headers'),
        ('Footer Generator', 'footer_generator.py', 'Generador de footers'),
        ('Legal Pages Generator', 'legal_pages_generator.py', 'Generador de páginas legales'),
        ('Template Combiner', 'template_combiner.py', 'Combinador de templates'),
        
        # Módulo de generación final
        ('Generate Sites', 'generate-sites.py', 'Generador final de sitios HTML'),
    ]
    
    print(f"{Colors.BOLD}Verificando {len(modules)} módulos...{Colors.ENDC}")
    print("=" * 70)
    
    results = []
    for i, (name, path, desc) in enumerate(modules, 1):
        result = test_module(name, path, desc)
        results.append(result)
        print_module_result(result, i)
    
    # Resumen
    print("\n" + "=" * 70)
    print(f"{Colors.BOLD}📊 RESUMEN{Colors.ENDC}\n")
    
    total = len(results)
    exists_count = sum(1 for r in results if r['exists'])
    importable_count = sum(1 for r in results if r['importable'])
    
    print(f"Total de módulos: {total}")
    print(f"Archivos encontrados: {Colors.GREEN}{exists_count}{Colors.ENDC}/{total}")
    print(f"Módulos importables: {Colors.GREEN}{importable_count}{Colors.ENDC}/{total}")
    
    if importable_count == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Todos los módulos están operativos{Colors.ENDC}")
    elif importable_count >= total * 0.8:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  La mayoría de módulos funcionan correctamente{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Varios módulos tienen problemas{Colors.ENDC}")
    
    # Módulos con problemas
    problems = [r for r in results if not r['importable']]
    if problems:
        print(f"\n{Colors.YELLOW}Módulos con problemas:{Colors.ENDC}")
        for r in problems:
            print(f"  - {r['name']}: {r['error'] or 'No encontrado'}")
    
    print("\n" + "=" * 70)
    
    return 0 if importable_count == total else 1

if __name__ == '__main__':
    sys.exit(main())
