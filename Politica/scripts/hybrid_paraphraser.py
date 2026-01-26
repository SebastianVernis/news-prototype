#!/usr/bin/env python3
"""
Sistema Híbrido de Parafraseo Optimizado
- Blackbox AI: Artículos principales (20)
- Gemini (4 keys): Placeholders primarios (200)
- Blackbox Free: Backup si Gemini falla
"""

import os
from dotenv import load_dotenv
from typing import List, Dict
from gemini_paraphraser import GeminiParaphraser
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests

load_dotenv()

BLACKBOX_API_KEY_PRO = os.getenv('BLACKBOX_API_KEY_PRO')
BLACKBOX_MODEL_PRO = os.getenv('BLACKBOX_MODEL_PRO', os.getenv('BLACKBOX_CURRENT_MODEL', 'blackboxai/x-ai/grok-code-fast-1:free'))
BLACKBOX_API_URL = 'https://api.blackbox.ai/chat/completions'


class HybridParaphraser:
    """Sistema híbrido que usa Blackbox Pro + Gemini paralelo + Blackbox Free"""
    
    def __init__(self):
        self.gemini = GeminiParaphraser()  # 4 keys Gemini
        
        # Verificar Blackbox
        if not BLACKBOX_API_KEY_PRO:
            raise ValueError("BLACKBOX_API_KEY_PRO no encontrada")
        
        self.blackbox_key = BLACKBOX_API_KEY_PRO
        self.blackbox_model = BLACKBOX_MODEL_PRO
        
        print(f"🔑 Sistema Híbrido inicializado:")
        print(f"   • Gemini: {len(self.gemini.api_keys)} keys (placeholders)")
        print(f"   • Blackbox AI: {self.blackbox_model} (artículos principales)")
    
    def parafrasear_articulo_completo(self, article: Dict, style: str = "formal y objetivo") -> Dict:
        """
        Parafraseo completo con Blackbox Pro (para artículos principales)
        Usa el mismo prompt que paraphrase.py
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
        
        prompt = f"""Eres un periodista senior especializado en política. Reescribe el siguiente artículo de noticias con un estilo {style}.

INSTRUCCIONES CRÍTICAS DE FORMATO Y CALIDAD:

1. TÍTULO: 
   - Crea un título informativo y descriptivo (60-120 caracteres)

2. ESTRUCTURA DE PÁRRAFOS (MUY IMPORTANTE):
   - Escribe 8-12 párrafos SEPARADOS con doble salto de línea
   - Cada párrafo: 3-5 oraciones (100-150 palabras)
   - NUNCA escribas todo en un solo bloque

3. GRAMÁTICA Y PUNTUACIÓN:
   - Puntos, comas, punto y coma correctos
   - Oraciones máximo 30-35 palabras

4. FORMATO DE RESPUESTA:
   [TÍTULO]
   Título informativo aquí
   
   [ARTÍCULO]
   
   Primer párrafo con introducción.
   
   Segundo párrafo desarrollando.
   
   [Continuar con 9 párrafos más]

Artículo original:
{base_text}

Artículo expandido:"""

        payload = {
            "model": self.blackbox_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un periodista senior especializado en política con excelente dominio del español. Escribes artículos profundos. SIEMPRE separas el contenido en párrafos distintos usando doble salto de línea. Tienes impecable gramática."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.blackbox_key}'
            }
            
            response = requests.post(BLACKBOX_API_URL, headers=headers, json=payload, timeout=90)
            response.raise_for_status()
            
            result = response.json()
            paraphrased = result['choices'][0]['message']['content'].strip()
            
            # Parsear respuesta
            article_copy = article.copy()
            
            if '[TÍTULO]' in paraphrased and '[ARTÍCULO]' in paraphrased:
                parts = paraphrased.split('[ARTÍCULO]')
                title_section = parts[0].replace('[TÍTULO]', '').strip().strip('[]').strip()
                article_body = parts[1].strip() if len(parts) > 1 else paraphrased
                
                article_copy['title'] = title_section[:150] if title_section else title
                article_copy['full_text'] = article_body
                article_copy['description'] = article_body[:300] + '...' if len(article_body) > 300 else article_body
            else:
                lines = paraphrased.split('\n\n')
                article_copy['title'] = lines[0][:150] if lines else title
                article_copy['full_text'] = '\n\n'.join(lines[1:]) if len(lines) > 1 else paraphrased
                article_copy['description'] = article_copy['full_text'][:300]
            
            if 'content' in article_copy:
                article_copy['content'] = article_copy['full_text']
            
            article_copy['paraphrased'] = True
            article_copy['paraphrase_method'] = 'blackbox-hybrid'
            article_copy['style'] = style
            article_copy['key_used'] = 'KEY_PRO'
            
            return article_copy
            
        except Exception as e:
            print(f"  ❌ Error Blackbox AI: {e}")
            article['paraphrased'] = False
            article['key_used'] = 'KEY_PRO'
            return article
    
    def parafrasear_principales_secuencial(
        self,
        articles: List[Dict],
        styles: List[str] = None
    ) -> List[Dict]:
        """
        Parafrasea artículos principales de forma secuencial con Blackbox Pro
        (Un solo worker porque solo hay 1 key Pro)
        """
        if not styles:
            styles = ["formal y objetivo", "casual y cercano", "técnico y detallado"]
        
        print(f"\n{'='*70}")
        print("📝 PARAFRASEO DE ARTÍCULOS PRINCIPALES (Blackbox AI)")
        print(f"{'='*70}")
        print(f"Artículos: {len(articles)}")
        print(f"Tiempo estimado: ~{len(articles) * 1.5:.0f} minutos")
        print()
        
        results = []
        start_time = time.time()
        
        for idx, article in enumerate(articles, 1):
            style = styles[idx % len(styles)]
            print(f"[{idx}/{len(articles)}] Parafraseando con estilo '{style}'...", end=" ", flush=True)
            
            result = self.parafrasear_articulo_completo(article, style)
            
            if result.get('paraphrased'):
                print(f"✅ {result['title'][:50]}...")
            else:
                print(f"⚠️  Usando original")
            
            results.append(result)
        
        elapsed = time.time() - start_time
        successful = sum(1 for r in results if r.get('paraphrased'))
        
        print(f"\n{'='*70}")
        print(f"✅ Artículos principales completados")
        print(f"{'='*70}")
        print(f"  Total: {len(articles)}")
        print(f"  Exitosos: {successful}")
        print(f"  Tiempo: {elapsed/60:.1f} minutos")
        print(f"{'='*70}")
        
        return results
    
    def generar_dataset_completo(
        self,
        num_principales: int = 20,
        num_placeholders_por_categoria: int = 20
    ) -> Dict:
        """
        Genera dataset completo optimizado
        
        Args:
            num_principales: Artículos principales con parafraseo completo
            num_placeholders_por_categoria: Placeholders por categoría
            
        Returns:
            Dataset con principales y placeholders
        """
        from newsapi import fetch_newsapi
        from categorizer import NewsCategorizador
        
        categorizador = NewsCategorizador()
        
        # PASO 1: Descargar principales
        print(f"\n{'='*70}")
        print("📥 PASO 1: Descargando artículos principales")
        print(f"{'='*70}")
        
        noticias_principales = fetch_newsapi(
            query='política México',
            language='es',
            page_size=num_principales,
            enrich=True,
            silent=False
        )
        
        # PASO 2: Parafrasear principales (Blackbox AI, secuencial)
        principales_parafraseados = self.parafrasear_principales_secuencial(noticias_principales)
        
        # PASO 3: Categorizar principales
        print(f"\n{'='*70}")
        print("🏷️  Categorizando artículos principales")
        print(f"{'='*70}")
        
        principales_categorizados = categorizador.categorizar_lote(
            principales_parafraseados,
            use_ai=True,
            batch_delay=0.3
        )
        
        # PASO 4: Generar placeholders (Gemini paralelo)
        total_placeholders = num_placeholders_por_categoria * 10
        
        print(f"\n{'='*70}")
        print("📥 Descargando noticias para placeholders")
        print(f"{'='*70}")
        
        noticias_placeholder = fetch_newsapi(
            query='política México',
            language='es',
            page_size=min(total_placeholders + 50, 100),
            enrich=False,
            silent=False
        )
        
        # PASO 5: Parafrasear placeholders (Gemini paralelo)
        print(f"\n{'='*70}")
        print("🚀 Parafraseando placeholders con Gemini (paralelo)")
        print(f"{'='*70}")
        
        placeholders_parafraseados = self.gemini.parafrasear_lote_paralelo(
            noticias_placeholder,
            max_workers=3,
            delay_between_batches=0.5
        )
        
        # PASO 6: Categorizar placeholders (keywords, rápido)
        placeholders_categorizados = categorizador.categorizar_lote(
            placeholders_parafraseados,
            use_ai=False,
            batch_delay=0
        )
        
        # PASO 7: Agrupar y distribuir
        placeholders_por_categoria = {}
        grouped = categorizador.agrupar_por_categoria(placeholders_categorizados)
        
        for cat_id in categorizador.CATEGORIAS.keys():
            cat_placeholders = grouped.get(cat_id, [])
            placeholders_por_categoria[cat_id] = cat_placeholders[:num_placeholders_por_categoria]
        
        total_placeholders_finales = sum(len(p) for p in placeholders_por_categoria.values())
        
        return {
            'principales': principales_categorizados,
            'placeholders_por_categoria': placeholders_por_categoria,
            'stats': {
                'total_principales': len(principales_categorizados),
                'total_placeholders': total_placeholders_finales,
                'categorias': len(placeholders_por_categoria)
            }
        }


def main():
    """Test del sistema híbrido"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║        🚀 SISTEMA HÍBRIDO DE PARAFRASEO OPTIMIZADO                  ║
║        Blackbox Pro + Gemini (4 keys) + Blackbox Free               ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    import json
    
    # Test con pocos artículos
    hybrid = HybridParaphraser()
    
    dataset = hybrid.generar_dataset_completo(
        num_principales=3,
        num_placeholders_por_categoria=5
    )
    
    # Guardar
    with open('dataset_hibrido_test.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print("✅ DATASET HÍBRIDO GENERADO")
    print(f"{'='*70}")
    print(f"  Artículos principales: {dataset['stats']['total_principales']}")
    print(f"  Placeholders: {dataset['stats']['total_placeholders']}")
    print(f"  Categorías: {dataset['stats']['categorias']}")
    print(f"\n💾 Guardado en: dataset_hibrido_test.json")


if __name__ == '__main__':
    main()
