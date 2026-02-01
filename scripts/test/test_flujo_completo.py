#!/usr/bin/env python3
"""
Test de Flujo Completo End-to-End
Genera 2 artículos de prueba rápidamente para verificar el flujo completo
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Añadir directorio scripts al path
scripts_dir = Path(__file__).parent.parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

# Colores ANSI
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def print_step(step_num: int, total: int, description: str):
    """Imprime un paso del proceso"""
    print(f"\n{Colors.CYAN}[{step_num}/{total}]{Colors.ENDC} {Colors.BOLD}{description}{Colors.ENDC}")

def print_success(message: str):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")

def print_error(message: str):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}")

def print_info(message: str):
    """Imprime mensaje informativo"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def main():
    """Ejecuta el test de flujo completo"""
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🧪 TEST DE FLUJO COMPLETO (END-TO-END)                          ║
║  Generación rápida de 2 artículos para verificar integración     ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
""")
    
    start_time = time.time()
    results = {
        'timestamp': datetime.now().isoformat(),
        'config': {
            'articulos': 2,
            'modo': 'test_rapido'
        },
        'steps': {},
        'success': False
    }
    
    total_steps = 7
    output_dir = Path('test/test_output_flujo')
    
    try:
        # Paso 1: Verificar dependencias
        print_step(1, total_steps, "Verificando dependencias")
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            blackbox_key = os.getenv('BLACKBOX_API_KEY')
            newsapi_key = os.getenv('NEWSAPI_KEY')
            
            if not blackbox_key:
                print_error("BLACKBOX_API_KEY no configurada")
                results['steps']['dependencies'] = {'status': 'error', 'error': 'BLACKBOX_API_KEY faltante'}
                return 1
            
            if not newsapi_key:
                print_error("NEWSAPI_KEY no configurada")
                results['steps']['dependencies'] = {'status': 'error', 'error': 'NEWSAPI_KEY faltante'}
                return 1
            
            print_success("API keys configuradas correctamente")
            results['steps']['dependencies'] = {'status': 'success'}
            
        except Exception as e:
            print_error(f"Error verificando dependencias: {e}")
            results['steps']['dependencies'] = {'status': 'error', 'error': str(e)}
            return 1
        
        # Paso 2: Obtener noticias
        print_step(2, total_steps, "Obteniendo 2 noticias de NewsAPI")
        
        try:
            from api.newsapi import fetch_newsapi
            
            articles = fetch_newsapi(page_size=2, silent=True)
            
            if not articles or len(articles) < 2:
                print_error(f"Solo se obtuvieron {len(articles)} artículos")
                results['steps']['fetch'] = {'status': 'error', 'count': len(articles)}
                return 1
            
            print_success(f"Obtenidos {len(articles)} artículos")
            print_info(f"Título 1: {articles[0].get('title', 'N/A')[:60]}...")
            print_info(f"Título 2: {articles[1].get('title', 'N/A')[:60]}...")
            
            results['steps']['fetch'] = {'status': 'success', 'count': len(articles)}
            
        except Exception as e:
            print_error(f"Error obteniendo noticias: {e}")
            results['steps']['fetch'] = {'status': 'error', 'error': str(e)}
            return 1
        
        # Paso 3: Parafrasear noticias
        print_step(3, total_steps, "Parafraseando artículos con Blackbox AI")

        try:
            # Intentar usar Blackbox paralelo si hay múltiples keys
            from blackbox_parallel import BlackboxParallelParaphraser
            from paraphrase import NewsParaphraser

            # Verificar si hay múltiples keys disponibles
            try:
                parallel_paraphraser = BlackboxParallelParaphraser()
                if len(parallel_paraphraser.api_configs) >= 2:
                    print_info(f"Usando Blackbox paralelo ({len(parallel_paraphraser.api_configs)} keys)")
                    all_variations = parallel_paraphraser.parafrasear_lote_paralelo(
                        articles[:2],  # Solo 2 artículos para test
                        max_workers=2
                    )
                    paraphrase_method = 'blackbox-parallel'
                else:
                    raise ValueError("Solo 1 key disponible")
            except Exception as parallel_error:
                print_info(f"Usando Blackbox estándar (fallback)")
                paraphraser = NewsParaphraser()
                all_variations = []

                for i, article in enumerate(articles[:2], 1):
                    print_info(f"Parafraseando artículo {i}/2...")
                    variations = paraphraser.generate_variations(article, num_variations=1)
                    all_variations.extend(variations)
                paraphrase_method = 'blackbox-standard'

            successful = sum(1 for v in all_variations if v.get('paraphrased', True))
            print_success(f"Generadas {len(all_variations)} variaciones ({successful} exitosas)")
            results['steps']['paraphrase'] = {
                'status': 'success',
                'variations': len(all_variations),
                'method': paraphrase_method,
                'successful': successful
            }

        except Exception as e:
            print_error(f"Error parafraseando: {e}")
            results['steps']['paraphrase'] = {'status': 'error', 'error': str(e)}
            return 1
        
        # Paso 4: Generar metadata de sitio
        print_step(4, total_steps, "Generando metadata del sitio")
        
        try:
            from site_pre_creation import SitePreCreation
            
            pre_creator = SitePreCreation()
            site_metadata = pre_creator.crear_metadata_sitio()
            
            print_success(f"Sitio: {site_metadata.get('site_name')}")
            print_info(f"Dominio: {site_metadata.get('domain')}")
            print_info(f"Tagline: {site_metadata.get('tagline')}")
            
            results['steps']['metadata'] = {
                'status': 'success',
                'site_name': site_metadata.get('site_name'),
                'domain': site_metadata.get('domain')
            }
            
        except Exception as e:
            print_error(f"Error generando metadata: {e}")
            results['steps']['metadata'] = {'status': 'error', 'error': str(e)}
            return 1
        
        # Paso 5: Generar diseño
        print_step(5, total_steps, "Generando diseño del sitio")
        
        try:
            from color_palette_generator import ColorPaletteGenerator
            from font_family_generator import FontFamilyGenerator
            from layout_generator import LayoutGenerator
            
            # Paleta de colores
            palette_gen = ColorPaletteGenerator()
            palette = palette_gen.obtener_paleta()
            
            # Tipografía
            font_gen = FontFamilyGenerator()
            fonts = font_gen.obtener_combinacion()
            
            # Layout
            layout_gen = LayoutGenerator()
            layout = layout_gen.generar_configuracion_layout()
            
            print_success(f"Paleta: {palette.get('name', 'Custom')}")
            print_success(f"Tipografía: {fonts.get('headings', {}).get('family', fonts.get('nombre', 'N/A'))}")
            print_success(f"Layout: {layout.get('type', layout.get('nombre', 'responsive'))}")
            
            results['steps']['design'] = {
                'status': 'success',
                'palette': palette.get('name'),
                'fonts': fonts.get('headings', {}).get('family', fonts.get('nombre', 'N/A')),
                'layout': layout.get('type', layout.get('nombre', 'responsive'))
            }
            
        except Exception as e:
            print_error(f"Error generando diseño: {e}")
            results['steps']['design'] = {'status': 'error', 'error': str(e)}
            return 1
        
        # Paso 6: Generar logo
        print_step(6, total_steps, "Generando logo SVG")
        
        try:
            from logo_generator_svg import LogoGeneratorSVG
            
            logo_gen = LogoGeneratorSVG()
            logo_svg, logo_style, logo_font = logo_gen.generate_logo(
                site_name=site_metadata.get('nombre_sitio', 'Test Site'),
                colors=palette
            )
            
            print_success(f"Logo generado: {logo_style} ({len(logo_svg)} caracteres)")
            print_info(f"Tipografía logo: {logo_font}")
            results['steps']['logo'] = {'status': 'success', 'size': len(logo_svg), 'style': logo_style}
            
        except Exception as e:
            print_error(f"Error generando logo: {e}")
            results['steps']['logo'] = {'status': 'error', 'error': str(e)}
            return 1
        
        # Paso 7: Guardar datos de prueba
        print_step(7, total_steps, "Guardando resultados del test")
        
        try:
            output_dir.mkdir(exist_ok=True)
            
            # Guardar artículos parafraseados
            articles_file = output_dir / 'articulos_test.json'
            with open(articles_file, 'w', encoding='utf-8') as f:
                json.dump(all_variations, f, ensure_ascii=False, indent=2)
            
            # Guardar metadata
            metadata_file = output_dir / 'metadata_test.json'
            site_data = {
                'metadata': site_metadata,
                'design': {
                    'palette': palette,
                    'fonts': fonts,
                    'layout': layout
                },
                'logo': logo_svg
            }
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(site_data, f, ensure_ascii=False, indent=2)
            
            print_success(f"Datos guardados en: {output_dir}")
            results['steps']['save'] = {'status': 'success', 'output_dir': str(output_dir)}
            
        except Exception as e:
            print_error(f"Error guardando resultados: {e}")
            results['steps']['save'] = {'status': 'error', 'error': str(e)}
            return 1
        
        # Test completado exitosamente
        elapsed = time.time() - start_time
        results['success'] = True
        results['tiempo_total_segundos'] = elapsed
        results['stats'] = {
            'noticias_parafraseadas': len(all_variations),
            'sitios_creados': 1
        }
        
        print(f"\n{Colors.CYAN}{'=' * 70}{Colors.ENDC}")
        print(f"{Colors.GREEN}{Colors.BOLD}✅ TEST COMPLETADO EXITOSAMENTE{Colors.ENDC}")
        print(f"{Colors.CYAN}{'=' * 70}{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Resumen:{Colors.ENDC}")
        print(f"  ⏱️  Tiempo total: {elapsed:.2f} segundos")
        print(f"  📰 Artículos procesados: {len(all_variations)}")
        print(f"  🎨 Sitio diseñado: {site_metadata.get('site_name')}")
        print(f"  📁 Salida: {output_dir}")
        
        print(f"\n{Colors.YELLOW}Para generar sitio HTML completo:{Colors.ENDC}")
        print(f"  python3 scripts/master_orchestrator.py")
        
        # Guardar resultados del test
        results_file = Path('test/test_flujo_completo_resultado.json')
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n{Colors.CYAN}Resultados guardados: {results_file}{Colors.ENDC}")
        
        return 0
        
    except Exception as e:
        print(f"\n{Colors.RED}{'=' * 70}{Colors.ENDC}")
        print_error(f"Error inesperado: {e}")
        print(f"{Colors.RED}{'=' * 70}{Colors.ENDC}")
        
        results['success'] = False
        results['error'] = str(e)
        
        return 1

if __name__ == '__main__':
    sys.exit(main())
