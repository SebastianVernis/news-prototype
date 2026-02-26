#!/usr/bin/env python3
"""
Generador de Sitios Dinámicos
Crea sitios HTML que extraen artículos parafraseados directamente desde la base de datos (vía API).
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "sites"
TEMPLATES_DIR = REPO_ROOT / "public" / "templates" / "css"

# Configuración de los 9 sitios
SITES_CONFIG = [
    {"id": 2, "name": "Tecámac al Momento", "domain": "tecamac-momento.pages.dev", "api_site": "tecamac-momento"},
    {"id": 3, "name": "Radar Tecámac", "domain": "radar-tecamac.pages.dev", "api_site": "radar-tecamac"},
    {"id": 4, "name": "Tecámac Meridiano", "domain": "tecamac-meridiano.pages.dev", "api_site": "tecamac-meridiano"},
    {"id": 5, "name": "Radio Cinco", "domain": "radio-cinco.pages.dev", "api_site": "radio-cinco"},
    {"id": 6, "name": "México Informado", "domain": "mexico-informado.pages.dev", "api_site": "mexico-informado"},
    {"id": 7, "name": "Noticias Objetivo", "domain": "noticias-objetivo.pages.dev", "api_site": "noticias-objetivo"},
    {"id": 8, "name": "CBN Noticias", "domain": "cbn-noticias.pages.dev", "api_site": "cbn-noticias"},
    {"id": 9, "name": "Central México", "domain": "central-mexico.pages.dev", "api_site": "central-mexico"},
    {"id": 10, "name": "TV México", "domain": "tv-mexico.pages.dev", "api_site": "tv-mexico"}
]

def slugify(value):
    import re
    return re.sub(r'[-\s]+', '-', re.sub(r'[^\w\s-]', '', value.strip().lower())).strip('-')

def generate_site_html(site_config):
    template_id = (site_config["id"] % 10) + 1
    api_site = site_config["api_site"]
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_config['name']} - Noticias de Hoy</title>
    <link rel="stylesheet" href="templates/css/template{template_id}.css">
    <style>
        .loading-overlay {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: white; display: flex; justify-content: center; align-items: center;
            z-index: 1000; transition: opacity 0.5s;
        }}
        .hidden {{ opacity: 0; pointer-events: none; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; padding: 2rem; }}
        .news-card {{ border: 1px solid #eee; border-radius: 8px; overflow: hidden; transition: transform 0.3s; }}
        .news-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        .news-card img {{ width: 100%; height: 200px; object-fit: cover; }}
        .news-card-content {{ padding: 1.5rem; }}
        .news-card h3 {{ margin-top: 0; font-size: 1.25rem; color: #333; }}
        .news-card p {{ color: #666; font-size: 0.9rem; line-height: 1.5; }}
        .category-badge {{ background: #667eea; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div id="loader" class="loading-overlay">
        <h2>Cargando noticias...</h2>
    </div>

    <header class="header">
        <div class="container">
            <div class="logo">
                <h1>{site_config['name']}</h1>
                <p class="tagline">Tu fuente confiable de información</p>
            </div>
            <nav class="nav">
                <a href="/" class="nav-link active">Inicio</a>
                <a href="#" class="nav-link">Nacional</a>
                <a href="#" class="nav-link">Internacional</a>
                <a href="#" class="nav-link">Política</a>
            </nav>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <h2 class="section-title">Últimas Noticias Parafraseadas</h2>
            <div id="news-container" class="news-grid">
                <!-- Las noticias se cargarán aquí dinámicamente -->
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; {datetime.now().year} {site_config['name']}. Todos los derechos reservados.</p>
            <p><small>Contenido extraído directamente de la base de datos centralizada.</small></p>
        </div>
    </footer>

    <script>
        const API_BASE = 'https://news-api.news-website.workers.dev/api'; // Cambiar por la URL real de tu Worker
        const SITE_ID = '{api_site}';

        async function fetchNews() {{
            try {{
                const response = await fetch(`${{API_BASE}}/articles?site=${{SITE_ID}}&limit=12`);
                const data = await response.json();
                renderNews(data.articles || []);
            }} catch (error) {{
                console.error('Error fetching news:', error);
                document.getElementById('news-container').innerHTML = '<p>Error al cargar las noticias. Por favor intenta más tarde.</p>';
            }} finally {{
                document.getElementById('loader').classList.add('hidden');
            }}
        }}

        function renderNews(articles) {{
            const container = document.getElementById('news-container');
            if (articles.length === 0) {{
                container.innerHTML = '<p>No hay noticias disponibles para este sitio en este momento.</p>';
                return;
            }}

            container.innerHTML = articles.map(article => `
                <article class="news-card">
                    <img src="${{article.imageUrl || '../assets/images/fallback-1.svg'}}" alt="${{article.title}}">
                    <div class="news-card-content">
                        <span class="category-badge">${{article.category}}</span>
                        <h3>${{article.title}}</h3>
                        <p>${{article.excerpt}}</p>
                        <div class="meta">
                            <small>Por ${{article.author}} | ${{new Date(article.publishedAt).toLocaleDateString()}}</small>
                        </div>
                    </div>
                </article>
            `).join('');
        }}

        document.addEventListener('DOMContentLoaded', fetchNews);
    </script>
</body>
</html>
"""
    return html

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Generando {len(SITES_CONFIG)} sitios dinámicos...")
    
    for config in SITES_CONFIG:
        site_slug = slugify(config["domain"].replace(".pages.dev", ""))
        site_dir = OUTPUT_DIR / site_slug
        site_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar CSS
        templates_css_dir = site_dir / 'templates' / 'css'
        templates_css_dir.mkdir(parents=True, exist_ok=True)
        if TEMPLATES_DIR.exists():
            for css_file in TEMPLATES_DIR.glob('*.css'):
                (templates_css_dir / css_file.name).write_bytes(css_file.read_bytes())
        
        # Generar HTML
        html_content = generate_site_html(config)
        (site_dir / "index.html").write_text(html_content, encoding="utf-8")
        
        print(f"✅ Sitio generado: {config['name']} -> sites/{site_slug}/index.html")

    print("
🎉 Proceso completado exitosamente.")

if __name__ == "__main__":
    main()
