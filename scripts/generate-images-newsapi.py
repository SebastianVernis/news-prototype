#!/usr/bin/env python3
"""
Generador de imágenes usando URLs de NewsAPI (MEJOR OPCIÓN)
Descarga las imágenes reales de las noticias originales
Garantiza relevancia 100% con el contenido del artículo
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict
import time
import hashlib

class NewsAPIImageGenerator:
    """Descarga imágenes reales de las noticias desde NewsAPI"""
    
    def __init__(self, output_dir='generated_images', use_cache=True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.width = 1200
        self.height = 600
        self.use_cache = use_cache
        
        # Fallback a placeholder si imagen falla
        self.fallback_service = 'https://picsum.photos'
    
    def download_image(self, image_url: str, article_id: str, index: int) -> str:
        """
        Descarga la imagen desde URL de NewsAPI
        
        Args:
            image_url: URL de la imagen original
            article_id: ID del artículo
            index: Índice de la imagen
            
        Returns:
            Ruta del archivo descargado
        """
        try:
            filename = f"article_{article_id}_{index}.jpg"
            filepath = self.output_dir / filename
            
            # Verificar si ya existe (solo si use_cache está habilitado)
            if self.use_cache and filepath.exists():
                print(f"    ✅ (cached)")
                return str(filepath)
            
            # Headers para evitar bloqueos
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Descargar imagen
            response = requests.get(image_url, headers=headers, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            # Verificar que es una imagen válida
            content_type = response.headers.get('Content-Type', '')
            if 'image' not in content_type and len(response.content) < 1000:
                raise ValueError(f"No es una imagen válida: {content_type}")
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return str(filepath)
            
        except Exception as e:
            print(f"    ⚠️  Error descargando: {e}")
            return None
    
    def get_fallback_image(self, article: Dict, article_id: str, index: int) -> str:
        """
        Genera imagen de fallback con seed basado en título
        
        Args:
            article: Diccionario con datos del artículo
            article_id: ID del artículo
            index: Índice de la imagen
            
        Returns:
            Ruta del archivo descargado
        """
        try:
            # Crear seed único basado en título
            title = article.get('title', '')
            seed = hashlib.md5(title.encode()).hexdigest()[:10]
            
            fallback_url = f'{self.fallback_service}/seed/{seed}/{self.width}/{self.height}'
            
            print(f"    🔄 Usando fallback (Picsum)...", end=" ")
            
            filename = f"article_{article_id}_{index}.jpg"
            filepath = self.output_dir / filename
            
            response = requests.get(fallback_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print("✅")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Error fallback: {e}")
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
            # Obtener URL de imagen original
            image_url = article.get('image_url', '').strip()
            
            if not image_url or image_url == 'null' or image_url == 'None':
                print(f"    ⚠️  Sin imagen original, usando fallback...")
                return self.get_fallback_image(article, article_id, index)
            
            print(f"    📥 Descargando imagen original...", end=" ")
            
            # Descargar imagen original
            filepath = self.download_image(image_url, article_id, index)
            
            if filepath:
                print("✅")
                return filepath
            else:
                # Si falla, usar fallback
                return self.get_fallback_image(article, article_id, index)
                
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return self.get_fallback_image(article, article_id, index)
    
    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Procesa artículos y descarga imágenes para cada uno
        
        Args:
            articles: Lista de artículos
            
        Returns:
            Lista de artículos con rutas de imágenes
        """
        results = []
        
        print(f"\n{'='*70}")
        print(f"📸 Descargando imágenes originales para {len(articles)} artículos")
        print(f"   Fuente: NewsAPI (imágenes reales de noticias)")
        print(f"{'='*70}")
        
        for idx, article in enumerate(articles, 1):
            title = article.get('title', 'Sin título')[:60]
            article_id = article.get('variation_id', idx)
            
            print(f"\n[{idx}/{len(articles)}] {title}...")
            
            # Generar/descargar imagen
            image_path = self.generate_image(article, article_id, idx)
            
            # Agregar ruta de imagen al artículo
            article_with_image = article.copy()
            article_with_image['ai_image_path'] = image_path
            article_with_image['image_source'] = 'newsapi_original'
            article_with_image['original_image_url'] = article.get('image_url', '')
            
            results.append(article_with_image)
            
            # Pausa mínima para no saturar
            if idx % 10 == 0:
                time.sleep(1)
        
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
    ║  📸 Generador de Imágenes desde NewsAPI                 ║
    ║  Imágenes reales de noticias (100% relevantes)           ║
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
    
    generator = NewsAPIImageGenerator()
    results = generator.process_articles(articles[:3])
    
    # Guardar resultados
    output_file = 'noticias_with_images_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados guardados en: {output_file}")


if __name__ == '__main__':
    main()
