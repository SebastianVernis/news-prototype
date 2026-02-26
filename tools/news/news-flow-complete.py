#!/usr/bin/env python3
"""
Sistema Completo de Gestión de 10 Sitios de Noticias
Flujo completo: descarga de noticias → parafraseo → gestión de imágenes → edición en worker → despliegue
"""

import os
import json
import requests
import boto3
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import hashlib
import mimetypes
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import random
import re
from text_supervisor import supervise_article

# Cargar variables de entorno
load_dotenv()
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites")).parent

class NewsDownloader:
    """Descargador de noticias desde APIs externas"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')
        self.base_url = 'https://newsapi.org/v2/everything'
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)', 'X-Api-Key': self.api_key}
    
    def fetch_news(self, query='México', language='es', page_size=50):
        """Descarga noticias de NewsAPI"""
        if not self.api_key:
            raise ValueError("Falta la API key de NewsAPI")
        
        params = {
            'q': query,
            'apiKey': self.api_key,
            'language': language,
            'sortBy': 'publishedAt',
            'pageSize': page_size
        }
        
        print(f"📡 Descargando noticias para: {query}")
        response = requests.get(self.base_url, params=params, headers=self.headers)
        
        if response.status_code != 200:
            print(f"⚠️ Error API: {response.status_code} - {response.text}")
            # Devolver noticias de ejemplo si la API falla
            return self.get_sample_news()
        
        articles = response.json()['articles']
        print(f"✅ Descargados {len(articles)} artículos")
        return articles
    
    def get_sample_news(self):
        """Devuelve noticias de ejemplo si la API falla"""
        print("⚠️ Usando noticias de ejemplo (API no disponible)")
        return [
            {
                "source": {"id": "example", "name": "Ejemplo Noticias"},
                "author": "Redacción",
                "title": "Ejemplo de Artículo de Noticia",
                "description": "Este es un artículo de ejemplo para demostrar el sistema de noticias.",
                "url": "https://example.com/noticia-ejemplo",
                "urlToImage": "https://placehold.co/800x450/667eea/ffffff?text=Noticia+Ejemplo",
                "publishedAt": datetime.now().isoformat(),
                "content": "Contenido de ejemplo del artículo de noticias."
            }
        ] * 20  # 20 ejemplos

class NewsParaphraser:
    """Sistema de parafraseo de noticias usando IA"""
    
    def __init__(self):
        self.api_key = os.getenv('BLACKBOX_API_KEY')
        self.api_url = 'https://api.blackbox.ai/chat/completions'
        
    def paraphrase_article(self, article):
        """Parafrasea un artículo usando reglas y supervisa gramática"""
        
        # Parafrasear título
        original_title = article.get('title', '')
        paraphrased_title = self.basic_paraphrase(original_title)
        
        # Parafrasear descripción
        original_desc = article.get('description', '')
        paraphrased_desc = self.basic_paraphrase(original_desc)
        
        # Parafrasear contenido
        original_content = article.get('content', '')
        paraphrased_content = self.basic_paraphrase(original_content)
        
        # Actualizar artículo con versiones parafraseadas
        article['title'] = paraphrased_title
        article['description'] = paraphrased_desc
        article['content'] = paraphrased_content
        
        # Agregar marca de parafraseo
        article['paraphrased'] = True
        article['original_title'] = original_title

        provider = os.getenv("SUPERVISOR_PROVIDER", "")
        model = os.getenv("SUPERVISOR_MODEL", "")
        if provider and model:
            article = supervise_article(article, provider, model)
        
        return article
    
    def basic_paraphrase(self, text):
        """Implementación básica de parafraseo"""
        if not text or len(text) < 10:
            return text
        
        # Patrón simple de parafraseo
        replacements = {
            'presidente': 'mandatario',
            'gobierno': 'administración',
            'política': 'políticas',
            'economía': 'sector económico',
            'país': 'nación',
            'ciudad': 'urbe',
            'mundo': 'planeta',
            'noticia': 'información',
            'informe': 'reporte',
            'declaración': 'afirmación'
        }
        
        paraphrased = text.lower()
        for old, new in replacements.items():
            paraphrased = paraphrased.replace(old, new)
        
        # Capitalizar la primera letra
        if paraphrased:
            paraphrased = paraphrased[0].upper() + paraphrased[1:]
        
        # Agregar un prefijo para indicar que fue parafraseado
        return f"[PARAFRASEADO] {paraphrased}"
    
    def paraphrase_multiple(self, articles, variations_per_article=3):
        """Genera múltiples variaciones de cada artículo"""
        all_articles = []
        
        for article in articles:
            # Artículo original
            all_articles.append(article)
            
            # Variaciones parafraseadas
            for i in range(variations_per_article):
                variation = self.paraphrase_article(article.copy())
                variation['variation_number'] = i + 1
                variation['title'] = f"{variation['title']} (Variación {i + 1})"
                all_articles.append(variation)
        
        return all_articles

class R2ImageManager:
    """Gestor de imágenes para R2 Cloudflare"""
    
    def __init__(self):
        # Cargar variables de entorno
        self.account_id = os.getenv('CF_ACCOUNT_ID')
        self.access_key_id = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('NEWS_IMAGES_BUCKET', 'news-images')
        
        # Validar que tengamos las credenciales necesarias
        if not all([self.account_id, self.access_key_id, self.secret_access_key]):
            print("⚠️ Advertencia: Credenciales de R2 no configuradas. Usando imágenes de ejemplo.")
            self.r2_available = False
            return
        
        self.r2_available = True
        
        # Endpoint de R2
        self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
        
        # Inicializar cliente S3 para R2
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        )
        
        # Directorio temporal para descargas
        self.download_dir = Path("/tmp/news_image_downloads")
        self.download_dir.mkdir(exist_ok=True)
    
    def download_image(self, url, local_filename=None):
        """Descarga una imagen desde una URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Generar nombre de archivo si no se proporciona
            if not local_filename:
                parsed_url = urlparse(url)
                filename = Path(parsed_url.path).name
                if not filename or '.' not in filename:
                    # Generar nombre basado en hash si no hay extensión
                    ext = mimetypes.guess_extension(response.headers.get('content-type', 'image/jpeg')) or '.jpg'
                    filename = f"image_{hashlib.md5(url.encode()).hexdigest()}{ext}"
                
                local_filename = self.download_dir / filename
            
            # Guardar imagen localmente
            with open(local_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Imagen descargada: {url} -> {local_filename}")
            return str(local_filename)
            
        except Exception as e:
            print(f"❌ Error descargando imagen {url}: {e}")
            return None
    
    def upload_to_r2(self, local_file_path, object_name=None):
        """Sube una imagen a R2 y devuelve la URL pública"""
        if not self.r2_available:
            # Si R2 no está disponible, devolver la URL original
            print("⚠️ R2 no disponible, usando imagen original")
            return local_file_path  # En este caso, sería la URL original
        
        try:
            # Generar nombre de objeto si no se proporciona
            if not object_name:
                file_ext = Path(local_file_path).suffix
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_id = hashlib.md5(f"{timestamp}_{Path(local_file_path).stem}".encode()).hexdigest()[:8]
                object_name = f"news-images/{timestamp}_{unique_id}{file_ext}"
            
            # Detectar tipo MIME
            mime_type, _ = mimetypes.guess_type(local_file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            
            # Subir archivo a R2
            self.s3_client.upload_file(
                local_file_path,
                self.bucket_name,
                object_name,
                ExtraArgs={
                    'ContentType': mime_type,
                    'CacheControl': 'public, max-age=31536000'  # Cache por 1 año
                }
            )
            
            # Generar URL pública
            public_url = f"https://{self.bucket_name}.{self.account_id}.r2.cloudflarestorage.com/{object_name}"
            print(f"✅ Imagen subida a R2: {public_url}")
            return public_url
            
        except ClientError as e:
            print(f"❌ Error subiendo imagen a R2: {e}")
            return local_file_path  # Devolver URL original si falla
    
    def process_article_images(self, articles):
        """Procesa las imágenes de los artículos"""
        if not self.r2_available:
            print("⚠️ Procesamiento de imágenes R2 deshabilitado (credenciales no configuradas)")
            return articles
        
        print(f"🖼️  Procesando imágenes para {len(articles)} artículos...")
        
        processed_articles = []
        image_mapping = {}
        
        for i, article in enumerate(articles):
            print(f"   Procesando imagen para artículo {i+1}/{len(articles)}: {article.get('title', 'Sin título')[:50]}...")
            
            # Procesar imagen principal
            image_url = article.get('urlToImage') or article.get('imageUrl')
            if image_url and image_url.startswith('http'):
                print(f"     Descargando imagen: {image_url}")
                
                # Descargar imagen
                local_path = self.download_image(image_url)
                if local_path:
                    # Subir a R2
                    r2_url = self.upload_to_r2(local_path)
                    
                    if r2_url:
                        # Actualizar artículo con nueva URL
                        article['imageUrl'] = r2_url
                        image_mapping[image_url] = r2_url
                        
                        # Limpiar archivo local
                        Path(local_path).unlink(missing_ok=True)
            
            processed_articles.append(article)
        
        print(f"✅ Procesadas imágenes para {len(processed_articles)} artículos")
        return processed_articles, image_mapping

class NewsEditorWorker:
    """Sistema de edición de noticias en el worker"""
    
    def __init__(self):
        self.backend_url = "https://noticias-hoy.pages.dev/api"  # URL del backend principal
    
    def create_editable_article(self, article_data):
        """Crea un artículo editable en el sistema"""
        # En un sistema real, esto haría una llamada al backend para crear/editar artículos
        # Por ahora, simplemente devuelve el artículo con metadatos de edición
        
        editable_article = article_data.copy()
        editable_article['editable'] = True
        editable_article['last_edited'] = datetime.now().isoformat()
        editable_article['editor_tracking'] = True
        
        return editable_article
    
    def update_article_in_backend(self, article_id, updated_data):
        """Actualiza un artículo en el backend (simulado)"""
        # En un sistema real, esto haría una llamada PATCH/PUT al backend
        print(f"✏️ Artículo {article_id} actualizado en backend (simulado)")
        return {"success": True, "article_id": article_id, "updated_fields": list(updated_data.keys())}
    
    def bulk_update_articles(self, articles):
        """Actualiza múltiples artículos en el backend"""
        results = []
        for i, article in enumerate(articles):
            # Simular actualización
            result = {
                "article_id": article.get('id', i),
                "status": "updated",
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)
            print(f"   Artículo {i+1}/{len(articles)} actualizado")
        
        return results

class SiteGenerator:
    """Generador de sitios de noticias con diferentes diseños"""
    
    def __init__(self):
        self.site_names = [
            "Vanguardia Tecámac",
            "Tecámac al Momento", 
            "Radar de Tecámac",
            "Tecámac Meridiano",
            "Radio Cinco Noticias",
            "México Informado",
            "Noticias Objetivo",
            "CBN Noticias",
            "Central México",
            "TV México"
        ]
        
        self.taglines = [
            "Tu fuente confiable de información en Tecámac",
            "Noticias frescas y actualizadas de Tecámac",
            "Lo que pasa en Tecámac, primero aquí",
            "La verdad detrás de cada noticia",
            "Cinco minutos, mil historias",
            "Información que te concierne",
            "Noticias sin filtro ni sesgo",
            "Comunicación que conecta",
            "Centro del acontecer nacional",
            "Televisión de noticias en vivo"
        ]
    
    def generate_site_html(self, site_index, articles):
        """Genera HTML para un sitio específico"""
        site_name = self.site_names[site_index]
        tagline = self.taglines[site_index % len(self.taglines)]
        
        # Seleccionar artículos para este sitio (usar diferentes subconjuntos)
        site_articles = articles[site_index::len(self.site_names)]  # Distribuir artículos entre sitios
        if not site_articles:
            site_articles = articles[:10]  # Asegurar al menos 10 artículos
        
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_name} - {tagline}</title>
    <meta name="description" content="{tagline}">
    <meta name="keywords" content="noticias, {site_name.lower()}, mexico, tecamac, ultima hora">
    <link rel="stylesheet" href="styles/site{site_index+1}.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="site-layout site-{site_index+1}">
    <header class="main-header">
        <div class="container">
            <div class="logo-area">
                <h1 class="site-logo">{site_name}</h1>
                <p class="site-tagline">{tagline}</p>
            </div>
            <nav class="main-nav">
                <a href="#" class="nav-link active">Inicio</a>
                <a href="#" class="nav-link">Nacional</a>
                <a href="#" class="nav-link">Internacional</a>
                <a href="#" class="nav-link">Política</a>
                <a href="#" class="nav-link">Economía</a>
                <a href="#" class="nav-link">Deportes</a>
            </nav>
        </div>
    </header>

    <main class="main-content">
        <section class="breaking-news">
            <div class="ticker-label">NOTICIAS DE ÚLTIMA HORA:</div>
            <div class="ticker-content">
                <marquee behavior="scroll" direction="left">
                    <span class="ticker-item">¡ÚLTIMO MOMENTO! Gobierno anuncia nuevas medidas económicas</span>
                    <span class="ticker-separator">•</span>
                    <span class="ticker-item">Incrementa popularidad de partido político en encuestas</span>
                    <span class="ticker-separator">•</span>
                    <span class="ticker-item">Celebran avances en negociaciones comerciales internacionales</span>
                </marquee>
            </div>
        </section>

        <section class="featured-section">
            <div class="container">
                <h2 class="section-title">Destacado</h2>
                <div class="featured-grid">
"""
        
        # Agregar artículos destacados
        for i, article in enumerate(site_articles[:3]):  # Primeros 3 como destacados
            html_content += f"""
                    <article class="featured-card">
                        <div class="card-image">
                            <img src="{article.get('imageUrl', article.get('urlToImage', 'https://placehold.co/600x400'))}" alt="{article.get('title', 'Noticia')}">
                        </div>
                        <div class="card-content">
                            <span class="category">{article.get('source', {}).get('name', 'General')}</span>
                            <h3><a href="article-{i+1}.html">{article.get('title', 'Título no disponible')}</a></h3>
                            <p>{article.get('description', 'Descripción no disponible')[:150]}...</p>
                            <div class="article-meta">
                                <span class="author">{article.get('author', 'Autor desconocido')}</span>
                                <span class="date">{article.get('publishedAt', 'Fecha desconocida')[:10]}</span>
                            </div>
                        </div>
                    </article>
"""
        
        html_content += """
                </div>
            </div>
        </section>

        <section class="news-section">
            <div class="container">
                <h2 class="section-title">Últimas Noticias</h2>
                <div class="news-grid">
"""
        
        # Agregar artículos restantes
        for i, article in enumerate(site_articles[3:], 3):  # Desde el 4to artículo
            html_content += f"""
                    <article class="news-card">
                        <div class="card-image">
                            <img src="{article.get('imageUrl', article.get('urlToImage', 'https://placehold.co/400x250'))}" alt="{article.get('title', 'Noticia')}" loading="lazy">
                        </div>
                        <div class="card-content">
                            <span class="category">{article.get('source', {}).get('name', 'General')}</span>
                            <h3><a href="article-{i+1}.html">{article.get('title', 'Título no disponible')}</a></h3>
                            <p>{article.get('description', 'Descripción no disponible')[:120]}...</p>
                            <div class="article-meta">
                                <span class="author">{article.get('author', 'Autor desconocido')}</span>
                                <span class="date">{article.get('publishedAt', 'Fecha desconocida')[:10]}</span>
                            </div>
                        </div>
                    </article>
"""
        
        html_content += """
                </div>
            </div>
        </section>
    </main>

    <footer class="main-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>Sobre Nosotros</h4>
                    <p>""" + tagline + """</p>
                </div>
                <div class="footer-section">
                    <h4>Categorías</h4>
                    <ul>
                        <li><a href="#">Política</a></li>
                        <li><a href="#">Economía</a></li>
                        <li><a href="#">Deportes</a></li>
                        <li><a href="#">Cultura</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Enlaces Rápidos</h4>
                    <ul>
                        <li><a href="#">Acerca de</a></li>
                        <li><a href="#">Contacto</a></li>
                        <li><a href="#">Privacidad</a></li>
                        <li><a href="#">Términos</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 {site_name}. Todos los derechos reservados.</p>
            </div>
        </div>
    </footer>

    <script src="js/site-{site_index+1}.js"></script>
</body>
</html>"""
        
        return html_content

class NewsManagementSystem:
    """Sistema completo de gestión de noticias"""
    
    def __init__(self):
        self.downloader = NewsDownloader()
        self.paraphraser = NewsParaphraser()
        self.image_manager = R2ImageManager()
        self.editor_worker = NewsEditorWorker()
        self.site_generator = SiteGenerator()
        
        # Directorios
        self.output_dir = Path(os.getenv("NEWS_SITES_ROOT", DEFAULT_OUTPUT_DIR))
        self.output_dir.mkdir(exist_ok=True)
        
        self.sites_dir = self.output_dir / "sites"
        self.sites_dir.mkdir(exist_ok=True)
        
        self.articles_dir = self.output_dir / "articles"
        self.articles_dir.mkdir(exist_ok=True)
    
    def run_complete_flow(self):
        """Ejecuta el flujo completo de gestión de noticias"""
        print("📰 Iniciando sistema completo de gestión de noticias")
        print("="*70)
        
        # 1. Descargar noticias
        print("\n1. 📥 Descargando noticias...")
        raw_articles = self.downloader.fetch_news(query="México", page_size=50)
        
        # 2. Parafrasear noticias
        print(f"\n2. 🔄 Parafraseando {len(raw_articles)} artículos...")
        paraphrased_articles = []
        for i, article in enumerate(raw_articles):
            print(f"   Parafraseando artículo {i+1}/{len(raw_articles)}...")
            paraphrased_article = self.paraphraser.paraphrase_article(article)
            paraphrased_articles.append(paraphrased_article)
        
        # 3. Procesar imágenes
        print(f"\n3. 🖼️  Procesando imágenes para {len(paraphrased_articles)} artículos...")
        processed_articles, image_mapping = self.image_manager.process_article_images(paraphrased_articles)
        
        # 4. Hacer artículos editables
        print(f"\n4. ✏️  Convirtiendo {len(processed_articles)} artículos en editables...")
        editable_articles = []
        for i, article in enumerate(processed_articles):
            editable_article = self.editor_worker.create_editable_article(article)
            editable_articles.append(editable_article)
            print(f"   Artículo {i+1}/{len(processed_articles)} marcado como editable")
        
        # 5. Generar 10 sitios diferentes
        print(f"\n5. 🏗️  Generando 10 sitios de noticias diferentes...")
        for site_idx in range(10):
            print(f"   Generando sitio {site_idx+1}/10: {self.site_generator.site_names[site_idx]}...")
            
            # Generar HTML para el sitio
            site_html = self.site_generator.generate_site_html(site_idx, editable_articles)
            
            # Guardar archivo HTML
            site_file = self.sites_dir / f"site_{site_idx+1}.html"
            with open(site_file, 'w', encoding='utf-8') as f:
                f.write(site_html)
            
            print(f"   ✅ Sitio {site_idx+1} guardado: {site_file}")
        
        # 6. Guardar artículos en formato JSON para el backend
        print(f"\n6. 💾 Guardando artículos en formato backend...")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        articles_file = self.articles_dir / f"articles_{timestamp}.json"
        
        # Preparar artículos en formato compatible con el backend
        backend_articles = []
        for i, article in enumerate(editable_articles):
            backend_article = {
                'id': i + 1,
                'title': article.get('title', ''),
                'slug': re.sub(r'[^a-zA-Z0-9]', '-', article.get('title', '').lower())[:100],
                'content': article.get('content', '') or article.get('description', ''),
                'excerpt': article.get('description', '')[:300],
                'category': random.choice(['nacional', 'internacional', 'politica', 'economia', 'deportes', 'cultura']),
                'author': article.get('author', 'Redacción'),
                'publishedAt': article.get('publishedAt', datetime.now().isoformat()),
                'updatedAt': datetime.now().isoformat(),
                'imageUrl': article.get('imageUrl', article.get('urlToImage', '')),
                'featured': i < 5,  # Primeros 5 como destacados
                'views': random.randint(100, 10000),
                'tags': ['noticias', 'mexico', 'actualidad']
            }
            backend_articles.append(backend_article)
        
        with open(articles_file, 'w', encoding='utf-8') as f:
            json.dump(backend_articles, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ {len(backend_articles)} artículos guardados para backend: {articles_file}")
        
        # 7. Actualizar backend con nuevos artículos (simulado)
        print(f"\n7. 🔄 Actualizando backend con nuevos artículos...")
        update_results = self.editor_worker.bulk_update_articles(backend_articles[:10])  # Actualizar primeros 10
        print(f"   ✅ {len(update_results)} artículos actualizados en backend")
        
        # 8. Generar reporte
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_articles_processed': len(editable_articles),
            'total_sites_generated': 10,
            'images_processed': len(image_mapping),
            'paraphrased_articles': len([a for a in editable_articles if a.get('paraphrased')]),
            'sites': self.site_generator.site_names,
            'image_mapping_sample': dict(list(image_mapping.items())[:3]) if image_mapping else {},
            'article_sample': backend_articles[:2]  # Primeros 2 artículos como ejemplo
        }

        report_file = self.output_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n8. 📊 Reporte generado: {report_file}")
        
        # Resumen
        print("\n" + "="*70)
        print("✅ SISTEMA DE GESTIÓN DE NOTICIAS COMPLETADO EXITOSAMENTE")
        print("="*70)
        print(f"📰 Artículos procesados: {len(editable_articles)}")
        print(f"🔄 Artículos parafraseados: {report['paraphrased_articles']}")
        print(f"🖼️  Imágenes procesadas: {report['images_processed']}")
        print(f"🌍 Sitios generados: {report['total_sites_generated']}")
        print(f"📝 Artículos guardados para backend: {len(backend_articles)}")
        print(f"📋 Reporte detallado: {report_file}")
        print("="*70)

        return report

def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(description="Sistema completo de gestión")
    parser.add_argument("--supervisor-provider", default=os.getenv("SUPERVISOR_PROVIDER", ""))
    parser.add_argument("--supervisor-model", default=os.getenv("SUPERVISOR_MODEL", ""))
    args = parser.parse_args()

    os.environ["SUPERVISOR_PROVIDER"] = args.supervisor_provider or ""
    os.environ["SUPERVISOR_MODEL"] = args.supervisor_model or ""

    print("🚀 Sistema Completo de Gestión de 10 Sitios de Noticias")
    print("   - Descarga de noticias")
    print("   - Parafraseo con reglas + supervisión ligera") 
    print("   - Gestión de imágenes en R2")
    print("   - Edición en backend worker")
    print("   - Generación de sitios con diseños únicos")
    
    try:
        # Inicializar sistema
        news_system = NewsManagementSystem()
        
        # Ejecutar flujo completo
        report = news_system.run_complete_flow()
        
        print(f"\n🎉 Sistema completado exitosamente!")
        print(f"📁 Sitios generados en: {news_system.sites_dir}")
        print(f"📄 Artículos backend en: {news_system.articles_dir}")
        print(f"📊 Reporte en: {report['timestamp']}")
        
    except Exception as e:
        print(f"\n❌ Error en el sistema de gestión de noticias: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
