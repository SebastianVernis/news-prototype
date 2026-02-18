#!/usr/bin/env python3
"""
Parafraseo rápido con Gemini API para artículos placeholder
Optimizado para ejecución paralela y alta velocidad
"""

import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import itertools
from threading import Lock

load_dotenv()

# Cargar múltiples keys para rotación
GEMINI_API_KEY_1 = os.getenv('GEMINI_API_KEY_1')
GEMINI_API_KEY_2 = os.getenv('GEMINI_API_KEY_2')
GEMINI_API_KEY_3 = os.getenv('GEMINI_API_KEY_3')
GEMINI_API_KEY_4 = os.getenv('GEMINI_API_KEY_4')

GEMINI_API_URL_BASE = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent'


class GeminiParaphraser:
    """Parafraseo rápido con Gemini API para placeholders con rotación de keys"""
    
    def __init__(self, api_keys: List[str] = None):
        # Cargar todas las keys disponibles
        if api_keys:
            self.api_keys = [k for k in api_keys if k]
        else:
            self.api_keys = [k for k in [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3, GEMINI_API_KEY_4] if k]
        
        if not self.api_keys:
            raise ValueError("No se encontraron GEMINI_API_KEY en .env. Agrega GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3")
        
        print(f"🔑 Keys cargadas: {len(self.api_keys)}")
        
        # Crear iterador circular para rotación
        self.key_iterator = itertools.cycle(self.api_keys)
        self.key_lock = Lock()  # Thread-safe para acceso paralelo
        
        self.headers = {
            'Content-Type': 'application/json'
        }
        
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
    
    def _get_next_key(self) -> str:
        """Obtiene la siguiente key en rotación (thread-safe)"""
        with self.key_lock:
            return next(self.key_iterator)
    
    def _limpiar_firmas(self, text: str) -> str:
        """Limpia firmas, autores y metadata del texto"""
        import re
        
        # Patrones a remover
        patrones_remover = [
            r'Con información de.*',
            r'Escuchar nota.*',
            r'Suscribite.*',
            r'Recibí.*noticias.*',
            r'Temas:?.*',
            r'Compartir en.*',
            r'Lectura:.*',
            r'\d{2}\.\d{2}\.\d{4}.*\d{2}:\d{2}',
            r'Montevideo Portal',
            r'Milenio',
            r'El Financiero',
            r'La Jornada',
            r'Genera.*audio',
            r'Para ver esta página.*JavaScript',
            r'//.*//.*',  # Firmas tipo // Autor //
        ]
        
        for patron in patrones_remover:
            text = re.sub(patron, '', text, flags=re.IGNORECASE)
        
        # Limpiar líneas vacías múltiples
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def parafrasear_simple(self, article: Dict, delay: float = 0.1) -> Dict:
        """
        Parafraseo simple y rápido para placeholder
        
        Args:
            article: Artículo original
            
        Returns:
            Artículo con título y descripción parafraseados
        """
        title = article.get('title', '')
        description = article.get('description', '')
        content = article.get('content', '')[:300]
        
        # Limpiar texto original de firmas y metadata
        text_to_paraphrase = f"{title}\n\n{description}\n\n{content}"
        
        prompt = f"""Reescribe este artículo político en español con estilo periodístico profesional.

INSTRUCCIONES CRÍTICAS:
1. NO incluyas firmas de autores, nombres de sitios, o metadata
2. NO uses frases como "Escuchar nota", "Suscríbete", "Temas", "Con información de"
3. Escribe 3-4 párrafos SEPARADOS con doble salto de línea
4. Cada párrafo: 2-3 oraciones (50-80 palabras)
5. Usa puntos y comas correctamente
6. Tono periodístico neutral y profesional

FORMATO DE RESPUESTA:

[TÍTULO]
Título reescrito aquí (60-100 caracteres)

[CONTENIDO]

Primer párrafo con introducción clara. Dos o tres oraciones que contextualicen.

Segundo párrafo desarrollando el tema. Información adicional relevante.

Tercer párrafo con datos o análisis. Conclusión si aplica.

Artículo original:
{text_to_paraphrase}

Tu reescritura (SIN firmas, SIN metadata):"""

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500,
                "topP": 0.8,
                "topK": 40
            }
        }
        
        try:
            # Obtener key para este request (rotación automática)
            api_key = self._get_next_key()
            api_url = f"{GEMINI_API_URL_BASE}?key={api_key}"
            
            self.request_count += 1
            
            response = requests.post(
                api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            self.success_count += 1
            
            result = response.json()
            
            # Validar estructura de respuesta
            if 'candidates' not in result or not result['candidates']:
                raise ValueError(f"Respuesta inválida de Gemini API: {result}")
            
            if 'content' not in result['candidates'][0] or 'parts' not in result['candidates'][0]['content']:
                raise ValueError(f"Estructura de respuesta inesperada: {result}")
            
            if not result['candidates'][0]['content']['parts']:
                raise ValueError(f"Respuesta vacía de Gemini: {result}")
            
            # Extraer texto de la respuesta de Gemini
            text = result['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Limpiar texto de firmas y metadata comunes
            text = self._limpiar_firmas(text)
            
            # Parsear respuesta
            article_copy = article.copy()
            
            import re
            
            if '[TÍTULO]' in text and '[CONTENIDO]' in text:
                parts = text.split('[CONTENIDO]')
                title_part = parts[0].replace('[TÍTULO]', '').strip()
                content_part = parts[1].strip() if len(parts) > 1 else text
                
                # Limpiar corchetes del título
                title_part = re.sub(r'[\[\]]', '', title_part).strip()
                
                article_copy['title'] = title_part[:150] if title_part else title
                article_copy['full_text'] = content_part
                article_copy['content'] = content_part
                article_copy['description'] = content_part[:300] + '...' if len(content_part) > 300 else content_part
                article_copy['paraphrased'] = True
                article_copy['paraphrase_method'] = 'gemini-simple'
            elif '[TÍTULO]' in text and '[DESCRIPCIÓN]' in text:
                # Formato antiguo
                parts = text.split('[DESCRIPCIÓN]')
                title_part = parts[0].replace('[TÍTULO]', '').strip()
                desc_part = parts[1].strip() if len(parts) > 1 else text
                
                # Limpiar corchetes
                title_part = re.sub(r'[\[\]]', '', title_part).strip()
                
                article_copy['title'] = title_part[:150] if title_part else title
                article_copy['full_text'] = desc_part
                article_copy['description'] = desc_part[:300] + '...' if len(desc_part) > 300 else desc_part
                article_copy['paraphrased'] = True
                article_copy['paraphrase_method'] = 'gemini-simple'
            else:
                # Fallback: usar párrafos
                parrafos = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 20]
                
                # Buscar título si empieza con [TÍTULO] o está en corchetes
                first_line = parrafos[0] if parrafos else ''
                
                # Remover cualquier formato [TEXTO] del título
                titulo_extraido = re.sub(r'^\[([^\]]+)\]', r'\1', first_line).strip()
                
                # Si el título tenía formato de corchetes, remover de párrafos
                if first_line.startswith('[') and ']' in first_line:
                    parrafos = parrafos[1:]  # Remover título de los párrafos
                elif len(parrafos) > 1:
                    parrafos = parrafos[1:]  # Primera línea es título
                
                # Si título está vacío, usar original
                if not titulo_extraido or len(titulo_extraido) < 10:
                    titulo_extraido = title
                
                if parrafos:
                    # Limpiar corchetes del título
                    titulo_limpio = re.sub(r'[\[\]]', '', titulo_extraido).strip()
                    
                    article_copy['title'] = titulo_limpio[:150] if titulo_limpio else title
                    article_copy['full_text'] = '\n\n'.join(parrafos)
                    article_copy['content'] = '\n\n'.join(parrafos)
                    article_copy['description'] = parrafos[0][:300] + '...' if parrafos[0] and len(parrafos[0]) > 300 else parrafos[0]
                    article_copy['paraphrased'] = True
                    article_copy['paraphrase_method'] = 'gemini-simple-fallback'
                else:
                    article_copy['paraphrased'] = False
                    article_copy['paraphrase_method'] = 'original'
            
            return article_copy
            
            # Si falla el parseo, retornar original SIN modificar
            article_copy = article.copy()
            article_copy['paraphrased'] = False
            article_copy['paraphrase_method'] = 'original'
            return article_copy
            
        except Exception as e:
            self.error_count += 1
            # print(f"  ⚠️  Error Gemini: {e}")
            article_copy = article.copy()
            article_copy['paraphrased'] = False
            article_copy['paraphrase_method'] = 'error'
            article_copy['error_message'] = str(e)
            return article_copy
    
    def parafrasear_lote_paralelo(
        self,
        articles: List[Dict],
        max_workers: int = 3,
        delay_between_batches: float = 0.5
    ) -> List[Dict]:
        """
        Parafrasea múltiples artículos en paralelo
        
        Args:
            articles: Lista de artículos
            max_workers: Número máximo de threads paralelos
            
        Returns:
            Lista de artículos parafraseados
        """
        print(f"\n{'='*70}")
        print(f"🚀 PARAFRASEO PARALELO CON GEMINI")
        print(f"{'='*70}")
        print(f"Artículos: {len(articles)}")
        print(f"Workers paralelos: {max_workers}")
        print(f"Tiempo estimado: ~{len(articles) / max_workers * 3:.0f}s")
        print()
        
        results = []
        start_time = time.time()
        
        # Procesar en lotes pequeños para evitar rate limiting
        batch_size = max_workers
        total_batches = (len(articles) + batch_size - 1) // batch_size
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(articles))
            batch = articles[start_idx:end_idx]
            
            if batch_num > 0:
                # Delay entre lotes
                time.sleep(delay_between_batches)
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Enviar trabajos del lote
                future_to_article = {
                    executor.submit(self.parafrasear_simple, article): (start_idx + idx, article)
                    for idx, article in enumerate(batch)
                }
                
                # Procesar resultados conforme se completen
                for future in as_completed(future_to_article):
                    idx, original = future_to_article[future]
                    try:
                        result = future.result()
                        results.append((idx, result))
                        
                        status = "✅" if result.get('paraphrased') else "⚠️"
                        print(f"  [{idx+1}/{len(articles)}] {status} {result.get('title', 'Sin título')[:50]}...")
                        
                    except Exception as e:
                        print(f"  [{idx+1}/{len(articles)}] ❌ Error: {e}")
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
        print(f"  Tiempo total: {elapsed:.1f}s")
        print(f"  Promedio por artículo: {elapsed/len(articles):.2f}s")
        print(f"  Requests/segundo: {len(articles)/elapsed:.1f}")
        print(f"\n🔑 Uso de Keys:")
        print(f"  Total requests: {self.request_count}")
        print(f"  Keys disponibles: {len(self.api_keys)}")
        print(f"  Requests por key: ~{self.request_count/len(self.api_keys):.1f}")
        print(f"{'='*70}")
        
        return final_results


def main():
    """Test del parafraseo con Gemini"""
    import glob
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║        🚀 PARAFRASEO RÁPIDO CON GEMINI API (PARALELO)               ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    if not any([GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3]):
        print("❌ ERROR: No se encontraron GEMINI_API_KEY en .env")
        print("💡 Agrega al menos una API key de Gemini a .env:")
        print("   GEMINI_API_KEY_1=tu_key_aqui")
        print("   GEMINI_API_KEY_2=tu_segunda_key_aqui")
        print("   GEMINI_API_KEY_3=tu_tercera_key_aqui")
        return
    
    # Buscar archivo de noticias
    json_files = glob.glob('newsapi_*.json')
    if not json_files:
        print("❌ No se encontraron archivos de noticias")
        print("💡 Ejecuta: python3 core/scripts/api/newsapi.py --size 5")
        return
    
    latest_file = sorted(json_files)[-1]
    print(f"📂 Cargando: {latest_file}\n")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Tomar solo 5 artículos para prueba
    test_articles = articles[:5]
    
    print(f"🧪 Test con {len(test_articles)} artículos\n")
    
    # Parafrasear en paralelo
    paraphraser = GeminiParaphraser()
    results = paraphraser.parafrasear_lote_paralelo(test_articles, max_workers=5)
    
    # Guardar resultado
    output_file = 'noticias_gemini_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Guardado en: {output_file}")
    
    # Mostrar ejemplo
    if results and results[0].get('paraphrased'):
        print(f"\n{'='*70}")
        print("📄 EJEMPLO DE RESULTADO")
        print(f"{'='*70}")
        print(f"\nOriginal:")
        print(f"  {test_articles[0].get('title', '')[:70]}...")
        print(f"\nParafraseado:")
        print(f"  {results[0].get('title', '')[:70]}...")
        print(f"\nDescripción:")
        print(f"  {results[0].get('description', '')[:150]}...")


if __name__ == '__main__':
    main()
