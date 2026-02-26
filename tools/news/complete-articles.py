#!/usr/bin/env python3
"""
Script para completar los artículos con contenido full_text
"""

import json
import os
from pathlib import Path
import re

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("NEWS_DATA_DIR", REPO_ROOT / "data"))
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))

# Cargar datos de noticias
NEWS_FILE = os.getenv("NEWS_FILE")
if not NEWS_FILE:
    candidates = sorted(DATA_DIR.glob("*.json"))
    NEWS_FILE = str(candidates[-1]) if candidates else None

if not NEWS_FILE:
    raise FileNotFoundError(
        "No se encontró archivo de noticias. Usa NEWS_FILE o coloca JSON en data/."
    )

# Cargar artículos
with open(NEWS_FILE, 'r', encoding='utf-8') as f:
    news_data = json.load(f)

print(f"📰 Artículos cargados: {len(news_data)}")

# Crear diccionario de artículos completos
articles_db = {}
for i, article in enumerate(news_data):
    articles_db[i] = {
        'title': article.get('title', 'Título no disponible'),
        'description': article.get('description', ''),
        'full_text': article.get('full_text', article.get('content', '')),
        'author': article.get('author', 'Redacción'),
        'url': article.get('url', '#'),
        'publishedAt': article.get('publishedAt', '')[:10] if article.get('publishedAt') else ''
    }

def update_site_articles(site_num):
    """Actualiza los artículos de un sitio con contenido completo"""
    site_file = SITES_DIR / f'site{site_num}.html'
    
    if not site_file.exists():
        print(f"⚠️ Archivo no encontrado: {site_file}")
        return False
    
    with open(site_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Actualizar cada artículo con contenido completo
    for i, article_data in articles_db.items():
        # Solo usar primeros 10 artículos por sitio
        if i > 9:
            break
        
        # Crear artículo completo expandido
        full_article = f"""
        <article class="news-card" id="article-{i+1}">
            <div class="card-image-wrapper">
                <img src="assets/images/article_article_{i+1}_{i+1}.jpg" alt="{article_data['title'][:50]}" class="card-image" loading="lazy">
            </div>
            <div class="card-content">
                <span class="category-badge">NOTICIA</span>
                <h3 class="card-title">{article_data['title']}</h3>
                <p class="card-excerpt">{article_data['description']}</p>
                <div class="full-article-content" style="margin-top:15px;padding:15px;background:#f9f9f9;border-left:3px solid #3498db;">
                    <p style="line-height:1.8;color:#333;">{article_data['full_text'][:500]}...</p>
                </div>
                <div class="card-meta">
                    <span class="meta-author">Por {article_data['author']}</span>
                    <span class="meta-date">{article_data['publishedAt']}</span>
                </div>
                <a href="{article_data['url']}" target="_blank" class="read-more" style="display:inline-block;margin-top:10px;padding:8px 16px;background:#3498db;color:white;text-decoration:none;border-radius:4px;">Leer nota completa</a>
            </div>
        </article>
"""
        
        # Reemplazar artículo en el contenido (búsqueda simple)
        # Nota: Esto es una simplificación - en producción se necesitaría un parser HTML real
    
    # Agregar sección de artículos completos antes del footer
    articles_section = """
    <section class="complete-articles" style="padding:40px 20px;max-width:1200px;margin:0 auto;">
        <h2 style="text-align:center;margin-bottom:40px;font-size:2.5em;color:#333;">Artículos Completos</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:30px;">
"""
    
    # Agregar artículos completos
    for i, article_data in list(articles_db.items())[:6]:  # Primeros 6 artículos
        articles_section += f"""
            <article style="background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.1);transition:transform 0.3s;">
                <img src="assets/images/article_article_{i+1}_{i+1}.jpg" alt="{article_data['title'][:50]}" style="width:100%;height:220px;object-fit:cover;">
                <div style="padding:25px;">
                    <span style="background:#3498db;color:white;padding:4px 12px;border-radius:20px;font-size:0.8em;">NOTICIA</span>
                    <h3 style="margin:15px 0 10px 0;font-size:1.3em;line-height:1.4;">{article_data['title']}</h3>
                    <p style="color:#666;line-height:1.7;margin-bottom:15px;">{article_data['description']}</p>
                    <div style="background:#f5f5f5;padding:15px;border-radius:8px;margin-bottom:15px;">
                        <p style="font-size:0.9em;line-height:1.6;color:#444;">{article_data['full_text'][:300]}...</p>
                    </div>
                    <div style="display:flex;justify-content:space-between;align-items:center;padding-top:15px;border-top:1px solid #eee;">
                        <span style="font-size:0.85em;color:#888;">Por {article_data['author']}</span>
                        <span style="font-size:0.85em;color:#888;">{article_data['publishedAt']}</span>
                    </div>
                </div>
            </article>
"""
    
    articles_section += """
        </div>
    </section>
"""
    
    # Insertar antes del footer
    if '</footer>' in content:
        content = content.replace('</footer>', articles_section + '\n    </footer>')
    
    # Guardar archivo actualizado
    with open(site_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Sitio {site_num} actualizado con artículos completos")
    return True

def main():
    print("📝 Completando artículos en los 10 sitios...")
    print("="*60)
    
    # Actualizar los 10 sitios
    for i in range(1, 11):
        update_site_articles(i)
    
    print("="*60)
    print("✅ Los 10 sitios actualizados con artículos completos")
    print(f"📊 Total de artículos disponibles: {len(articles_db)}")

if __name__ == "__main__":
    main()
