#!/usr/bin/env python3
"""
Script para generar sitios HTML con templates actualizados automáticamente
Lee datos de noticias y genera múltiples sitios con diferentes estilos
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path

try:
    from site_pre_creation import SitePreCreation
    METADATA_AVAILABLE = True
except ImportError:
    METADATA_AVAILABLE = False

try:
    from layout_generator import LayoutGenerator, HTMLLayoutBuilder
    LAYOUTS_AVAILABLE = True
except ImportError:
    LAYOUTS_AVAILABLE = False

# Configuración
NUM_TEMPLATES = 40  # Total de templates CSS disponibles (para modo no-interactivo)
OUTPUT_DIR = "../sites"
CSS_DIR = "../templates/css"
LATEST_NEWS_FILE = "../data/noticias_final_20260107_2358.json"
METADATA_DIR = "../data/sites_metadata"  # Directorio de metadatos de sitios
MAX_TEMPLATES = 100  # Máximo de templates CSS disponibles

# Títulos y taglines variados para los sitios
SITE_CONFIGS = [
    {"title": "El Diario Nacional", "tagline": "La Verdad en Cada Historia"},
    {"title": "Noticias al Momento", "tagline": "Tu Fuente de Información Confiable"},
    {"title": "El Informador", "tagline": "Noticias que Importan"},
    {"title": "Crónica Actual", "tagline": "Mantente Informado"},
    {"title": "Reporte Directo", "tagline": "Las Noticias más Recientes"},
    {"title": "El Observador", "tagline": "Periodismo de Calidad"},
    {"title": "Noticias Express", "tagline": "Rápido, Preciso, Confiable"},
    {"title": "El Noticiero", "tagline": "Información al Instante"},
    {"title": "Diario Digital", "tagline": "Noticias 24/7"},
    {"title": "La Prensa Hoy", "tagline": "Tu Conexión con el Mundo"},
]

# Categorías para el menú
CATEGORIES = ["Inicio", "Política", "Tecnología", "Deportes", "Entretenimiento", "Mundial", "Negocios"]

def load_news_data():
    """Carga los datos de noticias del archivo JSON más reciente"""
    if not os.path.exists(LATEST_NEWS_FILE):
        print(f"❌ Error: Archivo {LATEST_NEWS_FILE} no encontrado")
        return []
    
    with open(LATEST_NEWS_FILE, 'r', encoding='utf-8') as f:
        news = json.load(f)
    
    print(f"✅ Cargadas {len(news)} noticias")
    return news

def truncate_text(text, max_length=150):
    """Trunca el texto a una longitud máxima"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'

def format_date(date_str):
    """Formatea la fecha de manera legible"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return date_obj.strftime("%d de %B, %Y")
    except:
        return datetime.now().strftime("%d de %B, %Y")

def translate_month(date_str):
    """Traduce los meses al español"""
    months = {
        'January': 'enero', 'February': 'febrero', 'March': 'marzo',
        'April': 'abril', 'May': 'mayo', 'June': 'junio',
        'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
        'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
    }
    for eng, esp in months.items():
        date_str = date_str.replace(eng, esp)
    return date_str

def generate_html(template_num, site_config, news_data, max_templates=MAX_TEMPLATES, usar_layouts_dinamicos=True):
    """Genera el HTML para un template específico"""
    
    # Ajustar número de template si excede el máximo
    actual_template = ((template_num - 1) % max_templates) + 1
    
    # Generar configuración de layout dinámico si está disponible
    layout_config = None
    if usar_layouts_dinamicos and LAYOUTS_AVAILABLE:
        generator = LayoutGenerator()
        layout_config = generator.generar_configuracion_layout()
        distribucion = generator.generar_distribucion_noticias(len(news_data))
        
        # Randomizar categorías
        categorias_randomizadas = generator.randomizar_categorias(CATEGORIES.copy())
    else:
        categorias_randomizadas = CATEGORIES
        distribucion = {
            "featured": 1,
            "main": 4,
            "sidebar": 3
        }
    
    # Seleccionar noticias según distribución
    selected_news = random.sample(news_data, min(20, len(news_data)))
    featured_news = selected_news[:distribucion['featured']]
    main_news = selected_news[distribucion['featured']:distribucion['featured'] + distribucion['main']]
    sidebar_news = selected_news[distribucion['featured'] + distribucion['main']:][:distribucion['sidebar']]
    
    # Para compatibilidad con código antiguo
    featured = featured_news[0] if featured_news else {}
    
    # Construir el HTML usando layout dinámico o estático
    if layout_config and LAYOUTS_AVAILABLE:
        return generate_html_dynamic(actual_template, site_config, featured_news, main_news, sidebar_news, 
                                     categorias_randomizadas, layout_config, distribucion)
    
    # Modo estático (fallback)
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_config['title']} - Noticias de Última Hora</title>
    <link rel="stylesheet" href="{CSS_DIR}/template{actual_template}.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">
                <h1>{site_config['title']}</h1>
                <p class="tagline">{site_config['tagline']}</p>
            </div>
            <nav class="nav">
"""
    
    # Agregar categorías del menú
    for category in categorias_randomizadas:
        html += f'                <a href="#" class="nav-link">{category}</a>\n'
    
    html += """            </nav>
            <div class="header-actions">
                <input type="search" placeholder="Buscar noticias..." class="search-input">
                <button class="btn-subscribe">Suscribirse</button>
            </div>
        </div>
    </header>

    <main class="main-content">
"""
    
    # Sección destacada
    if featured:
        image_path = featured.get('ai_image_path') or 'https://via.placeholder.com/1200x600/4A90E2/ffffff?text=Noticia+Destacada'
        if not image_path.startswith('http'):
            image_path = f"../{image_path}"
        
        title = truncate_text(featured.get('title', 'Título no disponible'), 120)
        description = truncate_text(featured.get('description', 'Descripción no disponible'), 250)
        author = featured.get('author', 'Redacción')
        date = translate_month(format_date(featured.get('published_at', '')))
        
        html += f"""        <section class="hero-section">
            <article class="featured-article">
                <div class="article-image">
                    <img src="{image_path}" alt="Destacado">
                </div>
                <div class="article-content">
                    <span class="category">Última Hora</span>
                    <h2 class="article-title">{title}</h2>
                    <p class="article-excerpt">{description}</p>
                    <div class="article-meta">
                        <span class="author">Por {author}</span>
                        <span class="date">{date}</span>
                        <span class="reading-time">5 min de lectura</span>
                    </div>
                </div>
            </article>
        </section>

"""
    
    # Sección de noticias principales
    html += """        <section class="news-grid">
            <div class="main-column">
                <h2 class="section-title">Últimos Titulares</h2>
                
"""
    
    for news in main_news:
        image_path = news.get('ai_image_path') or 'https://via.placeholder.com/600x400/E74C3C/ffffff?text=Noticia'
        if not image_path.startswith('http'):
            image_path = f"../{image_path}"
        
        title = truncate_text(news.get('title', 'Título no disponible'), 100)
        description = truncate_text(news.get('description', 'Descripción no disponible'), 200)
        author = news.get('author', 'Redacción')
        date = translate_month(format_date(news.get('published_at', '')))
        category = news.get('category', 'General')
        
        html += f"""                <article class="news-card">
                    <img src="{image_path}" alt="{category}" class="card-image">
                    <div class="card-content">
                        <span class="category">{category.capitalize()}</span>
                        <h3 class="card-title">{title}</h3>
                        <p class="card-excerpt">{description}</p>
                        <div class="article-meta">
                            <span class="author">Por {author}</span>
                            <span class="date">{date}</span>
                        </div>
                    </div>
                </article>

"""
    
    # Sidebar
    html += """            </div>
            
            <aside class="sidebar">
                <section class="sidebar-section newsletter">
                    <h3 class="sidebar-title">Boletín de Noticias</h3>
                    <p>Recibe las noticias más importantes en tu correo</p>
                    <form class="newsletter-form">
                        <input type="email" placeholder="Tu correo electrónico" class="newsletter-input">
                        <button type="submit" class="newsletter-btn">Suscribirse</button>
                    </form>
                </section>

                <section class="sidebar-section">
                    <h3 class="sidebar-title">Más Leídas</h3>
                    <ul class="trending-list">
"""
    
    for i, news in enumerate(sidebar_news, 1):
        title = truncate_text(news.get('title', 'Título no disponible'), 80)
        date = translate_month(format_date(news.get('published_at', '')))
        
        html += f"""                        <li class="trending-item">
                            <span class="trending-number">{i}</span>
                            <div class="trending-content">
                                <h4>{title}</h4>
                                <p class="trending-meta">{date}</p>
                            </div>
                        </li>
"""
    
    html += """                    </ul>
                </section>
            </aside>
        </section>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-column">
                    <h4>Sobre Nosotros</h4>
                    <p>Tu fuente confiable de noticias e información actualizada las 24 horas del día.</p>
                    <div class="social-links">
                        <a href="#" class="social-link">Facebook</a>
                        <a href="#" class="social-link">Twitter</a>
                        <a href="#" class="social-link">Instagram</a>
                    </div>
                </div>
                <div class="footer-column">
                    <h4>Secciones</h4>
                    <ul class="footer-links">
"""
    
    for category in CATEGORIES[1:]:
        html += f'                        <li><a href="#">{category}</a></li>\n'
    
    html += f"""                    </ul>
                </div>
                <div class="footer-column">
                    <h4>Legal</h4>
                    <ul class="footer-links">
                        <li><a href="#">Términos de Uso</a></li>
                        <li><a href="#">Política de Privacidad</a></li>
                        <li><a href="#">Cookies</a></li>
                        <li><a href="#">Contacto</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h4>Contacto</h4>
                    <p>Email: contacto@{site_config['title'].lower().replace(' ', '')}.com</p>
                    <p>Tel: +52 55 1234 5678</p>
                    <p>Ciudad de México, México</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} {site_config['title']}. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""
    
    return html


def generate_html_dynamic(template_num, site_config, featured_news, main_news, sidebar_news,
                          categorias, layout_config, distribucion):
    """
    Genera HTML usando el sistema de layouts dinámicos
    
    Args:
        template_num: Número de template CSS
        site_config: Configuración del sitio (nombre, tagline)
        featured_news: Noticias destacadas
        main_news: Noticias principales
        sidebar_news: Noticias para sidebar
        categorias: Lista de categorías
        layout_config: Configuración del layout
        distribucion: Distribución de noticias
        
    Returns:
        str: HTML completo del sitio
    """
    # Crear builder con configuración
    builder = HTMLLayoutBuilder(layout_config)
    generator = LayoutGenerator()
    
    # Generar widgets para sidebar si es necesario
    widgets = []
    if layout_config['sidebar_position'] != 'none' and layout_config.get('show_sidebar_widgets', True):
        widgets = generator.generar_estilos_widget_sidebar()
    
    # Clases CSS dinámicas
    css_classes = generator.generar_clases_css_dinamicas(layout_config)
    
    # Construir HTML
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_config['title']} - Noticias de Última Hora</title>
    <link rel="stylesheet" href="{CSS_DIR}/template{template_num}.css">
    <meta name="description" content="{site_config['tagline']}">
    <meta name="layout" content="{layout_config['layout_type']}">
</head>
<body class="{css_classes['container']}">

"""
    
    # Header dinámico
    html += builder.build_header(site_config, categorias)
    
    # Main content
    html += '    <main class="' + css_classes['main'] + '">\n'
    html += '        <div class="content-wrapper">\n'
    
    # Sección destacada
    if featured_news:
        html += builder.build_featured_section(featured_news)
    
    # Layout con o sin sidebar
    if layout_config['sidebar_position'] != 'none':
        html += '            <div class="main-with-sidebar">\n'
        html += '                <div class="main-column">\n'
    
    # Grid de noticias principales
    if main_news:
        html += builder.build_news_grid(main_news, distribucion)
    
    if layout_config['sidebar_position'] != 'none':
        html += '                </div>\n'
        html += builder.build_sidebar(sidebar_news, widgets)
        html += '            </div>\n'
    
    html += '        </div>\n'
    html += '    </main>\n\n'
    
    # Footer
    html += f'''    <footer class="{css_classes['footer']}">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-column">
                    <h3>{site_config['title']}</h3>
                    <p>{site_config['tagline']}</p>
                    <div class="social-links">
                        <a href="#" class="social-link">Facebook</a>
                        <a href="#" class="social-link">Twitter</a>
                        <a href="#" class="social-link">Instagram</a>
                    </div>
                </div>
'''
    
    # Columnas adicionales del footer según configuración
    footer_sections = [
        ("Secciones", categorias[:4]),
        ("Legal", ["Términos de Uso", "Política de Privacidad", "Cookies", "Contacto"]),
        ("Contacto", [f"Email: contacto@{site_config['title'].lower().replace(' ', '')}.com", "Tel: +52 55 1234 5678", "Ciudad de México, México"])
    ]
    
    for i, (titulo, items) in enumerate(footer_sections[:layout_config['footer_columns'] - 1]):
        html += f'''                <div class="footer-column">
                    <h4>{titulo}</h4>
                    <ul class="footer-links">
'''
        for item in items:
            if isinstance(item, str) and '@' not in item and ':' not in item:
                html += f'                        <li><a href="#">{item}</a></li>\n'
            else:
                html += f'                        <li>{item}</li>\n'
        html += '                    </ul>\n'
        html += '                </div>\n'
    
    html += f'''            </div>
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} {site_config['title']}. Todos los derechos reservados.</p>
                <p class="layout-info">Layout: {layout_config['layout_type']} | Template: {template_num}</p>
            </div>
        </div>
    </footer>
</body>
</html>
'''
    
    return html


def load_sites_metadata(metadata_file=None):
    """Carga metadatos de sitios si están disponibles"""
    if not METADATA_AVAILABLE:
        return None
    
    # Si no se especifica archivo, buscar el más reciente
    if not metadata_file:
        metadata_dir = Path(METADATA_DIR)
        if not metadata_dir.exists():
            return None
        
        # Buscar archivos de metadata
        metadata_files = list(metadata_dir.glob("sites_metadata_*.json"))
        if not metadata_files:
            return None
        
        # Usar el más reciente
        metadata_file = max(metadata_files, key=lambda p: p.stat().st_mtime)
    
    try:
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"✅ Cargados metadatos de {len(metadata)} sitios: {metadata_file}")
        return metadata
    except Exception as e:
        print(f"⚠️ Error cargando metadatos: {e}")
        return None


def modo_interactivo():
    """Modo interactivo para configurar generación de sitios"""
    print("🎉 Generador de Sitios de Noticias - Modo Interactivo")
    print("=" * 60)
    print()
    
    # Pregunta 1: Cantidad de sitios
    while True:
        try:
            cantidad = input("📊 ¿Cuántos sitios deseas crear? (1-100) [default: 10]: ").strip()
            if not cantidad:
                cantidad = 10
                break
            cantidad = int(cantidad)
            if 1 <= cantidad <= 100:
                break
            else:
                print("⚠️  Por favor ingresa un número entre 1 y 100")
        except ValueError:
            print("⚠️  Por favor ingresa un número válido")
    
    print(f"✅ Se crearán {cantidad} sitios")
    print()
    
    # Pregunta 2: Verificar dominios
    print("🔍 ¿Deseas verificar disponibilidad de dominios con whois?")
    print("   (Requiere tener 'whois' instalado en el sistema)")
    while True:
        verificar = input("   [s/N]: ").strip().lower()
        if verificar in ['', 's', 'si', 'sí', 'y', 'yes', 'n', 'no']:
            verificar_dominios = verificar in ['s', 'si', 'sí', 'y', 'yes']
            break
        print("⚠️  Por favor responde 's' para sí o 'n' para no")
    
    if verificar_dominios:
        print("✅ Se verificarán los dominios con whois")
    else:
        print("ℹ️  Se omitirá la verificación de dominios")
    print()
    
    # Pregunta 3: Usar metadatos existentes o generar nuevos
    usar_existentes = False
    metadata_file = None
    
    if METADATA_AVAILABLE:
        metadata_dir = Path(METADATA_DIR)
        if metadata_dir.exists():
            metadata_files = list(metadata_dir.glob("sites_metadata_*.json"))
            if metadata_files:
                print(f"💾 Se encontraron {len(metadata_files)} archivos de metadatos existentes")
                while True:
                    usar = input("¿Deseas usar metadatos existentes? [s/N]: ").strip().lower()
                    if usar in ['', 's', 'si', 'sí', 'y', 'yes', 'n', 'no']:
                        usar_existentes = usar in ['s', 'si', 'sí', 'y', 'yes']
                        break
                    print("⚠️  Por favor responde 's' para sí o 'n' para no")
                
                if usar_existentes:
                    # Mostrar archivos disponibles
                    print("\nArchivos disponibles:")
                    for idx, mf in enumerate(metadata_files[-5:], 1):  # Últimos 5
                        size = len(json.load(open(mf)))
                        print(f"  {idx}. {mf.name} ({size} sitios)")
                    
                    # Seleccionar archivo
                    while True:
                        try:
                            seleccion = input(f"\nSelecciona archivo [1-{min(5, len(metadata_files))}] o ENTER para el más reciente: ").strip()
                            if not seleccion:
                                metadata_file = max(metadata_files, key=lambda p: p.stat().st_mtime)
                                break
                            idx = int(seleccion) - 1
                            if 0 <= idx < min(5, len(metadata_files)):
                                metadata_file = metadata_files[-(min(5, len(metadata_files)) - idx)]
                                break
                            else:
                                print(f"⚠️  Por favor ingresa un número entre 1 y {min(5, len(metadata_files))}")
                        except ValueError:
                            print("⚠️  Por favor ingresa un número válido")
                    
                    print(f"✅ Usando: {metadata_file.name}")
                print()
    
    # Resumen de configuración
    print("📝 Resumen de Configuración:")
    print("=" * 60)
    print(f"  📊 Cantidad de sitios: {cantidad}")
    print(f"  🔍 Verificar dominios: {'Sí' if verificar_dominios else 'No'}")
    if usar_existentes:
        print(f"  💾 Metadatos: Usar existentes ({metadata_file.name})")
    else:
        print(f"  🆕 Metadatos: Generar nuevos")
    print("=" * 60)
    print()
    
    # Confirmación final
    while True:
        confirmar = input("❓ ¿Proceder con esta configuración? [S/n]: ").strip().lower()
        if confirmar in ['', 's', 'si', 'sí', 'y', 'yes', 'n', 'no']:
            if confirmar in ['n', 'no']:
                print("\n❌ Operación cancelada")
                return None
            break
        print("⚠️  Por favor responde 's' para sí o 'n' para no")
    
    return {
        'cantidad': cantidad,
        'verificar_dominios': verificar_dominios,
        'usar_existentes': usar_existentes,
        'metadata_file': metadata_file
    }


def main():
    """Función principal"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description="Generador de Sitios de Noticias",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Ejemplos:
  Modo interactivo (recomendado):
    python3 generate-sites.py
  
  Modo no-interactivo:
    python3 generate-sites.py --cantidad 10 --generar-metadata
    python3 generate-sites.py --cantidad 5 --verificar-dominios
        """
    )
    parser.add_argument(
        '--cantidad',
        type=int,
        help='Cantidad de sitios a crear (1-100)'
    )
    parser.add_argument(
        '--generar-metadata',
        action='store_true',
        help='Generar nuevos metadatos de sitios'
    )
    parser.add_argument(
        '--metadata-file',
        type=str,
        help='Archivo de metadatos específico a usar'
    )
    parser.add_argument(
        '--verificar-dominios',
        action='store_true',
        help='Verificar disponibilidad de dominios (requiere whois)'
    )
    parser.add_argument(
        '--no-interactivo',
        action='store_true',
        help='Desactivar modo interactivo'
    )
    
    args = parser.parse_args()
    
    # Determinar si usar modo interactivo
    modo_no_interactivo = args.no_interactivo or args.cantidad is not None or args.generar_metadata or args.metadata_file
    
    if not modo_no_interactivo and sys.stdin.isatty():
        # Modo interactivo
        config = modo_interactivo()
        if config is None:
            return
        
        cantidad = config['cantidad']
        verificar_dominios = config['verificar_dominios']
        usar_existentes = config['usar_existentes']
        metadata_file = config['metadata_file']
        generar_metadata = not usar_existentes
    else:
        # Modo no-interactivo (argumentos de línea de comandos)
        print("🚀 Generador de Sitios de Noticias")
        print("=" * 50)
        print()
        
        cantidad = args.cantidad or NUM_TEMPLATES
        verificar_dominios = args.verificar_dominios
        generar_metadata = args.generar_metadata
        metadata_file = args.metadata_file
        usar_existentes = metadata_file is not None
    
    # Validar cantidad
    if cantidad < 1 or cantidad > 100:
        print("❌ Error: La cantidad debe estar entre 1 y 100")
        return
    
    print("\n🚀 Iniciando proceso de generación...")
    print("=" * 60)
    
    # Crear directorio de salida
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    Path(METADATA_DIR).mkdir(parents=True, exist_ok=True)
    
    # Generar o cargar metadatos
    sites_metadata = None
    
    if usar_existentes and metadata_file:
        # Cargar metadatos existentes
        print(f"\n💾 Cargando metadatos desde {metadata_file}...")
        sites_metadata = load_sites_metadata(metadata_file)
        if not sites_metadata:
            print("⚠️  No se pudieron cargar metadatos, generando nuevos...")
            generar_metadata = True
    
    if generar_metadata or (not usar_existentes and not sites_metadata):
        if not METADATA_AVAILABLE:
            print("⚠️ Módulo de metadatos no disponible, usando configuración por defecto")
        else:
            print(f"\n🆕 Generando {cantidad} metadatos de sitios...")
            print("=" * 60)
            protocolo = SitePreCreation(output_dir=METADATA_DIR)
            sites_metadata = protocolo.crear_batch_sitios(
                cantidad=cantidad,
                verificar_dominios=verificar_dominios,
                guardar_archivo=True
            )
    
    # Limpiar sitios HTML antiguos
    print(f"\n🧹 Limpiando sitios antiguos...")
    output_path = Path(OUTPUT_DIR)
    if output_path.exists():
        old_sites = list(output_path.glob("site*.html"))
        if old_sites:
            for site in old_sites:
                site.unlink()
            print(f"   Eliminados {len(old_sites)} sitios antiguos")
        else:
            print("   No hay sitios antiguos")
    
    # Cargar datos de noticias
    print(f"\n📰 Cargando noticias...")
    news_data = load_news_data()
    if not news_data:
        print("❌ No se pudieron cargar las noticias")
        return
    
    # Generar sitios HTML
    print(f"\n🏭 Generando {cantidad} sitios HTML...")
    print("=" * 60)
    
    for i in range(1, cantidad + 1):
        # Seleccionar configuración del sitio
        if sites_metadata and i <= len(sites_metadata):
            # Usar metadata generada
            metadata = sites_metadata[i - 1]
            site_config = {
                'title': metadata['nombre'],
                'tagline': metadata['tagline']
            }
            print(f"  [{i}/{cantidad}] 📦 {metadata['nombre']} ({metadata['dominio']})")
        else:
            # Usar configuración por defecto
            site_config = SITE_CONFIGS[(i - 1) % len(SITE_CONFIGS)]
            print(f"  [{i}/{cantidad}] 📦 {site_config['title']}")
        
        # Generar HTML
        html_content = generate_html(i, site_config, news_data)
        
        # Guardar archivo
        output_file = f"{OUTPUT_DIR}/site{i}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    print(f"\n🎉 ¡Completado!")
    print("=" * 60)
    print(f"📁 {cantidad} sitios generados en '{OUTPUT_DIR}/'")
    print(f"👀 Abre site1.html hasta site{cantidad}.html para ver los resultados")
    if sites_metadata:
        print(f"📦 Metadatos guardados en '{METADATA_DIR}/'")
    print()

if __name__ == "__main__":
    main()
