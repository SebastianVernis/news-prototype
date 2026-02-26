#!/usr/bin/env python3
"""
Script para verificar artículos completos y descargar nuevas noticias
Mantiene las noticias antiguas y agrega las nuevas
"""

import json
import requests
import os
from pathlib import Path
from datetime import datetime

# Configuración
NEWS_API_KEY = os.getenv('NEWSAPI_KEY', 'YOUR_NEWSAPI_KEY')
REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))
DATA_DIR = Path(os.getenv("NEWS_DATA_DIR", REPO_ROOT / "data"))
DATA_DIR.mkdir(exist_ok=True)

# Archivo de noticias existentes
EXISTING_NEWS_FILE = DATA_DIR / 'existing_news.json'
NEW_NEWS_FILE = DATA_DIR / f'new_news_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

def load_existing_news():
    """Carga las noticias existentes"""
    if EXISTING_NEWS_FILE.exists():
        with open(EXISTING_NEWS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def download_new_news(query='México', page_size=30):
    """Descarga nuevas noticias desde NewsAPI"""
    print(f"📡 Descargando nuevas noticias para: {query}")
    
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'language': 'es',
        'sortBy': 'publishedAt',
        'pageSize': page_size
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get('articles', [])
        
        print(f"✅ {len(articles)} nuevas noticias descargadas")
        return articles
        
    except Exception as e:
        print(f"⚠️ Error descargando noticias: {e}")
        return []

def get_full_article_content(url):
    """Intenta obtener el contenido completo de un artículo"""
    try:
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remover scripts y estilos
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Extraer párrafos
            paragraphs = soup.find_all('p')
            full_text = ' '.join([p.get_text(strip=True) for p in paragraphs[:20]])
            
            return full_text[:5000] if full_text else None
    except:
        pass
    
    return None

def complete_articles(articles):
    """Completa artículos con contenido full_text si está incompleto"""
    print(f"📝 Verificando contenido completo en {len(articles)} artículos...")
    
    completed_count = 0
    
    for i, article in enumerate(articles):
        content = article.get('content', '') or article.get('full_text', '')
        description = article.get('description', '')
        
        # Si el contenido es muy corto (< 200 chars), intentar obtener más
        if len(content) < 200 and article.get('url'):
            print(f"   Completando artículo {i+1}/{len(articles)}...")
            full_content = get_full_article_content(article['url'])
            
            if full_content:
                article['full_text'] = full_content
                article['content'] = full_content
                completed_count += 1
    
    print(f"✅ {completed_count} artículos completados")
    return articles

def merge_news(existing, new):
    """Combina noticias existentes con nuevas (sin duplicados)"""
    print(f"🔄 Combinando {len(existing)} noticias existentes con {len(new)} nuevas...")
    
    # Crear set de URLs existentes para evitar duplicados
    existing_urls = set([article.get('url', '') for article in existing])
    
    # Agregar solo noticias nuevas
    merged = existing.copy()
    added_count = 0
    
    for article in new:
        if article.get('url') not in existing_urls:
            merged.append(article)
            added_count += 1
    
    print(f"✅ {added_count} noticias nuevas agregadas, total: {len(merged)} artículos")
    return merged

def update_sites_with_news(all_news):
    """Actualiza los 10 sitios con todas las noticias (existentes + nuevas)"""
    print(f"📰 Actualizando 10 sitios con {len(all_news)} noticias...")
    
    # Guardar todas las noticias actualizadas
    with open(EXISTING_NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    with open(NEW_NEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    # Actualizar cada sitio
    for site_num in range(1, 11):
        site_file = SITES_DIR / f'site{site_num}.html'
        
        if not site_file.exists():
            continue
        
        with open(site_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Sección para artículos adicionales
        additional_articles_section = """
    <section class="additional-articles" style="padding:40px 20px;background:#f9f9f9;">
        <div style="max-width:1200px;margin:0 auto;">
            <h2 style="text-align:center;margin-bottom:40px;font-size:2.5em;color:#333;">Más Noticias</h2>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:25px;">
"""
        
        # Agregar artículos adicionales (del 11 al 20)
        for i, article in enumerate(all_news[10:20], 11):
            title = article.get('title', 'Noticia')[:100]
            description = article.get('description', '')[:200]
            full_text = article.get('full_text', article.get('content', ''))[:400]
            author = article.get('author', 'Redacción')
            published = article.get('publishedAt', '')[:10] if article.get('publishedAt') else ''
            image = article.get('urlToImage', 'https://via.placeholder.com/400x250')
            
            additional_articles_section += f"""
                <article style="background:white;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px rgba(0,0,0,0.1);">
                    <img src="{image}" alt="{title[:50]}" style="width:100%;height:200px;object-fit:cover;">
                    <div style="padding:25px;">
                        <span style="background:#27ae60;color:white;padding:4px 12px;border-radius:20px;font-size:0.8em;">NUEVO</span>
                        <h3 style="margin:15px 0 10px 0;font-size:1.2em;line-height:1.4;">{title}</h3>
                        <p style="color:#666;line-height:1.6;margin-bottom:15px;">{description}</p>
                        {(f'<div style="background:#f5f5f5;padding:15px;border-radius:8px;margin-bottom:15px;"><p style="font-size:0.9em;line-height:1.6;color:#444;">{full_text}...</p></div>' if full_text else '')}
                        <div style="display:flex;justify-content:space-between;align-items:center;padding-top:15px;border-top:1px solid #eee;">
                            <span style="font-size:0.85em;color:#888;">Por {author}</span>
                            <span style="font-size:0.85em;color:#888;">{published}</span>
                        </div>
                    </div>
                </article>
"""
        
        additional_articles_section += """
            </div>
        </div>
    </section>
"""
        
        # Insertar antes del footer
        if '</footer>' in content:
            content = content.replace('</footer>', additional_articles_section + '\n    </footer>')
        
        # Guardar sitio actualizado
        with open(site_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Sitio {site_num} actualizado con {len(all_news)} noticias")
    
    print(f"✅ 10 sitios actualizados")

def main():
    print("📰 SISTEMA DE GESTIÓN DE NOTICIAS")
    print("="*60)
    
    # 1. Cargar noticias existentes
    print("\n1. 📂 Cargando noticias existentes...")
    existing_news = load_existing_news()
    print(f"   {len(existing_news)} noticias existentes encontradas")
    
    # 2. Descargar nuevas noticias
    print("\n2. 📡 Descargando nuevas noticias...")
    new_news = download_new_news(query='México', page_size=30)
    
    # 3. Completar artículos con contenido full
    print("\n3. 📝 Completando artículos...")
    new_news = complete_articles(new_news)
    
    # 4. Combinar noticias (mantener viejas + agregar nuevas)
    print("\n4. 🔄 Combinando noticias...")
    all_news = merge_news(existing_news, new_news)
    
    # 5. Actualizar sitios con todas las noticias
    print("\n5. 🌐 Actualizando sitios...")
    update_sites_with_news(all_news)
    
    # Resumen
    print("\n" + "="*60)
    print("✅ PROCESO COMPLETADO")
    print("="*60)
    print(f"📊 Noticias existentes: {len(existing_news)}")
    print(f"📊 Noticias nuevas: {len(new_news)}")
    print(f"📊 Total combinado: {len(all_news)}")
    print(f"🌐 Sitios actualizados: 10")
    print(f"💾 Archivo guardado: {EXISTING_NEWS_FILE}")

if __name__ == "__main__":
    main()
