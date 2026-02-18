#!/usr/bin/env python3
"""
Generador automático de imágenes para noticias
Crea visualizaciones artísticas abstractas basadas en categorías
NO genera rostros ni personas - solo arte conceptual
"""

import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import colorsys
    import random
    import math
except ImportError:
    print("Instalando dependencias necesarias...")
    os.system("pip install Pillow")
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    import colorsys
    import random
    import math


class NewsImageGenerator:
    """Genera imágenes abstractas artísticas para categorías de noticias"""
    
    # Paletas de colores por categoría (sin rostros/personas)
    CATEGORY_THEMES = {
        'technology': {
            'colors': [(0, 150, 255), (100, 50, 255), (0, 255, 200)],
            'shapes': ['circuit', 'grid', 'waves', 'particles'],
            'description': 'Circuitos digitales y ondas tecnológicas'
        },
        'sports': {
            'colors': [(255, 100, 0), (0, 200, 100), (255, 200, 0)],
            'shapes': ['dynamic', 'motion', 'energy', 'abstract_field'],
            'description': 'Movimiento y energía abstracta'
        },
        'politics': {
            'colors': [(50, 50, 150), (150, 50, 50), (200, 200, 200)],
            'shapes': ['buildings', 'monuments', 'flags_abstract', 'pillars'],
            'description': 'Arquitectura y símbolos abstractos'
        },
        'business': {
            'colors': [(0, 100, 200), (50, 150, 100), (200, 150, 0)],
            'shapes': ['graphs', 'charts', 'geometric', 'growth'],
            'description': 'Gráficos y crecimiento visual'
        },
        'entertainment': {
            'colors': [(255, 50, 150), (255, 200, 0), (150, 0, 255)],
            'shapes': ['stage_lights', 'musical_waves', 'colorful', 'celebration'],
            'description': 'Luces y celebración abstracta'
        },
        'health': {
            'colors': [(0, 200, 150), (50, 150, 255), (200, 250, 200)],
            'shapes': ['organic', 'heartbeat', 'wellness', 'nature'],
            'description': 'Formas orgánicas y bienestar'
        },
        'science': {
            'colors': [(100, 0, 200), (0, 255, 255), (255, 100, 255)],
            'shapes': ['atoms', 'molecules', 'space', 'laboratory'],
            'description': 'Átomos y conceptos científicos'
        },
        'environment': {
            'colors': [(50, 150, 50), (100, 200, 100), (0, 150, 200)],
            'shapes': ['nature', 'earth', 'eco', 'sustainability'],
            'description': 'Naturaleza y sostenibilidad'
        },
        'world': {
            'colors': [(100, 100, 255), (255, 150, 0), (0, 200, 200)],
            'shapes': ['globe_abstract', 'connections', 'continents', 'networks'],
            'description': 'Conexiones globales abstractas'
        },
        'tourism': {
            'colors': [(255, 200, 100), (100, 200, 255), (255, 150, 150)],
            'shapes': ['landscapes', 'horizons', 'destinations', 'journey'],
            'description': 'Paisajes y horizontes'
        },
        'lifestyle': {
            'colors': [(255, 150, 200), (200, 150, 255), (255, 200, 150)],
            'shapes': ['modern', 'minimalist', 'comfort', 'balance'],
            'description': 'Diseño moderno y equilibrio'
        },
        'default': {
            'colors': [(100, 100, 200), (200, 100, 100), (100, 200, 100)],
            'shapes': ['abstract', 'geometric', 'minimal'],
            'description': 'Diseño abstracto y geométrico'
        }
    }

    def __init__(self, output_dir=None):
        default_dir = Path(__file__).resolve().parents[2] / 'output' / 'generated_images' / 'news'
        self.output_dir = Path(output_dir) if output_dir else default_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = 1200
        self.height = 600
        
    def generate_gradient_background(self, colors):
        """Genera fondo con gradiente artístico"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        for y in range(self.height):
            ratio = y / self.height
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
            
        return img

    def draw_circuit_pattern(self, draw, colors):
        """Patrón de circuitos tecnológicos"""
        for _ in range(30):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            width = random.randint(50, 200)
            height = random.randint(50, 200)
            color = random.choice(colors)
            draw.rectangle([x, y, x + width, y + 3], fill=color, outline=color)
            draw.rectangle([x, y, x + 3, y + height], fill=color, outline=color)
            draw.ellipse([x + width - 10, y + height - 10, x + width + 10, y + height + 10], 
                        fill=color, outline=color)

    def draw_wave_pattern(self, draw, colors):
        """Ondas abstractas dinámicas"""
        for i in range(5):
            points = []
            amplitude = random.randint(50, 150)
            frequency = random.uniform(0.01, 0.03)
            offset = random.randint(0, self.height)
            
            for x in range(0, self.width, 5):
                y = offset + int(amplitude * math.sin(frequency * x + i))
                points.append((x, y))
            
            if len(points) > 1:
                color = random.choice(colors)
                draw.line(points, fill=color, width=random.randint(3, 8))

    def draw_geometric_shapes(self, draw, colors):
        """Formas geométricas abstractas"""
        for _ in range(15):
            shape_type = random.choice(['circle', 'triangle', 'rectangle'])
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(30, 150)
            color = random.choice(colors)
            
            if shape_type == 'circle':
                draw.ellipse([x, y, x + size, y + size], fill=color, outline=color)
            elif shape_type == 'rectangle':
                draw.rectangle([x, y, x + size, y + size], fill=color, outline=color)
            elif shape_type == 'triangle':
                points = [(x, y + size), (x + size//2, y), (x + size, y + size)]
                draw.polygon(points, fill=color, outline=color)

    def draw_particle_system(self, draw, colors):
        """Sistema de partículas abstracto"""
        for _ in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(2, 10)
            color = random.choice(colors)
            draw.ellipse([x, y, x + size, y + size], fill=color)
            
            # Líneas de conexión
            if random.random() > 0.7:
                x2 = x + random.randint(-100, 100)
                y2 = y + random.randint(-100, 100)
                draw.line([(x, y), (x2, y2)], fill=color, width=1)

    def draw_graph_pattern(self, draw, colors):
        """Gráficos y charts abstractos para negocios"""
        for i in range(6):
            x_start = i * (self.width // 6) + 50
            points = []
            
            for j in range(10):
                x = x_start + j * 20
                y = random.randint(100, self.height - 100)
                points.append((x, y))
            
            if len(points) > 1:
                color = random.choice(colors)
                draw.line(points, fill=color, width=4)
                
                # Puntos en el gráfico
                for point in points:
                    draw.ellipse([point[0]-6, point[1]-6, point[0]+6, point[1]+6], 
                               fill=color, outline=color)

    def draw_network_pattern(self, draw, colors):
        """Red de conexiones globales"""
        nodes = [(random.randint(100, self.width-100), 
                 random.randint(100, self.height-100)) for _ in range(20)]
        
        # Conexiones
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                if random.random() > 0.7:
                    color = random.choice(colors)
                    draw.line([node1, node2], fill=color, width=2)
        
        # Nodos
        for node in nodes:
            color = random.choice(colors)
            size = random.randint(10, 30)
            draw.ellipse([node[0]-size, node[1]-size, node[0]+size, node[1]+size], 
                        fill=color, outline=color)

    def generate_category_image(self, category, source_name, index):
        """Genera imagen para una categoría específica"""
        theme = self.CATEGORY_THEMES.get(category.lower(), self.CATEGORY_THEMES['default'])
        colors = theme['colors']
        
        # Crear imagen base con gradiente
        img = self.generate_gradient_background(colors[:2])
        
        # Crear capa para transparencia
        overlay = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Aplicar patrón según la categoría
        shape_style = random.choice(theme['shapes'])
        
        if 'circuit' in shape_style or 'grid' in shape_style:
            self.draw_circuit_pattern(draw, colors)
        elif 'wave' in shape_style or 'motion' in shape_style:
            self.draw_wave_pattern(draw, colors)
        elif 'particle' in shape_style or 'space' in shape_style:
            self.draw_particle_system(draw, colors)
        elif 'graph' in shape_style or 'chart' in shape_style:
            self.draw_graph_pattern(draw, colors)
        elif 'network' in shape_style or 'connection' in shape_style:
            self.draw_network_pattern(draw, colors)
        else:
            self.draw_geometric_shapes(draw, colors)
        
        # Combinar capas
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        
        # Aplicar blur sutil para efecto artístico
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        # Agregar texto decorativo (categoría)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except:
            font = ImageFont.load_default()
        
        # Texto con sombra
        category_text = category.upper()
        bbox = draw.textbbox((0, 0), category_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (self.width - text_width) // 2
        text_y = self.height // 2 - 50
        
        # Sombra
        draw.text((text_x + 4, text_y + 4), category_text, fill=(0, 0, 0, 128), font=font)
        # Texto principal
        draw.text((text_x, text_y), category_text, fill=(255, 255, 255, 200), font=font)
        
        # Guardar imagen
        filename = f"{category}_{source_name}_{index}.jpg"
        filepath = self.output_dir / filename
        img.save(filepath, 'JPEG', quality=85)
        
        return filepath

    def process_news_data(self, json_file):
        """Procesa el archivo de noticias y genera imágenes"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = data.get('results', [])
        generated_images = []
        
        print(f"\n🎨 Generando imágenes artísticas para {len(results)} fuentes de noticias...")
        print("=" * 70)
        
        for idx, source in enumerate(results, 1):
            source_id = source.get('id', f'source_{idx}')
            source_name = source.get('name', 'Unknown')
            categories = source.get('category', ['default'])
            
            # Generar imagen para la categoría principal
            primary_category = categories[0] if categories else 'default'
            
            print(f"\n[{idx}/{len(results)}] {source_name}")
            print(f"  📁 Categoría: {primary_category}")
            print(f"  🎨 Estilo: {self.CATEGORY_THEMES.get(primary_category, self.CATEGORY_THEMES['default'])['description']}")
            
            try:
                filepath = self.generate_category_image(primary_category, source_id, idx)
                generated_images.append({
                    'source': source_name,
                    'category': primary_category,
                    'file': str(filepath),
                    'id': source_id
                })
                print(f"  ✅ Generada: {filepath.name}")
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        print("\n" + "=" * 70)
        print(f"✨ Proceso completado: {len(generated_images)} imágenes generadas")
        print(f"📂 Directorio: {self.output_dir.absolute()}")
        
        # Guardar índice de imágenes
        index_file = self.output_dir / 'index.json'
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(generated_images, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Índice guardado: {index_file}")
        
        return generated_images


def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🎨 Generador de Imágenes Artísticas para Noticias       ║
    ║  Sin rostros ni personas - Solo arte conceptual          ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Verificar archivo de noticias
    news_file = Path('noticias.txt')
    if not news_file.exists():
        print(f"❌ Error: No se encontró el archivo {news_file}")
        sys.exit(1)
    
    # Generar imágenes
    generator = NewsImageGenerator()
    images = generator.process_news_data(news_file)
    
    print(f"\n🎉 ¡Listo! Generadas {len(images)} imágenes artísticas abstractas")
    print("\n💡 Categorías disponibles:")
    categories = set(img['category'] for img in images)
    for cat in sorted(categories):
        count = sum(1 for img in images if img['category'] == cat)
        print(f"   • {cat}: {count} imágenes")


if __name__ == '__main__':
    main()
