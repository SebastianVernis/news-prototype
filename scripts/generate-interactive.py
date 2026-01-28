#!/usr/bin/env python3
"""
Script Interactivo de Generación de Sitios de Noticias
Flujo completo: Pre-creación → Generación → Imágenes
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text):
    """Imprime encabezado con estilo"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_step(step, text):
    """Imprime paso con numeración"""
    print(f"{Colors.BOLD}{Colors.BLUE}[Paso {step}]{Colors.END} {text}")

def print_success(text):
    """Mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """Mensaje de error"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """Mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """Mensaje informativo"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def get_input(prompt, default=None, tipo=str):
    """Obtiene input del usuario con validación"""
    if default is not None:
        prompt_text = f"{Colors.BOLD}{prompt} [{default}]{Colors.END}: "
    else:
        prompt_text = f"{Colors.BOLD}{prompt}{Colors.END}: "
    
    while True:
        try:
            respuesta = input(prompt_text).strip()
            if not respuesta and default is not None:
                return default
            
            if not respuesta:
                print_error("No puede estar vacío. Intenta de nuevo.")
                continue
            
            if tipo == int:
                return int(respuesta)
            elif tipo == bool:
                return respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']
            else:
                return respuesta
        except ValueError:
            print_error(f"Entrada inválida. Se esperaba {tipo.__name__}.")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Operación cancelada por el usuario{Colors.END}")
            sys.exit(0)

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print_step(0, "Verificando dependencias...")
    
    dependencias = {
        'whois': 'whois',
        'Python': 'python3'
    }
    
    faltantes = []
    for nombre, comando in dependencias.items():
        resultado = subprocess.run(['which', comando], capture_output=True)
        if resultado.returncode != 0:
            faltantes.append(nombre)
    
    if faltantes:
        print_warning(f"Dependencias faltantes: {', '.join(faltantes)}")
        return False
    
    print_success("Todas las dependencias están instaladas")
    return True

def obtener_archivos_noticias():
    """Lista archivos de noticias disponibles"""
    data_dir = Path("../data")
    archivos = list(data_dir.glob("noticias_final_*.json"))
    
    if not archivos:
        return None
    
    # Ordenar por fecha (más reciente primero)
    archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return archivos

def seleccionar_archivo_noticias():
    """Permite al usuario seleccionar el archivo de noticias"""
    print_step(1, "Seleccionar archivo de noticias")
    
    archivos = obtener_archivos_noticias()
    
    if not archivos:
        print_error("No se encontraron archivos de noticias en ../data/")
        print_info("Ejecuta primero el script de obtención de noticias")
        return None
    
    print(f"\n{Colors.BOLD}Archivos disponibles:{Colors.END}")
    for i, archivo in enumerate(archivos, 1):
        # Obtener fecha de modificación
        timestamp = datetime.fromtimestamp(archivo.stat().st_mtime)
        fecha_str = timestamp.strftime("%d/%m/%Y %H:%M")
        
        # Contar noticias
        with open(archivo, 'r', encoding='utf-8') as f:
            noticias = json.load(f)
            num_noticias = len(noticias)
        
        print(f"  {Colors.CYAN}{i}.{Colors.END} {archivo.name}")
        print(f"     📅 {fecha_str} | 📰 {num_noticias} noticias")
    
    while True:
        seleccion = get_input(f"\nSelecciona un archivo (1-{len(archivos)})", "1", int)
        if 1 <= seleccion <= len(archivos):
            archivo_seleccionado = archivos[seleccion - 1]
            print_success(f"Seleccionado: {archivo_seleccionado.name}")
            return str(archivo_seleccionado)
        print_error("Selección inválida")

def configurar_generacion():
    """Configura los parámetros de generación"""
    print_step(2, "Configurar generación de sitios")
    
    config = {}
    
    # Número de sitios
    print(f"\n{Colors.BOLD}¿Cuántos sitios deseas generar?{Colors.END}")
    config['num_sitios'] = get_input("Número de sitios", "5", int)
    
    # Verificar dominios
    print(f"\n{Colors.BOLD}¿Verificar disponibilidad de dominios con whois?{Colors.END}")
    print_info("Esto toma ~20-30 segundos por sitio (rate limiting)")
    config['verificar_dominios'] = get_input("Verificar dominios (s/n)", "n", bool)
    
    # Generar imágenes
    print(f"\n{Colors.BOLD}¿Generar imágenes para los sitios?{Colors.END}")
    print_info("Usa IA para crear imágenes representativas")
    config['generar_imagenes'] = get_input("Generar imágenes (s/n)", "s", bool)
    
    # Layouts dinámicos
    print(f"\n{Colors.BOLD}¿Usar layouts dinámicos variados?{Colors.END}")
    print_info("Cada sitio tendrá estructura visual única")
    config['layouts_dinamicos'] = get_input("Layouts dinámicos (s/n)", "s", bool)
    
    # Usar metadatos pre-creados
    print(f"\n{Colors.BOLD}¿Usar metadatos de sitios pre-creados?{Colors.END}")
    print_info("Si no, se generarán nombres y metadatos al vuelo")
    config['usar_metadata'] = get_input("Usar metadata (s/n)", "n", bool)
    
    return config

def ejecutar_pre_creacion(num_sitios, verificar_dominios):
    """Ejecuta el proceso de pre-creación de sitios"""
    print_step(3, "Pre-creación de sitios (metadata)")
    
    cmd = [
        'python3', 'site_pre_creation.py',
        '--cantidad', str(num_sitios)
    ]
    
    if verificar_dominios:
        cmd.append('--verificar-dominios')
    
    print_info(f"Ejecutando: {' '.join(cmd)}")
    
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print_success("Pre-creación completada")
        
        # Extraer nombre del archivo generado
        for linea in resultado.stdout.split('\n'):
            if 'sites_metadata_' in linea and '.json' in linea:
                return linea.split('/')[-1].strip()
        return None
    else:
        print_error("Error en pre-creación")
        print(resultado.stderr)
        return None

def ejecutar_generacion_sitios(archivo_noticias, num_sitios, layouts_dinamicos, metadata_file=None):
    """Ejecuta la generación de sitios HTML"""
    print_step(4, "Generación de sitios HTML")
    
    cmd = [
        'python3', 'generate-sites.py',
        '--num-sites', str(num_sitios),
        '--news-file', archivo_noticias
    ]
    
    if layouts_dinamicos:
        cmd.append('--layouts-dinamicos')
    
    if metadata_file:
        cmd.extend(['--metadata-file', f"../data/sites_metadata/{metadata_file}"])
    
    print_info(f"Ejecutando: {' '.join(cmd)}")
    
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print_success("Sitios HTML generados")
        print(resultado.stdout)
        return True
    else:
        print_error("Error en generación de sitios")
        print(resultado.stderr)
        return False

def ejecutar_generacion_imagenes():
    """Ejecuta la generación de imágenes"""
    print_step(5, "Generación de imágenes con IA")
    
    print_info("Generando imágenes representativas...")
    
    cmd = ['python3', 'generate-images-ai.py']
    
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print_success("Imágenes generadas")
        return True
    else:
        print_error("Error en generación de imágenes")
        print(resultado.stderr)
        return False

def mostrar_resumen(config, archivo_noticias):
    """Muestra resumen de la configuración"""
    print_header("RESUMEN DE CONFIGURACIÓN")
    
    print(f"{Colors.BOLD}Archivo de noticias:{Colors.END}")
    print(f"  📰 {archivo_noticias}")
    
    print(f"\n{Colors.BOLD}Parámetros:{Colors.END}")
    print(f"  🔢 Número de sitios: {config['num_sitios']}")
    print(f"  🌐 Verificar dominios: {'Sí' if config['verificar_dominios'] else 'No'}")
    print(f"  🖼️  Generar imágenes: {'Sí' if config['generar_imagenes'] else 'No'}")
    print(f"  🎨 Layouts dinámicos: {'Sí' if config['layouts_dinamicos'] else 'No'}")
    print(f"  📋 Usar metadata: {'Sí' if config['usar_metadata'] else 'No'}")
    
    print(f"\n{Colors.BOLD}Tiempo estimado:{Colors.END}")
    tiempo = 10  # Base
    if config['verificar_dominios']:
        tiempo += config['num_sitios'] * 25
    if config['generar_imagenes']:
        tiempo += config['num_sitios'] * 5
    
    if tiempo < 60:
        print(f"  ⏱️  ~{tiempo} segundos")
    else:
        print(f"  ⏱️  ~{tiempo // 60} minutos {tiempo % 60} segundos")

def main():
    """Función principal"""
    print_header("🚀 GENERADOR INTERACTIVO DE SITIOS DE NOTICIAS")
    
    # Verificar dependencias
    if not verificar_dependencias():
        print_warning("Algunas dependencias faltan. ¿Continuar de todos modos?")
        if not get_input("Continuar (s/n)", "n", bool):
            sys.exit(1)
    
    # Seleccionar archivo de noticias
    archivo_noticias = seleccionar_archivo_noticias()
    if not archivo_noticias:
        sys.exit(1)
    
    # Configurar generación
    config = configurar_generacion()
    
    # Mostrar resumen
    mostrar_resumen(config, archivo_noticias)
    
    print(f"\n{Colors.BOLD}¿Proceder con la generación?{Colors.END}")
    if not get_input("Continuar (s/n)", "s", bool):
        print_warning("Generación cancelada")
        sys.exit(0)
    
    # Iniciar proceso
    print_header("INICIANDO GENERACIÓN")
    
    metadata_file = None
    
    # Pre-creación (si es necesario)
    if config['usar_metadata']:
        metadata_file = ejecutar_pre_creacion(
            config['num_sitios'],
            config['verificar_dominios']
        )
        if not metadata_file:
            print_error("No se pudo completar la pre-creación")
            sys.exit(1)
    
    # Generación de sitios
    if not ejecutar_generacion_sitios(
        archivo_noticias,
        config['num_sitios'],
        config['layouts_dinamicos'],
        metadata_file
    ):
        print_error("No se pudieron generar los sitios")
        sys.exit(1)
    
    # Generación de imágenes
    if config['generar_imagenes']:
        if not ejecutar_generacion_imagenes():
            print_warning("Las imágenes no se generaron correctamente")
    
    # Resumen final
    print_header("✅ GENERACIÓN COMPLETADA")
    
    print(f"{Colors.BOLD}Archivos generados:{Colors.END}")
    print(f"  📁 Sitios HTML: ../sites/")
    print(f"  🎨 Estilos CSS: ../templates/css/")
    if config['generar_imagenes']:
        print(f"  🖼️  Imágenes: ../images/news/")
    if metadata_file:
        print(f"  📋 Metadata: ../data/sites_metadata/{metadata_file}")
    
    print(f"\n{Colors.BOLD}Para ver los sitios:{Colors.END}")
    print(f"  {Colors.CYAN}cd ../templates && python3 -m http.server 8000{Colors.END}")
    print(f"  {Colors.CYAN}Luego abre: http://localhost:8000/index.html{Colors.END}")
    
    print(f"\n{Colors.GREEN}¡Proceso completado exitosamente!{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Operación cancelada por el usuario{Colors.END}\n")
        sys.exit(130)
    except Exception as e:
        print_error(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
