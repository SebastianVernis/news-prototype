#!/usr/bin/env python3
"""
Generador de imágenes usando Unsplash API (Gratuito, sin límites estrictos)
Alternativa confiable cuando los modelos de IA no están disponibles
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict
import time
import hashlib

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "output" / "generated_images"


class UnsplashImageGenerator:
    """Genera imágenes desde Unsplash basadas en keywords del artículo"""
    
    def __init__(self, output_dir=None, api_key: str = None):
        self.output_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Unsplash API es gratuita con límite razonable (50 req/hora)
        self.api_key = api_key or os.getenv('UNSPLASH_ACCESS_KEY', 'demo')
        
        self.base_url = 'https://api.unsplash.com'
        self.headers = {
            'Accept-Version': 'v1'
        }
        
        if self.api_key != 'demo':
            self.headers['Authorization'] = f'Client-ID {self.api_key}'
        
        self.width = 1200
        self.height = 600
    
    def extract_keywords(self, article: Dict) -> str:
        """
        Extrae keywords del artículo para buscar imagen relevante
        
        Args:
            article: Diccionario con datos del artículo
            
        Returns:
            Query string para búsqueda de imagen
        """
        title = article.get('title', '')
        description = article.get('description', '')
        category = article.get('category', 'news')
        
        # Crear query simple pero efectivo
        # Priorizar categoría + primeras palabras del título
        title_words = title.split()[:3]  # Primeras 3 palabras
        query = f"{category} {' '.join(title_words)}"
        
        return query.strip()
    
    def search_image(self, query: str) -> str:
        """
        Busca una imagen en Unsplash
        
        Args:
            query: Términos de búsqueda
            
        Returns:
            URL de la imagen o None si falla
        """
        try:
            # Endpoint de búsqueda
            url = f'{self.base_url}/search/photos'
            params = {
                'query': query,
                'per_page': 1,
                'orientation': 'landscape',
                'content_filter': 'high'
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            
            # Si no hay API key, usar demo mode con URLs genéricas
            if response.status_code == 401 or self.api_key == 'demo':
                # Usar picsum.photos como fallback (no requiere API key)
                seed = hashlib.md5(query.encode()).hexdigest()[:10]
                return f'https://picsum.photos/seed/{seed}/{self.width}/{self.height}'
            
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('total', 0) > 0:
                photo = result['results'][0]
                # Obtener URL en tamaño optimizado
                image_url = photo['urls']['regular']
                return image_url
            
            # Fallback a imagen genérica
            return f'https://picsum.photos/{self.width}/{self.height}'
            
        except Exception as e:
            print(f"    ⚠️  Error buscando imagen: {e}")
            # Fallback a imagen placeholder
            return f'https://picsum.photos/{self.width}/{self.height}'
    
    def download_image(self, image_url: str, article_id: str, index: int) -> str:
        """
        Descarga la imagen desde URL
        
        Args:
            image_url: URL de la imagen
            article_id: ID del artículo
            index: Índice de la imagen
            
        Returns:
            Ruta del archivo descargado
        """
        try:
            filename = f"article_{article_id}_{index}.jpg"
            filepath = self.output_dir / filename
            
            # Descargar imagen
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return str(filepath)
            
        except Exception as e:
            print(f"    ❌ Error descargando: {e}")
            return None
    
    def generate_image(self, article: Dict, article_id: str, index: int) -> str:
        """
        Genera/descarga imagen para un artículo
        
        Args:
            article: Diccionario con datos del artículo
            article_id: ID del artículo
            index: Índice de la imagen
            
        Returns:
            Ruta del archivo de imagen
        """
        try:
            # Extraer keywords
            query = self.extract_keywords(article)
            print(f"    🔍 Buscando: {query}")
            
            # Buscar imagen
            image_url = self.search_image(query)
            
            if not image_url:
                print("    ❌ No se encontró imagen")
                return None
            
            print(f"    📥 Descargando...", end=" ")
            
            # Descargar
            filepath = self.download_image(image_url, article_id, index)
            
            if filepath:
                print("✅")
                return filepath
            else:
                return None
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return None
    
    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Procesa artículos y genera imágenes para cada uno
        
        Args:
            articles: Lista de artículos
            
        Returns:
            Lista de artículos con rutas de imágenes
        """
        results = []
        
        print(f"\n{'='*70}")
        print(f"🖼️  Generando imágenes desde Unsplash para {len(articles)} artículos")
        print(f"   Fuente: Unsplash API + Picsum (fallback)")
        print(f"{'='*70}")
        
        for idx, article in enumerate(articles, 1):
            title = article.get('title', 'Sin título')[:60]
            article_id = article.get('variation_id', idx)
            
            print(f"\n[{idx}/{len(articles)}] {title}...")
            
            # Generar imagen
            image_path = self.generate_image(article, article_id, idx)
            
            # Agregar ruta de imagen al artículo
            article_with_image = article.copy()
            article_with_image['ai_image_path'] = image_path
            article_with_image['image_source'] = 'unsplash'
            
            results.append(article_with_image)
            
            # Pausa para no saturar la API (Unsplash: 50 req/hora)
            if idx % 5 == 0:
                time.sleep(2)
        
        print(f"\n{'='*70}")
        print(f"✨ Proceso completado")
        successful = sum(1 for r in results if r.get('ai_image_path'))
        print(f"📊 Imágenes descargadas: {successful}/{len(articles)}")
        print(f"📂 Directorio: {self.output_dir.absolute()}")
        print(f"{'='*70}")
        
        return results


def main():
    """Función principal para pruebas"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🖼️  Generador de Imágenes con Unsplash                 ║
    ║  Alternativa gratuita y confiable                        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Cargar artículos parafraseados
    test_file = 'noticias_paraphrased_test.json'
    
    if not Path(test_file).exists():
        print(f"❌ No se encontró {test_file}")
        print("💡 Ejecuta primero: python3 paraphrase.py")
        return
    
    print(f"📂 Cargando: {test_file}")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Procesar solo los primeros 3 artículos para prueba
    print(f"\n⚠️  MODO PRUEBA: Procesando solo 3 artículos")
    
    generator = UnsplashImageGenerator()
    results = generator.process_articles(articles[:3])
    
    # Guardar resultados
    output_file = 'noticias_with_images_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados guardados en: {output_file}")


if __name__ == '__main__':
    main()
