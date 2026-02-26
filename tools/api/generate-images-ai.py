#!/usr/bin/env python3
"""
Generador de imágenes con IA usando Blackbox API + Flux Schnell
Crea imágenes basadas en el contenido de artículos de noticias
Modelo: blackboxai/black-forest-labs/flux-schnell ($0.003/imagen)
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict
import time
from datetime import datetime
import base64

load_dotenv()

API_KEY = os.getenv('BLACKBOX_API_KEY')
API_URL = 'https://api.blackbox.ai/chat/completions'

class AIImageGenerator:
    """Genera imágenes usando IA (Flux Schnell de Blackbox)"""
    
    def __init__(self, output_dir=None, api_key: str = None):
        if output_dir is None:
            repo_root = Path(__file__).resolve().parents[2]
            output_dir = os.getenv("NEWS_IMAGES_DIR", str(repo_root / "generated_images"))
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("BLACKBOX_API_KEY no encontrada en .env")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        self.width = 1200
        self.height = 600
    
    def create_image_prompt(self, article: Dict) -> str:
        """
        Crea un prompt descriptivo para generar la imagen
        
        Args:
            article: Diccionario con datos del artículo
            
        Returns:
            Prompt para generación de imagen
        """
        title = article.get('title', '')
        description = article.get('description', '')
        
        # Crear prompt descriptivo pero abstracto (sin personas/rostros)
        prompt = f"""Create a professional news article illustration for: {title}

Style: Modern, abstract, editorial illustration
Theme: {description[:200]}

Requirements:
- NO human faces or people
- Abstract and symbolic representation
- Professional news media aesthetic
- Clean, modern design
- Relevant visual metaphors
- High quality, photorealistic when applicable
- Dimensions: 1200x600px landscape format"""
        
        return prompt
    
    def generate_image(self, prompt: str, article_id: str, index: int) -> str:
        """
        Genera una imagen usando Flux Schnell (rápido y económico)
        
        Args:
            prompt: Descripción de la imagen a generar
            article_id: ID del artículo
            index: Índice de la imagen
            
        Returns:
            Ruta del archivo de imagen generado
        """
        # Usar Flux Schnell: rápido, económico ($0.003/imagen), hasta 4 imágenes
        # Alternativas: flux-dev ($0.025), flux-1.1-pro ($0.04), flux-pro ($0.055)
        payload = {
            "model": "blackboxai/black-forest-labs/flux-schnell",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            print(f"    🎨 Generando imagen con Flux Schnell...", end=" ")
            
            response = requests.post(API_URL, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # La respuesta puede contener la imagen en diferentes formatos
            # Intentar extraer la URL o datos de la imagen
            image_data = None
            image_url = None
            
            # Verificar si hay una URL de imagen en la respuesta
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0].get('message', {}).get('content', '')
                
                # Buscar URL de imagen en el contenido
                if 'http' in content:
                    # Extraer URL
                    import re
                    urls = re.findall(r'https?://[^\s<>"]+', content)
                    if urls:
                        image_url = urls[0]
                
                # O puede venir como base64
                elif 'base64' in content or len(content) > 1000:
                    image_data = content
            
            # Descargar o guardar la imagen
            filename = f"article_{article_id}_{index}.jpg"
            filepath = self.output_dir / filename
            
            if image_url:
                # Descargar desde URL
                img_response = requests.get(image_url, timeout=30)
                img_response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                print("✅")
                return str(filepath)
                
            elif image_data:
                # Guardar desde base64
                if 'base64,' in image_data:
                    image_data = image_data.split('base64,')[1]
                
                img_bytes = base64.b64decode(image_data)
                
                with open(filepath, 'wb') as f:
                    f.write(img_bytes)
                
                print("✅")
                return str(filepath)
            
            else:
                print("⚠️  No se pudo extraer imagen de la respuesta")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en API: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
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
        print(f"🎨 Generando imágenes con IA para {len(articles)} artículos")
        print(f"   Modelo: Flux Schnell (Black Forest Labs)")
        print(f"{'='*70}")
        
        for idx, article in enumerate(articles, 1):
            title = article.get('title', 'Sin título')[:60]
            article_id = article.get('variation_id', idx)
            
            print(f"\n[{idx}/{len(articles)}] {title}...")
            
            # Crear prompt
            prompt = self.create_image_prompt(article)
            print(f"    📝 Prompt: {prompt[:100]}...")
            
            # Generar imagen
            image_path = self.generate_image(prompt, article_id, idx)
            
            # Agregar ruta de imagen al artículo
            article_with_image = article.copy()
            article_with_image['ai_image_path'] = image_path
            article_with_image['image_prompt'] = prompt
            
            results.append(article_with_image)
            
            # Pausa para no saturar la API
            if idx % 3 == 0:
                time.sleep(2)
        
        print(f"\n{'='*70}")
        print(f"✨ Proceso completado")
        successful = sum(1 for r in results if r.get('ai_image_path'))
        print(f"📊 Imágenes generadas: {successful}/{len(articles)}")
        print(f"📂 Directorio: {self.output_dir.absolute()}")
        print(f"{'='*70}")
        
        return results


def main():
    """CLI principal"""
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Generador de imágenes con IA")
    parser.add_argument("--input", type=str, help="Archivo JSON de entrada")
    parser.add_argument("--output", type=str, help="Archivo JSON de salida con rutas de imágenes")
    parser.add_argument("--limit", type=int, default=5, help="Número de artículos a procesar")
    parser.add_argument("--output-dir", type=str, help="Directorio para guardar imágenes")
    args = parser.parse_args()

    data_dir = Path(os.getenv("NEWS_DATA_DIR", Path(__file__).resolve().parents[2] / "data"))
    data_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else None
    if not input_path or not input_path.exists():
        candidates = []
        patterns = ['noticias_mx_*.json', 'newsapi_*.json', 'newsdata_*.json', 'worldnews_*.json', 'apitube_*.json', '*paraphrased*.json']
        for pattern in patterns:
            candidates.extend(data_dir.glob(pattern))
        if not candidates:
            print("❌ No se encontraron archivos de noticias en data/")
            return
        input_path = sorted(candidates)[-1]

    print(f"📂 Cargando: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    generator = AIImageGenerator(output_dir=args.output_dir)
    results = generator.process_articles(articles[: args.limit])

    output_path = Path(args.output) if args.output else data_dir / f"noticias_with_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Resultados guardados en: {output_path}")


if __name__ == '__main__':
    main()
