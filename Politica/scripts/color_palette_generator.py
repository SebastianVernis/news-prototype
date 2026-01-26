#!/usr/bin/env python3
"""
Generador de Paletas de Colores para Templates CSS
Genera múltiples esquemas de color independientes que pueden combinarse con cualquier layout
"""

import random
from typing import Dict, List


class ColorPaletteGenerator:
    """Genera paletas de colores variadas para sitios de noticias"""
    
    # Paletas profesionales verificadas de sitios reales
    PALETAS = [
        # 1. Milenio Style (Rojo característico)
        {
            "nombre": "milenio_rojo",
            "descripcion": "Rojo Milenio profesional",
            "primary": "#B10B1F",
            "secondary": "#F1F1F1",
            "accent": "#D1D1D1",
            "background": "#FFFFFF",
            "background_2": "#EDEDED",
            "text": "#202124",
            "light_text": "#999999",
            "urgent": "#FDE636",
            "card_bg": "#FFFFFF"
        },
        # 2. Radio M Style (Azul moderno)
        {
            "nombre": "radio_m_azul",
            "descripcion": "Azul Radio M moderno",
            "primary": "#3D55EF",
            "secondary": "#F7F9F8",
            "accent": "#0693E3",
            "background": "#FFFFFF",
            "background_2": "#EFEFEF",
            "text": "#202124",
            "light_text": "#999999",
            "urgent": "#CF2E2E",
            "card_bg": "#FFFFFF"
        },
        # 3. Sobrio Corporativo
        {
            "nombre": "sobrio_corporativo",
            "descripcion": "Negro corporativo profesional",
            "primary": "#1C1C1C",
            "secondary": "#F5F5F5",
            "accent": "#3D55EF",
            "background": "#FFFFFF",
            "background_2": "#F7F9F8",
            "text": "#161617",
            "light_text": "#999999",
            "urgent": "#FF6900",
            "card_bg": "#FFFFFF"
        },
        # 4. Periodístico Clásico
        {
            "nombre": "periodistico_clasico",
            "descripcion": "Negro clásico tradicional",
            "primary": "#000000",
            "secondary": "#EFEFEF",
            "accent": "#CF2E2E",
            "background": "#FFFFFF",
            "background_2": "#F7F9F8",
            "text": "#333333",
            "light_text": "#666666",
            "urgent": "#FDE636",
            "card_bg": "#FAFAFA"
        },
        # 5. Profesional Azul
        {
            "nombre": "professional_blue",
            "descripcion": "Azul profesional corporativo",
            "primary": "#2C3E50",
            "secondary": "#3498DB",
            "accent": "#E74C3C",
            "background": "#ECF0F1",
            "background_2": "#FFFFFF",
            "text": "#2C3E50",
            "light_text": "#7F8C8D",
            "urgent": "#E74C3C",
            "card_bg": "#FFFFFF"
        },
        # 6. Clásico Rojo-Negro
        {
            "nombre": "classic_red_black",
            "descripcion": "Clásico periodístico rojo y negro",
            "primary": "#1A1A1A",
            "secondary": "#C0392B",
            "accent": "#E67E22",
            "background": "#FFFFFF",
            "background_2": "#F8F9FA",
            "text": "#2C3E50",
            "light_text": "#7F8C8D",
            "urgent": "#C0392B",
            "card_bg": "#F8F9FA"
        },
        # 7. Moderno Verde
        {
            "nombre": "modern_green",
            "descripcion": "Verde moderno y fresco",
            "primary": "#2D6A4F",
            "secondary": "#52B788",
            "accent": "#95D5B2",
            "background": "#F1FAEE",
            "background_2": "#FFFFFF",
            "text": "#1B4332",
            "light_text": "#74C69D",
            "urgent": "#E74C3C",
            "card_bg": "#FFFFFF"
        },
        # 8. Elegante Púrpura
        {
            "nombre": "elegant_purple",
            "descripcion": "Púrpura elegante y sofisticado",
            "primary": "#8E44AD",
            "secondary": "#9B59B6",
            "accent": "#E74C3C",
            "background": "#F8F9FA",
            "background_2": "#FFFFFF",
            "text": "#2C3E50",
            "light_text": "#A569BD",
            "urgent": "#E74C3C",
            "card_bg": "#FFFFFF"
        },
        # 9. Corporativo Azul Oscuro
        {
            "nombre": "corporate_dark_blue",
            "descripcion": "Azul oscuro corporativo",
            "primary": "#34495E",
            "secondary": "#2980B9",
            "accent": "#E67E22",
            "background": "#ECF0F1",
            "background_2": "#FFFFFF",
            "text": "#2C3E50",
            "light_text": "#95A5A6",
            "urgent": "#E67E22",
            "card_bg": "#FFFFFF"
        },
        # 10. Minimalista Gris
        {
            "nombre": "minimalist_gray",
            "descripcion": "Gris minimalista neutro",
            "primary": "#4A4A4A",
            "secondary": "#7F8C8D",
            "accent": "#E74C3C",
            "background": "#FFFFFF",
            "background_2": "#F8F9FA",
            "text": "#2C3E50",
            "light_text": "#95A5A6",
            "urgent": "#E74C3C",
            "card_bg": "#F8F9FA"
        },
        # 11. Vibrante Naranja
        {
            "nombre": "vibrant_orange",
            "descripcion": "Naranja vibrante y enérgico",
            "primary": "#FF6F00",
            "secondary": "#FFA726",
            "accent": "#FFD54F",
            "background": "#FFF8E1",
            "background_2": "#FFFFFF",
            "text": "#E65100",
            "light_text": "#FF8A50",
            "urgent": "#FF6F00",
            "card_bg": "#FFFFFF"
        },
        # 8. Tecnológico Cyan
        {
            "nombre": "tech_cyan",
            "descripcion": "Cyan tecnológico futurista",
            "primary": "#00ACC1",
            "secondary": "#26C6DA",
            "accent": "#FF6F00",
            "background": "#E0F7FA",
            "text": "#006064",
            "light_text": "#4DD0E1",
            "card_bg": "#FFFFFF"
        },
        # 9. Serio Marino
        {
            "nombre": "navy_serious",
            "descripcion": "Azul marino serio y confiable",
            "primary": "#1A237E",
            "secondary": "#303F9F",
            "accent": "#FF5252",
            "background": "#E8EAF6",
            "text": "#1A237E",
            "light_text": "#5C6BC0",
            "card_bg": "#FFFFFF"
        },
        # 10. Cálido Terracota
        {
            "nombre": "warm_terracotta",
            "descripcion": "Terracota cálido y acogedor",
            "primary": "#BF360C",
            "secondary": "#FF6E40",
            "accent": "#FFD180",
            "background": "#FFF3E0",
            "text": "#4E342E",
            "light_text": "#FF8A65",
            "card_bg": "#FFFFFF"
        },
        # 11. Fresco Turquesa
        {
            "nombre": "fresh_turquoise",
            "descripcion": "Turquesa fresco y limpio",
            "primary": "#00897B",
            "secondary": "#26A69A",
            "accent": "#FFB300",
            "background": "#E0F2F1",
            "text": "#004D40",
            "light_text": "#4DB6AC",
            "card_bg": "#FFFFFF"
        },
        # 12. Intenso Magenta
        {
            "nombre": "intense_magenta",
            "descripcion": "Magenta intenso y audaz",
            "primary": "#AD1457",
            "secondary": "#EC407A",
            "accent": "#FFA726",
            "background": "#FCE4EC",
            "text": "#880E4F",
            "light_text": "#F06292",
            "card_bg": "#FFFFFF"
        },
        # 13. Sobrio Carbón
        {
            "nombre": "sober_charcoal",
            "descripcion": "Carbón sobrio y profesional",
            "primary": "#263238",
            "secondary": "#455A64",
            "accent": "#FF5722",
            "background": "#ECEFF1",
            "text": "#263238",
            "light_text": "#78909C",
            "card_bg": "#FFFFFF"
        },
        # 14. Brillante Amarillo
        {
            "nombre": "bright_yellow",
            "descripcion": "Amarillo brillante y optimista",
            "primary": "#F57F17",
            "secondary": "#FBC02D",
            "accent": "#0288D1",
            "background": "#FFFDE7",
            "text": "#F57F17",
            "light_text": "#FDD835",
            "card_bg": "#FFFFFF"
        },
        # 15. Místico Índigo
        {
            "nombre": "mystic_indigo",
            "descripcion": "Índigo místico y profundo",
            "primary": "#311B92",
            "secondary": "#512DA8",
            "accent": "#FFA000",
            "background": "#EDE7F6",
            "text": "#311B92",
            "light_text": "#7E57C2",
            "card_bg": "#FFFFFF"
        },
        # 16. Natural Verde Oliva
        {
            "nombre": "natural_olive",
            "descripcion": "Verde oliva natural",
            "primary": "#827717",
            "secondary": "#AFB42B",
            "accent": "#FF6F00",
            "background": "#F9FBE7",
            "text": "#827717",
            "light_text": "#C0CA33",
            "card_bg": "#FFFFFF"
        },
        # 17. Enérgico Rojo
        {
            "nombre": "energetic_red",
            "descripcion": "Rojo enérgico y llamativo",
            "primary": "#C62828",
            "secondary": "#E53935",
            "accent": "#FFA726",
            "background": "#FFEBEE",
            "text": "#B71C1C",
            "light_text": "#EF5350",
            "card_bg": "#FFFFFF"
        },
        # 18. Suave Rosa
        {
            "nombre": "soft_pink",
            "descripcion": "Rosa suave y moderno",
            "primary": "#C2185B",
            "secondary": "#E91E63",
            "accent": "#9C27B0",
            "background": "#FCE4EC",
            "text": "#880E4F",
            "light_text": "#F06292",
            "card_bg": "#FFFFFF"
        },
        # 19. Profundo Azul Noche
        {
            "nombre": "deep_night_blue",
            "descripcion": "Azul noche profundo",
            "primary": "#0D47A1",
            "secondary": "#1976D2",
            "accent": "#FFC107",
            "background": "#E3F2FD",
            "text": "#01579B",
            "light_text": "#42A5F5",
            "card_bg": "#FFFFFF"
        },
        # 20. Refrescante Menta
        {
            "nombre": "refreshing_mint",
            "descripcion": "Menta refrescante",
            "primary": "#00695C",
            "secondary": "#00897B",
            "accent": "#FF6F00",
            "background": "#E0F2F1",
            "text": "#004D40",
            "light_text": "#26A69A",
            "card_bg": "#FFFFFF"
        }
    ]
    
    def __init__(self):
        """Inicializa el generador"""
        self.paletas_disponibles = self.PALETAS.copy()
    
    def obtener_paleta(self, index: int = None) -> Dict[str, str]:
        """
        Obtiene una paleta por índice o aleatoria
        
        Args:
            index: Índice de la paleta (0-19), None para aleatoria
            
        Returns:
            dict: Paleta de colores
        """
        if index is not None:
            return self.PALETAS[index % len(self.PALETAS)]
        return random.choice(self.PALETAS)
    
    def obtener_todas_las_paletas(self) -> List[Dict[str, str]]:
        """
        Obtiene todas las paletas disponibles
        
        Returns:
            list: Lista de todas las paletas
        """
        return self.PALETAS.copy()
    
    def generar_css_variables(self, paleta: Dict[str, str]) -> str:
        """
        Genera CSS con variables de la paleta
        
        Args:
            paleta: Diccionario con la paleta de colores
            
        Returns:
            str: CSS con variables
        """
        css = ":root {\n"
        css += f"    /* Paleta: {paleta['nombre']} - {paleta['descripcion']} */\n"
        css += f"    --primary-color: {paleta['primary']};\n"
        css += f"    --secondary-color: {paleta['secondary']};\n"
        css += f"    --accent-color: {paleta['accent']};\n"
        css += f"    --background-color: {paleta['background']};\n"
        css += f"    --background-color-2: {paleta.get('background_2', paleta['background'])};\n"
        css += f"    --text-color: {paleta['text']};\n"
        css += f"    --light-text: {paleta['light_text']};\n"
        css += f"    --urgent-color: {paleta.get('urgent', paleta['accent'])};\n"
        css += f"    --card-bg: {paleta['card_bg']};\n"
        css += "}\n"
        return css
    
    def generar_archivo_paleta(self, paleta: Dict[str, str], output_path: str):
        """
        Genera un archivo CSS con una paleta específica
        
        Args:
            paleta: Diccionario con la paleta
            output_path: Ruta del archivo de salida
        """
        css = self.generar_css_variables(paleta)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(css)
    
    def generar_todas_las_paletas_css(self, output_dir: str):
        """
        Genera archivos CSS para todas las paletas
        
        Args:
            output_dir: Directorio de salida
        """
        from pathlib import Path
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for i, paleta in enumerate(self.PALETAS, 1):
            filename = f"palette_{i:02d}_{paleta['nombre']}.css"
            output_path = f"{output_dir}/{filename}"
            self.generar_archivo_paleta(paleta, output_path)
            print(f"✅ Generada paleta {i}: {paleta['nombre']}")
    
    def obtener_info_paletas(self) -> str:
        """
        Genera información legible de todas las paletas
        
        Returns:
            str: Descripción de todas las paletas
        """
        info = "📊 Paletas de Colores Disponibles\n"
        info += "=" * 70 + "\n\n"
        
        for i, paleta in enumerate(self.PALETAS, 1):
            info += f"{i:2d}. {paleta['nombre']:25s} - {paleta['descripcion']}\n"
            info += f"    Primary: {paleta['primary']:8s}  Secondary: {paleta['secondary']:8s}  Accent: {paleta['accent']}\n"
        
        return info


def main():
    """Función de prueba"""
    print("🎨 Generador de Paletas de Colores CSS")
    print("=" * 70)
    
    generator = ColorPaletteGenerator()
    
    # Mostrar información de paletas
    print(generator.obtener_info_paletas())
    
    # Ejemplo de generación de CSS
    print("\n📝 Ejemplo de CSS generado para una paleta:\n")
    paleta = generator.obtener_paleta(0)
    print(generator.generar_css_variables(paleta))
    
    # Generar todas las paletas
    output_dir = "../templates/css/palettes"
    print(f"\n💾 Generando archivos CSS en {output_dir}...\n")
    generator.generar_todas_las_paletas_css(output_dir)
    
    print(f"\n✅ Se generaron {len(generator.PALETAS)} archivos de paletas")
    print(f"📂 Ubicación: {output_dir}/")


if __name__ == "__main__":
    main()
