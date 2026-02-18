#!/usr/bin/env python3
"""
Generador de Preloaders/Animaciones de Entrada
Crea diferentes estilos de animaciones para sitios web
"""

from typing import Dict


class PreloaderGenerator:
    """Genera código de preloaders para sitios"""
    
    PRELOADERS = {
        "contador": {
            "nombre": "Contador de Carga (0-100%)",
            "descripcion": "Animación de contador numérico similar a Titan Preloader",
            "complejidad": "media"
        },
        "fade": {
            "nombre": "Fade In Simple",
            "descripcion": "Fade in suave del contenido",
            "complejidad": "baja"
        },
        "slide-down": {
            "nombre": "Slide Down",
            "descripcion": "Cortina que baja revelando el contenido",
            "complejidad": "media"
        },
        "logo-animation": {
            "nombre": "Logo Animado",
            "descripcion": "Logo que se anima y desaparece",
            "complejidad": "media"
        },
        "circle-expand": {
            "nombre": "Círculo Expandible",
            "descripcion": "Círculo que se expande desde el centro",
            "complejidad": "media"
        },
        "bars-loading": {
            "nombre": "Barras de Carga",
            "descripcion": "Barras verticales animadas",
            "complejidad": "baja"
        },
        "dots-pulse": {
            "nombre": "Puntos Pulsantes",
            "descripcion": "Tres puntos que pulsan",
            "complejidad": "baja"
        },
        "spinning-logo": {
            "nombre": "Logo Giratorio",
            "descripcion": "Logo que gira con efecto 3D",
            "complejidad": "media"
        },
        "wave-animation": {
            "nombre": "Onda Animada",
            "descripcion": "Efecto de onda que recorre la pantalla",
            "complejidad": "media"
        },
        "glitch-effect": {
            "nombre": "Efecto Glitch",
            "descripcion": "Animación de glitch moderno",
            "complejidad": "alta"
        }
    }
    
    def generar_contador_loading(self, colores: Dict = None) -> Dict[str, str]:
        """
        Genera un preloader estilo contador (0-100%) similar al de ejemplo.html
        
        Args:
            colores: Dict con primary y secondary
            
        Returns:
            Dict con 'html', 'css', 'js'
        """
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        html = '''
<!-- Preloader -->
<div id="preloader" class="preloader-contador">
    <div class="preloader-content">
        <div class="preloader-number" id="preloader-number">0</div>
        <div class="preloader-percent">%</div>
    </div>
    <div class="preloader-progress">
        <div class="preloader-progress-bar" id="preloader-progress-bar"></div>
    </div>
</div>
'''
        
        css = f'''
/* Preloader Contador */
.preloader-contador {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.5s ease, visibility 0.5s ease;
}}

.preloader-contador.loaded {{
    opacity: 0;
    visibility: hidden;
}}

.preloader-content {{
    display: flex;
    align-items: baseline;
    gap: 1rem;
}}

.preloader-number {{
    font-family: 'Bebas Neue', 'Arial Black', sans-serif;
    font-size: clamp(120px, 20vw, 280px);
    font-weight: 700;
    color: white;
    line-height: 1;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
}}

.preloader-percent {{
    font-family: 'Bebas Neue', 'Arial Black', sans-serif;
    font-size: clamp(40px, 8vw, 80px);
    font-weight: 700;
    color: rgba(255,255,255,0.7);
    line-height: 1;
}}

.preloader-progress {{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: rgba(255,255,255,0.2);
}}

.preloader-progress-bar {{
    height: 100%;
    width: 0%;
    background: white;
    transition: width 0.1s linear;
}}
'''
        
        js = '''
// Preloader Contador
document.addEventListener('DOMContentLoaded', function() {
    const preloader = document.getElementById('preloader');
    const numberEl = document.getElementById('preloader-number');
    const progressBar = document.getElementById('preloader-progress-bar');
    
    if (!preloader || !numberEl || !progressBar) return;
    
    let count = 0;
    const duration = 2000; // 2 segundos
    const interval = 20; // Update cada 20ms
    const steps = duration / interval;
    const increment = 100 / steps;
    
    const counter = setInterval(() => {
        count += increment;
        
        if (count >= 100) {
            count = 100;
            clearInterval(counter);
            
            // Esperar un momento en 100% y luego ocultar
            setTimeout(() => {
                preloader.classList.add('loaded');
                
                // Remover del DOM después de la animación
                setTimeout(() => {
                    preloader.remove();
                }, 500);
            }, 300);
        }
        
        numberEl.textContent = Math.floor(count);
        progressBar.style.width = count + '%';
    }, interval);
});
'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_slide_down(self, colores: Dict = None) -> Dict[str, str]:
        """
        Genera preloader con cortina que baja
        
        Args:
            colores: Dict con primary y secondary
            
        Returns:
            Dict con 'html', 'css', 'js'
        """
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        html = '''
<!-- Preloader Slide Down -->
<div id="preloader" class="preloader-slide">
    <div class="preloader-curtain preloader-curtain-top"></div>
    <div class="preloader-curtain preloader-curtain-bottom"></div>
    <div class="preloader-logo">
        <div class="preloader-spinner"></div>
    </div>
</div>
'''
        
        css = f'''
/* Preloader Slide Down */
.preloader-slide {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 99999;
    pointer-events: none;
}}

.preloader-curtain {{
    position: absolute;
    left: 0;
    width: 100%;
    height: 50%;
    background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
    transition: transform 0.8s cubic-bezier(0.77, 0, 0.175, 1);
}}

.preloader-curtain-top {{
    top: 0;
}}

.preloader-curtain-bottom {{
    bottom: 0;
}}

.preloader-slide.loaded .preloader-curtain-top {{
    transform: translateY(-100%);
}}

.preloader-slide.loaded .preloader-curtain-bottom {{
    transform: translateY(100%);
}}

.preloader-logo {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    opacity: 1;
    transition: opacity 0.3s ease;
}}

.preloader-slide.loaded .preloader-logo {{
    opacity: 0;
}}

.preloader-spinner {{
    width: 60px;
    height: 60px;
    border: 4px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}
'''
        
        js = '''
// Preloader Slide Down
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    
    // Pequeño delay para efecto
    setTimeout(() => {
        preloader.classList.add('loaded');
        
        // Remover del DOM
        setTimeout(() => {
            preloader.remove();
        }, 1000);
    }, 500);
});
'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_fade_simple(self, colores: Dict = None) -> Dict[str, str]:
        """
        Genera fade in simple y elegante
        
        Args:
            colores: Dict con primary y secondary
            
        Returns:
            Dict con 'html', 'css', 'js'
        """
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        
        html = '''
<!-- Preloader Fade -->
<div id="preloader" class="preloader-fade">
    <div class="preloader-spinner-wrapper">
        <div class="preloader-spinner-circle"></div>
    </div>
</div>
'''
        
        css = f'''
/* Preloader Fade Simple */
.preloader-fade {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    opacity: 1;
    transition: opacity 0.6s ease;
}}

.preloader-fade.loaded {{
    opacity: 0;
    pointer-events: none;
}}

.preloader-spinner-wrapper {{
    position: relative;
}}

.preloader-spinner-circle {{
    width: 50px;
    height: 50px;
    border: 3px solid rgba(0,0,0,0.1);
    border-top-color: {primary};
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}
'''
        
        js = '''
// Preloader Fade
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => {
            preloader.remove();
        }, 600);
    }, 300);
});
'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_logo_animado(self, colores: Dict = None, logo_url: str = None) -> Dict[str, str]:
        """
        Genera preloader con logo animado
        
        Args:
            colores: Dict con primary y secondary
            logo_url: URL del logo (opcional)
            
        Returns:
            Dict con 'html', 'css', 'js'
        """
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        logo_html = f'<img src="{logo_url}" alt="Logo" class="preloader-logo-img">' if logo_url else '<div class="preloader-logo-placeholder">📰</div>'
        
        html = f'''
<!-- Preloader Logo -->
<div id="preloader" class="preloader-logo">
    <div class="preloader-logo-container">
        {logo_html}
        <div class="preloader-loading-bar"></div>
    </div>
</div>
'''
        
        css = f'''
/* Preloader Logo Animado */
.preloader-logo {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, {primary} 0%, {secondary} 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    opacity: 1;
    transition: opacity 0.5s ease;
}}

.preloader-logo.loaded {{
    opacity: 0;
    pointer-events: none;
}}

.preloader-logo-container {{
    text-align: center;
    animation: pulse 2s ease-in-out;
}}

.preloader-logo-img {{
    max-width: 200px;
    max-height: 200px;
    animation: logoFade 2s ease-in-out;
}}

.preloader-logo-placeholder {{
    font-size: 120px;
    color: white;
    animation: logoFade 2s ease-in-out;
}}

.preloader-loading-bar {{
    width: 200px;
    height: 3px;
    background: rgba(255,255,255,0.3);
    margin: 2rem auto 0;
    border-radius: 2px;
    overflow: hidden;
}}

.preloader-loading-bar::after {{
    content: '';
    display: block;
    width: 0%;
    height: 100%;
    background: white;
    animation: loadBar 2s ease-out forwards;
}}

@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50% {{ transform: scale(1.05); }}
}}

@keyframes logoFade {{
    0% {{ opacity: 0; transform: scale(0.8); }}
    50% {{ opacity: 1; transform: scale(1); }}
    100% {{ opacity: 1; transform: scale(1); }}
}}

@keyframes loadBar {{
    to {{ width: 100%; }}
}}
'''
        
        js = '''
// Preloader Logo
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    
    // Esperar a que termine la animación de la barra
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => {
            preloader.remove();
        }, 500);
    }, 2200);
});
'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_circle_expand(self, colores: Dict = None) -> Dict[str, str]:
        """Círculo que se expande desde el centro"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        html = '''
<div id="preloader" class="preloader-circle">
    <div class="circle-expand"></div>
    <div class="preloader-text">Cargando...</div>
</div>'''
        
        css = f'''
.preloader-circle {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, {primary}, {secondary});
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.6s ease;
}}
.preloader-circle.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.circle-expand {{
    position: absolute;
    width: 50px;
    height: 50px;
    border: 3px solid white;
    border-radius: 50%;
    animation: expandCircle 1.5s ease-in-out infinite;
}}
.preloader-text {{
    color: white;
    font-size: 1.2rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    animation: pulse 1.5s ease-in-out infinite;
}}
@keyframes expandCircle {{
    0% {{ transform: scale(1); opacity: 1; }}
    100% {{ transform: scale(3); opacity: 0; }}
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.5; }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 600);
    }, 800);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_bars_loading(self, colores: Dict = None) -> Dict[str, str]:
        """Barras verticales animadas"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        
        html = '''
<div id="preloader" class="preloader-bars">
    <div class="bars-container">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>
</div>'''
        
        css = f'''
.preloader-bars {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.4s ease;
}}
.preloader-bars.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.bars-container {{
    display: flex;
    gap: 8px;
    align-items: flex-end;
    height: 60px;
}}
.bar {{
    width: 8px;
    height: 20px;
    background: {primary};
    border-radius: 4px;
    animation: barBounce 1s ease-in-out infinite;
}}
.bar:nth-child(1) {{ animation-delay: 0s; }}
.bar:nth-child(2) {{ animation-delay: 0.1s; }}
.bar:nth-child(3) {{ animation-delay: 0.2s; }}
.bar:nth-child(4) {{ animation-delay: 0.3s; }}
.bar:nth-child(5) {{ animation-delay: 0.4s; }}
@keyframes barBounce {{
    0%, 100% {{ height: 20px; }}
    50% {{ height: 60px; }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 400);
    }, 600);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_dots_pulse(self, colores: Dict = None) -> Dict[str, str]:
        """Tres puntos pulsantes"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        
        html = '''
<div id="preloader" class="preloader-dots">
    <div class="dots-container">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
</div>'''
        
        css = f'''
.preloader-dots {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.5s ease;
}}
.preloader-dots.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.dots-container {{
    display: flex;
    gap: 15px;
}}
.dot {{
    width: 20px;
    height: 20px;
    background: {primary};
    border-radius: 50%;
    animation: dotPulse 1.4s ease-in-out infinite;
}}
.dot:nth-child(1) {{ animation-delay: 0s; }}
.dot:nth-child(2) {{ animation-delay: 0.2s; }}
.dot:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes dotPulse {{
    0%, 100% {{ transform: scale(1); opacity: 1; }}
    50% {{ transform: scale(1.5); opacity: 0.5; }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 500);
    }, 500);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_spinning_logo(self, colores: Dict = None, logo_url: str = None) -> Dict[str, str]:
        """Logo que gira con efecto 3D"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        logo_html = f'<img src="{logo_url}" alt="Logo" class="spinning-logo-img">' if logo_url else '<div class="spinning-logo-placeholder">📰</div>'
        
        html = f'''
<div id="preloader" class="preloader-spinning">
    <div class="spinning-container">
        {logo_html}
    </div>
</div>'''
        
        css = f'''
.preloader-spinning {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, {primary}, {secondary});
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.5s ease;
}}
.preloader-spinning.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.spinning-container {{
    animation: spin3D 2s ease-in-out infinite;
}}
.spinning-logo-img {{
    max-width: 150px;
    max-height: 150px;
    filter: drop-shadow(0 10px 30px rgba(0,0,0,0.3));
}}
.spinning-logo-placeholder {{
    font-size: 100px;
    color: white;
    filter: drop-shadow(0 10px 30px rgba(0,0,0,0.3));
}}
@keyframes spin3D {{
    0% {{ transform: rotateY(0deg) scale(1); }}
    50% {{ transform: rotateY(180deg) scale(1.1); }}
    100% {{ transform: rotateY(360deg) scale(1); }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 500);
    }, 1200);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_wave_animation(self, colores: Dict = None) -> Dict[str, str]:
        """Onda que recorre la pantalla"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        html = '''
<div id="preloader" class="preloader-wave">
    <div class="wave"></div>
    <div class="wave"></div>
    <div class="wave"></div>
</div>'''
        
        css = f'''
.preloader-wave {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: {primary};
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    overflow: hidden;
    transition: opacity 0.6s ease;
}}
.preloader-wave.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.wave {{
    position: absolute;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: waveMove 3s ease-in-out infinite;
}}
.wave:nth-child(1) {{ animation-delay: 0s; }}
.wave:nth-child(2) {{ animation-delay: 1s; }}
.wave:nth-child(3) {{ animation-delay: 2s; }}
@keyframes waveMove {{
    0% {{ transform: scale(0) translateX(-50%) translateY(-50%); opacity: 1; }}
    100% {{ transform: scale(1) translateX(0) translateY(0); opacity: 0; }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 600);
    }, 1000);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_glitch_effect(self, colores: Dict = None) -> Dict[str, str]:
        """Efecto glitch moderno"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        
        html = '''
<div id="preloader" class="preloader-glitch">
    <div class="glitch-text" data-text="CARGANDO">CARGANDO</div>
</div>'''
        
        css = f'''
.preloader-glitch {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.3s ease;
}}
.preloader-glitch.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.glitch-text {{
    position: relative;
    font-size: 4rem;
    font-weight: 900;
    color: white;
    letter-spacing: 0.5rem;
    animation: glitch 1s infinite;
}}
.glitch-text::before,
.glitch-text::after {{
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}}
.glitch-text::before {{
    left: 2px;
    text-shadow: -2px 0 {primary};
    animation: glitchTop 0.5s infinite;
    clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%);
}}
.glitch-text::after {{
    left: -2px;
    text-shadow: -2px 0 cyan;
    animation: glitchBottom 0.7s infinite;
    clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%);
}}
@keyframes glitch {{
    0%, 100% {{ transform: translate(0); }}
    20% {{ transform: translate(-2px, 2px); }}
    40% {{ transform: translate(-2px, -2px); }}
    60% {{ transform: translate(2px, 2px); }}
    80% {{ transform: translate(2px, -2px); }}
}}
@keyframes glitchTop {{
    0%, 100% {{ clip-path: polygon(0 0, 100% 0, 100% 33%, 0 33%); }}
    50% {{ clip-path: polygon(0 10%, 100% 10%, 100% 43%, 0 43%); }}
}}
@keyframes glitchBottom {{
    0%, 100% {{ clip-path: polygon(0 67%, 100% 67%, 100% 100%, 0 100%); }}
    50% {{ clip-path: polygon(0 57%, 100% 57%, 100% 90%, 0 90%); }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 300);
    }, 1500);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_rotating_square(self, colores: Dict = None) -> Dict[str, str]:
        """Cuadrado rotante"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        html = '''
<div id="preloader" class="preloader-square">
    <div class="rotating-square"></div>
</div>'''
        
        css = f'''
.preloader-square {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, {primary}, {secondary});
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.5s ease;
}}
.preloader-square.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.rotating-square {{
    width: 60px;
    height: 60px;
    background: white;
    animation: rotateSquare 2s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
}}
@keyframes rotateSquare {{
    0%, 100% {{ transform: rotate(0deg) scale(1); border-radius: 0%; }}
    25% {{ transform: rotate(90deg) scale(1.2); border-radius: 50%; }}
    50% {{ transform: rotate(180deg) scale(1); border-radius: 0%; }}
    75% {{ transform: rotate(270deg) scale(1.2); border-radius: 50%; }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 500);
    }, 800);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_typing_text(self, colores: Dict = None) -> Dict[str, str]:
        """Texto escribiéndose"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        html = '''
<div id="preloader" class="preloader-typing">
    <div class="typing-text">
        <span id="typing-content">Cargando noticias</span>
        <span class="cursor">|</span>
    </div>
</div>'''
        
        css = f'''
.preloader-typing {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, {primary}, {secondary});
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.5s ease;
}}
.preloader-typing.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.typing-text {{
    font-size: 2rem;
    font-weight: 600;
    color: white;
    font-family: 'Courier New', monospace;
}}
.cursor {{
    animation: blink 0.7s infinite;
}}
@keyframes blink {{
    0%, 50% {{ opacity: 1; }}
    51%, 100% {{ opacity: 0; }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 500);
    }, 1500);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_ripple_effect(self, colores: Dict = None) -> Dict[str, str]:
        """Efecto de ondas concéntricas"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        
        html = '''
<div id="preloader" class="preloader-ripple">
    <div class="ripple-container">
        <div class="ripple"></div>
        <div class="ripple"></div>
        <div class="ripple"></div>
    </div>
</div>'''
        
        css = f'''
.preloader-ripple {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.6s ease;
}}
.preloader-ripple.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.ripple-container {{
    position: relative;
    width: 100px;
    height: 100px;
}}
.ripple {{
    position: absolute;
    border: 3px solid {primary};
    border-radius: 50%;
    width: 100%;
    height: 100%;
    animation: rippleEffect 1.5s ease-out infinite;
}}
.ripple:nth-child(2) {{ animation-delay: 0.5s; }}
.ripple:nth-child(3) {{ animation-delay: 1s; }}
@keyframes rippleEffect {{
    0% {{ transform: scale(0); opacity: 1; }}
    100% {{ transform: scale(1.5); opacity: 0; }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 600);
    }, 800);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_progress_circle(self, colores: Dict = None) -> Dict[str, str]:
        """Círculo de progreso con porcentaje"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        secondary = colores.get('secondary', '#764ba2') if colores else '#764ba2'
        
        html = '''
<div id="preloader" class="preloader-progress-circle">
    <svg class="progress-ring" width="200" height="200">
        <circle class="progress-ring-bg" cx="100" cy="100" r="90"></circle>
        <circle class="progress-ring-circle" cx="100" cy="100" r="90" id="progress-circle"></circle>
    </svg>
    <div class="progress-text" id="progress-text">0%</div>
</div>'''
        
        css = f'''
.preloader-progress-circle {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, {primary}, {secondary});
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.5s ease;
}}
.preloader-progress-circle.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.progress-ring {{
    position: relative;
}}
.progress-ring-bg {{
    fill: none;
    stroke: rgba(255,255,255,0.2);
    stroke-width: 8;
}}
.progress-ring-circle {{
    fill: none;
    stroke: white;
    stroke-width: 8;
    stroke-linecap: round;
    stroke-dasharray: 565.48;
    stroke-dashoffset: 565.48;
    transform: rotate(-90deg);
    transform-origin: 50% 50%;
    transition: stroke-dashoffset 0.1s linear;
}}
.progress-text {{
    position: absolute;
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    const circle = document.getElementById('progress-circle');
    const text = document.getElementById('progress-text');
    if (!preloader || !circle || !text) return;
    
    const circumference = 565.48;
    let progress = 0;
    const duration = 2000;
    const interval = 20;
    const steps = duration / interval;
    const increment = 100 / steps;
    
    const timer = setInterval(() => {
        progress += increment;
        if (progress >= 100) {
            progress = 100;
            clearInterval(timer);
            setTimeout(() => {
                preloader.classList.add('loaded');
                setTimeout(() => preloader.remove(), 500);
            }, 300);
        }
        const offset = circumference - (progress / 100) * circumference;
        circle.style.strokeDashoffset = offset;
        text.textContent = Math.floor(progress) + '%';
    }, interval);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_bouncing_balls(self, colores: Dict = None) -> Dict[str, str]:
        """Bolas rebotando"""
        primary = colores.get('primary', '#667eea') if colores else '#667eea'
        
        html = '''
<div id="preloader" class="preloader-balls">
    <div class="balls-container">
        <div class="ball"></div>
        <div class="ball"></div>
        <div class="ball"></div>
    </div>
</div>'''
        
        css = f'''
.preloader-balls {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
    transition: opacity 0.4s ease;
}}
.preloader-balls.loaded {{
    opacity: 0;
    pointer-events: none;
}}
.balls-container {{
    display: flex;
    gap: 10px;
}}
.ball {{
    width: 20px;
    height: 20px;
    background: {primary};
    border-radius: 50%;
    animation: bounce 0.6s ease-in-out infinite alternate;
}}
.ball:nth-child(1) {{ animation-delay: 0s; }}
.ball:nth-child(2) {{ animation-delay: 0.2s; }}
.ball:nth-child(3) {{ animation-delay: 0.4s; }}
@keyframes bounce {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(-40px); }}
}}'''
        
        js = '''
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    setTimeout(() => {
        preloader.classList.add('loaded');
        setTimeout(() => preloader.remove(), 400);
    }, 600);
});'''
        
        return {'html': html, 'css': css, 'js': js}
    
    def generar_preloader_completo(
        self,
        tipo: str = "contador",
        colores: Dict = None,
        logo_url: str = None
    ) -> Dict[str, str]:
        """
        Genera un preloader completo según el tipo
        
        Args:
            tipo: Tipo de preloader (contador, fade, slide-down, etc.)
            colores: Dict con colores del sitio
            logo_url: URL del logo (para tipo logo-animation)
            
        Returns:
            Dict con 'html', 'css', 'js'
        """
        generators = {
            "contador": lambda: self.generar_contador_loading(colores),
            "fade": lambda: self.generar_fade_simple(colores),
            "slide-down": lambda: self.generar_slide_down(colores),
            "logo-animation": lambda: self.generar_logo_animado(colores, logo_url),
            "circle-expand": lambda: self.generar_circle_expand(colores),
            "bars-loading": lambda: self.generar_bars_loading(colores),
            "dots-pulse": lambda: self.generar_dots_pulse(colores),
            "spinning-logo": lambda: self.generar_spinning_logo(colores, logo_url),
            "wave-animation": lambda: self.generar_wave_animation(colores),
            "glitch-effect": lambda: self.generar_glitch_effect(colores),
            "rotating-square": lambda: self.generar_rotating_square(colores),
            "progress-circle": lambda: self.generar_progress_circle(colores),
            "bouncing-balls": lambda: self.generar_bouncing_balls(colores),
        }
        
        return generators.get(tipo, lambda: self.generar_fade_simple(colores))()
    
    def inyectar_en_html(self, html_content: str, preloader_code: Dict[str, str]) -> str:
        """
        Inyecta el código del preloader en un HTML existente
        
        Args:
            html_content: Contenido HTML completo
            preloader_code: Dict con 'html', 'css', 'js'
            
        Returns:
            HTML con preloader inyectado
        """
        # Inyectar CSS en <head>
        if '</head>' in html_content:
            css_injection = f'\n    <style>\n{preloader_code["css"]}\n    </style>\n</head>'
            html_content = html_content.replace('</head>', css_injection)
        
        # Inyectar HTML después de <body>
        if '<body' in html_content:
            # Encontrar el cierre de la etiqueta body
            import re
            body_match = re.search(r'<body[^>]*>', html_content)
            if body_match:
                insert_pos = body_match.end()
                html_content = (
                    html_content[:insert_pos] +
                    preloader_code['html'] +
                    html_content[insert_pos:]
                )
        
        # Inyectar JS antes de </body>
        if '</body>' in html_content:
            js_injection = f'\n    <script>\n{preloader_code["js"]}\n    </script>\n</body>'
            html_content = html_content.replace('</body>', js_injection)
        
        return html_content


def main():
    """Demo de preloaders - Genera todos los 10 estilos"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║          ✨ GENERADOR DE 10 PRELOADERS/ANIMACIONES                  ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    generator = PreloaderGenerator()
    
    print(f"Total de preloaders disponibles: {len(generator.PRELOADERS)}\n")
    for tipo_id, info in generator.PRELOADERS.items():
        print(f"  {tipo_id:20} - {info['nombre']}")
    print()
    
    # Generar ejemplos de TODOS los tipos
    colores = {'primary': '#667eea', 'secondary': '#764ba2'}
    
    # Lista de todos los tipos a generar
    tipos_a_generar = [
        'contador', 'fade', 'slide-down', 
        'circle-expand', 'bars-loading', 'dots-pulse',
        'spinning-logo', 'wave-animation', 'glitch-effect',
        'rotating-square', 'progress-circle', 'bouncing-balls', 'typing-text', 'ripple-effect'
    ]
    
    print("="*70)
    print("Generando ejemplos de preloaders...")
    print("="*70)
    
    # Contador
    contador = generator.generar_contador_loading(colores)
    with open('preloader/preloader_contador_example.html', 'w', encoding='utf-8') as f:
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplo Preloader Contador</title>
    <style>
{contador['css']}
        body {{
            font-family: Arial, sans-serif;
            padding: 2rem;
        }}
        h1 {{ color: #667eea; }}
    </style>
</head>
<body>
{contador['html']}
    <h1>Contenido del Sitio</h1>
    <p>Este contenido aparece después del preloader.</p>
    
    <script>
{contador['js']}
    </script>
</body>
</html>'''
        f.write(html)
    
    print("  ✅ preloader/preloader_contador_example.html")
    
    # Fade simple
    fade = generator.generar_fade_simple(colores)
    with open('preloader/preloader_fade_example.html', 'w', encoding='utf-8') as f:
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplo Preloader Fade</title>
    <style>
{fade['css']}
        body {{ font-family: Arial, sans-serif; padding: 2rem; }}
        h1 {{ color: #667eea; }}
    </style>
</head>
<body>
{fade['html']}
    <h1>Contenido del Sitio</h1>
    <p>Este contenido aparece con fade in.</p>
    
    <script>
{fade['js']}
    </script>
</body>
</html>'''
        f.write(html)
    
    print("  ✅ preloader/preloader_fade_example.html")
    
    # Slide down
    slide = generator.generar_slide_down(colores)
    with open('preloader/preloader_slide_example.html', 'w', encoding='utf-8') as f:
        html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplo Preloader Slide</title>
    <style>
{slide['css']}
        body {{ font-family: Arial, sans-serif; padding: 2rem; }}
        h1 {{ color: #667eea; }}
    </style>
</head>
<body>
{slide['html']}
    <h1>Contenido del Sitio</h1>
    <p>Este contenido se revela con cortinas.</p>
    
    <script>
{slide['js']}
    </script>
</body>
</html>'''
        f.write(html)
    
    print("  ✅ preloader/preloader_slide_example.html")
    
    # Generar el resto
    print("\nGenerando preloaders adicionales...")
    
    for tipo in ['circle-expand', 'bars-loading', 'dots-pulse', 'spinning-logo', 
                 'wave-animation', 'glitch-effect', 'rotating-square', 
                 'progress-circle', 'bouncing-balls', 'typing-text', 'ripple-effect']:
        
        preloader_code = generator.generar_preloader_completo(tipo, colores)
        filename = f'preloader/preloader_{tipo.replace("-", "_")}_example.html'
        
        with open(filename, 'w', encoding='utf-8') as f:
            html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejemplo Preloader {tipo}</title>
    <style>
{preloader_code['css']}
        body {{ font-family: Arial, sans-serif; padding: 2rem; }}
        h1 {{ color: #667eea; }}
    </style>
</head>
<body>
{preloader_code['html']}
    <h1>Preloader: {tipo}</h1>
    <p>Este preloader usa el estilo "{tipo}". Recarga la página para ver la animación de nuevo.</p>
    
    <script>
{preloader_code['js']}
    </script>
</body>
</html>'''
            f.write(html)
        
        print(f"  ✅ {filename}")
    
    print("\n" + "="*70)
    print(f"✅ {len(tipos_a_generar)} Preloaders generados")
    print("="*70)
    print("""
💡 Abre los archivos en tu navegador para ver las animaciones:
   
   Principales (ya generados):
   • preloader/preloader_contador_example.html (contador 0-100%)
   • preloader/preloader_fade_example.html (fade in simple)
   • preloader/preloader_slide_example.html (cortinas que se abren)
   
   Nuevos (7 adicionales):
   • preloader/preloader_circle_expand_example.html
   • preloader/preloader_bars_loading_example.html
   • preloader/preloader_dots_pulse_example.html
   • preloader/preloader_spinning_logo_example.html
   • preloader/preloader_wave_animation_example.html
   • preloader/preloader_glitch_effect_example.html
   • preloader/preloader_rotating_square_example.html
   • preloader/preloader_progress_circle_example.html
   • preloader/preloader_bouncing_balls_example.html
   • preloader/preloader_typing_text_example.html
   • preloader/preloader_ripple_effect_example.html
   
   Servidor: http://localhost:8004/preloader/preloader_[nombre]_example.html
    """)


if __name__ == '__main__':
    main()
