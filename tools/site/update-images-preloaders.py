#!/usr/bin/env python3
"""
Script para actualizar imágenes, agregar preloaders y carruseles a los 10 sitios
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))
ASSETS_DIR = Path(os.getenv("NEWS_ASSETS_DIR", REPO_ROOT / "assets")) / "images"
TEMPLATES_DIR = Path(os.getenv("NEWS_TEMPLATES_DIR", REPO_ROOT / "public" / "templates" / "css"))

# Lista de imágenes disponibles en assets
available_images = list(ASSETS_DIR.glob('*.jpg'))[:20]  # Usar primeras 20 imágenes

def get_image_path(index):
    """Obtiene la ruta de una imagen del assets"""
    if available_images:
        img_index = index % len(available_images)
        return f"assets/images/{available_images[img_index].name}"
    fallback = f"assets/images/fallback-{(index % 3) + 1}.svg"
    return fallback

def extract_palette(template_num):
    css_file = TEMPLATES_DIR / f"template{template_num}.css"
    if not css_file.exists():
        return {"primary": "#1d3557", "secondary": "#457b9d", "accent": "#a8dadc"}
    css = css_file.read_text(encoding="utf-8", errors="ignore")
    def _find(var):
        match = re.search(rf"{var}\s*:\s*([^;]+);", css)
        return match.group(1).strip() if match else None
    return {
        "primary": _find("--primary-color") or "#1d3557",
        "secondary": _find("--secondary-color") or "#457b9d",
        "accent": _find("--accent-color") or "#a8dadc",
    }


def add_preloader(palette, variant=0):
    """Genera HTML del preloader con el logo del sitio girando"""
    primary = palette["primary"]
    return f'''
    <!-- Preloader -->
    <div id="preloader" style="position:fixed;top:0;left:0;width:100%;height:100%;background:{primary};z-index:999999;display:flex;flex-direction:column;justify-content:center;align-items:center;">
        <div style="text-align:center;">
            <div id="preloader-logo-container" style="margin-bottom:25px;animation:spin3D 2s ease-in-out infinite;">
                <img src="logo.png" alt="Logo" style="height:120px;width:auto;filter:brightness(0) invert(1);">
            </div>
            <div class="preloader-spinner" style="width:40px;height:40px;border:4px solid rgba(255,255,255,0.2);border-top:4px solid white;border-radius:50%;animation:spin 1s linear infinite;margin:0 auto 20px;"></div>
            <p style="font-family:Arial,sans-serif;color:white;font-weight:bold;letter-spacing:2px;text-transform:uppercase;font-size:0.9rem;">Cargando...</p>
        </div>
    </div>
    <style>
        @keyframes spin{{0%{{transform:rotate(0deg)}}100%{{transform:rotate(360deg)}}}}
        @keyframes spin3D {{
            0% {{ transform: rotateY(0deg) scale(1); }}
            50% {{ transform: rotateY(180deg) scale(1.1); }}
            100% {{ transform: rotateY(360deg) scale(1); }}
        }}
    </style>
    <script>
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                var preloader = document.getElementById('preloader');
                if(preloader) {{
                    preloader.style.transition = 'opacity 0.5s ease';
                    preloader.style.opacity = '0';
                    setTimeout(function() {{ preloader.style.display = 'none'; }}, 500);
                }}
            }}, 1500);
        }});
    </script>
'''

def add_carousel():
    """Genera sección de carrusel de noticias"""
    img1 = get_image_path(1)
    img2 = get_image_path(2)
    img3 = get_image_path(3)
    return f'''
    <!-- Carrusel de Noticias -->
    <section style="background:var(--background-color, #E0F2F1);padding:40px 20px;margin:20px 0;">
        <div style="max-width:1200px;margin:0 auto;">
            <h2 style="text-align:center;margin-bottom:30px;font-size:2em;color:var(--text-color, #004D40);">Últimas Noticias</h2>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;">
                <article style="background:var(--card-bg, #FFFFFF);border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
                    <img src="{img1}" alt="Noticia 1" style="width:100%;height:200px;object-fit:cover;">
                    <div style="padding:20px;">
                        <h3 style="margin:0 0 10px 0;font-size:1.2em;">Actualización destacada</h3>
                        <p style="color:#666;line-height:1.6;">Resumen informativo con contexto actualizado.</p>
                    </div>
                </article>
                <article style="background:white;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
                    <img src="{img2}" alt="Noticia 2" style="width:100%;height:200px;object-fit:cover;">
                    <div style="padding:20px;">
                        <h3 style="margin:0 0 10px 0;font-size:1.2em;">Cobertura en curso</h3>
                        <p style="color:#666;line-height:1.6;">Contenido editorial revisado y consistente.</p>
                    </div>
                </article>
                <article style="background:white;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
                    <img src="{img3}" alt="Noticia 3" style="width:100%;height:200px;object-fit:cover;">
                    <div style="padding:20px;">
                        <h3 style="margin:0 0 10px 0;font-size:1.2em;">Análisis del día</h3>
                        <p style="color:#666;line-height:1.6;">Síntesis precisa sin contenido incompleto.</p>
                    </div>
                </article>
            </div>
        </div>
    </section>
'''

def update_site_file(site_file: Path, template_fallback: int, allow_carousel: bool = True, allow_images: bool = True):
    """Actualiza un archivo HTML con preloader (y opcionalmente carrusel/imagenes)"""
    if not site_file.exists():
        print(f"⚠️ Archivo no encontrado: {site_file}")
        return False

    content = site_file.read_text(encoding='utf-8')

    # 1. Reemplazar placeholders con imágenes reales (opcional)
    if allow_images:
        img_index = 0
        def replace_placeholder(match):
            nonlocal img_index
            img_path = get_image_path(img_index)
            img_index += 1
            return f'<img src="{img_path}" alt="Noticia" class="card-image" loading="lazy">'

        content = re.sub(
            r'<img src="https://via\.placeholder\.com/[^"]*"[^>]*class="card-image"[^>]*>',
            replace_placeholder,
            content
        )

    # 2. Actualizar o agregar preloader después del <body>
    match = re.search(r'template(\d+)\.css', content)
    template_num = int(match.group(1)) if match else template_fallback
    palette = extract_palette(template_num)
    
    # ELIMINAR CUALQUIER PRELOADER EXISTENTE
    # Usamos una técnica más agresiva: buscar cualquier div con id o clase preloader y capturar hasta que veamos el header o un comentario de carrusel
    content = re.sub(r'<!-- Preloader -->.*?<script>.*?</script>', '', content, flags=re.DOTALL)
    # Eliminar bloques de preloader de forma más amplia (desde el div hasta el script que lo suele acompañar o el siguiente bloque grande)
    content = re.sub(r'<div[^>]*?(id|class)="preloader[^"]*".*?</div>\s*</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div[^>]*?(id|class)="preloader[^"]*".*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*window\.addEventListener\(\'load\', function\(\) \{.*?\}\);?\s*</script>', '', content, flags=re.DOTALL)

    def _insert_preloader(match):
        return match.group(0) + "\n" + add_preloader(palette, variant=template_num)

    content = re.sub(r"<body[^>]*>", _insert_preloader, content, count=1)

    # 3. Agregar carrusel después del header principal (opcional)
    if allow_carousel and '<main' in content and '<!-- Carrusel de Noticias -->' not in content:
        content = content.replace('<main', add_carousel() + '\n    <main')

    # 4. Agregar estilos para imágenes si aplica
    if allow_images and '.card-image' in content and '</head>' in content:
        styles = '''
    <style>
        .card-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        .card-image:hover {
            transform: scale(1.05);
        }
        .card-image-wrapper {
            overflow: hidden;
            border-radius: 8px;
        }
    </style>
    '''
        content = content.replace('</head>', styles + '\n</head>')

    site_file.write_text(content, encoding='utf-8')
    print(f"✅ Actualizado: {site_file}")
    return True

def main():
    print("🖼️  Actualizando imágenes, preloaders y carruseles...")
    print("="*60)
    
    # Verificar imágenes disponibles
    if available_images:
        print(f"✅ Imágenes encontradas: {len(available_images)} imágenes en assets")
    else:
        print("⚠️ No se encontraron imágenes en assets, se usarán placeholders")
    
    # Actualizar todos los archivos HTML de forma recursiva
    print("📂 Actualizando archivos de forma recursiva...")
    for html_file in SITES_DIR.rglob('*.html'):
        if 'admin' in str(html_file): continue
        
        is_main_index = html_file.name == 'index.html' and html_file.parent.parent == SITES_DIR
        update_site_file(
            html_file, 
            template_fallback=1, 
            allow_carousel=is_main_index, 
            allow_images=True
        )
    
    print("="*60)
    print("✅ Sitios actualizados con preloaders.")

if __name__ == "__main__":
    main()
