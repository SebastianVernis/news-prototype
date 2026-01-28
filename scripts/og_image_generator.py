#!/usr/bin/env python3
"""
Generador de Imágenes Open Graph
Crea miniaturas optimizadas para redes sociales (1200x630)
"""

import os
import sys
from pathlib import Path
from typing import Dict, List
from PIL import Image, ImageDraw, ImageFont
import textwrap


class OGImageGenerator:
    """Genera imágenes Open Graph para artículos"""
    
    # Dimensiones estándar Open Graph
    OG_WIDTH = 1200
    OG_HEIGHT = 630
    
    def __init__(self):
        self.output_dir = Path('public/og-images')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Colores por defecto
        self.default_bg_color = (102, 126, 234)  # #667eea
        self.default_text_color = (255, 255, 255)
        
        # Intentar cargar fuentes
        self.font_title = self._load_font(60)
        self.font_subtitle = self._load_font(32)
        self.font_category = self._load_font(28)
    
    def _load_font(self, size: int):
        """Intenta cargar una fuente"""
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            'C:/Windows/Fonts/arialbd.ttf',
            '/System/Library/Fonts/Helvetica.ttc',
        ]
        
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            except:
                pass
        
        # Fallback a fuente por defecto
        return ImageFont.load_default()
    
    def generar_og_image(
        self,
        article: Dict,
        site_metadata: Dict,
        output_name: str = None
    ) -> str:
        """
        Genera imagen Open Graph para un artículo
        
        Args:
            article: Datos del artículo
            site_metadata: Metadata del sitio
            output_name: Nombre del archivo de salida
            
        Returns:
            Path de la imagen generada
        """
        # Crear imagen
        img = Image.new('RGB', (self.OG_WIDTH, self.OG_HEIGHT), self.default_bg_color)
        draw = ImageDraw.Draw(img)
        
        # Agregar gradiente (simulado con rectángulos)
        for i in range(self.OG_HEIGHT):
            # Gradiente de púrpura a azul
            r = int(102 + (118 - 102) * (i / self.OG_HEIGHT))
            g = int(126 + (75 - 126) * (i / self.OG_HEIGHT))
            b = int(234 + (162 - 234) * (i / self.OG_HEIGHT))
            draw.rectangle([(0, i), (self.OG_WIDTH, i + 1)], fill=(r, g, b))
        
        # Padding
        padding = 60
        max_width = self.OG_WIDTH - (padding * 2)
        
        # Categoría (arriba)
        category = article.get('category_name', 'Noticias')
        category_y = padding
        draw.text(
            (padding, category_y),
            category.upper(),
            font=self.font_category,
            fill=(255, 255, 255, 200)
        )
        
        # Título (centro)
        title = article.get('title', 'Sin título')
        
        # Envolver texto del título
        wrapped_title = textwrap.fill(title, width=40)
        title_lines = wrapped_title.split('\n')[:4]  # Máximo 4 líneas
        
        title_y = 180
        for line in title_lines:
            draw.text(
                (padding, title_y),
                line,
                font=self.font_title,
                fill=self.default_text_color
            )
            title_y += 75
        
        # Site name (abajo)
        site_name = site_metadata.get('site_name', 'Noticias')
        site_y = self.OG_HEIGHT - padding - 40
        draw.text(
            (padding, site_y),
            site_name,
            font=self.font_subtitle,
            fill=(255, 255, 255, 230)
        )
        
        # Guardar imagen
        if not output_name:
            # Crear nombre desde título
            safe_title = "".join(c for c in title[:50] if c.isalnum() or c in (' ', '-')).strip()
            safe_title = safe_title.replace(' ', '-').lower()
            output_name = f"og_{safe_title}.png"
        
        output_path = self.output_dir / output_name
        img.save(output_path, 'PNG', optimize=True)
        
        return str(output_path)
    
    def generar_og_images_lote(
        self,
        articles: List[Dict],
        site_metadata: Dict
    ) -> Dict[int, str]:
        """
        Genera imágenes OG para múltiples artículos
        
        Args:
            articles: Lista de artículos
            site_metadata: Metadata del sitio
            
        Returns:
            Dict con índice -> path de imagen
        """
        print(f"\n{'='*70}")
        print(f"🖼️  GENERANDO IMÁGENES OPEN GRAPH")
        print(f"{'='*70}")
        print(f"Dimensiones: {self.OG_WIDTH}x{self.OG_HEIGHT}")
        print(f"Total artículos: {len(articles)}\n")
        
        images = {}
        
        for idx, article in enumerate(articles, 1):
            title = article.get('title', 'Sin título')[:50]
            print(f"[{idx}/{len(articles)}] {title}...", end=" ")
            
            try:
                output_name = f"og_article_{idx}.png"
                image_path = self.generar_og_image(article, site_metadata, output_name)
                images[idx] = image_path
                
                # Agregar path al artículo
                article['og_image_path'] = image_path
                
                print(f"✅")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\n{'='*70}")
        print(f"✅ Generadas {len(images)} imágenes OG")
        print(f"📁 Directorio: {self.output_dir}")
        print(f"{'='*70}")
        
        return images
    
    def _escape_html(self, text: str) -> str:
        """Escapa HTML"""
        if not text:
            return ''
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;'))
    
    def _escape_json(self, text: str) -> str:
        """Escapa para JSON"""
        if not text:
            return ''
        return (text
                .replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', ' '))


def main():
    """Test del generador de imágenes OG"""
    import json
    import glob
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║        🖼️  GENERADOR DE IMÁGENES OPEN GRAPH (1200x630)             ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Cargar artículos
    json_files = glob.glob('noticias_parafraseadas*.json')
    if not json_files:
        print("❌ No se encontraron artículos")
        return
    
    with open(sorted(json_files)[-1], 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    site_metadata = {
        'site_name': 'Política México Hoy',
        'site_url': 'https://politica-mexico.com'
    }
    
    # Generar imágenes
    generator = OGImageGenerator()
    images = generator.generar_og_images_lote(articles[:2], site_metadata)
    
    print(f"\n📊 Imágenes generadas:")
    for idx, path in images.items():
        print(f"  {idx}. {path}")


if __name__ == '__main__':
    main()
