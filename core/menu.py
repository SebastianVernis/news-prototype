#!/usr/bin/env python3
"""
🎮 MENÚ PRINCIPAL INTERACTIVO
Sistema de Generación de Sitios de Noticias
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional

# Colores ANSI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Limpia la pantalla"""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header():
    """Imprime el header del menú"""
    clear_screen()
    print(f"""
{Colors.CYAN}╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║  {Colors.BOLD}📰 GENERADOR AUTOMÁTICO DE SITIOS DE NOTICIAS{Colors.ENDC}{Colors.CYAN}                  ║
║                                                                    ║
║  Sistema modular con 16 componentes integrados                    ║
║  Genera sitios completos en 2-3 minutos                           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
""")

def print_menu(title: str, options: list, show_back: bool = True):
    """
    Imprime un menú con opciones
    
    Args:
        title: Título del menú
        options: Lista de tuplas (key, description)
        show_back: Si mostrar opción de volver
    """
    print(f"\n{Colors.BOLD}{Colors.BLUE}═══ {title} ═══{Colors.ENDC}\n")
    
    for key, desc in options:
        print(f"  {Colors.GREEN}{key}{Colors.ENDC}) {desc}")
    
    if show_back:
        print(f"\n  {Colors.YELLOW}0{Colors.ENDC}) ← Volver al menú principal")
    
    print(f"  {Colors.RED}q{Colors.ENDC}) ✖ Salir\n")

def get_user_choice(valid_options: list) -> str:
    """
    Obtiene la opción del usuario
    
    Args:
        valid_options: Lista de opciones válidas
        
    Returns:
        Opción seleccionada
    """
    while True:
        choice = input(f"{Colors.CYAN}➜ Selecciona una opción: {Colors.ENDC}").strip().lower()
        
        if choice in valid_options or choice in ['0', 'q']:
            return choice
        
        print(f"{Colors.RED}✖ Opción inválida. Intenta de nuevo.{Colors.ENDC}")

def pause():
    """Pausa hasta que el usuario presione Enter"""
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")

def listar_sitios_disponibles() -> list:
    """
    Lista todos los sitios generados
    
    Returns:
        Lista de directorios de sitios
    """
    repo_root = Path(__file__).resolve().parents[1]
    site_dir = repo_root / 'output' / 'generated_sites'
    if not site_dir.exists():
        return []
    
    sites = sorted([d for d in site_dir.iterdir() if d.is_dir() and d.name.startswith('site_')])
    return sites

def servir_sitio(site_path: Path, port: int = 8000):
    """
    Sirve un sitio en un servidor HTTP
    
    Args:
        site_path: Ruta al directorio del sitio
        port: Puerto a usar
    """
    print(f"\n{Colors.GREEN}🌐 Sirviendo sitio en el puerto {port}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'═'*70}{Colors.ENDC}\n")
    print(f"  📁 Directorio: {site_path}")
    print(f"  🔗 URL: http://localhost:{port}")
    print(f"\n{Colors.YELLOW}Presiona Ctrl+C para detener el servidor{Colors.ENDC}\n")
    print(f"{Colors.CYAN}{'═'*70}{Colors.ENDC}\n")
    
    try:
        subprocess.run(['python3', '-m', 'http.server', str(port)], cwd=site_path)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}🛑 Servidor detenido{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error al servir sitio: {e}{Colors.ENDC}")

def menu_servir_sitios():
    """Menú para servir sitios generados"""
    while True:
        print_header()
        
        sites = listar_sitios_disponibles()
        
        if not sites:
            print(f"\n{Colors.RED}❌ No hay sitios generados{Colors.ENDC}")
            print(f"\n{Colors.YELLOW}Genera un sitio primero:{Colors.ENDC}")
            print(f"  Menú Principal → 1 (Generación) → 1 (Generar rápido)")
            pause()
            break
        
        print_menu("🌐 SERVIR SITIOS EN NAVEGADOR", [
            ('1', f'🚀 Servir último sitio (site_1) en puerto 8000'),
            ('2', f'📋 Seleccionar sitio específico'),
            ('3', f'🌍 Servir todos los sitios (puertos múltiples)'),
            ('4', f'📊 Listar todos los sitios disponibles ({len(sites)} sitios)')
        ])
        
        choice = get_user_choice(['1', '2', '3', '4'])
        
        if choice == '0':
            break
        elif choice == 'q':
            sys.exit(0)
        elif choice == '1':
            # Servir site_1
            site_1 = Path(__file__).resolve().parents[1] / 'output' / 'generated_sites' / 'site_1'
            if site_1.exists():
                servir_sitio(site_1, 8000)
            else:
                print(f"\n{Colors.RED}❌ site_1 no existe{Colors.ENDC}")
                pause()
        
        elif choice == '2':
            # Seleccionar sitio específico
            print(f"\n{Colors.GREEN}📋 Sitios disponibles:{Colors.ENDC}\n")
            for idx, site in enumerate(sites, 1):
                index_file = site / 'index.html'
                size = sum(f.stat().st_size for f in site.rglob('*') if f.is_file()) / (1024 * 1024)
                files_count = len(list(site.rglob('*.html')))
                print(f"  {idx}) {site.name} ({files_count} páginas, {size:.2f} MB)")
            
            print(f"\n  0) ← Volver")
            
            try:
                site_choice = input(f"\n{Colors.CYAN}Selecciona un sitio (número): {Colors.ENDC}").strip()
                
                if site_choice == '0':
                    continue
                
                site_idx = int(site_choice) - 1
                if 0 <= site_idx < len(sites):
                    port_input = input(f"{Colors.CYAN}Puerto (default: 8000): {Colors.ENDC}").strip()
                    port = int(port_input) if port_input else 8000
                    
                    servir_sitio(sites[site_idx], port)
                else:
                    print(f"{Colors.RED}✖ Número inválido{Colors.ENDC}")
                    pause()
            except ValueError:
                print(f"{Colors.RED}✖ Entrada inválida{Colors.ENDC}")
                pause()
        
        elif choice == '3':
            # Servir todos los sitios
            if len(sites) > 10:
                print(f"\n{Colors.YELLOW}⚠️  Hay {len(sites)} sitios. Esto abrirá muchos servidores.{Colors.ENDC}")
                confirm = input(f"{Colors.CYAN}¿Continuar? (s/N): {Colors.ENDC}").strip().lower()
                if confirm != 's':
                    continue
            
            print(f"\n{Colors.GREEN}🌍 Iniciando servidores para {len(sites)} sitios...{Colors.ENDC}\n")
            print(f"{Colors.YELLOW}IMPORTANTE:{Colors.ENDC}")
            print(f"  - Cada sitio se servirá en un puerto diferente")
            print(f"  - Los servidores se ejecutarán en segundo plano")
            print(f"  - Para detener, usa: pkill -f 'http.server'")
            print(f"\n{Colors.CYAN}{'═'*70}{Colors.ENDC}\n")
            
            for idx, site in enumerate(sites):
                port = 8000 + idx
                print(f"  🌐 {site.name}: http://localhost:{port}")
                
                # Ejecutar en segundo plano
                subprocess.Popen(
                    ['python3', '-m', 'http.server', str(port)],
                    cwd=site,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            print(f"\n{Colors.GREEN}✅ {len(sites)} servidores iniciados{Colors.ENDC}")
            print(f"\n{Colors.YELLOW}Para detener todos los servidores:{Colors.ENDC}")
            print(f"  pkill -f 'http.server'")
            pause()
        
        elif choice == '4':
            # Listar todos los sitios
            print(f"\n{Colors.GREEN}📋 Sitios disponibles: {len(sites)}{Colors.ENDC}\n")
            
            for idx, site in enumerate(sites, 1):
                # Leer metadata si existe
                index_file = site / 'index.html'
                
                if index_file.exists():
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extraer título
                        import re
                        title_match = re.search(r'<title>(.*?)</title>', content)
                        title = title_match.group(1) if title_match else 'Sin título'
                else:
                    title = 'Sin index.html'
                
                # Contar archivos
                html_files = len(list(site.glob('*.html')))
                images = len(list(site.glob('images/*.jpg')))
                size = sum(f.stat().st_size for f in site.rglob('*') if f.is_file()) / (1024 * 1024)
                
                print(f"  {Colors.BOLD}{idx}. {site.name}{Colors.ENDC}")
                print(f"     Título: {title[:60]}")
                print(f"     Archivos: {html_files} HTML, {images} imágenes")
                print(f"     Tamaño: {size:.2f} MB")
                print(f"     Puerto sugerido: {8000 + idx - 1}")
                print()
            
            pause()

def run_script(script_path: str, description: str, args: list = None):
    """
    Ejecuta un script Python
    
    Args:
        script_path: Ruta al script
        description: Descripción de lo que hace
        args: Argumentos adicionales
    """
    print(f"\n{Colors.GREEN}🚀 Ejecutando: {description}{Colors.ENDC}\n")
    print(f"{Colors.CYAN}{'═'*70}{Colors.ENDC}\n")
    
    try:
        repo_root = Path(__file__).resolve().parents[1]
        script_file = (repo_root / script_path).resolve()
        cmd = ['python3', str(script_file)]
        if args:
            cmd.extend(args)

        result = subprocess.run(cmd, cwd=repo_root)
        
        print(f"\n{Colors.CYAN}{'═'*70}{Colors.ENDC}")
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Completado exitosamente{Colors.ENDC}")
        else:
            print(f"{Colors.RED}❌ Hubo un error (código: {result.returncode}){Colors.ENDC}")
        
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error ejecutando script: {e}{Colors.ENDC}")
    
    pause()

def view_documentation(doc_path: str, title: str):
    """
    Muestra documentación usando less o cat
    
    Args:
        doc_path: Ruta al documento
        title: Título del documento
    """
    print(f"\n{Colors.GREEN}📖 Mostrando: {title}{Colors.ENDC}\n")
    print(f"{Colors.CYAN}{'═'*70}{Colors.ENDC}\n")
    
    try:
        repo_root = Path(__file__).resolve().parents[1]
        doc_file = (repo_root / doc_path).resolve()
        # Intentar usar bat (mejor que less)
        try:
            subprocess.run(['bat', '--paging=always', '--style=plain', str(doc_file)])
        except FileNotFoundError:
            # Si no hay bat, usar less
            try:
                subprocess.run(['less', '-R', str(doc_file)])
            except FileNotFoundError:
                # Si no hay less, usar cat con paginación manual
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(content)
                    pause()
    
    except Exception as e:
        print(f"{Colors.RED}❌ Error mostrando documento: {e}{Colors.ENDC}")
        pause()

def menu_generacion():
    """Menú de generación de sitios"""
    while True:
        print_header()
        print_menu("🏗️  GENERACIÓN DE SITIOS", [
            ('1', '🚀 Generar sitio completo (20 noticias, modo rápido)'),
            ('2', '🔍 Generar sitio con verificación de dominios'),
            ('3', '💾 Generar usando cache de noticias'),
            ('4', '🔌 Generar en MODO OFFLINE (Spacy+NLTK, sin APIs de IA)'),
            ('5', '⚡ Generar con Blackbox paralelo (2 workers)'),
            ('6', '🤖 Generar con Blackbox estándar'),
            ('7', '⚙️  Generar con opciones personalizadas'),
            ('8', '📊 Ver último sitio generado'),
            ('9', '🌐 Servir sitios en navegador')
        ])

        choice = get_user_choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

        if choice == '0':
            break
        elif choice == 'q':
            sys.exit(0)
        elif choice == '1':
            run_script('core/scripts/master_orchestrator.py', 'Generación rápida de sitio completo')
        elif choice == '2':
            run_script('core/scripts/master_orchestrator.py', 'Generación con verificación de dominios',
                      ['--verificar-dominios'])
        elif choice == '3':
            run_script('core/scripts/master_orchestrator.py', 'Generación usando cache',
                      ['--usar-cache'])
        elif choice == '4':
            print(f"\n{Colors.CYAN}🔌 MODO OFFLINE{Colors.ENDC}")
            print(f"{Colors.GREEN}Usa Spacy + NLTK para parafraseo sin APIs de IA{Colors.ENDC}")
            print(f"{Colors.YELLOW}Ventajas:{Colors.ENDC}")
            print("  • No requiere API keys de Blackbox/Gemini")
            print("  • Funciona 100% offline")
            print("  • Más rápido (no hay latencia de red)")
            print(f"{Colors.YELLOW}Nota:{Colors.ENDC} La calidad es diferente al usar IA generativa")
            confirm = input(f"\n{Colors.CYAN}¿Continuar? (s/N): {Colors.ENDC}").strip().lower()
            if confirm == 's':
                run_script('core/scripts/master_orchestrator.py', 'Generación modo offline (Spacy+NLTK)',
                          ['--offline'])
        elif choice == '5':
            print(f"\n{Colors.CYAN}⚡ BLACKBOX PARALELO{Colors.ENDC}")
            print(f"{Colors.YELLOW}Requiere 2+ API keys configuradas en .env:{Colors.ENDC}")
            print("  - BLACKBOX_API_KEY_PRO")
            print("  - BLACKBOX_API_KEY_FREE")
            print("  - BLACKBOX_API_KEY_ALT")
            confirm = input(f"\n{Colors.CYAN}¿Continuar? (s/N): {Colors.ENDC}").strip().lower()
            if confirm == 's':
                run_script('core/scripts/blackbox_parallel.py', 'Parafraseo paralelo con Blackbox')
        elif choice == '6':
            print(f"\n{Colors.CYAN}🤖 BLACKBOX ESTÁNDAR{Colors.ENDC}")
            print(f"{Colors.YELLOW}Usa BLACKBOX_API_KEY única{Colors.ENDC}")
            run_script('core/scripts/paraphrase.py', 'Parafraseo estándar con Blackbox')
        elif choice == '7':
            print(f"\n{Colors.YELLOW}⚙️  Opciones disponibles:{Colors.ENDC}")
            print("  --verificar-dominios  : Verificar disponibilidad con WHOIS")
            print("  --usar-cache         : Usar noticias guardadas")
            print("  --output-dir PATH    : Directorio de salida personalizado")
            print("  --api-whois          : Usar APILayer WHOIS API")
            print("  --offline            : Modo offline (sin APIs externas)")

            args_input = input(f"\n{Colors.CYAN}Ingresa argumentos (o Enter para ninguno): {Colors.ENDC}").strip()
            args = args_input.split() if args_input else []

            run_script('core/scripts/master_orchestrator.py', 'Generación personalizada', args)
        elif choice == '8':
            site_dir = Path(__file__).resolve().parents[1] / 'output' / 'generated_sites' / 'site_1'
            if site_dir.exists():
                print(f"\n{Colors.GREEN}📁 Último sitio generado:{Colors.ENDC}")
                print(f"   Ubicación: {site_dir}")
                print(f"\n{Colors.CYAN}Para visualizarlo:{Colors.ENDC}")
                print(f"   cd {site_dir}")
                print(f"   python -m http.server 8001")
                print(f"   Abrir: http://localhost:8001")
            else:
                print(f"\n{Colors.RED}❌ No hay sitios generados aún{Colors.ENDC}")
            pause()
        elif choice == '9':
            menu_servir_sitios()

def menu_tests():
    """Menú de tests"""
    while True:
        print_header()
        print_menu("🧪 TESTS Y VERIFICACIÓN", [
            ('1', '✅ Test de integración de módulos (verificar 16 módulos)'),
            ('2', '🚀 Test de flujo completo (2 artículos, rápido)'),
            ('3', '🔌 Test de parafraseo OFFLINE (Spacy+NLTK)'),
            ('4', '🤖 Test de Blackbox API'),
            ('5', '⚡ Test de Blackbox paralelo'),
            ('6', '📝 Test de parafraseo rápido'),
            ('7', '🔌 Test de parafraseo Blackbox directo'),
            ('8', '🔗 Test de integración general'),
            ('9', '📊 Ver resultados del último test')
        ])

        choice = get_user_choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])

        if choice == '0':
            break
        elif choice == 'q':
            sys.exit(0)
        elif choice == '1':
            run_script('core/scripts/test/test_modulos_completo.py',
                      'Test de verificación de 16 módulos')
        elif choice == '2':
            run_script('core/scripts/test/test_flujo_completo.py',
                      'Test de flujo end-to-end (2 artículos)')
        elif choice == '3':
            print(f"\n{Colors.CYAN}🔌 TEST PARAFRASEO OFFLINE{Colors.ENDC}")
            print(f"{Colors.GREEN}Prueba el parafraseo lingüístico con Spacy+NLTK{Colors.ENDC}")
            print(f"{Colors.YELLOW}No requiere API keys - 100% offline{Colors.ENDC}")
            run_script('core/scripts/linguistic_paraphraser.py',
                      'Test de parafraseo offline (Spacy+NLTK)')
        elif choice == '4':
            run_script('core/scripts/test/test_blackbox.py',
                      'Test de conexión con Blackbox AI')
        elif choice == '5':
            print(f"\n{Colors.CYAN}⚡ TEST BLACKBOX PARALELO{Colors.ENDC}")
            print(f"{Colors.YELLOW}Este test usa múltiples API keys para acelerar el parafraseo{Colors.ENDC}")
            run_script('core/scripts/blackbox_parallel.py',
                      'Test de parafraseo paralelo con Blackbox')
        elif choice == '6':
            run_script('core/scripts/test/test_paraphrase_quick.py',
                      'Test rápido de parafraseo')
        elif choice == '7':
            print(f"\n{Colors.CYAN}🔌 TEST PARAFRASEO BLACKBOX DIRECTO{Colors.ENDC}")
            print(f"{Colors.YELLOW}Prueba el módulo paraphrase.py directamente{Colors.ENDC}")
            run_script('core/scripts/paraphrase.py',
                      'Test de parafraseo Blackbox directo')
        elif choice == '8':
            run_script('core/scripts/test/test_integration.py',
                      'Test de integración general')
        elif choice == '9':
            # Mostrar resultados de tests disponibles
            print(f"\n{Colors.CYAN}📊 RESULTADOS DE TESTS DISPONIBLES:{Colors.ENDC}\n")

            result_files = [
                ('output/tests/test_flujo_completo_resultado.json', 'Flujo Completo'),
                ('output/tests/noticias_blackbox_parallel_test.json', 'Blackbox Paralelo'),
                ('output/tests/test_results.json', 'Integración'),
            ]

            found_any = False
            repo_root = Path(__file__).resolve().parents[1]
            for file_path, name in result_files:
                result_file = repo_root / file_path
                if result_file.exists():
                    found_any = True
                    try:
                        import json
                        with open(result_file, 'r') as f:
                            data = json.load(f)

                        print(f"{Colors.BOLD}{name}:{Colors.ENDC}")
                        if 'timestamp' in data:
                            print(f"  Timestamp: {data.get('timestamp')}")
                        if 'success' in data:
                            print(f"  Éxito: {'✅' if data.get('success') else '❌'}")
                        if 'tiempo_total_segundos' in data:
                            print(f"  Tiempo: {data.get('tiempo_total_segundos', 0):.2f}s")

                        # Stats específicos
                        if 'stats' in data:
                            stats = data.get('stats', {})
                            print(f"  Stats: {stats}")
                        elif 'articles' in data:
                            print(f"  Artículos: {len(data.get('articles', []))}")
                        print()
                    except Exception as e:
                        print(f"{Colors.YELLOW}  ⚠️ Error leyendo {name}: {e}{Colors.ENDC}\n")

            if not found_any:
                print(f"{Colors.RED}❌ No hay resultados de tests disponibles{Colors.ENDC}")
                print(f"\n{Colors.YELLOW}Ejecuta un test primero:{Colors.ENDC}")
                print("  Menú Principal → 2 (Tests) → 1-7")

            pause()

def menu_documentacion():
    """Menú de documentación"""
    while True:
        print_header()
        print_menu("📚 DOCUMENTACIÓN", [
            ('1', '📖 README - Guía principal'),
            ('2', '🚀 README-GENERADOR - Quick Start'),
            ('3', '📊 RESUMEN-FLUJO - Resumen ejecutivo'),
            ('4', '🔄 DIAGRAMA-FLUJO-COMPLETO - Arquitectura detallada'),
            ('5', '🤖 AGENTS - Guía para desarrolladores'),
            ('6', '✅ VERIFICACION-MODULOS - Test de integración'),
            ('7', '📑 INDEX-DOCUMENTACION - Índice completo'),
            ('8', '🎨 TODO-MEJORAS-DISEÑO - Plan de mejoras (NUEVO)'),
            ('9', '🔍 ANALISIS-DISEÑO-REFERENCIA - Análisis sitios (NUEVO)'),
            ('10', '📱 ANALISIS-EJEMPLO-HTML - Radio M técnico (NUEVO)')
        ])
        
        choice = get_user_choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        
        if choice == '0':
            break
        elif choice == 'q':
            sys.exit(0)
        elif choice == '1':
            view_documentation('README.md', 'README Principal')
        elif choice == '2':
            view_documentation('docs/README-GENERADOR.md', 'Quick Start del Generador CLI')
        elif choice == '3':
            view_documentation('docs/changelog/RESUMEN-FLUJO.md', 'Resumen Ejecutivo')
        elif choice == '4':
            view_documentation('docs/guides/DIAGRAMA-FLUJO-COMPLETO.md', 'Arquitectura Completa del Sistema')
        elif choice == '5':
            view_documentation('docs/guides/AGENTS.md', 'Guía para Desarrolladores y Agentes IA')
        elif choice == '6':
            view_documentation('docs/testing/VERIFICACION-MODULOS.md', 'Tests de Integración de Módulos')
        elif choice == '7':
            view_documentation('docs/guides/INDEX-DOCUMENTACION.md', 'Índice Maestro de Documentación')
        elif choice == '8':
            view_documentation('docs/design/TODO-MEJORAS-DISEÑO.md', 'Plan de Mejoras de Diseño')
        elif choice == '9':
            view_documentation('docs/design/ANALISIS-DISEÑO-REFERENCIA.md', 'Análisis de Sitios Profesionales')
        elif choice == '10':
            view_documentation('docs/design/ANALISIS-EJEMPLO-HTML.md', 'Análisis Técnico Radio M')

def menu_utilidades():
    """Menú de utilidades"""
    while True:
        print_header()
        print_menu("🔧 UTILIDADES", [
            ('1', '🧹 Limpiar archivos generados'),
            ('2', '📊 Ver estadísticas del sistema'),
            ('3', '🔍 Verificar API keys'),
            ('4', '📁 Abrir directorio de sitios generados'),
            ('5', '💾 Ver archivos de datos'),
            ('6', '🎨 Ver templates CSS disponibles'),
            ('7', '🖼️  Probar generador de logos SVG (NUEVO)'),
            ('8', '🎨 Ver paletas de colores profesionales (NUEVO)')
        ])
        
        choice = get_user_choice(['1', '2', '3', '4', '5', '6', '7', '8'])
        
        if choice == '0':
            break
        elif choice == 'q':
            sys.exit(0)
        elif choice == '1':
            print(f"\n{Colors.YELLOW}⚠️  Esto eliminará:{Colors.ENDC}")
            print("  - output/generated_sites/")
            print("  - output/generated_sites_test/")
            print("  - output/tests/")
            
            confirm = input(f"\n{Colors.RED}¿Continuar? (s/N): {Colors.ENDC}").strip().lower()
            if confirm == 's':
                import shutil
                dirs_to_clean = [
                    'output/generated_sites',
                    'output/generated_sites_test',
                    'output/tests/test_output_flujo',
                    'output/tests/test_output_modules',
                ]
                repo_root = Path(__file__).resolve().parents[1]
                for dir_name in dirs_to_clean:
                    dir_path = repo_root / dir_name
                    if dir_path.exists():
                        shutil.rmtree(dir_path)
                        print(f"{Colors.GREEN}✅ {dir_name}/ eliminado{Colors.ENDC}")
                print(f"\n{Colors.GREEN}🧹 Limpieza completada{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}Cancelado{Colors.ENDC}")
            pause()
        
        elif choice == '2':
            print(f"\n{Colors.GREEN}📊 Estadísticas del Sistema:{Colors.ENDC}\n")
            print(f"  {Colors.BOLD}Módulos:{Colors.ENDC}")
            print(f"    - Total módulos: 17 (+ logo_generator_svg)")
            print(f"    - Uso directo: 9")
            print(f"    - Uso indirecto: 7")
            print(f"\n  {Colors.BOLD}Blackbox AI:{Colors.ENDC}")
            print(f"    - Modo estándar: 1 API key")
            print(f"    - Modo paralelo: 2+ API keys")
            print(f"    - Modelos soportados: blackboxai-pro, grok-code-fast")
            print(f"    - Rotación automática de keys")
            print(f"\n  {Colors.BOLD}Combinaciones:{Colors.ENDC}")
            print(f"    - Paletas profesionales: 20 (4 verificadas)")
            print(f"    - Tipografías: 15 (4 de sitios reales)")
            print(f"    - Layouts: 20 (2 profesionales)")
            print(f"    - Templates CSS: 6,000")
            print(f"    - Configuraciones HTML: 43,200")
            print(f"    - Total únicas: 16.5 millones")
            print(f"\n  {Colors.BOLD}Generación:{Colors.ENDC}")
            print(f"    - Noticias por sitio: 20")
            print(f"    - Palabras por artículo: 800")
            print(f"    - Imágenes: 20 (NewsAPI + Unsplash)")
            print(f"    - Logos: SVG (5 estilos, sin IA)")
            print(f"    - Páginas HTML: 25")
            print(f"    - Tiempo estimado: 1-2 minutos")
            print(f"\n  {Colors.BOLD}Mejoras Sprint 1 (19 Ene 2026):{Colors.ENDC}")
            print(f"    - ✅ Sistema de logos SVG sin IA")
            print(f"    - ✅ 10 iconos SVG profesionales")
            print(f"    - ✅ Paletas verificadas (Milenio, Radio M)")
            print(f"    - ✅ Variables CSS unificadas")
            print(f"    - ✅ Headers sticky + offcanvas")
            print(f"    - ✅ Cards profesionales con badges")
            print(f"\n  {Colors.BOLD}Mejoras Blackbox (31 Ene 2026):{Colors.ENDC}")
            print(f"    - ✅ Parafraseo paralelo con múltiples keys")
            print(f"    - ✅ Menú actualizado con flujos Blackbox")
            print(f"    - ✅ Tests específicos para Blackbox")
            pause()
        
        elif choice == '3':
            print(f"\n{Colors.GREEN}🔑 Verificando API Keys:{Colors.ENDC}\n")

            from dotenv import load_dotenv
            load_dotenv()

            # Verificar todas las posibles keys de Blackbox
            blackbox_keys = {
                'BLACKBOX_API_KEY': os.getenv('BLACKBOX_API_KEY'),
                'BLACKBOX_API_KEY_PRO': os.getenv('BLACKBOX_API_KEY_PRO'),
                'BLACKBOX_API_KEY_FREE': os.getenv('BLACKBOX_API_KEY_FREE'),
                'BLACKBOX_API_KEY_ALT': os.getenv('BLACKBOX_API_KEY_ALT'),
                'BLACKBOX_API_KEY_1': os.getenv('BLACKBOX_API_KEY_1'),
                'BLACKBOX_API_KEY_2': os.getenv('BLACKBOX_API_KEY_2'),
            }

            news_keys = {
                'NEWS_API_KEY': os.getenv('NEWS_API_KEY'),
                'NEWSAPI_KEY': os.getenv('NEWSAPI_KEY'),
            }

            print(f"{Colors.BOLD}Blackbox API Keys:{Colors.ENDC}")
            active_blackbox = 0
            for key_name, key_value in blackbox_keys.items():
                if key_value and 'PENDIENTE' not in str(key_value):
                    masked = key_value[:8] + '...' + key_value[-4:] if len(key_value) > 12 else '***'
                    print(f"  ✅ {key_name}: {masked}")
                    active_blackbox += 1
                else:
                    print(f"  ⚪ {key_name}: No configurada")

            print(f"\n{Colors.BOLD}News API Keys:{Colors.ENDC}")
            for key_name, key_value in news_keys.items():
                if key_value:
                    masked = key_value[:8] + '...' + key_value[-4:] if len(key_value) > 12 else '***'
                    print(f"  ✅ {key_name}: {masked}")
                else:
                    print(f"  ⚪ {key_name}: No configurada")

            print(f"\n{Colors.CYAN}Resumen:{Colors.ENDC}")
            print(f"  Blackbox keys activas: {active_blackbox}")
            if active_blackbox >= 2:
                print(f"  {Colors.GREEN}✅ Configuración paralela disponible{Colors.ENDC}")
            elif active_blackbox == 1:
                print(f"  {Colors.YELLOW}⚠️  Solo modo estándar disponible{Colors.ENDC}")
            else:
                print(f"  {Colors.RED}❌ Se requiere al menos una API key{Colors.ENDC}")

            pause()
        
        elif choice == '4':
            site_dir = Path(__file__).resolve().parents[1] / 'output' / 'generated_sites'
            if site_dir.exists():
                sites = list(site_dir.glob('site_*'))
                print(f"\n{Colors.GREEN}📁 Sitios generados: {len(sites)}{Colors.ENDC}\n")
                for site in sorted(sites)[:10]:
                    print(f"  {site}")
                if len(sites) > 10:
                    print(f"  ... y {len(sites) - 10} más")
            else:
                print(f"\n{Colors.RED}❌ No hay sitios generados{Colors.ENDC}")
            pause()
        
        elif choice == '5':
            data_dir = Path(__file__).resolve().parents[1] / 'content' / 'data'
            if data_dir.exists():
                files = list(data_dir.glob('*.json'))
                print(f"\n{Colors.GREEN}💾 Archivos de datos: {len(files)}{Colors.ENDC}\n")
                for file in sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:10]:
                    size = file.stat().st_size / 1024
                    print(f"  {file.name} ({size:.1f} KB)")
            else:
                print(f"\n{Colors.RED}❌ No hay archivos de datos{Colors.ENDC}")
            pause()
        
        elif choice == '6':
            templates_dir = Path(__file__).resolve().parents[1] / 'content' / 'templates' / 'css'
            if templates_dir.exists():
                templates = list(templates_dir.glob('template*.css'))
                print(f"\n{Colors.GREEN}🎨 Templates CSS disponibles: {len(templates)}{Colors.ENDC}\n")
                print(f"  Total combinaciones posibles: 6,000")
                print(f"  Templates generados: {len(templates)}")
            else:
                print(f"\n{Colors.RED}❌ No hay templates CSS{Colors.ENDC}")
            pause()
        
        elif choice == '7':
            run_script('core/scripts/logo_generator_svg.py', 'Generador de Logos SVG - Prueba')
        
        elif choice == '8':
            run_script('core/scripts/color_palette_generator.py', 'Ver paletas de colores profesionales')

def main_menu():
    """Menú principal"""
    while True:
        print_header()
        
        print(f"{Colors.BOLD}Selecciona una opción:{Colors.ENDC}\n")
        print(f"  {Colors.GREEN}1{Colors.ENDC}) 🏗️  Generación de Sitios")
        print(f"  {Colors.GREEN}2{Colors.ENDC}) 🧪 Tests y Verificación")
        print(f"  {Colors.GREEN}3{Colors.ENDC}) 📚 Documentación")
        print(f"  {Colors.GREEN}4{Colors.ENDC}) 🔧 Utilidades")
        print(f"\n  {Colors.RED}q{Colors.ENDC}) ✖ Salir\n")
        
        choice = get_user_choice(['1', '2', '3', '4'])
        
        if choice == 'q':
            print(f"\n{Colors.CYAN}👋 ¡Hasta luego!{Colors.ENDC}\n")
            sys.exit(0)
        elif choice == '1':
            menu_generacion()
        elif choice == '2':
            menu_tests()
        elif choice == '3':
            menu_documentacion()
        elif choice == '4':
            menu_utilidades()

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Interrumpido por el usuario{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error inesperado: {e}{Colors.ENDC}")
        sys.exit(1)
