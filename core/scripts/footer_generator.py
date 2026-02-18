#!/usr/bin/env python3
"""
Generador Modular de Footers para Sitios de Noticias
Crea componentes de footer con diferentes estilos y variaciones
"""

import random
from typing import Dict, List, Optional
from datetime import datetime


class FooterGenerator:
    """Generador de componentes de footer dinámicos"""
    
    # Estilos de footer disponibles
    FOOTER_STYLES = {
        "classic_4col": {
            "name": "Clásico 4 Columnas",
            "description": "Footer tradicional con 4 columnas de contenido",
            "columns": 4,
            "classes": "footer-classic cols-4"
        },
        "modern_3col": {
            "name": "Moderno 3 Columnas",
            "description": "Footer moderno con 3 columnas balanceadas",
            "columns": 3,
            "classes": "footer-modern cols-3"
        },
        "minimal_2col": {
            "name": "Minimal 2 Columnas",
            "description": "Footer minimalista con 2 columnas",
            "columns": 2,
            "classes": "footer-minimal cols-2"
        },
        "centered": {
            "name": "Centrado",
            "description": "Footer con contenido centrado",
            "columns": 1,
            "classes": "footer-centered"
        },
        "mega_footer": {
            "name": "Mega Footer",
            "description": "Footer extenso con múltiples secciones",
            "columns": 5,
            "classes": "footer-mega cols-5"
        },
        "newsletter_focus": {
            "name": "Enfoque Newsletter",
            "description": "Footer destacando suscripción a newsletter",
            "columns": 3,
            "classes": "footer-newsletter cols-3"
        },
        "social_focus": {
            "name": "Enfoque Social",
            "description": "Footer destacando redes sociales",
            "columns": 3,
            "classes": "footer-social cols-3"
        },
        "compact": {
            "name": "Compacto",
            "description": "Footer compacto de una sola línea",
            "columns": 1,
            "classes": "footer-compact"
        },
        "split": {
            "name": "Dividido",
            "description": "Footer dividido en secciones visuales",
            "columns": 2,
            "classes": "footer-split cols-2"
        },
        "boxed": {
            "name": "En Caja",
            "description": "Footer contenido en una caja",
            "columns": 3,
            "classes": "footer-boxed cols-3"
        }
    }
    
    # Secciones disponibles para footer
    FOOTER_SECTIONS = {
        "about": {
            "title": "Acerca de Nosotros",
            "content_type": "text",
            "include_social": True
        },
        "sections": {
            "title": "Secciones",
            "content_type": "links",
            "links": ["Inicio", "Política", "Entretenimiento", "Tecnología", "Mundial", "Deportes", "Negocios"]
        },
        "legal": {
            "title": "Legal",
            "content_type": "legal_links",
            "links": [
                {"text": "Términos de Uso", "url": "terminos.html"},
                {"text": "Política de Privacidad", "url": "privacidad.html"},
                {"text": "FAQs", "url": "faqs.html"},
                {"text": "Acerca de Nosotros", "url": "acerca.html"}
            ]
        },
        "contact": {
            "title": "Contacto",
            "content_type": "contact_info"
        },
        "newsletter": {
            "title": "Boletín",
            "content_type": "newsletter_form"
        },
        "recent_posts": {
            "title": "Artículos Recientes",
            "content_type": "links",
            "dynamic": True
        },
        "categories": {
            "title": "Categorías",
            "content_type": "links",
            "links": ["Nacional", "Internacional", "Economía", "Cultura"]
        },
        "services": {
            "title": "Servicios",
            "content_type": "links",
            "links": ["Publicidad", "RSS", "API", "Prensa"]
        },
        "apps": {
            "title": "Aplicaciones",
            "content_type": "app_links"
        }
    }
    
    def __init__(self):
        """Inicializa el generador"""
        pass
    
    def generar_footer(self, site_name: str, tagline: str,
                      footer_style: Optional[str] = None,
                      secciones: Optional[List[str]] = None,
                      year: Optional[int] = None,
                      include_social: bool = True,
                      include_newsletter: bool = False,
                      custom_text: Optional[str] = None,
                      layout_info: Optional[str] = None,
                      template_num: Optional[int] = None) -> str:
        """
        Genera el HTML de un footer completo
        
        Args:
            site_name: Nombre del sitio
            tagline: Lema/tagline del sitio
            footer_style: Estilo de footer (aleatorio si es None)
            secciones: Secciones a incluir (aleatorias si es None)
            year: Año para copyright (actual si es None)
            include_social: Incluir enlaces sociales
            include_newsletter: Incluir formulario de newsletter
            custom_text: Texto personalizado adicional
            layout_info: Información del layout usado
            template_num: Número de template
            
        Returns:
            str: HTML del footer
        """
        # Seleccionar estilo
        if not footer_style:
            footer_style = random.choice(list(self.FOOTER_STYLES.keys()))
        
        footer_config = self.FOOTER_STYLES[footer_style]
        
        # Determinar secciones a incluir
        if not secciones:
            secciones = self._seleccionar_secciones_automaticas(
                footer_config['columns'],
                include_newsletter
            )
        
        # Año actual si no se especifica
        if not year:
            year = datetime.now().year
        
        # Generar contenido de columnas
        columns_html = self._generar_columnas(
            secciones,
            site_name,
            tagline,
            include_social,
            custom_text
        )
        
        # Generar footer bottom
        footer_bottom = self._generar_footer_bottom(
            site_name,
            year,
            layout_info,
            template_num
        )
        
        # Ensamblar footer
        footer_html = f"""
    <footer class="footer {footer_config['classes']}">
        <div class="container">
            <div class="footer-grid">
{columns_html}
            </div>
{footer_bottom}
        </div>
    </footer>"""
        
        return footer_html
    
    def _seleccionar_secciones_automaticas(self, num_columnas: int,
                                          include_newsletter: bool) -> List[str]:
        """Selecciona secciones automáticamente (siempre 3 columnas en grid horizontal)"""
        
        # Siempre retornar 3 secciones para grid horizontal
        if include_newsletter:
            return ["about", "sections", "newsletter"]
        return ["about", "sections", "legal"]
    
    def _generar_columnas(self, secciones: List[str], site_name: str,
                         tagline: str, include_social: bool,
                         custom_text: Optional[str]) -> str:
        """Genera el HTML de las columnas del footer"""
        
        columns = []
        
        for seccion_key in secciones:
            if seccion_key not in self.FOOTER_SECTIONS:
                continue
            
            seccion = self.FOOTER_SECTIONS[seccion_key]
            column_html = ""
            
            if seccion_key == "about":
                about_text = custom_text or f"{site_name} es tu fuente confiable de noticias de última hora, análisis profundo e historias de todo el mundo."
                column_html = f"""
                <div class="footer-column">
                    <h3>{site_name}</h3>
                    <p>{tagline}</p>
                    <p class="footer-about">{about_text}</p>"""
                
                if include_social:
                    column_html += """
                    <div class="social-links">
                        <a href="#" class="social-link">Facebook</a>
                        <a href="#" class="social-link">Twitter</a>
                        <a href="#" class="social-link">Instagram</a>
                    </div>"""
                
                column_html += "\n                </div>"
            
            elif seccion['content_type'] == "links":
                links_html = []
                for link in seccion['links']:
                    link_slug = link.lower().replace(' ', '-')
                    links_html.append(f'                        <li><a href="#{link_slug}">{link}</a></li>')
                
                column_html = f"""
                <div class="footer-column">
                    <h4>{seccion['title']}</h4>
                    <ul class="footer-links">
{chr(10).join(links_html)}
                    </ul>
                </div>"""
            
            elif seccion['content_type'] == "legal_links":
                links_html = []
                for link in seccion['links']:
                    links_html.append(f'                        <li><a href="{link["url"]}">{link["text"]}</a></li>')
                
                column_html = f"""
                <div class="footer-column">
                    <h4>{seccion['title']}</h4>
                    <ul class="footer-links">
{chr(10).join(links_html)}
                    </ul>
                </div>"""
            
            elif seccion_key == "contact":
                domain = site_name.lower().replace(' ', '')
                column_html = f"""
                <div class="footer-column">
                    <h4>{seccion['title']}</h4>
                    <ul class="footer-links">
                        <li>Email: contacto@{domain}.com</li>
                        <li>Tel: +52 55 1234 5678</li>
                        <li><a href="#">Ciudad de México, México</a></li>
                    </ul>
                </div>"""
            
            elif seccion_key == "newsletter":
                column_html = f"""
                <div class="footer-column">
                    <h4>{seccion['title']}</h4>
                    <p>Recibe noticias en tu correo</p>
                    <form class="footer-newsletter-form">
                        <input type="email" placeholder="Tu email" required>
                        <button type="submit">Suscribirse</button>
                    </form>
                </div>"""
            
            elif seccion_key == "apps":
                column_html = f"""
                <div class="footer-column">
                    <h4>{seccion['title']}</h4>
                    <div class="app-links">
                        <a href="#" class="app-link">📱 App Store</a>
                        <a href="#" class="app-link">🤖 Google Play</a>
                    </div>
                </div>"""
            
            if column_html:
                columns.append(column_html)
        
        return '\n'.join(columns)
    
    def _generar_footer_bottom(self, site_name: str, year: int,
                              layout_info: Optional[str],
                              template_num: Optional[int]) -> str:
        """Genera la sección inferior del footer con copyright"""
        
        bottom_html = f"""
            <div class="footer-bottom">
                <p>&copy; {year} {site_name}. Todos los derechos reservados.</p>"""
        
        # Agregar info de layout/template si se proporciona (útil para desarrollo)
        if layout_info and template_num:
            bottom_html += f"""
                <p class="layout-info">Layout: {layout_info} | Template: {template_num}</p>"""
        
        bottom_html += """
            </div>"""
        
        return bottom_html
    
    def generar_configuracion_aleatoria(self) -> Dict:
        """
        Genera una configuración aleatoria de footer
        
        Returns:
            dict: Configuración del footer
        """
        footer_style = random.choice(list(self.FOOTER_STYLES.keys()))
        config = self.FOOTER_STYLES[footer_style]
        
        return {
            "footer_style": footer_style,
            "include_social": random.choice([True, True, False]),  # 66% probabilidad
            "include_newsletter": random.choice([True, False]),
            "num_columns": config['columns']
        }
    
    def obtener_estilos_css_base(self) -> str:
        """
        Retorna CSS base para los footers
        
        Returns:
            str: CSS base
        """
        return """
/* ===== BASE FOOTER STYLES ===== */
.footer {
    background: var(--primary-color);
    color: white;
    padding: 3rem 0 1rem;
    margin-top: 4rem;
}

.footer-grid {
    display: flex;
    gap: 2rem;
    margin-bottom: 2rem;
}

/* Footer columns - flex distribution */
.footer-grid.cols-2,
.footer-grid.cols-3,
.footer-grid.cols-4,
.footer-grid.cols-5 {
    display: flex;
}

.footer-column {
    flex: 1;
    min-width: 0;
}

/* Footer Column */
.footer-column h3,
.footer-column h4 {
    color: white;
    margin-bottom: 1rem;
    font-family: var(--font-primary);
}

.footer-column p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
    font-family: var(--font-secondary);
}

.footer-about {
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

/* Footer Links */
.footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-links li {
    margin-bottom: 0.5rem;
}

.footer-links a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: color 0.3s ease;
    font-family: var(--font-secondary);
}

.footer-links a:hover {
    color: white;
}

/* Social Links */
.social-links {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.social-link {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    text-decoration: none;
    border-radius: 5px;
    transition: background 0.3s ease;
    font-family: var(--font-secondary);
}

.social-link:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* Newsletter Form */
.footer-newsletter-form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 1rem;
}

.footer-newsletter-form input {
    padding: 0.75rem;
    border: none;
    border-radius: 5px;
    font-family: var(--font-secondary);
}

.footer-newsletter-form button {
    padding: 0.75rem;
    background: var(--accent-color);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 600;
    transition: opacity 0.3s ease;
    font-family: var(--font-secondary);
}

.footer-newsletter-form button:hover {
    opacity: 0.9;
}

/* App Links */
.app-links {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 1rem;
}

.app-link {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    text-decoration: none;
    border-radius: 5px;
    text-align: center;
    transition: background 0.3s ease;
    font-family: var(--font-secondary);
}

.app-link:hover {
    background: rgba(255, 255, 255, 0.2);
}

/* Footer Bottom */
.footer-bottom {
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding-top: 1.5rem;
    text-align: center;
}

.footer-bottom p {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    margin: 0.25rem 0;
    font-family: var(--font-secondary);
}

.layout-info {
    font-size: 0.8rem !important;
    color: rgba(255, 255, 255, 0.5) !important;
}

/* Footer Style Variations */
.footer-centered .footer-grid {
    flex-direction: column;
    text-align: center;
}

.footer-centered .social-links {
    justify-content: center;
}

.footer-compact {
    padding: 1.5rem 0;
}

.footer-compact .footer-grid {
    flex-direction: column;
    margin-bottom: 0;
}

.footer-boxed {
    margin: 2rem auto;
    max-width: 1200px;
    border-radius: 10px;
}

/* Responsive */
@media (max-width: 640px) {
    /* Solo en móvil pequeño: 1 columna vertical */
    .footer-grid {
        flex-direction: column !important;
    }
    
    .footer {
        padding: 2rem 0 1rem;
    }
    
    .social-links {
        justify-content: center;
    }
}

@media (min-width: 641px) {
    /* Tablets y desktop: siempre 3 columnas horizontales */
    .footer-grid {
        flex-direction: row;
    }
}
"""


if __name__ == "__main__":
    # Ejemplo de uso
    generator = FooterGenerator()
    
    # Generar configuración aleatoria
    config = generator.generar_configuracion_aleatoria()
    print("Configuración generada:")
    print(f"  Footer Style: {config['footer_style']}")
    print(f"  Columns: {config['num_columns']}")
    print(f"  Include Social: {config['include_social']}")
    print(f"  Include Newsletter: {config['include_newsletter']}")
    
    # Generar footer
    footer_html = generator.generar_footer(
        site_name="El Diario Digital",
        tagline="Tu fuente de noticias confiable",
        footer_style=config['footer_style'],
        include_social=config['include_social'],
        include_newsletter=config['include_newsletter'],
        layout_info="modern_cards",
        template_num=1
    )
    
    print("\nFooter HTML generado:")
    print(footer_html)
