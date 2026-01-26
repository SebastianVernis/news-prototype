#!/usr/bin/env python3
"""
Generador de Logos SVG sin IA
Crea logos profesionales usando SVG, tipografía y formas geométricas
"""

import os
import random
from pathlib import Path

class LogoGeneratorSVG:
    def __init__(self, assets_dir: str = None):
        self.assets_dir = Path(assets_dir) if assets_dir else Path(__file__).parent.parent / "assets"
        self.svg_icons_dir = self.assets_dir / "svg-icons"
        
        # Biblioteca de fuentes profesionales
        self.fonts = {
            "display": ["Bebas Neue", "Montserrat", "Oswald", "Anton", "Archivo Black"],
            "modern": ["Poppins", "Inter", "Roboto", "Work Sans"],
            "classic": ["Playfair Display", "Merriweather", "Source Serif Pro"],
            "geometric": ["Raleway", "Quicksand", "Comfortaa"]
        }
        
        # Iconos disponibles
        self.icons = {
            "news": ["newspaper", "microphone", "camera", "video", "globe", "trending"],
            "shapes": ["circle", "hexagon", "badge", "square", "shield"],
            "political": ["flag", "capitol", "ballot"]
        }
    
    def get_initials(self, site_name: str, max_chars: int = 3) -> str:
        """Extrae iniciales del nombre del sitio"""
        words = [w for w in site_name.split() if len(w) > 0]
        initials = ''.join([word[0].upper() for word in words[:max_chars]])
        return initials
    
    def generate_typographic_logo(self, site_name: str, color_primary: str, 
                                   font_style: str = "display") -> str:
        """Genera logo puramente tipográfico (solo texto)"""
        font = random.choice(self.fonts.get(font_style, self.fonts["display"]))
        
        # Determinar si usar nombre completo o iniciales
        use_full = len(site_name) <= 20
        text = site_name.upper() if use_full else self.get_initials(site_name)
        
        font_size = 48 if use_full else 80
        viewbox_width = len(text) * (font_size * 0.6) if use_full else 200
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewbox_width} 100" width="{viewbox_width}" height="100">
    <text x="50%" y="70" 
          font-family="{font}, sans-serif" 
          font-size="{font_size}"
          font-weight="900"
          text-anchor="middle"
          fill="{color_primary}">
        {text}
    </text>
</svg>'''
    
    def generate_badge_logo(self, site_name: str, color_primary: str, 
                           color_secondary: str = "#FFFFFF") -> str:
        """Genera logo tipo badge circular con iniciales"""
        initials = self.get_initials(site_name, 3)
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
    <!-- Círculo de fondo -->
    <circle cx="100" cy="100" r="90" fill="{color_primary}"/>
    
    <!-- Iniciales -->
    <text x="100" y="130" 
          font-family="Bebas Neue, Impact, sans-serif" 
          font-size="80"
          font-weight="bold"
          text-anchor="middle"
          fill="{color_secondary}">
        {initials}
    </text>
</svg>'''
    
    def generate_icon_text_logo(self, site_name: str, color_primary: str, 
                                icon_category: str = "news") -> str:
        """Genera logo combinando icono SVG + texto"""
        # Seleccionar icono aleatorio de la categoría
        available_icons = self.icons.get(icon_category, self.icons["news"])
        icon_name = random.choice(available_icons)
        
        # Intentar cargar el icono SVG
        icon_path = self.svg_icons_dir / icon_category / f"{icon_name}.svg"
        icon_svg_content = ""
        
        if icon_path.exists():
            with open(icon_path, 'r', encoding='utf-8') as f:
                icon_content = f.read()
                # Extraer solo el path del SVG
                if '<path' in icon_content:
                    start = icon_content.find('<path')
                    end = icon_content.find('/>', start) + 2
                    icon_svg_content = icon_content[start:end]
        
        # Nombre corto para el logo
        short_name = site_name[:15].upper() if len(site_name) > 15 else site_name.upper()
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 80" width="300" height="80">
    <!-- Icono -->
    <g transform="translate(10, 15) scale(2)">
        {icon_svg_content if icon_svg_content else '<circle cx="20" cy="20" r="15" fill="' + color_primary + '"/>'}
    </g>
    
    <!-- Texto -->
    <text x="80" y="55" 
          font-family="Bebas Neue, sans-serif" 
          font-size="36"
          font-weight="bold"
          fill="{color_primary}">
        {short_name}
    </text>
</svg>'''
    
    def generate_geometric_logo(self, site_name: str, color_primary: str, 
                               shape: str = "hexagon") -> str:
        """Genera logo geométrico con iniciales"""
        initials = self.get_initials(site_name, 2)
        
        # Cargar forma geométrica
        shape_path = self.svg_icons_dir / "shapes" / f"{shape}.svg"
        shape_svg = ""
        
        if shape_path.exists():
            with open(shape_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '<circle' in content or '<polygon' in content or '<path' in content:
                    start = content.find('<', content.find('viewBox'))
                    start = content.find('<', start + 1)
                    end = content.rfind('</svg>')
                    shape_svg = content[start:end]
        else:
            shape_svg = f'<circle cx="50" cy="50" r="45" fill="{color_primary}"/>'
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="200" height="200">
    {shape_svg.replace('fill="currentColor"', f'fill="{color_primary}"')}
    
    <!-- Iniciales -->
    <text x="50" y="70" 
          font-family="Bebas Neue, Impact, sans-serif" 
          font-size="40"
          font-weight="bold"
          text-anchor="middle"
          fill="white">
        {initials}
    </text>
</svg>'''
    
    def generate_stacked_logo(self, site_name: str, tagline: str, color_primary: str) -> str:
        """Genera logo con nombre y tagline apilados"""
        words = site_name.split()
        line1 = " ".join(words[:2]) if len(words) > 2 else site_name
        line2 = " ".join(words[2:]) if len(words) > 2 else tagline
        
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 120" width="300" height="120">
    <!-- Nombre principal -->
    <text x="150" y="50" 
          font-family="Bebas Neue, sans-serif" 
          font-size="42"
          font-weight="900"
          text-anchor="middle"
          fill="{color_primary}">
        {line1.upper()}
    </text>
    
    <!-- Tagline o segunda línea -->
    <text x="150" y="85" 
          font-family="Poppins, sans-serif" 
          font-size="14"
          font-weight="600"
          text-anchor="middle"
          fill="#666666"
          letter-spacing="2">
        {line2.upper()}
    </text>
    
    <!-- Línea decorativa -->
    <line x1="70" y1="65" x2="230" y2="65" 
          stroke="{color_primary}" 
          stroke-width="2"/>
</svg>'''
    
    def generate_logo(self, site_name: str, colors: dict, style: str = "auto") -> tuple:
        """
        Genera logo SVG según estilo especificado
        
        Retorna: (svg_content, logo_type, font_used)
        """
        color_primary = colors.get("primary", "#000000")
        color_secondary = colors.get("secondary", "#FFFFFF")
        
        # Determinar estilo automáticamente si es "auto"
        if style == "auto":
            styles = ["badge", "icon_text", "typographic", "geometric"]
            style = random.choice(styles)
        
        # Generar según estilo
        if style == "badge":
            svg = self.generate_badge_logo(site_name, color_primary, color_secondary)
            logo_type = "badge_circle"
            font = "Bebas Neue"
            
        elif style == "icon_text":
            svg = self.generate_icon_text_logo(site_name, color_primary)
            logo_type = "icon_text"
            font = "Bebas Neue"
            
        elif style == "geometric":
            shapes = ["hexagon", "circle", "badge", "shield"]
            shape = random.choice(shapes)
            svg = self.generate_geometric_logo(site_name, color_primary, shape)
            logo_type = f"geometric_{shape}"
            font = "Bebas Neue"
            
        elif style == "stacked":
            tagline = "Noticias y Análisis"
            svg = self.generate_stacked_logo(site_name, tagline, color_primary)
            logo_type = "stacked"
            font = "Bebas Neue + Poppins"
            
        else:  # typographic
            font_style = random.choice(["display", "modern", "classic"])
            svg = self.generate_typographic_logo(site_name, color_primary, font_style)
            logo_type = f"typographic_{font_style}"
            font = random.choice(self.fonts[font_style])
        
        return svg, logo_type, font
    
    def save_logo(self, svg_content: str, output_path: str) -> str:
        """Guarda logo SVG a archivo"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        return str(output_file)
    
    def generate_and_save(self, site_name: str, colors: dict, 
                         output_dir: str, style: str = "auto") -> dict:
        """Genera logo y guarda en directorio de salida"""
        svg_content, logo_type, font_used = self.generate_logo(site_name, colors, style)
        
        # Guardar SVG
        output_path = Path(output_dir) / "logo.svg"
        logo_path = self.save_logo(svg_content, output_path)
        
        # También crear versión PNG usando embedded SVG
        # (Los navegadores pueden cargar SVG directamente, no necesitamos conversión)
        
        return {
            "logo_path": logo_path,
            "logo_type": logo_type,
            "font_used": font_used,
            "format": "svg",
            "fallback_available": True
        }


def generar_logo_svg(site_name: str, output_dir: str, colors: dict = None, 
                    style: str = "auto") -> dict:
    """
    Función wrapper para fácil integración con flujo existente
    
    Args:
        site_name: Nombre del sitio
        output_dir: Directorio donde guardar el logo
        colors: Dict con 'primary' y 'secondary'
        style: Tipo de logo (auto, badge, icon_text, typographic, geometric, stacked)
    
    Returns:
        Dict con info del logo generado
    """
    if colors is None:
        colors = {"primary": "#B10B1F", "secondary": "#FFFFFF"}
    
    generator = LogoGeneratorSVG()
    result = generator.generate_and_save(site_name, colors, output_dir, style)
    
    print(f"✅ Logo SVG generado: {result['logo_type']}")
    print(f"   Fuente: {result['font_used']}")
    print(f"   Archivo: {result['logo_path']}")
    
    return result


if __name__ == "__main__":
    # Pruebas
    test_dir = Path(__file__).parent.parent / "test_logos"
    test_dir.mkdir(exist_ok=True)
    
    test_sites = [
        ("Noticias Hoy", {"primary": "#B10B1F", "secondary": "#FFFFFF"}),
        ("El Diario", {"primary": "#3D55EF", "secondary": "#F7F9F8"}),
        ("Política MX", {"primary": "#1C1C1C", "secondary": "#F5F5F5"}),
        ("Radio Información", {"primary": "#000000", "secondary": "#EFEFEF"})
    ]
    
    generator = LogoGeneratorSVG()
    
    for i, (name, colors) in enumerate(test_sites, 1):
        style = ["badge", "icon_text", "typographic", "geometric"][i % 4]
        output = test_dir / f"test_{i}"
        
        result = generator.generate_and_save(name, colors, output, style)
        print(f"\n{i}. {name} - {result['logo_type']}")
        print(f"   → {result['logo_path']}")
