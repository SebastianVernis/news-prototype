#!/usr/bin/env python3
"""
Componentes Mejorados para Layouts
Headers y Footers completos con todas las características
"""

from typing import List, Dict


class EnhancedComponents:
    """Genera componentes mejorados y completos"""
    
    def header_completo_horizontal(
        self,
        site_metadata: Dict,
        categorias: List[Dict],
        logo_path: str = 'assets/logo.svg'
    ) -> str:
        """Header horizontal completo con logo, slogan, categorías y menú"""
        
        site_name = site_metadata.get('nombre', 'Noticias')
        tagline = site_metadata.get('tagline', 'Información de calidad')
        primary = site_metadata.get('color_primario', '#667eea')
        secondary = site_metadata.get('color_secundario', '#764ba2')
        
        # Items de categorías para el menú
        cat_items = [f'<a href="categoria/{cat.get("id", "")}.html" class="dropdown-item">{cat.get("nombre", "")}</a>' 
                     for cat in categorias[:8]]
        
        return f'''
<header class="header-completo">
    <div class="header-top">
        <div class="container">
            <div class="header-top-content">
                <div class="social-links">
                    <a href="#" class="social-icon" aria-label="Facebook">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                    </a>
                    <a href="#" class="social-icon" aria-label="Twitter">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
                    </a>
                    <a href="#" class="social-icon" aria-label="Instagram">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                    </a>
                    <a href="#" class="social-icon" aria-label="YouTube">
                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                    </a>
                </div>
                <div class="header-date">{self._get_fecha_actual()}</div>
            </div>
        </div>
    </div>
    
    <div class="header-main">
        <div class="container">
            <div class="header-main-content">
                <div class="brand">
                    <a href="index.html" class="brand-link">
                        <img src="{logo_path}" alt="{site_name}" class="brand-logo">
                        <div class="brand-text">
                            <h1 class="brand-name">{site_name}</h1>
                            <p class="brand-tagline">{tagline}</p>
                        </div>
                    </a>
                </div>
                
                <nav class="main-nav">
                    <a href="index.html" class="nav-link">Inicio</a>
                    
                    <div class="dropdown">
                        <button class="nav-link dropdown-toggle">Categorías ▼</button>
                        <div class="dropdown-menu">
                            {chr(10).join(cat_items)}
                        </div>
                    </div>
                    
                    <a href="feed.xml" class="nav-link">RSS</a>
                    <button class="search-btn">🔍</button>
                </nav>
            </div>
        </div>
    </div>
</header>

<style>
.header-completo {{
    background: white;
    box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
}}

.header-top {{
    background: {primary};
    color: white;
    padding: 0.5rem 0;
}}

.header-top-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.85rem;
}}

.social-links {{
    display: flex;
    gap: 1rem;
}}

.social-icon {{
    color: white;
    opacity: 0.8;
    transition: opacity 0.3s;
}}

.social-icon:hover {{
    opacity: 1;
}}

.header-main {{
    padding: 1.5rem 0;
}}

.header-main-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.brand-link {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.brand-logo {{
    height: 60px;
    width: 60px;
}}

.brand-name {{
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, {primary}, {secondary});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}}

.brand-tagline {{
    font-size: 0.9rem;
    color: #6c757d;
    font-weight: 500;
}}

.main-nav {{
    display: flex;
    gap: 0.5rem;
    align-items: center;
}}

.nav-link {{
    padding: 0.75rem 1.25rem;
    color: #2c3e50;
    font-weight: 600;
    border-radius: 6px;
    transition: all 0.3s;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1rem;
}}

.nav-link:hover {{
    background: {primary}15;
    color: {primary};
}}

.dropdown {{
    position: relative;
}}

.dropdown-menu {{
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    background: white;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    border-radius: 8px;
    padding: 0.5rem 0;
    min-width: 250px;
    margin-top: 0.5rem;
    z-index: 100;
}}

.dropdown:hover .dropdown-menu {{
    display: block;
}}

.dropdown-item {{
    display: block;
    padding: 0.75rem 1.25rem;
    color: #2c3e50;
    transition: all 0.3s;
}}

.dropdown-item:hover {{
    background: {primary}10;
    color: {primary};
}}

.search-btn {{
    background: {primary};
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    font-size: 1.1rem;
    transition: all 0.3s;
}}

.search-btn:hover {{
    background: {secondary};
    transform: scale(1.1);
}}
</style>
'''
        
        return header
    
    def footer_completo_profesional(
        self,
        site_metadata: Dict,
        categorias: List[Dict]
    ) -> str:
        """Footer completo con categorías, redes, TyC, PdP"""
        
        site_name = site_metadata.get('nombre', 'Noticias')
        tagline = site_metadata.get('tagline', 'Información de calidad')
        primary = site_metadata.get('color_primario', '#667eea')
        secondary = site_metadata.get('color_secundario', '#764ba2')
        
        # Dividir categorías en 2 columnas
        cat_col1 = categorias[:5]
        cat_col2 = categorias[5:10] if len(categorias) > 5 else []
        
        return f'''
<footer class="footer-completo">
    <div class="footer-main">
        <div class="container">
            <div class="footer-grid">
                <!-- Columna 1: Sobre el sitio -->
                <div class="footer-col">
                    <div class="footer-brand">
                        <h3 class="footer-logo">{site_name}</h3>
                        <p class="footer-tagline">{tagline}</p>
                    </div>
                    <p class="footer-description">
                        Tu fuente confiable de noticias políticas de México. 
                        Información veraz, análisis profundo y cobertura completa 
                        de los acontecimientos más relevantes del país.
                    </p>
                    <div class="footer-social">
                        <a href="#" class="footer-social-btn facebook">
                            <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                        </a>
                        <a href="#" class="footer-social-btn twitter">
                            <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
                        </a>
                        <a href="#" class="footer-social-btn instagram">
                            <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                        </a>
                        <a href="#" class="footer-social-btn youtube">
                            <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                        </a>
                    </div>
                </div>
                
                <!-- Columna 2: Categorías parte 1 -->
                <div class="footer-col">
                    <h4 class="footer-title">Categorías</h4>
                    <ul class="footer-links">
                        {chr(10).join([f'<li><a href="categoria/{cat.get("id", "")}.html">{cat.get("nombre", "")}</a></li>' for cat in cat_col1])}
                    </ul>
                </div>
                
                <!-- Columna 3: Categorías parte 2 / Información -->
                <div class="footer-col">
                    <h4 class="footer-title">Más Categorías</h4>
                    <ul class="footer-links">
                        {chr(10).join([f'<li><a href="categoria/{cat.get("id", "")}.html">{cat.get("nombre", "")}</a></li>' for cat in cat_col2]) if cat_col2 else '<li><a href="categorias.html">Ver todas</a></li>'}
                    </ul>
                    <h4 class="footer-title" style="margin-top: 1.5rem;">Información</h4>
                    <ul class="footer-links">
                        <li><a href="about.html">Acerca de</a></li>
                        <li><a href="contact.html">Contacto</a></li>
                        <li><a href="team.html">Equipo Editorial</a></li>
                    </ul>
                </div>
                
                <!-- Columna 4: Newsletter y Legal -->
                <div class="footer-col">
                    <h4 class="footer-title">Mantente Informado</h4>
                    <p class="footer-newsletter-text">Recibe las noticias más importantes directamente en tu correo</p>
                    <form class="newsletter-form" onsubmit="return false;">
                        <input type="email" placeholder="tu@email.com" class="newsletter-input" required>
                        <button type="submit" class="newsletter-btn">Suscribir</button>
                    </form>
                    
                    <div class="footer-legal">
                        <a href="privacy.html">Política de Privacidad</a>
                        <span class="separator">•</span>
                        <a href="terms.html">Términos y Condiciones</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer-bottom">
        <div class="container">
            <div class="footer-bottom-content">
                <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
                <p class="footer-credits">Diseñado con ❤️ para informar con calidad</p>
            </div>
        </div>
    </div>
</footer>

<style>
.footer-completo {{
    background: #2c3e50;
    color: white;
    margin-top: 4rem;
}}

.footer-main {{
    padding: 3rem 0 2rem;
}}

.footer-grid {{
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr 1.2fr;
    gap: 3rem;
}}

.footer-col {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.footer-logo {{
    font-size: 1.75rem;
    font-weight: 800;
    margin-bottom: 0.25rem;
}}

.footer-tagline {{
    color: #bdc3c7;
    font-size: 0.95rem;
    font-style: italic;
}}

.footer-description {{
    color: #bdc3c7;
    line-height: 1.7;
    font-size: 0.95rem;
}}

.footer-social {{
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}}

.footer-social-btn {{
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    transition: all 0.3s;
}}

.footer-social-btn:hover {{
    background: {primary};
    transform: translateY(-3px);
}}

.footer-title {{
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: white;
}}

.footer-links {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.footer-links a {{
    color: #bdc3c7;
    transition: all 0.3s;
    font-size: 0.95rem;
}}

.footer-links a:hover {{
    color: white;
    padding-left: 0.5rem;
}}

.footer-newsletter-text {{
    color: #bdc3c7;
    font-size: 0.9rem;
    line-height: 1.5;
}}

.newsletter-form {{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 0.5rem;
}}

.newsletter-input {{
    padding: 0.75rem 1rem;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 6px;
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 0.95rem;
}}

.newsletter-input::placeholder {{
    color: rgba(255,255,255,0.5);
}}

.newsletter-btn {{
    padding: 0.75rem;
    background: {primary};
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}}

.newsletter-btn:hover {{
    background: {secondary};
}}

.footer-legal {{
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    font-size: 0.85rem;
}}

.footer-legal a {{
    color: #bdc3c7;
}}

.footer-legal a:hover {{
    color: white;
    text-decoration: underline;
}}

.separator {{
    margin: 0 0.5rem;
    color: #7f8c8d;
}}

.footer-bottom {{
    background: #1a252f;
    padding: 1.5rem 0;
}}

.footer-bottom-content {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #95a5a6;
    font-size: 0.9rem;
}}

.footer-credits {{
    font-size: 0.85rem;
    color: #7f8c8d;
}}

@media (max-width: 1024px) {{
    .footer-grid {{
        grid-template-columns: repeat(2, 1fr);
        gap: 2rem;
    }}
}}

@media (max-width: 640px) {{
    .footer-grid {{
        grid-template-columns: 1fr;
    }}
    
    .footer-bottom-content {{
        flex-direction: column;
        gap: 0.5rem;
        text-align: center;
    }}
}}
</style>
'''
        
        return footer
    
    def sidebar_iconos_collapsible(
        self,
        site_metadata: Dict,
        categorias: List[Dict],
        colores: Dict,
        position: str = "left"
    ) -> str:
        """
        Sidebar con iconos que se expande al hover (REEMPLAZA al header)
        
        Args:
            site_metadata: Metadata del sitio (nombre, tagline)
            categorias: Lista de categorías
            colores: Paleta de colores
            position: 'left' o 'right'
            
        Returns:
            HTML del sidebar (funciona como header)
        """
        primary = colores.get('primary', '#667eea')
        secondary = colores.get('secondary', '#764ba2')
        site_name = site_metadata.get('nombre', 'Noticias')
        tagline = site_metadata.get('tagline', 'Información de calidad')
        side = position  # left o right
        
        # Iconos para categorías
        iconos = {
            'política-nacional': '🏛️',
            'política-internacional': '🌍',
            'economía-política': '💰',
            'economía': '💰',
            'seguridad': '🚔',
            'elecciones': '🗳️',
            'judicial': '⚖️',
            'análisis': '📝',
            'default': '📰'
        }
        
        cat_items = []
        for cat in categorias[:10]:
            cat_id = cat.get('id', '')
            cat_nombre = cat.get('nombre', '')
            icono = iconos.get(cat_id, iconos['default'])
            
            cat_items.append(f'''
                <a href="categoria/{cat_id}.html" class="sidebar-nav-item" data-tooltip="{cat_nombre}">
                    <span class="sidebar-icon">{icono}</span>
                    <span class="sidebar-text">{cat_nombre}</span>
                </a>
''')
        
        # Redes sociales
        social_items = f'''
        <div class="sidebar-social">
            <div class="sidebar-nav-item sidebar-social-label">
                <span class="sidebar-icon">🔗</span>
                <span class="sidebar-text">Síguenos</span>
            </div>
            <a href="#" class="sidebar-nav-item" title="Facebook">
                <span class="sidebar-icon">📘</span>
                <span class="sidebar-text">Facebook</span>
            </a>
            <a href="#" class="sidebar-nav-item" title="Twitter">
                <span class="sidebar-icon">🐦</span>
                <span class="sidebar-text">Twitter</span>
            </a>
            <a href="#" class="sidebar-nav-item" title="Instagram">
                <span class="sidebar-icon">📷</span>
                <span class="sidebar-text">Instagram</span>
            </a>
        </div>
'''
        
        return f'''
<!-- Sidebar como Header (NO hay header tradicional) -->
<nav class="sidebar-header sidebar-{side}">
    <div class="sidebar-content">
        <!-- Branding del sitio -->
        <div class="sidebar-brand">
            <a href="index.html" class="sidebar-brand-link">
                <span class="sidebar-icon">📰</span>
                <div class="sidebar-brand-text">
                    <span class="sidebar-brand-name">{site_name}</span>
                    <span class="sidebar-brand-tagline">{tagline}</span>
                </div>
            </a>
        </div>
        
        <div class="sidebar-divider"></div>
        
        <a href="index.html" class="sidebar-nav-item" title="Inicio">
            <span class="sidebar-icon">🏠</span>
            <span class="sidebar-text">Inicio</span>
        </a>
        
        <a href="categorias.html" class="sidebar-nav-item" title="Todas las Categorías">
            <span class="sidebar-icon">📑</span>
            <span class="sidebar-text">Todas las Categorías</span>
        </a>
        
        <div class="sidebar-divider"></div>
        
        <div class="sidebar-section-label">
            <span class="sidebar-icon">📂</span>
            <span class="sidebar-text">Categorías</span>
        </div>
        
        {chr(10).join(cat_items)}
        
        <div class="sidebar-divider"></div>
        
        <a href="feed.xml" class="sidebar-nav-item" title="RSS Feed">
            <span class="sidebar-icon">📡</span>
            <span class="sidebar-text">RSS Feed</span>
        </a>
        
        {social_items}
    </div>
</nav>

<style>
.sidebar-header {{
    position: fixed;
    top: 0;
    {side}: 0;
    height: 100vh;
    width: 80px;
    background: linear-gradient(180deg, {primary} 0%, {secondary} 100%);
    box-shadow: {'2px' if side == 'left' else '-2px'} 0 20px rgba(0,0,0,0.15);
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow-x: hidden;
    overflow-y: auto;
    z-index: 1000;
}}

.sidebar-header:hover {{
    width: 300px;
}}

.sidebar-content {{
    padding: 1.5rem 0;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}}

.sidebar-brand {{
    padding: 0.5rem 1.25rem 1.5rem;
}}

.sidebar-brand-link {{
    display: flex;
    align-items: center;
    gap: 1rem;
    color: white;
    text-decoration: none;
}}

.sidebar-brand-text {{
    display: flex;
    flex-direction: column;
    opacity: 0;
    transition: opacity 0.3s;
}}

.sidebar-header:hover .sidebar-brand-text {{
    opacity: 1;
}}

.sidebar-brand-name {{
    font-size: 1.25rem;
    font-weight: 800;
    line-height: 1.2;
}}

.sidebar-brand-tagline {{
    font-size: 0.75rem;
    opacity: 0.9;
    font-style: italic;
}}

.sidebar-section-label {{
    padding: 0.75rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    color: rgba(255,255,255,0.7);
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.sidebar-social {{
    margin-top: auto;
    padding-top: 1rem;
}}

.sidebar-social-label {{
    font-size: 0.85rem;
    color: rgba(255,255,255,0.9);
}}

.sidebar-nav-item {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    color: white;
    text-decoration: none;
    transition: all 0.3s;
    white-space: nowrap;
}}

.sidebar-nav-item:hover {{
    background: rgba(255,255,255,0.15);
}}

.sidebar-icon {{
    font-size: 1.5rem;
    width: 30px;
    text-align: center;
    flex-shrink: 0;
}}

.sidebar-text {{
    opacity: 0;
    transition: opacity 0.3s;
    font-weight: 600;
    font-size: 0.95rem;
}}

.sidebar-collapsible:hover .sidebar-text {{
    opacity: 1;
}}

.sidebar-divider {{
    height: 1px;
    background: rgba(255,255,255,0.2);
    margin: 0.5rem 1.25rem;
}}

/* Ajustar contenido principal para sidebar (NO hay header tradicional) */
.content-with-sidebar-{side} {{
    margin-{side}: 80px;
    transition: margin 0.3s;
    min-height: 100vh;
}}

@media (max-width: 768px) {{
    .sidebar-collapsible {{
        width: 60px;
    }}
    
    .sidebar-collapsible:hover {{
        width: 240px;
    }}
    
    .content-with-sidebar-{side} {{
        margin-{side}: 60px;
    }}
}}
</style>
'''
        
        return sidebar
    
    def _get_fecha_actual(self) -> str:
        """Obtiene fecha actual formateada"""
        from datetime import datetime
        meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        
        now = datetime.now()
        return f"{now.day} de {meses[now.month]}, {now.year}"


def main():
    """Demo de componentes mejorados"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║        🎨 COMPONENTES MEJORADOS - HEADERS Y FOOTERS                 ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    site_metadata = {
        'nombre': 'Política México Hoy',
        'tagline': 'Información Veraz y Análisis Profundo',
        'color_primario': '#667eea',
        'color_secundario': '#764ba2'
    }
    
    categorias = [
        {'id': 'política-nacional', 'nombre': 'Política Nacional'},
        {'id': 'política-internacional', 'nombre': 'Internacional'},
        {'id': 'economía-política', 'nombre': 'Economía'},
        {'id': 'seguridad', 'nombre': 'Seguridad'},
        {'id': 'elecciones', 'nombre': 'Elecciones'},
        {'id': 'judicial', 'nombre': 'Poder Judicial'},
    ]
    
    components = EnhancedComponents()
    
    # Generar componentes
    header = components.header_completo_horizontal(site_metadata, categorias)
    footer = components.footer_completo_profesional(site_metadata, categorias)
    sidebar_left = components.sidebar_iconos_collapsible(site_metadata, categorias, site_metadata, 'left')
    sidebar_right = components.sidebar_iconos_collapsible(site_metadata, categorias, site_metadata, 'right')
    
    # Demo con sidebar izquierdo (SIN HEADER - el sidebar ES el header)
    html_left = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layout con Sidebar Izquierdo (Sin Header)</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #f5f7fa; }}
        .demo-notice {{ background: #fff3cd; color: #856404; padding: 1rem; text-align: center; font-weight: 600; }}
    </style>
</head>
<body>
<!-- EL SIDEBAR ES EL HEADER - No hay header tradicional -->
{sidebar_left}

<div class="content-with-sidebar-left">
    <div class="demo-notice">
        ⚠️ NOTA: El sidebar es el HEADER. Pasa el mouse sobre él para expandir y ver navegación completa.
    </div>
    
    <main style="padding: 3rem 2rem; max-width: 1400px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-top: 2rem;">
        <h1 style="font-size: 2.5rem; color: #2c3e50; margin-bottom: 1rem;">Contenido Principal</h1>
        <p style="color: #6c757d; margin-bottom: 2rem; font-size: 1.1rem;">
            El sidebar izquierdo funciona como header. Incluye:
            <br>• Logo y nombre del sitio
            <br>• Tagline
            <br>• Navegación completa
            <br>• Todas las categorías
            <br>• RSS feed
            <br>• Redes sociales
        </p>
        <p style="color: #6c757d; line-height: 1.8;">
            Este es el área donde aparecerán los artículos destacados, carrusel, 
            grids de noticias, etc. El sidebar permanece fijo y se expande al hover.
        </p>
    </main>
    
{footer}
</div>
</body>
</html>'''
    
    # Demo con sidebar derecho (SIN HEADER - el sidebar ES el header)
    html_right = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layout con Sidebar Derecho (Sin Header)</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #f5f7fa; }}
        .demo-notice {{ background: #d1ecf1; color: #0c5460; padding: 1rem; text-align: center; font-weight: 600; }}
    </style>
</head>
<body>
<!-- EL SIDEBAR ES EL HEADER - No hay header tradicional -->
{sidebar_right}

<div class="content-with-sidebar-right">
    <div class="demo-notice">
        ⚠️ NOTA: El sidebar derecho es el HEADER. Pasa el mouse sobre el borde derecho para expandir.
    </div>
    
    <main style="padding: 3rem 2rem; max-width: 1400px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-top: 2rem;">
        <h1 style="font-size: 2.5rem; color: #2c3e50; margin-bottom: 1rem;">Contenido Principal</h1>
        <p style="color: #6c757d; margin-bottom: 2rem; font-size: 1.1rem;">
            El sidebar derecho funciona como header. Incluye todo lo necesario:
            <br>• Logo y branding
            <br>• Navegación completa
            <br>• Categorías con iconos
            <br>• Redes sociales
        </p>
        <p style="color: #6c757d; line-height: 1.8;">
            Layout invertido ideal para diseños únicos. El sidebar permanece en el 
            lado derecho y se expande al hover sin tapar el contenido.
        </p>
    </main>
    
{footer}
</div>
</body>
</html>'''
    
    # Guardar demos
    with open('demo/components_demo_sidebar_left.html', 'w', encoding='utf-8') as f:
        f.write(html_left)
    
    with open('demo/components_demo_sidebar_right.html', 'w', encoding='utf-8') as f:
        f.write(html_right)
    
    print("✅ Componentes mejorados generados:")
    print("   • Header completo con categorías, social, slogan")
    print("   • Footer completo con TyC, PdP, categorías, newsletter")
    print("   • Sidebar collapsible izquierdo con iconos")
    print("   • Sidebar collapsible derecho con iconos")
    print()
    print("🌐 Demos disponibles:")
    print("   http://localhost:8006/demo/components_demo_sidebar_left.html")
    print("   http://localhost:8006/demo/components_demo_sidebar_right.html")


if __name__ == '__main__':
    main()
