#!/usr/bin/env python3
"""
Generador de Familias de Fuentes para Templates CSS
Genera combinaciones de fuentes independientes que pueden combinarse con cualquier layout y paleta
"""

import random
from typing import Dict, List, Tuple


class FontFamilyGenerator:
    """Genera combinaciones de fuentes variadas para sitios de noticias"""
    
    # Combinaciones profesionales verificadas de sitios reales
    FONT_COMBINATIONS = [
        # 1. Radio M Style (Bebas Neue + Poppins)
        {
            "nombre": "radio_m_style",
            "descripcion": "Bebas Neue + Poppins (Radio M)",
            "primary": "'Bebas Neue', Impact, sans-serif",
            "secondary": "'Poppins', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap",
                "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap"
            ],
            "line_height": "1.7",
            "heading_weight": "400",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 2. Milenio Style (Source Serif + Source Sans)
        {
            "nombre": "milenio_style",
            "descripcion": "Source Serif + Sans (Milenio)",
            "primary": "'Source Serif Pro', serif",
            "secondary": "'Source Sans Pro', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;600;700;900&display=swap",
                "https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700;900&display=swap"
            ],
            "line_height": "1.6",
            "heading_weight": "700",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 3. Modern Professional (Montserrat + Roboto)
        {
            "nombre": "modern_professional",
            "descripcion": "Montserrat + Roboto moderno",
            "primary": "'Montserrat', sans-serif",
            "secondary": "'Roboto', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&display=swap",
                "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap"
            ],
            "line_height": "1.6",
            "heading_weight": "800",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 4. Elegant Editorial (Playfair + Poppins)
        {
            "nombre": "elegant_editorial",
            "descripcion": "Playfair Display + Poppins",
            "primary": "'Playfair Display', serif",
            "secondary": "'Poppins', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800;900&display=swap",
                "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
            ],
            "line_height": "1.7",
            "heading_weight": "900",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 5. Clásico Serif
        {
            "nombre": "classic_serif",
            "descripcion": "Serif clásico elegante",
            "primary": "'Merriweather', serif",
            "secondary": "'Open Sans', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Merriweather:wght@300;400;700;900&display=swap",
                "https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap"
            ],
            "line_height": "1.6",
            "heading_weight": "700",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 6. Moderno Sans
        {
            "nombre": "modern_sans",
            "descripcion": "Sans-serif moderno y limpio",
            "primary": "'Inter', sans-serif",
            "secondary": "'Source Serif Pro', serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap",
                "https://fonts.googleapis.com/css2?family=Source+Serif+Pro:wght@400;700&display=swap"
            ],
            "line_height": "1.6",
            "heading_weight": "800",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 7. Audaz Display
        {
            "nombre": "bold_display",
            "descripcion": "Display audaz y llamativo",
            "primary": "'Oswald', sans-serif",
            "secondary": "'PT Sans', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;600;700&display=swap",
                "https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&display=swap"
            ],
            "line_height": "1.55",
            "heading_weight": "700",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 8. Editorial Premium
        {
            "nombre": "editorial_premium",
            "descripcion": "Editorial de revista premium",
            "primary": "'Playfair Display', serif",
            "secondary": "'Lato', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&display=swap",
                "https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap"
            ],
            "line_height": "1.65",
            "heading_weight": "900",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 9. Tecnológico
        {
            "nombre": "tech_modern",
            "descripcion": "Tecnológico y futurista",
            "primary": "'Roboto', sans-serif",
            "secondary": "'Roboto Mono', monospace",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap",
                "https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap"
            ],
            "line_height": "1.5",
            "heading_weight": "900",
            "body_weight": "400",
            "menu_size": "12px",
            "menu_transform": "uppercase"
        },
        # 6. Minimalista
        {
            "nombre": "minimalist_clean",
            "descripcion": "Minimalista ultra limpio",
            "primary": "'Montserrat', sans-serif",
            "secondary": "'Crimson Text', serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap",
                "https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600;700&display=swap"
            ],
            "line_height": "1.7",
            "heading_weight": "800",
            "body_weight": "400"
        },
        # 7. Corporativo Profesional
        {
            "nombre": "corporate_professional",
            "descripcion": "Corporativo y profesional",
            "primary": "'Work Sans', sans-serif",
            "secondary": "'Spectral', serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;600;800&display=swap",
                "https://fonts.googleapis.com/css2?family=Spectral:wght@400;700&display=swap"
            ],
            "line_height": "1.6",
            "heading_weight": "800",
            "body_weight": "400"
        },
        # 8. Expresivo Condensado
        {
            "nombre": "expressive_condensed",
            "descripcion": "Condensado expresivo",
            "primary": "'Oswald', sans-serif",
            "secondary": "'PT Sans', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;600;700&display=swap",
                "https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&display=swap"
            ],
            "line_height": "1.55",
            "heading_weight": "700",
            "body_weight": "400"
        },
        # 9. Elegante Clásico
        {
            "nombre": "elegant_classic",
            "descripcion": "Elegancia clásica atemporal",
            "primary": "'Cormorant Garamond', serif",
            "secondary": "'Nunito', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&display=swap",
                "https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;800&display=swap"
            ],
            "line_height": "1.7",
            "heading_weight": "700",
            "body_weight": "400"
        },
        # 10. Geométrico Moderno
        {
            "nombre": "geometric_modern",
            "descripcion": "Geométrico moderno",
            "primary": "'Poppins', sans-serif",
            "secondary": "'Noto Serif', serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap",
                "https://fonts.googleapis.com/css2?family=Noto+Serif:wght@400;700&display=swap"
            ],
            "line_height": "1.6",
            "heading_weight": "800",
            "body_weight": "400"
        },
        # 11. Humanista
        {
            "nombre": "humanist_friendly",
            "descripcion": "Humanista y amigable",
            "primary": "'Source Sans Pro', sans-serif",
            "secondary": "'Libre Baskerville', serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;900&display=swap",
                "https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&display=swap"
            ],
            "line_height": "1.65",
            "heading_weight": "900",
            "body_weight": "400"
        },
        # 12. Dinámico Contraste
        {
            "nombre": "dynamic_contrast",
            "descripcion": "Contraste dinámico",
            "primary": "'Archivo Black', sans-serif",
            "secondary": "'Fira Sans', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap",
                "https://fonts.googleapis.com/css2?family=Fira+Sans:wght@300;400;600;700&display=swap"
            ],
            "line_height": "1.6",
            "heading_weight": "400",
            "body_weight": "400"
        },
        # 13. Refinado Editorial
        {
            "nombre": "refined_editorial",
            "descripcion": "Editorial refinado",
            "primary": "'Lora', serif",
            "secondary": "'Karla', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&display=swap",
                "https://fonts.googleapis.com/css2?family=Karla:wght@300;400;600;800&display=swap"
            ],
            "line_height": "1.7",
            "heading_weight": "700",
            "body_weight": "400"
        },
        # 14. Impactante Bold
        {
            "nombre": "impactful_bold",
            "descripcion": "Impacto visual bold",
            "primary": "'Anton', sans-serif",
            "secondary": "'Roboto Condensed', sans-serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Anton&display=swap",
                "https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@300;400;700&display=swap"
            ],
            "line_height": "1.5",
            "heading_weight": "400",
            "body_weight": "400"
        },
        # 15. Sofisticado
        {
            "nombre": "sophisticated_style",
            "descripcion": "Estilo sofisticado",
            "primary": "'Quicksand', sans-serif",
            "secondary": "'Eczar', serif",
            "imports": [
                "https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap",
                "https://fonts.googleapis.com/css2?family=Eczar:wght@400;700&display=swap"
            ],
            "line_height": "1.65",
            "heading_weight": "700",
            "body_weight": "400"
        }
    ]
    
    def __init__(self):
        """Inicializa el generador"""
        self.combinaciones_disponibles = self.FONT_COMBINATIONS.copy()
    
    def obtener_combinacion(self, index: int = None) -> Dict[str, any]:
        """
        Obtiene una combinación de fuentes por índice o aleatoria
        
        Args:
            index: Índice de la combinación (0-14), None para aleatoria
            
        Returns:
            dict: Combinación de fuentes
        """
        if index is not None:
            return self.FONT_COMBINATIONS[index % len(self.FONT_COMBINATIONS)]
        return random.choice(self.FONT_COMBINATIONS)
    
    def obtener_todas_las_combinaciones(self) -> List[Dict[str, any]]:
        """
        Obtiene todas las combinaciones disponibles
        
        Returns:
            list: Lista de todas las combinaciones
        """
        return self.FONT_COMBINATIONS.copy()
    
    def generar_css_imports(self, combinacion: Dict[str, any]) -> str:
        """
        Genera los imports CSS para las fuentes
        
        Args:
            combinacion: Diccionario con la combinación de fuentes
            
        Returns:
            str: CSS imports
        """
        css = ""
        for import_url in combinacion['imports']:
            css += f"@import url('{import_url}');\n"
        return css
    
    def generar_css_variables(self, combinacion: Dict[str, any]) -> str:
        """
        Genera CSS con variables de fuentes
        
        Args:
            combinacion: Diccionario con la combinación de fuentes
            
        Returns:
            str: CSS con variables
        """
        css = ":root {\n"
        css += f"    /* Fuentes: {combinacion['nombre']} - {combinacion['descripcion']} */\n"
        css += f"    --font-primary: {combinacion['primary']};\n"
        css += f"    --font-secondary: {combinacion['secondary']};\n"
        css += f"    --line-height: {combinacion['line_height']};\n"
        css += f"    --heading-weight: {combinacion['heading_weight']};\n"
        css += f"    --body-weight: {combinacion['body_weight']};\n"
        css += f"    --menu-size: {combinacion.get('menu_size', '12px')};\n"
        css += f"    --menu-transform: {combinacion.get('menu_transform', 'uppercase')};\n"
        css += "}\n"
        return css
    
    def generar_css_completo(self, combinacion: Dict[str, any]) -> str:
        """
        Genera CSS completo con imports y variables
        
        Args:
            combinacion: Diccionario con la combinación
            
        Returns:
            str: CSS completo
        """
        css = self.generar_css_imports(combinacion)
        css += "\n"
        css += self.generar_css_variables(combinacion)
        return css
    
    def generar_archivo_fuente(self, combinacion: Dict[str, any], output_path: str):
        """
        Genera un archivo CSS con una combinación específica
        
        Args:
            combinacion: Diccionario con la combinación
            output_path: Ruta del archivo de salida
        """
        css = self.generar_css_completo(combinacion)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(css)
    
    def generar_todas_las_fuentes_css(self, output_dir: str):
        """
        Genera archivos CSS para todas las combinaciones de fuentes
        
        Args:
            output_dir: Directorio de salida
        """
        from pathlib import Path
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for i, combinacion in enumerate(self.FONT_COMBINATIONS, 1):
            filename = f"fonts_{i:02d}_{combinacion['nombre']}.css"
            output_path = f"{output_dir}/{filename}"
            self.generar_archivo_fuente(combinacion, output_path)
            print(f"✅ Generada combinación {i}: {combinacion['nombre']}")
    
    def obtener_info_combinaciones(self) -> str:
        """
        Genera información legible de todas las combinaciones
        
        Returns:
            str: Descripción de todas las combinaciones
        """
        info = "🔤 Combinaciones de Fuentes Disponibles\n"
        info += "=" * 70 + "\n\n"
        
        for i, comb in enumerate(self.FONT_COMBINATIONS, 1):
            info += f"{i:2d}. {comb['nombre']:30s} - {comb['descripcion']}\n"
            info += f"    Primary: {comb['primary']:40s}\n"
            info += f"    Secondary: {comb['secondary']}\n"
        
        return info


def main():
    """Función de prueba"""
    print("🔤 Generador de Familias de Fuentes CSS")
    print("=" * 70)
    
    generator = FontFamilyGenerator()
    
    # Mostrar información de combinaciones
    print(generator.obtener_info_combinaciones())
    
    # Ejemplo de generación de CSS
    print("\n📝 Ejemplo de CSS generado para una combinación:\n")
    combinacion = generator.obtener_combinacion(0)
    print(generator.generar_css_completo(combinacion))
    
    # Generar todas las combinaciones
    output_dir = Path(__file__).resolve().parents[2] / "content" / "templates" / "css" / "fonts"
    print(f"\n💾 Generando archivos CSS en {output_dir}...\n")
    generator.generar_todas_las_fuentes_css(output_dir)
    
    print(f"\n✅ Se generaron {len(generator.FONT_COMBINATIONS)} archivos de fuentes")
    print(f"📂 Ubicación: {output_dir}/")


if __name__ == "__main__":
    main()
