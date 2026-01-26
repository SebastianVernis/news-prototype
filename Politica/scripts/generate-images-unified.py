#!/usr/bin/env python3
"""
Generador Unificado de Imágenes
Estrategia: NewsAPI Original → IA (Flux Schnell) → Unsplash
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict

# Importar ambos generadores
import importlib.util

def import_module_from_file(module_name, file_path):
    """Importa un módulo desde un archivo"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"No se pudo importar {module_name}")

current_dir = Path(__file__).parent

# Importar generadores
newsapi_module = import_module_from_file('generate_images_newsapi', current_dir / 'generate-images-newsapi.py')
ai_module = import_module_from_file('generate_images_ai', current_dir / 'generate-images-ai.py')
unsplash_module = import_module_from_file('generate_images_unsplash', current_dir / 'generate-images-unsplash.py')

NewsAPIImageGenerator = newsapi_module.NewsAPIImageGenerator
AIImageGenerator = ai_module.AIImageGenerator
UnsplashImageGenerator = unsplash_module.UnsplashImageGenerator


class UnifiedImageGenerator:
    """Generador unificado con estrategia de fallback múltiple"""
    
    def __init__(self, output_dir='generated_images', prefer_ai: bool = False, use_cache: bool = True):
        """
        Inicializa el generador unificado
        
        Args:
            output_dir: Directorio de salida
            prefer_ai: Si True, intenta IA antes de NewsAPI original
            use_cache: Si False, fuerza descarga de imágenes nuevas
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.prefer_ai = prefer_ai
        self.ai_available = False
        self.use_cache = use_cache
        
        # Siempre inicializar NewsAPI (mejor opción)
        self.newsapi_generator = NewsAPIImageGenerator(output_dir, use_cache=use_cache)
        
        # Intentar inicializar IA si se prefiere
        if prefer_ai:
            try:
                self.ai_generator = AIImageGenerator(output_dir)
                print("🔍 Verificando disponibilidad de IA...")
                self.ai_available = self._test_ai_availability()
            except Exception as e:
                print(f"⚠️  IA no disponible: {e}")
                self.ai_available = False
        
        # Unsplash como último recurso
        self.unsplash_generator = UnsplashImageGenerator(output_dir)
        
        # Reportar estrategia
        if self.ai_available:
            print("✅ Estrategia: IA (Flux Schnell) → NewsAPI → Unsplash")
        else:
            print("✅ Estrategia: NewsAPI Original → Unsplash (fallback)")
    
    def _test_ai_availability(self) -> bool:
        """
        Test rápido de disponibilidad de IA
        
        Returns:
            True si IA está disponible
        """
        try:
            import requests
            from dotenv import load_dotenv
            
            load_dotenv()
            api_key = os.getenv('BLACKBOX_API_KEY')
            
            if not api_key:
                return False
            
            # Test simple
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            payload = {
                'model': 'blackboxai/black-forest-labs/flux-schnell',
                'messages': [{'role': 'user', 'content': 'test'}]
            }
            
            response = requests.post(
                'https://api.blackbox.ai/chat/completions',
                headers=headers,
                json=payload,
                timeout=10
            )
            
            # Si status es 500, probablemente es problema de balance
            if response.status_code == 500:
                error_msg = response.json().get('error', {}).get('message', '')
                if 'Exhausted balance' in error_msg or 'fal.ai' in error_msg:
                    print("⚠️  IA no disponible: Balance agotado en fal.ai")
                    return False
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"⚠️  Error test IA: {e}")
            return False
    
    def generate_image(self, prompt: str, article_id: str, index: int, article: Dict = None) -> str:
        """
        Genera una sola imagen (compatible con master_orchestrator)
        
        Args:
            prompt: Prompt de la imagen (usado solo para IA)
            article_id: ID del artículo
            index: Índice de la imagen
            article: Datos del artículo (opcional, para NewsAPI)
            
        Returns:
            Ruta del archivo de imagen o None
        """
        # Si no hay artículo, crear uno temporal
        if not article:
            article = {
                'title': prompt[:100],
                'description': prompt,
                'category': 'technology',
                'variation_id': article_id,
                'image_url': None
            }
        
        # Estrategia 1: IA (solo si está habilitada Y es preferida)
        if self.ai_available and self.prefer_ai:
            try:
                return self.ai_generator.generate_image(prompt, article_id, index)
            except Exception as e:
                print(f"⚠️  IA falló: {e}")
        
        # Estrategia 2: NewsAPI Original (MEJOR OPCIÓN)
        try:
            result = self.newsapi_generator.generate_image(article, article_id, index)
            if result:
                return result
        except Exception as e:
            print(f"⚠️  NewsAPI falló: {e}")
        
        # Estrategia 3: Unsplash (fallback final)
        return self.unsplash_generator.generate_image(article, article_id, index)
    
    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Procesa artículos usando el generador apropiado
        
        Args:
            articles: Lista de artículos
            
        Returns:
            Lista de artículos con imágenes
        """
        # Prioridad 1: IA (solo si está habilitada Y preferida)
        if self.ai_available and self.prefer_ai:
            print("\n🎨 Usando generador de IA...")
            try:
                return self.ai_generator.process_articles(articles)
            except Exception as e:
                print(f"\n⚠️  Error con IA, fallback a NewsAPI: {e}")
        
        # Prioridad 2: NewsAPI Original (RECOMENDADO)
        print("\n📸 Usando imágenes originales de NewsAPI...")
        try:
            return self.newsapi_generator.process_articles(articles)
        except Exception as e:
            print(f"\n⚠️  Error con NewsAPI, fallback a Unsplash: {e}")
            return self.unsplash_generator.process_articles(articles)


def main():
    """Función principal para pruebas"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🎨 Generador Unificado de Imágenes                     ║
    ║  IA (Flux Schnell) con fallback a Unsplash              ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Cargar artículos
    test_file = 'noticias_paraphrased_test.json'
    
    if not Path(test_file).exists():
        print(f"❌ No se encontró {test_file}")
        print("💡 Ejecuta primero: python3 paraphrase.py")
        return
    
    print(f"📂 Cargando: {test_file}")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Procesar solo 3 artículos en modo test
    print(f"\n⚠️  MODO PRUEBA: Procesando solo 3 artículos")
    
    # Crear generador (intenta IA, fallback a Unsplash)
    generator = UnifiedImageGenerator(prefer_ai=True)
    results = generator.process_articles(articles[:3])
    
    # Guardar resultados
    output_file = 'noticias_with_images_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados guardados en: {output_file}")


if __name__ == '__main__':
    main()
