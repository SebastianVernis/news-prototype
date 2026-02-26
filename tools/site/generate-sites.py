#!/usr/bin/env python3
"""
Script para generar sitios HTML con templates actualizados automáticamente
Lee datos de noticias y genera múltiples sitios con diferentes estilos
"""

import json
import os
import random
import re
import struct
import zlib
from datetime import datetime
from pathlib import Path

try:
    from layout_generator import LayoutGenerator, HTMLLayoutBuilder
    LAYOUTS_AVAILABLE = True
except ImportError:
    LAYOUTS_AVAILABLE = False

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("NEWS_DATA_DIR", REPO_ROOT / "data"))
OUTPUT_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))
CSS_DIR_FS = Path(os.getenv("NEWS_TEMPLATES_DIR", REPO_ROOT / "public" / "templates" / "css"))
CSS_LINK_PATH = os.getenv("NEWS_TEMPLATES_LINK", "templates/css")
ASSETS_DIR = Path(os.getenv("NEWS_ASSETS_DIR", REPO_ROOT / "assets")) / "images"
ASSET_IMAGES = [p for p in ASSETS_DIR.glob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".svg"}]
METADATA_DIR = Path(os.getenv("NEWS_METADATA_DIR", DATA_DIR / "sites_metadata"))

# Configuración
TEMPLATE_FILES = sorted(CSS_DIR_FS.glob("template*.css"))
TEMPLATE_COUNT = len(TEMPLATE_FILES)
NUM_TEMPLATES = TEMPLATE_COUNT if TEMPLATE_COUNT > 0 else 1
MAX_TEMPLATES = TEMPLATE_COUNT if TEMPLATE_COUNT > 0 else 1

# Categorías unificadas (mismas que create-complete-structure.py)
CATEGORIES = ["Política", "Economía", "Deportes", "Tecnología", "Cultura", "Internacional"]

def create_smoke_logo(output_path: Path, seed: int = 0, size: int = 256) -> None:
    """Crea un PNG 'smoke' simple como placeholder de logo."""
    rng = random.Random(seed)
    width = height = size
    raw = bytearray()

    for y in range(height):
        raw.append(0)  # filtro PNG: None
        for x in range(width):
            cx = (x - width / 2) / width
            cy = (y - height / 2) / height
            dist = (cx * cx + cy * cy) ** 0.5
            base = 225 - int(dist * 110)
            noise = rng.randint(-20, 20)
            val = max(160, min(240, base + noise))
            raw.extend([val, val, val, 255])

    compressed = zlib.compress(bytes(raw), level=9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        )

    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = header + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")
    output_path.write_bytes(png)

def slugify(value: str) -> str:
    """Convierte un string a slug sin tildes ni caracteres especiales"""
    import re
    value = (value or "").strip().lower()
    # Eliminar tildes y caracteres especiales
    value = re.sub(r'[^\w\s-]', '', value)
    value = re.sub(r'[-\s]+', '-', value)
    value = value.strip('-')
    return value or "site"

def _find_latest_news_file():
    # Priorizar archivos con imágenes cacheadas
    patterns = [
        "*paraphrased*_cached_images.json",  # Primero: paraphrased con imágenes
        "*_cached_images.json",               # Segundo: cualquier cached images
        "noticias_mx_*.json",
        "newsapi_*.json",
        "newsdata_*.json",
        "worldnews_*.json",
        "apitube_*.json",
        "*paraphrased*.json"
    ]
    files = []
    for pattern in patterns:
        files.extend(DATA_DIR.glob(pattern))
    
    # Si hay archivos cached, priorizarlos
    cached_files = [f for f in files if "cached_images" in str(f)]
    if cached_files:
        return sorted(cached_files)[-1]
    
    return sorted(files)[-1] if files else None


def load_news_data():
    """Carga los datos de noticias del archivo JSON más reciente"""
    news_file = os.getenv("NEWS_FILE")
    path = Path(news_file) if news_file else _find_latest_news_file()
    if not path or not path.exists():
        print("❌ Error: No se encontró archivo de noticias en data/")
        return []

    with open(path, "r", encoding="utf-8") as f:
        news = json.load(f)

    print(f"✅ Cargadas {len(news)} noticias desde {path}")
    return news

def extract_sentences(text, max_sentences=2):
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    parts = [p for p in parts if p]
    return " ".join(parts[:max_sentences]).strip()


def safe_excerpt(text, max_chars=220):
    """Extrae un resumen sin usar ellipsis ni cortar frases"""
    excerpt = extract_sentences(text, 2)
    if excerpt:
        return excerpt
    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return cleaned
    cut = cleaned[:max_chars]
    return cut.rsplit(" ", 1)[0].strip()


def sanitize_title(title, fallback):
    title = (title or "").strip()
    if not title or title.lower().startswith("noticia"):
        return extract_sentences(fallback, 1) or "Actualización informativa"
    return title


def sanitize_description(description, fallback):
    description = (description or "").strip()
    if not description or "..." in description:
        return safe_excerpt(fallback)
    return safe_excerpt(description)

def render_logo_block(site_config: dict) -> str:
    title = site_config["title"]
    tagline = site_config["tagline"]
    logo_path = site_config.get("logo_path")
    if logo_path:
        return f"""            <div class="logo-image">
                <img src="{logo_path}" alt="Logo {title}" class="logo-img">
                <div class="logo-text">
                    <h1>{title}</h1>
                    <p class="tagline">{tagline}</p>
                </div>
            </div>
"""
    return f"""            <div class="logo">
                <h1>{title}</h1>
                <p class="tagline">{tagline}</p>
            </div>
"""

def normalize_image_path(path_value: str) -> str:
    if not path_value:
        return ''
    if path_value.startswith('http'):
        return path_value
    if 'assets/' in path_value:
        return path_value
    filename = Path(path_value).name
    return f"assets/images/{filename}"


def fallback_image(index: int) -> str:
    if ASSET_IMAGES:
        return f"assets/images/{ASSET_IMAGES[index % len(ASSET_IMAGES)].name}"
    return f"assets/images/fallback-{(index % 3) + 1}.svg"

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

def generate_html(template_num, site_config, news_data, max_templates=MAX_TEMPLATES, usar_layouts_dinamicos=True, css_link_path: str | None = None):
    """Genera el HTML para un template específico"""
    
    # Ajustar número de template si excede el máximo
    actual_template = ((template_num - 1) % max_templates) + 1
    
    # Generar configuración de layout dinámico si está disponible
    layout_config = None
    if usar_layouts_dinamicos and LAYOUTS_AVAILABLE:
        generator = LayoutGenerator()
        layout_config = generator.generar_configuracion_layout(seed=template_num)
        distribucion = generator.generar_distribucion_noticias(len(news_data), seed=template_num)
        
        # Randomizar categorías
        categorias_randomizadas = generator.randomizar_categorias(CATEGORIES.copy(), seed=template_num)
    else:
        categorias_randomizadas = CATEGORIES.copy()
        distribucion = {
            "featured": 1,
            "main": 4,
            "sidebar": 3
        }
    # Siempre aleatorizar el orden de categorías
    random.shuffle(categorias_randomizadas)
    
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
                                     categorias_randomizadas, layout_config, distribucion, css_link_path)
    
    # Modo estático (fallback)
    css_link = css_link_path or CSS_LINK_PATH
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_config['title']} - Noticias de Última Hora</title>
    <link rel="stylesheet" href="{css_link}/template{actual_template}.css">
</head>
<body>
    <header class="header">
        <div class="container">
{render_logo_block(site_config)}            <nav class="nav">
"""
    
    # Agregar categorías del menú
    for category in categorias_randomizadas:
        slug = slugify(category)
        html += f'                <a href="categoria-{slug}.html" class="nav-link">{category}</a>\n'
    
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
        image_path = normalize_image_path(
            featured.get('ai_image_path')
            or featured.get('image')
            or featured.get('urlToImage')
            or fallback_image(0)
        )
        
        base_text = featured.get('full_text') or featured.get('content') or featured.get('description') or ''
        title = sanitize_title(featured.get('title', ''), base_text)
        description = sanitize_description(featured.get('description', ''), base_text)
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
        image_path = normalize_image_path(
            news.get('ai_image_path')
            or news.get('image')
            or news.get('urlToImage')
            or fallback_image(i)
        )
        
        base_text = news.get('full_text') or news.get('content') or news.get('description') or ''
        title = sanitize_title(news.get('title', ''), base_text)
        description = sanitize_description(news.get('description', ''), base_text)
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
        base_text = news.get('full_text') or news.get('content') or news.get('description') or ''
        title = sanitize_title(news.get('title', ''), base_text)
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
        slug = slugify(category)
        html += f'                        <li><a href="categoria-{slug}.html">{category}</a></li>\n'
    
    html += f"""                    </ul>
                </div>
                <div class="footer-column">
                    <h4>Legal</h4>
                    <ul class="footer-links">
                        <li><a href="terminos.html">Términos de Uso</a></li>
                        <li><a href="privacidad.html">Política de Privacidad</a></li>
                        <li><a href="cookies.html">Cookies</a></li>
                        <li><a href="contacto.html">Contacto</a></li>
                        <li><a href="acerca-de.html">Acerca de</a></li>
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
                          categorias, layout_config, distribucion, css_link_path: str | None = None):
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
    css_link = css_link_path or CSS_LINK_PATH
    favicon_html = f'<link rel="icon" href="{site_config["favicon_path"]}" type="image/{os.path.splitext(site_config["favicon_path"])[1].lower().replace(".", "")}">' if site_config.get('favicon_path') else '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📰</text></svg>'
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_config['title']} - Noticias de Última Hora</title>
    <link rel="stylesheet" href="{css_link}/template{template_num}.css">
    {favicon_html}
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
        ("Legal", ["Términos de Uso", "Política de Privacidad", "Cookies", "Contacto", "Acerca de"]),
        ("Contacto", [f"Email: contacto@{site_config['title'].lower().replace(' ', '')}.com", "Tel: +52 55 1234 5678", "Ciudad de México, México"])
    ]
    
    for i, (titulo, items) in enumerate(footer_sections[:layout_config['footer_columns'] - 1]):
        html += f'''                <div class="footer-column">
                    <h4>{titulo}</h4>
                    <ul class="footer-links">
'''
        for item in items:
            if isinstance(item, str) and '@' not in item and ':' not in item:
                if titulo == "Secciones":
                    slug = slugify(item)
                    html += f'                        <li><a href="categoria-{slug}.html">{item}</a></li>\n'
                elif titulo == "Legal":
                    legal_map = {
                        "Términos de Uso": "terminos.html",
                        "Política de Privacidad": "privacidad.html",
                        "Cookies": "cookies.html",
                        "Contacto": "contacto.html",
                        "Acerca de": "acerca-de.html",
                    }
                    href = legal_map.get(item, "#")
                    html += f'                        <li><a href="{href}">{item}</a></li>\n'
                else:
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
    """Modo interactivo simplificado - solo pide cantidad de sitios"""
    print("🎉 Generador de Sitios de Noticias")
    print("=" * 60)
    print()

    # Única pregunta: Cantidad de sitios
    while True:
        try:
            cantidad = input("📊 ¿Cuántos sitios deseas crear? (1-100) [default: 3]: ").strip()
            if not cantidad:
                cantidad = 3
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
    print("✍️  Se solicitará nombre y dominio para cada sitio")
    print()

    # Configuración fija
    verificar_dominios = False
    usar_existentes = False
    metadata_file = None
    manual_sites = True  # Siempre manual

    return {
        'cantidad': cantidad,
        'verificar_dominios': verificar_dominios,
        'usar_existentes': usar_existentes,
        'metadata_file': metadata_file,
        'manual_sites': manual_sites
    }


def prompt_site_details(index: int) -> dict:
    """Solicita configuración del sitio incluyendo logo y favicon"""
    print(f"\n🧩 Configuración del sitio {index}")
    
    while True:
        name = input("Nombre del sitio: ").strip()
        if name:
            break
        print("⚠️  El nombre no puede estar vacío")
    
    while True:
        domain = input("Dominio (sin https): ").strip()
        if domain:
            break
        print("⚠️  El dominio no puede estar vacío")
    
    tagline = input("Tagline (opcional, Enter para automático): ").strip()
    if not tagline:
        tagline = "Tu fuente confiable de información"
    
    # Preguntar por logo
    print("\n📁 Logo del sitio:")
    logo_path = input("   Ruta del archivo de logo (opcional, Enter para omitir): ").strip()
    if logo_path:
        logo_path = os.path.expanduser(logo_path)
        if not os.path.exists(logo_path):
            print(f"⚠️  Archivo no encontrado: {logo_path}")
            logo_path = None
    
    # Preguntar por favicon
    print("\n🎨 Favicon del sitio:")
    favicon_path = input("   Ruta del archivo de favicon (opcional, Enter para omitir): ").strip()
    if favicon_path:
        favicon_path = os.path.expanduser(favicon_path)
        if not os.path.exists(favicon_path):
            print(f"⚠️  Archivo no encontrado: {favicon_path}")
            favicon_path = None
    
    return {
        "title": name,
        "tagline": tagline,
        "domain": domain,
        "logo_path": logo_path,
        "favicon_path": favicon_path
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

  Modo no-interactivo (batch):
    python3 generate-sites.py --cantidad 10 --no-interactivo
        """
    )
    parser.add_argument(
        '--cantidad',
        type=int,
        help='Cantidad de sitios a crear (1-100)'
    )
    parser.add_argument(
        '--no-interactivo',
        action='store_true',
        help='Desactivar modo interactivo (usar valores por defecto)'
    )

    args = parser.parse_args()

    # Determinar modo de operación
    if args.cantidad is not None:
        # Modo semi-interactivo: cantidad ya especificada, pero pedir nombres de sitios
        cantidad = args.cantidad
        verificar_dominios = False
        usar_existentes = False
        metadata_file = None
        generar_metadata = False
        manual_sites = True  # Siempre pedir nombres
        print("🚀 Generador de Sitios de Noticias")
        print("=" * 50)
        print(f"📊 Cantidad de sitios: {cantidad}")
        print("✍️  Se solicitará nombre y dominio para cada sitio")
        print()
    elif not args.no_interactivo and sys.stdin.isatty():
        # Modo interactivo completo - pregunta cantidad
        config = modo_interactivo()
        if config is None:
            return

        cantidad = config['cantidad']
        verificar_dominios = config['verificar_dominios']
        usar_existentes = config['usar_existentes']
        metadata_file = config['metadata_file']
        generar_metadata = not usar_existentes
        manual_sites = config.get('manual_sites', True)
    else:
        # Modo batch - preguntar cantidad
        print("🚀 Generador de Sitios de Noticias")
        print("=" * 50)
        print()
        
        while True:
            try:
                cantidad_input = input("📊 ¿Cuántos sitios deseas crear? (1-100) [default: 3]: ").strip()
                if not cantidad_input:
                    cantidad = 3
                    break
                cantidad = int(cantidad_input)
                if 1 <= cantidad <= 100:
                    break
                print("⚠️  Por favor ingresá un número entre 1 y 100")
            except ValueError:
                print("⚠️  Por favor ingresá un número válido")
        
        verificar_dominios = False
        generar_metadata = True
        metadata_file = None
        usar_existentes = False
        manual_sites = True
    
    # Validar cantidad
    if cantidad < 1 or cantidad > 100:
        print("❌ Error: La cantidad debe estar entre 1 y 100")
        return
    
    print("\n🚀 Iniciando proceso de generación...")
    print("=" * 60)

    # Crear directorio de salida
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Limpiar sitios HTML antiguos
    print(f"\n🧹 Limpiando sitios antiguos...")
    output_path = OUTPUT_DIR
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
        # Solicitar configuración manual del sitio
        site_config = prompt_site_details(i)
        print(f"  [{i}/{cantidad}] 📦 {site_config['title']} ({site_config['domain']})")

        # Definir carpeta de salida por sitio (usando el dominio)
        base_dir_name = slugify(site_config.get("domain"))

        site_dir = output_path / base_dir_name
        if site_dir.exists():
            suffix = 2
            while (output_path / f"{base_dir_name}-{suffix}").exists():
                suffix += 1
            site_dir = output_path / f"{base_dir_name}-{suffix}"
            print(f"   ⚠️  Directorio existente, usando: {site_dir.name}")
        site_dir.mkdir(parents=True, exist_ok=True)

        # Crear directorio templates/css y copiar CSS
        templates_css_dir = site_dir / 'templates' / 'css'
        templates_css_dir.mkdir(parents=True, exist_ok=True)
        source_css = REPO_ROOT / 'public' / 'templates' / 'css'
        if source_css.exists():
            for css_file in source_css.glob('*.css'):
                dest_css = templates_css_dir / css_file.name
                if not dest_css.exists():
                    dest_css.write_bytes(css_file.read_bytes())

        # Copiar logo si se proporcionó
        logo_filename = "logo.png"
        logo_dest = site_dir / logo_filename
        if site_config.get('logo_path') and os.path.exists(site_config['logo_path']):
            import shutil
            shutil.copy2(site_config['logo_path'], logo_dest)
            print(f"   ✅ Logo copiado: {site_config['logo_path']} → {logo_dest}")
        else:
            # Crear logo smoke como fallback
            create_smoke_logo(logo_dest, seed=i)
            print(f"   🎨 Logo generado (placeholder)")
        site_config["logo_path"] = logo_filename

        # Copiar favicon si se proporcionó
        if site_config.get('favicon_path') and os.path.exists(site_config['favicon_path']):
            import shutil
            favicon_ext = os.path.splitext(site_config['favicon_path'])[1].lower()
            favicon_filename = f"favicon{favicon_ext}"
            shutil.copy2(site_config['favicon_path'], site_dir / favicon_filename)
            site_config["favicon_path"] = favicon_filename
            print(f"   ✅ Favicon copiado: {site_config['favicon_path']}")
        else:
            site_config["favicon_path"] = None

        site_config["output_dir"] = site_dir.name

        # Generar HTML
        html_content = generate_html(i, site_config, news_data, css_link_path="templates/css")
        
        # Reemplazar rutas de imágenes para que sean relativas (desde el sitio hacia assets/)
        html_content = html_content.replace('src="assets/images/', 'src="../assets/images/')
        html_content = html_content.replace('src="/assets/images/', 'src="../assets/images/')

        # Guardar archivo
        output_file = site_dir / "index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Guardar site_config.json
        config_file = site_dir / "site_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(
                {
                    "name": site_config.get("title"),
                    "tagline": site_config.get("tagline"),
                    "domain": site_config.get("domain"),
                    "output_dir": site_dir.name,
                    "logo": logo_filename
                },
                f,
                ensure_ascii=False,
                indent=2
            )
    
    print(f"\n🎉 ¡Completado!")
    print("=" * 60)
    print(f"📁 {cantidad} sitios generados en '{output_path}/'")
    print(f"👀 Abre sites/*/index.html para ver los resultados")
    print()

if __name__ == "__main__":
    main()
