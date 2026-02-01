#!/usr/bin/env python3
"""
Test rápido de parafraseo - Versión mejorada para Blackbox
Soporta múltiples estilos y muestra métricas
"""

import sys
import time
from pathlib import Path

# Añadir directorio scripts al path
scripts_dir = Path(__file__).parent.parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from paraphrase import NewsParaphraser

# Colores ANSI
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

def main():
    """Ejecuta test rápido de parafraseo"""
    print(f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  📝 TEST RÁPIDO DE PARAFRASEO CON BLACKBOX                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
""")

    # Artículo de prueba
    article = {
        'source': 'test',
        'title': 'México anuncia nuevas políticas económicas para el próximo año fiscal',
        'description': 'El gobierno federal presenta un paquete de reformas importantes enfocadas en el crecimiento económico',
        'content': 'El presidente anunció reformas económicas significativas durante su conferencia matutina',
        'full_text': 'El presidente de México anunció reformas económicas significativas para el próximo año fiscal. Estas medidas incluyen incentivos fiscales para pequeñas y medianas empresas, así como programas de apoyo al empleo juvenil.'
    }

    print(f"{Colors.BOLD}Artículo original:{Colors.ENDC}")
    print(f"  Título: {article['title']}")
    print(f"  Descripción: {article['description']}")
    print(f"  Texto: {article['full_text'][:100]}...")

    print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}Iniciando parafraseo...{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

    try:
        start_time = time.time()
        paraphraser = NewsParaphraser()

        print(f"  📝 Generando variaciones con diferentes estilos...\n")

        # Generar 2 variaciones con estilos diferentes
        variations = paraphraser.generate_variations(article, num_variations=2)

        elapsed = time.time() - start_time

        if variations:
            print(f"{Colors.GREEN}✅ Parafraseo completado en {elapsed:.1f}s{Colors.ENDC}\n")

            for i, var in enumerate(variations, 1):
                print(f"{Colors.BOLD}Variación {i}:{Colors.ENDC}")
                print(f"  Estilo: {Colors.CYAN}{var.get('style', 'default')}{Colors.ENDC}")
                print(f"  Título: {var['title'][:80]}...")
                print(f"  Descripción: {var['description'][:100]}...")

                # Mostrar longitud del texto parafraseado
                full_text = var.get('full_text', '')
                word_count = len(full_text.split()) if full_text else 0
                print(f"  Palabras: {word_count}")
                print()

            print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}")
            print(f"{Colors.GREEN}{Colors.BOLD}✅ Test completado exitosamente{Colors.ENDC}")
            print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}")
            print(f"\n  Variaciones generadas: {len(variations)}")
            print(f"  Tiempo total: {elapsed:.1f}s")
            print(f"  Promedio por variación: {elapsed/len(variations):.1f}s")
            return 0
        else:
            print(f"{Colors.RED}❌ No se generaron variaciones{Colors.ENDC}")
            print(f"\n{Colors.YELLOW}Posibles causas:{Colors.ENDC}")
            print("  - API key no configurada")
            print("  - Problemas de conectividad")
            print("  - Límites de rate limit")
            return 1

    except Exception as e:
        print(f"{Colors.RED}❌ Error durante el parafraseo: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
