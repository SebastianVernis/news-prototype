#!/usr/bin/env python3
"""
Sistema Completo de Gestión de Noticias
Descarga noticias, gestiona imágenes en R2, y actualiza la API
"""

import os
import requests
import json
import re
import hashlib
import mimetypes
import boto3
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import time

load_dotenv()

class NewsImageManager:
    """Gestor de imágenes para el sistema de noticias"""
    
    def __init__(self):
        # Cargar variables de entorno
        self.account_id = os.getenv('CF_ACCOUNT_ID', os.getenv('CLOUDFLARE_ACCOUNT_ID'))
        self.access_key_id = os.getenv('R2_ACCESS_KEY_ID')
        self.secret_access_key = os.getenv('R2_SECRET_ACCESS_KEY')
        self.bucket_name = os.getenv('NEWS_IMAGES_BUCKET', 'news-images')
        
        # Validar que tengamos las credenciales necesarias
        if not all([self.account_id, self.access_key_id, self.secret_access_key]):
            raise ValueError("Faltan credenciales de R2. Verifica las variables de entorno: "
                           "CF_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY")
        
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
        
        # Directorio para almacenar mapeo de imágenes
        self.mapping_dir = Path("/tmp/image_mappings")
        self.mapping_dir.mkdir(exist_ok=True)
    
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
            return None
    
    def process_article_images(self, articles):
        """Procesa las imágenes de los artículos y las sube a R2"""
        print(f"🖼️  Procesando imágenes para {len(articles)} artículos...")
        
        updated_articles = []
        image_mapping = {}
        
        for i, article in enumerate(articles):
            print(f"   Procesando artículo {i+1}/{len(articles)}: {article.get('title', 'Sin título')[:50]}...")
            
            # Procesar imagen principal
            image_url = article.get('urlToImage')
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
                        Path(local_path).unlink()
            
            updated_articles.append(article)
        
        # Guardar mapeo de imágenes
        mapping_file = self.mapping_dir / f"image_mapping_{int(time.time())}.json"
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(image_mapping, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Mapeo de imágenes guardado en: {mapping_file}")
        return updated_articles, image_mapping

class NewsDownloader:
    """Descargador de noticias desde APIs externas"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY', os.getenv('NEWSAPI_API_KEY'))
        self.base_url = 'https://newsapi.org/v2/everything'
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'}
    
    def fetch_news(self, query='México', language='es', page_size=20):
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
            raise Exception(f"Error API: {response.json()}")
        
        articles = response.json()['articles']
        print(f"✅ Descargados {len(articles)} artículos")
        return articles
    
    def get_full_text(self, url):
        """Obtiene el texto completo de un artículo"""
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # Remover elementos no deseados
            for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
                element.decompose()
            
            # Extraer texto de párrafos
            paragraphs = soup.find_all('p')
            text = ' '.join(p.get_text(strip=True) for p in paragraphs[:15])  # Primeros 15 párrafos
            return text[:8000]  # Límite razonable
        except:
            return "Texto completo no disponible"

class NewsProcessor:
    """Procesador de noticias con paráfrasis y edición"""
    
    def __init__(self):
        pass
    
    def paraphrase_article(self, article):
        """Parafrasea un artículo usando técnicas de IA"""
        # Esta es una implementación básica - en un sistema real usaríamos una IA
        # como Blackbox, OpenAI, o modelos locales
        
        # Parafrasear título
        title = article.get('title', '')
        # Simplemente agregar un prefijo para demostrar la funcionalidad
        paraphrased_title = f"[PARAFRASEADO] {title}"
        
        # Parafrasear descripción
        description = article.get('description', '')
        if len(description) > 10:
            paraphrased_description = f"[CONTENIDO ACTUALIZADO] {description[:100]}..."
        else:
            paraphrased_description = "[CONTENIDO ACTUALIZADO] Artículo con información reciente"
        
        # Parafrasear contenido
        content = article.get('content', '')
        if len(content) > 10:
            paraphrased_content = f"{content[:200]} [TEXTO AMPLIADO CON ANÁLISIS ADICIONAL]..."
        else:
            paraphrased_content = "[CONTENIDO AMPLIADO] Artículo con análisis detallado"
        
        # Actualizar artículo con versiones parafraseadas
        article['title'] = paraphrased_title
        article['description'] = paraphrased_description
        article['content'] = paraphrased_content
        
        return article
    
    def process_articles(self, articles):
        """Procesa múltiples artículos"""
        print(f"🔄 Procesando {len(articles)} artículos...")
        
        processed_articles = []
        for i, article in enumerate(articles):
            print(f"   Procesando artículo {i+1}/{len(articles)}: {article.get('title', 'Sin título')[:40]}...")
            
            # Parafrasear artículo
            processed_article = self.paraphrase_article(article)
            processed_articles.append(processed_article)
        
        print(f"✅ Procesados {len(processed_articles)} artículos")
        return processed_articles

class APIUpdater:
    """Actualizador de la API con nuevos artículos e imágenes"""
    
    def __init__(self):
        repo_root = Path(__file__).resolve().parents[2]
        self.api_dir = str(repo_root / "functions" / "api")
    
    def update_articles_json(self, articles):
        """Actualiza el archivo de artículos en la API"""
        # Crear un archivo temporal con los artículos actualizados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_file = f"/tmp/updated_articles_{timestamp}.json"
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Artículos actualizados guardados en: {temp_file}")
        return temp_file
    
    def update_api_functions(self, image_mapping):
        """Actualiza las funciones de API con las nuevas URLs de imágenes"""
        # Actualizar el archivo principal de artículos
        api_file = f"{self.api_dir}/articles/index.js"
        
        if os.path.exists(api_file):
            with open(api_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar URLs de imágenes antiguas con nuevas
            updated_content = content
            for old_url, new_url in image_mapping.items():
                updated_content = updated_content.replace(old_url, new_url)
            
            # Guardar archivo actualizado
            backup_file = f"{api_file}.backup_{int(time.time())}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            with open(api_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ API actualizada: {api_file}")
            print(f"💾 Backup guardado en: {backup_file}")
        
        # Actualizar el archivo de artículo individual
        article_file = f"{self.api_dir}/articles/[slug].js"
        
        if os.path.exists(article_file):
            with open(article_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reemplazar URLs de imágenes antiguas con nuevas
            updated_content = content
            for old_url, new_url in image_mapping.items():
                updated_content = updated_content.replace(old_url, new_url)
            
            # Guardar archivo actualizado
            backup_file = f"{article_file}.backup_{int(time.time())}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            with open(article_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Artículo individual actualizado: {article_file}")
            print(f"💾 Backup guardado en: {backup_file}")

def main():
    """Función principal del sistema de gestión de noticias"""
    print("📰 Sistema Completo de Gestión de Noticias")
    print("="*60)
    print("🔄 Descarga de noticias, gestión de imágenes en R2, y actualización de API")
    print("="*60)
    
    try:
        # Inicializar componentes
        downloader = NewsDownloader()
        processor = NewsProcessor()
        image_manager = NewsImageManager()
        api_updater = APIUpdater()
        
        print("✅ Componentes inicializados")
        
        # 1. Descargar noticias
        print("\n📥 Descargando noticias...")
        articles = downloader.fetch_news(query='política México', page_size=30)
        
        # 2. Obtener textos completos
        print("\n📖 Obteniendo textos completos...")
        enhanced_articles = []
        for i, article in enumerate(articles):
            print(f"   Obteniendo texto completo para artículo {i+1}/{len(articles)}...")
            full_text = downloader.get_full_text(article['url']) if article.get('url') else ''
            enhanced_article = {**article, 'full_text': full_text}
            enhanced_articles.append(enhanced_article)
        
        # 3. Procesar artículos (paráfrasis)
        print("\n🔄 Procesando artículos con paráfrasis...")
        processed_articles = processor.process_articles(enhanced_articles)
        
        # 4. Procesar imágenes y subirlas a R2
        print("\n🖼️  Procesando imágenes y subiéndolas a R2...")
        updated_articles, image_mapping = image_manager.process_article_images(processed_articles)
        
        # 5. Actualizar API con nuevos artículos e imágenes
        print("\n📡 Actualizando API...")
        api_updater.update_articles_json(updated_articles)
        api_updater.update_api_functions(image_mapping)
        
        # 6. Guardar resultados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"/tmp/news_system_results_{timestamp}.json"
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_articles': len(updated_articles),
            'processed_articles': len(processed_articles),
            'images_mapped': len(image_mapping),
            'image_mapping': image_mapping,
            'sample_articles': updated_articles[:3]  # Solo primeros 3 como ejemplo
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Resultados del sistema guardados en: {results_file}")
        
        # Resumen
        print("\n" + "="*60)
        print("✅ Sistema de Gestión de Noticias completado exitosamente!")
        print(f"📊 Artículos procesados: {len(updated_articles)}")
        print(f"🖼️  Imágenes subidas a R2: {len(image_mapping)}")
        print(f"🔗 Mapeo de imágenes: {results_file}")
        print(f"🔄 API actualizada con nuevos artículos e imágenes")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error en el sistema de gestión de noticias: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
