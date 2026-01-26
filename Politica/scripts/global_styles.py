#!/usr/bin/env python3
"""
Estilos Globales para Todos los Layouts
Incluye ocultamiento de scrollbars y estilos base
"""


class GlobalStyles:
    """Genera estilos globales para aplicar a todos los layouts"""
    
    @staticmethod
    def get_scrollbar_hidden_css() -> str:
        """
        CSS para ocultar scrollbars pero mantener funcionalidad de scroll
        Compatible con todos los navegadores
        """
        return '''
/* Ocultar scrollbars en todos los navegadores */

/* Firefox */
* {
    scrollbar-width: none;
}

/* Chrome, Safari, Edge, Opera */
*::-webkit-scrollbar {
    display: none;
    width: 0;
    height: 0;
}

/* Internet Explorer y Edge Legacy */
* {
    -ms-overflow-style: none;
}

/* Asegurar que el scroll funcione */
html {
    overflow-y: scroll;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

html::-webkit-scrollbar {
    display: none;
}

body {
    overflow-x: hidden;
}

/* Para elementos con overflow */
.sidebar-content,
.main-nav,
.dropdown-menu,
.ticker-content,
.carousel-track,
nav,
aside,
.sidebar-header {
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.sidebar-content::-webkit-scrollbar,
.main-nav::-webkit-scrollbar,
.dropdown-menu::-webkit-scrollbar,
.ticker-content::-webkit-scrollbar,
.carousel-track::-webkit-scrollbar,
nav::-webkit-scrollbar,
aside::-webkit-scrollbar,
.sidebar-header::-webkit-scrollbar {
    display: none;
    width: 0;
    height: 0;
}
'''
    
    @staticmethod
    def get_smooth_scroll_css() -> str:
        """CSS para scroll suave"""
        return '''
/* Scroll suave */
html {
    scroll-behavior: smooth;
}

/* Scroll snap para carruseles (opcional) */
.carousel-container {
    scroll-snap-type: x mandatory;
}

.carousel-slide {
    scroll-snap-align: start;
}
'''
    
    @staticmethod
    def get_base_reset_css() -> str:
        """Reset CSS base para consistencia"""
        return '''
/* Reset y Base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    width: 100%;
    height: 100%;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    line-height: 1.6;
    color: #2c3e50;
    background: #f5f7fa;
}

a {
    text-decoration: none;
    color: inherit;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
}

button {
    font-family: inherit;
}
'''
    
    @staticmethod
    def get_complete_global_styles() -> str:
        """
        Retorna todos los estilos globales combinados
        Para insertar en el <head> de cada página
        """
        return f'''
<style>
{GlobalStyles.get_base_reset_css()}
{GlobalStyles.get_scrollbar_hidden_css()}
{GlobalStyles.get_smooth_scroll_css()}
</style>
'''
    
    @staticmethod
    def inject_global_styles(html: str) -> str:
        """
        Inyecta estilos globales en un HTML existente
        
        Args:
            html: HTML completo
            
        Returns:
            HTML con estilos globales inyectados
        """
        global_styles = GlobalStyles.get_complete_global_styles()
        
        # Inyectar después de <head>
        if '<head>' in html:
            html = html.replace('<head>', f'<head>\n{global_styles}', 1)
        
        return html


def main():
    """Demo de estilos globales"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║        🎨 ESTILOS GLOBALES - SCROLLBARS OCULTAS                     ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Crear demo
    demo_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Demo - Scrollbars Ocultas</title>
</head>
<body>
    <div style="max-width: 800px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 8px;">
        <h1>Demo de Scrollbars Ocultas</h1>
        <p style="margin: 1rem 0; color: #6c757d;">
            Esta página tiene scroll funcional pero las barras están ocultas.
            Funciona en todos los navegadores.
        </p>
        
        <div style="height: 200px; overflow-y: auto; border: 1px solid #ddd; padding: 1rem; margin: 2rem 0;">
            <h3>Contenedor con scroll (barra oculta)</h3>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            <p>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco.</p>
            <p>Duis aute irure dolor in reprehenderit in voluptate velit esse.</p>
            <p>Excepteur sint occaecat cupidatat non proident, sunt in culpa.</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            <p>Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            <p>Ut enim ad minim veniam, quis nostrud exercitation ullamco.</p>
        </div>
        
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 6px;">
            <h3>✅ Scrollbars ocultas en:</h3>
            <ul style="margin-top: 1rem; list-style-position: inside; color: #495057;">
                <li>Todo el documento (html, body)</li>
                <li>Sidebars y menús</li>
                <li>Carruseles y tickers</li>
                <li>Dropdowns</li>
                <li>Cualquier elemento con overflow</li>
            </ul>
            
            <p style="margin-top: 1rem; color: #6c757d; font-size: 0.9rem;">
                Compatible con: Chrome, Firefox, Safari, Edge, Opera
            </p>
        </div>
    </div>
</body>
</html>'''
    
    # Inyectar estilos globales
    demo_html = GlobalStyles.inject_global_styles(demo_html)
    
    # Guardar
    with open('demo/global_styles_demo.html', 'w', encoding='utf-8') as f:
        f.write(demo_html)
    
    print("✅ Demo generado: demo/global_styles_demo.html")
    print("\n🌐 Ver en: http://localhost:8006/demo/global_styles_demo.html")
    print("\n💡 Scrollea la página y el contenedor - las barras están ocultas")
    print("   pero el scroll funciona perfectamente.")


if __name__ == '__main__':
    main()
