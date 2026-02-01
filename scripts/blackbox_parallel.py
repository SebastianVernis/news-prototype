#!/usr/bin/env python3
"""
Parafraseo paralelo con Blackbox API
Usa rotación de keys para acelerar generación de artículos principales
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import itertools
from threading import Lock

load_dotenv()

# Cargar múltiples keys para rotación
# Modelo por defecto: blackboxai/x-ai/grok-code-fast-1:free (recomendado)
DEFAULT_MODEL = 'blackboxai/x-ai/grok-code-fast-1:free'
BLACKBOX_API_KEY_1 = os.getenv('BLACKBOX_API_KEY_1')
BLACKBOX_MODEL_1 = os.getenv('BLACKBOX_MODEL_1', DEFAULT_MODEL)
BLACKBOX_API_KEY_2 = os.getenv('BLACKBOX_API_KEY_2')
BLACKBOX_MODEL_2 = os.getenv('BLACKBOX_MODEL_2', DEFAULT_MODEL)

BLACKBOX_API_URL = 'https://api.blackbox.ai/chat/completions'


class BlackboxParallelParaphraser:
    """Parafraseo de artículos principales con Blackbox en paralelo"""
    
    def __init__(self, api_keys: List[str] = None):
        # Cargar todas las keys y modelos disponibles
        # Usar siempre el modelo blackboxai/x-ai/grok-code-fast-1:free por defecto
        if api_keys:
            self.api_configs = [{'key': k, 'model': DEFAULT_MODEL, 'id': f'CUSTOM_{i}'} for i, k in enumerate(api_keys) if k and 'PENDIENTE' not in k]
        else:
            self.api_configs = []
            
            # Intentar cargar todas las posibles keys del .env
            env_keys = [
                ('PRO', os.getenv('BLACKBOX_API_KEY_PRO')),
                ('FREE', os.getenv('BLACKBOX_API_KEY_FREE')),
                ('ALT', os.getenv('BLACKBOX_API_KEY_ALT')),
                ('KEY1', os.getenv('BLACKBOX_API_KEY_1')),
                ('KEY2', os.getenv('BLACKBOX_API_KEY_2'))
            ]
            
            # Eliminar duplicados de keys manteniendo el primer ID encontrado
            seen_keys = set()
            unique_env_keys = []
            for name, key in env_keys:
                if key and 'PENDIENTE' not in str(key) and key not in seen_keys:
                    unique_env_keys.append((name, key))
                    seen_keys.add(key)
            
            # Modelos a usar
            model_list_str = os.getenv('BLACKBOX_MODEL_LIST')
            if model_list_str:
                models = [m.strip() for m in model_list_str.split(',') if m.strip()]
            else:
                models = [BLACKBOX_MODEL_1]
            
            # Si tenemos múltiples keys, rotar sobre ellas
            for name, key in unique_env_keys:
                for i, model in enumerate(models):
                    self.api_configs.append({
                        'key': key,
                        'model': model,
                        'id': f'{name}_M{i+1}' if len(models) > 1 else name
                    })
        
        if not self.api_configs:
            raise ValueError("No se encontraron BLACKBOX_API_KEY en .env")
        
        print(f"🔑 Blackbox keys cargadas: {len(self.api_configs)}")
        for config in self.api_configs:
            print(f"   {config['id']}: {config['model']}")
        
        # Crear iterador circular para rotación
        self.config_iterator = itertools.cycle(self.api_configs)
        self.config_lock = Lock()
        
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
    
    def _get_next_config(self) -> Dict:
        """Obtiene la siguiente configuración en rotación (thread-safe)"""
        with self.config_lock:
            return next(self.config_iterator)
    
    def parafrasear_articulo(self, article: Dict, style: str = "formal y objetivo") -> Dict:
        """
        Parafrasea un artículo completo usando Blackbox
        Similar a NewsParaphraser pero con rotación de keys
        
        Args:
            article: Artículo a parafrasear
            style: Estilo de parafraseo
            
        Returns:
            Artículo parafraseado
        """
        # Extraer texto
        title = article.get('title', '')
        description = article.get('description', '')
        content = article.get('content', '')
        full_text = article.get('full_text', '')
        
        text_parts = [title, description]
        if full_text:
            text_parts.append(full_text[:1000])
        elif content:
            text_parts.append(content[:1000])
        
        base_text = '\n\n'.join(filter(None, text_parts))
        
        # Prompt (mismo que paraphrase.py)
        prompt = f"""Eres un periodista senior especializado en política. Reescribe el siguiente artículo de noticias con un estilo {style}.

INSTRUCCIONES CRÍTICAS DE FORMATO Y CALIDAD:

1. TÍTULO: 
   - Crea un título informativo y descriptivo (60-120 caracteres)
   - Debe capturar la esencia de la noticia de forma clara y atractiva

2. ESTRUCTURA DE PÁRRAFOS (MUY IMPORTANTE):
   - Escribe 8-12 párrafos SEPARADOS con doble salto de línea entre cada uno
   - Cada párrafo debe tener 3-5 oraciones (100-150 palabras)
   - NUNCA escribas todo el texto en un solo bloque
   - Usa puntos y comas correctamente
   - Separa ideas diferentes en párrafos diferentes

3. GRAMÁTICA Y PUNTUACIÓN:
   - Usa puntos (.) para terminar oraciones completas
   - Usa comas (,) correctamente para separar ideas dentro de oraciones
   - Usa punto y coma (;) cuando conectes ideas relacionadas
   - Usa dos puntos (:) antes de listas o explicaciones
   - Evita oraciones excesivamente largas (máximo 30-35 palabras)

4. FORMATO DE RESPUESTA:
   [TÍTULO]
   Título informativo y descriptivo aquí
   
   [ARTÍCULO]
   
   Primer párrafo con introducción clara y concisa.
   
   Segundo párrafo desarrollando el primer punto importante.
   
   [Continuar con 9 párrafos más]

Artículo original:
{base_text}

Artículo expandido con PÁRRAFOS BIEN SEPARADOS:"""

        current_key_id = "UNKNOWN"
        try:
            # Obtener configuración para este request (key + modelo)
            config = self._get_next_config()
            api_key = config['key']
            model = config['model']
            current_key_id = config.get('id', 'UNKNOWN')
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un periodista senior especializado en política con excelente dominio del español. Escribes artículos profundos, detallados y políticamente precisos de más de 1000 palabras. SIEMPRE separas el contenido en párrafos distintos usando doble salto de línea. Tienes impecable gramática, puntuación y estructura narrativa."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            self.request_count += 1
            
            response = requests.post(BLACKBOX_API_URL, headers=headers, json=payload, timeout=90)
            response.raise_for_status()
            
            self.success_count += 1
            
            result = response.json()
            
            # Validar estructura de respuesta
            if 'choices' not in result or not result['choices']:
                raise ValueError(f"Respuesta inválida de Blackbox API: {result}")
            
            if 'message' not in result['choices'][0] or 'content' not in result['choices'][0]['message']:
                raise ValueError(f"Estructura de respuesta inesperada: {result}")
            
            paraphrased = result['choices'][0]['message']['content'].strip()
            
            # Crear copia del artículo con texto parafraseado
            article_copy = article.copy()
            
            # Extraer título y artículo del formato estructurado
            if '[TÍTULO]' in paraphrased and '[ARTÍCULO]' in paraphrased:
                parts = paraphrased.split('[ARTÍCULO]')
                title_section = parts[0].replace('[TÍTULO]', '').strip()
                article_body = parts[1].strip() if len(parts) > 1 else paraphrased
                
                title_section = title_section.strip('[]').strip()
                
                article_copy['title'] = title_section[:150] if title_section else article.get('title', '')[:150]
                article_copy['full_text'] = article_body
                article_copy['description'] = article_body[:300] + '...' if len(article_body) > 300 else article_body
            else:
                lines = paraphrased.split('\n\n')
                article_copy['title'] = lines[0][:150] if lines else article.get('title', '')[:150]
                article_copy['full_text'] = '\n\n'.join(lines[1:]) if len(lines) > 1 else paraphrased
                article_copy['description'] = article_copy['full_text'][:300] + '...' if len(article_copy['full_text']) > 300 else article_copy['full_text']
            
            if 'content' in article_copy:
                article_copy['content'] = article_copy['full_text']
            
            article_copy['paraphrased'] = True
            article_copy['paraphrase_method'] = 'blackbox-parallel'
            article_copy['style'] = style
            article_copy['key_used'] = current_key_id
            
            return article_copy
            
        except Exception as e:
            self.error_count += 1
            article['paraphrased'] = False
            article['paraphrase_method'] = 'error'
            article['error_message'] = str(e)
            article['key_used'] = current_key_id
            return article
    
    def parafrasear_lote_paralelo(
        self,
        articles: List[Dict],
        max_workers: int = 2,
        styles: List[str] = None
    ) -> List[Dict]:
        """
        Parafrasea múltiples artículos en paralelo
        
        Args:
            articles: Lista de artículos
            max_workers: Número de workers paralelos
            styles: Lista de estilos (rotará entre ellos)
            
        Returns:
            Lista de artículos parafraseados
        """
        if not styles:
            styles = ["formal y objetivo", "casual y cercano", "técnico y detallado"]
        
        print(f"\n{'='*70}")
        print(f"🚀 PARAFRASEO PARALELO CON BLACKBOX")
        print(f"{'='*70}")
        print(f"Artículos: {len(articles)}")
        print(f"Workers paralelos: {max_workers}")
        print(f"Keys disponibles: {len(self.api_configs)}")
        print(f"Tiempo estimado: ~{len(articles) / max_workers * 90 / 60:.1f} minutos")
        print()
        
        results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Enviar todos los trabajos
            future_to_article = {}
            for idx, article in enumerate(articles):
                style = styles[idx % len(styles)]
                future = executor.submit(self.parafrasear_articulo, article, style)
                future_to_article[future] = (idx + 1, article)
            
            # Procesar resultados conforme se completen
            for future in as_completed(future_to_article):
                idx, original = future_to_article[future]
                try:
                    result = future.result()
                    results.append((idx, result))
                    
                    status = "✅" if result.get('paraphrased') else "⚠️"
                    print(f"  [{idx}/{len(articles)}] {status} {result.get('title', 'Sin título')[:60]}...")
                    
                except Exception as e:
                    # Este bloque catch atrapa excepciones de future.result() que NUNCA deberían ocurrir
                    # porque parafrasear_articulo ya captura todas las excepciones.
                    print(f"  [{idx}/{len(articles)}] ❌ Error CRÍTICO en thread: {e}")
                    original['paraphrased'] = False
                    results.append((idx, original))
        
        # Ordenar por índice original
        results.sort(key=lambda x: x[0])
        final_results = [r[1] for r in results]
        
        elapsed = time.time() - start_time
        successful = sum(1 for r in final_results if r.get('paraphrased'))
        
        print(f"\n{'='*70}")
        print(f"✅ Parafraseo paralelo completado")
        print(f"{'='*70}")
        print(f"  Total artículos: {len(articles)}")
        print(f"  Exitosos: {successful}")
        print(f"  Fallidos: {len(articles) - successful}")
        print(f"  Tiempo total: {elapsed/60:.1f} minutos")
        print(f"  Promedio por artículo: {elapsed/len(articles):.1f}s")
        print(f"\n🔑 Uso de Keys:")
        print(f"  Total requests: {self.request_count}")
        print(f"  Keys disponibles: {len(self.api_configs)}")
        print(f"  Requests por key: ~{self.request_count/len(self.api_configs):.1f}")
        print(f"{'='*70}")
        
        return final_results


def main():
    """Test del parafraseo paralelo con Blackbox"""
    import json
    import glob
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║     🚀 PARAFRASEO PARALELO CON BLACKBOX (Artículos Principales)     ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Cargar noticias
    json_files = glob.glob('newsapi_*.json')
    if not json_files:
        print("❌ No se encontraron archivos de noticias")
        return
    
    with open(sorted(json_files)[-1], 'r', encoding='utf-8') as f:
        articles = json.load(f)[:3]  # Solo 3 para test
    
    print(f"📰 Test con {len(articles)} artículos\n")
    
    # Parafrasear en paralelo
    paraphraser = BlackboxParallelParaphraser()
    results = paraphraser.parafrasear_lote_paralelo(articles, max_workers=2)
    
    # Guardar
    with open('noticias_blackbox_parallel_test.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Guardado en: noticias_blackbox_parallel_test.json")


if __name__ == '__main__':
    main()
