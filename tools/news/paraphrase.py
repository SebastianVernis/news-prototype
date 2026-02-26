#!/usr/bin/env python3
"""
Módulo de parafraseado con IA usando Blackbox API
Genera múltiples variaciones de artículos de noticias
"""

import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict
import time
from datetime import datetime
from text_supervisor import supervise_article
from llm_client import chat

load_dotenv()

API_KEY = os.getenv('BLACKBOX_API_KEY')
API_URL = 'https://api.blackbox.ai/chat/completions'
PARAPHRASE_PROVIDER = os.getenv("PARAPHRASE_PROVIDER", "")
PARAPHRASE_MODEL = os.getenv("PARAPHRASE_MODEL", "")

class NewsParaphraser:
    """Genera variaciones de artículos usando IA"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        if not PARAPHRASE_PROVIDER or not PARAPHRASE_MODEL:
            print("⚠️ PARAPHRASE_PROVIDER/MODEL no configurados. Se usará texto original como fallback.")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        # Estilos de parafraseado para generar variaciones
        self.styles = [
            "formal y objetivo",
            "casual y cercano",
            "técnico y detallado",
            "breve y directo",
            "narrativo y descriptivo",
            "analítico y crítico",
            "informativo neutral",
            "editorial con opinión"
        ]
    
    def paraphrase_text(self, text: str, style: str = "neutral") -> str:
        """
        Parafrasea y EXPANDE un texto usando la API de Blackbox
        Objetivo: 800-1000 palabras mínimo

        Args:
            text: Texto original a parafrasear
            style: Estilo de escritura deseado

        Returns:
            Texto parafraseado y expandido
        """
        if not PARAPHRASE_PROVIDER or not PARAPHRASE_MODEL:
            print("⚠️ Sin proveedor de parafraseo configurado, usando texto original")
            return text

        prompt = f"""Eres un periodista senior con excelente dominio del español. Tu tarea es EXPANDIR y reescribir esta noticia para que tenga ENTRE 800 Y 1000 PALABRAS mínimo.

INSTRUCCIONES DETALLADAS:
1. Mantené TODOS los hechos y datos del original
2. Expandé cada punto con contexto, antecedentes y explicaciones
3. Agregá párrafos de transición entre secciones
4. Incluí análisis de implicaciones y posibles consecuencias
5. Usá un estilo {style}
6. Separá el contenido en párrafos distintos usando doble salto de línea
7. Gramática, puntuación y estructura impecables

ESTRUCTURA OBLIGATORIA:
- Lead expansivo (150-200 palabras): Presentar el hecho principal con detalle
- Contexto y antecedentes (200-250 palabras): Qué llevó a esta situación
- Desarrollo del hecho (250-300 palabras): Detalles completos del evento
- Fuentes y declaraciones (150-200 palabras): Citas y testimonios relevantes
- Implicaciones (150-200 palabras): Consecuencias y qué esperar

NO resumas, NO acortes, NO omitas información. EXPANDÉ cada punto con detalle.
El resultado final DEBE tener al menos 800 palabras.

Texto original:
{text}

Artículo expandido (800-1000+ palabras):"""

        try:
            paraphrased = chat(
                PARAPHRASE_PROVIDER,
                PARAPHRASE_MODEL,
                [
                    {"role": "system", "content": "Sos un periodista senior que expande noticias a 800-1000 palabras mínimo. Nunca resumes, siempre expandís con contexto, análisis y detalles."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=4000,
            )
            
            # Verificar longitud
            word_count = len(paraphrased.split())
            if word_count < 600:
                print(f"⚠️ Artículo corto ({word_count} palabras), intentando re-expandir...")
                # Reintentar con énfasis en longitud
                prompt_retry = f"El artículo anterior tiene solo {word_count} palabras. Necesito al menos 800 palabras. Expandí más cada sección:\n\n{prompt}"
                paraphrased = chat(
                    PARAPHRASE_PROVIDER,
                    PARAPHRASE_MODEL,
                    [{"role": "user", "content": prompt_retry}],
                    temperature=0.7,
                    max_tokens=4000,
                )
            
            return paraphrased
        except Exception as e:
            print(f"❌ Error en parafraseo: {e}")
            return text

    def paraphrase_article(self, article: Dict, style: str = "neutral") -> Dict:
        """
        Parafrasea un artículo completo expandiéndolo a 800-1000 palabras

        Args:
            article: Diccionario con datos del artículo
            style: Estilo de escritura deseado

        Returns:
            Diccionario con artículo parafraseado y expandido
        """
        # Detectar formato del artículo
        is_normalized = isinstance(article.get('source'), str)

        # Extraer campos según formato
        if is_normalized:
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            full_text = article.get('full_text', '')
        else:
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            full_text = article.get('full_text', article.get('content', ''))

        # Usar el texto COMPLETO para parafrasear y expandir
        text_parts = [title]
        if full_text:
            text_parts.append(full_text)  # Texto completo, no truncado
        elif content:
            text_parts.append(content)  # Texto completo
        elif description:
            text_parts.append(description)

        base_text = '\n\n'.join(filter(None, text_parts))

        # Parafrasear expandiendo a 800-1000 palabras
        paraphrased = self.paraphrase_text(base_text, style)
        
        # Crear copia del artículo con texto parafraseado
        result = article.copy()
        
        # Extraer título y artículo del formato estructurado
        if '[TÍTULO]' in paraphrased and '[ARTÍCULO]' in paraphrased:
            parts = paraphrased.split('[ARTÍCULO]')
            title_section = parts[0].replace('[TÍTULO]', '').strip()
            article_body = parts[1].strip() if len(parts) > 1 else paraphrased
            
            title_section = title_section.strip('[]').strip()
            
            result['title'] = title_section[:150] if title_section else article.get('title', '')[:150]
            result['full_text'] = article_body
            result['description'] = article_body[:300] + '...' if len(article_body) > 300 else article_body
        else:
            lines = paraphrased.split('\n\n')
            result['title'] = lines[0][:150] if lines else article.get('title', '')[:150]
            result['full_text'] = '\n\n'.join(lines[1:]) if len(lines) > 1 else paraphrased
            result['description'] = result['full_text'][:300] + '...' if len(result['full_text']) > 300 else result['full_text']
        
        # Actualizar campo 'content'
        if 'content' in result:
            result['content'] = result['full_text']

        # Reemplazar autor con 'Redacción {categoría}'
        category = article.get('category', 'General')
        result['author'] = f"Redacción {category}"
        
        # Eliminar fuente original
        if 'source' in result:
            del result['source']

        return result
    
    def generate_variations(self, article: Dict, num_variations: int = 40) -> List[Dict]:
        """
        Genera múltiples variaciones de un artículo
        
        Args:
            article: Diccionario con datos del artículo
            num_variations: Número de variaciones a generar
            
        Returns:
            Lista de artículos con variaciones
        """
        variations = []
        
        # Detectar formato del artículo (normalizado vs original)
        # Formato normalizado tiene 'source' como string, original como dict
        is_normalized = isinstance(article.get('source'), str)
        
        # Extraer campos según formato
        if is_normalized:
            # Formato normalizado de utils.py
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            full_text = article.get('full_text', '')
        else:
            # Formato original de NewsAPI
            title = article.get('title', '')
            description = article.get('description', '')
            content = article.get('content', '')
            full_text = article.get('full_text', article.get('content', ''))
        
        # Texto base para parafrasear (usar el más largo disponible)
        text_parts = [title, description]
        if full_text:
            text_parts.append(full_text[:1000])
        elif content:
            text_parts.append(content[:1000])
        
        base_text = '\n\n'.join(filter(None, text_parts))
        
        print(f"\n📝 Generando {num_variations} variaciones para: {article.get('title', 'Sin título')[:60]}...")
        
        # Generar variaciones usando diferentes estilos
        for i in range(num_variations):
            style = self.styles[i % len(self.styles)]
            
            print(f"  [{i+1}/{num_variations}] Estilo: {style}...", end=" ")
            
            paraphrased = self.paraphrase_text(base_text, style)
            
            # Crear copia del artículo con texto parafraseado
            variation = article.copy()
            
            # Extraer título y artículo del formato estructurado
            if '[TÍTULO]' in paraphrased and '[ARTÍCULO]' in paraphrased:
                # Formato estructurado presente
                parts = paraphrased.split('[ARTÍCULO]')
                title_section = parts[0].replace('[TÍTULO]', '').strip()
                article_body = parts[1].strip() if len(parts) > 1 else paraphrased
                
                # Limpiar corchetes del título si existen
                title_section = title_section.strip('[]').strip()
                
                variation['title'] = title_section[:150] if title_section else article.get('title', '')[:150]
                variation['full_text'] = article_body
                variation['description'] = article_body[:300] + '...' if len(article_body) > 300 else article_body
            else:
                # Fallback si no hay formato estructurado
                lines = paraphrased.split('\n\n')
                variation['title'] = lines[0][:150] if lines else article.get('title', '')[:150]
                variation['full_text'] = '\n\n'.join(lines[1:]) if len(lines) > 1 else paraphrased
                variation['description'] = variation['full_text'][:300] + '...' if len(variation['full_text']) > 300 else variation['full_text']
            
            # Actualizar campo 'content' con el texto completo
            if 'content' in variation:
                variation['content'] = variation['full_text']
            
            variation['variation_id'] = i + 1
            variation['style'] = style
            variation['original_title'] = title
            variation['original_article_id'] = article.get('id', article.get('url', hash(title) % 10000))
            
            variations.append(variation)
            print("✅")
            
            # Pequeña pausa para no saturar la API
            if (i + 1) % 5 == 0:
                time.sleep(1)
        
        return variations
    
    def process_articles(self, articles: List[Dict], variations_per_article: int = 1) -> List[Dict]:
        """
        Procesa múltiples artículos generando UNA SOLA variación por artículo.
        
        Args:
            articles: Lista de artículos originales
            variations_per_article: Número de variaciones por artículo (default: 1)
            
        Returns:
            Lista con UNA variación por cada artículo original
        """
        all_variations = []
        
        print(f"\n{'='*70}")
        print(f"🎯 Procesando {len(articles)} artículos (1 variación por artículo)")
        print(f"{'='*70}")
        
        for idx, article in enumerate(articles, 1):
            print(f"\n[{idx}/{len(articles)}] Artículo: {article.get('title', 'Sin título')[:60]}...")
            
            # Forzar 1 variación por artículo
            variations = self.generate_variations(article, num_variations=1)
            all_variations.extend(variations)
            
            print(f"✅ Generada 1 variación")
        
        print(f"\n{'='*70}")
        print(f"✨ Total de artículos generados: {len(all_variations)}")
        print(f"{'='*70}")
        
        return all_variations


def main():
    """CLI principal"""
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Parafraseador de noticias con IA")
    parser.add_argument("--input", type=str, help="Archivo JSON de entrada")
    parser.add_argument("--output", type=str, help="Archivo JSON de salida")
    parser.add_argument("--limit", type=int, default=20, help="Número de artículos a procesar")
    parser.add_argument("--supervisor", action="store_true", help="Aplicar supervisión gramatical con LLM")
    parser.add_argument("--supervisor-provider", type=str, default=os.getenv("SUPERVISOR_PROVIDER", ""))
    parser.add_argument("--supervisor-model", type=str, default=os.getenv("SUPERVISOR_MODEL", ""))
    parser.add_argument("--provider", type=str, default=os.getenv("PARAPHRASE_PROVIDER", ""))
    parser.add_argument("--model", type=str, default=os.getenv("PARAPHRASE_MODEL", ""))
    args = parser.parse_args()

    data_dir = Path(os.getenv("NEWS_DATA_DIR", Path(__file__).resolve().parents[2] / "data"))
    data_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input) if args.input else None
    if not input_path or not input_path.exists():
        # Buscar archivo más reciente en data/
        candidates = []
        patterns = ['noticias_mx_*.json', 'newsapi_*.json', 'newsdata_*.json', 'worldnews_*.json', 'apitube_*.json']
        for pattern in patterns:
            candidates.extend(data_dir.glob(pattern))
        if not candidates:
            print("❌ No se encontraron archivos de noticias en data/")
            return
        input_path = sorted(candidates)[-1]

    print(f"📂 Cargando: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    paraphraser = NewsParaphraser()
    global PARAPHRASE_PROVIDER, PARAPHRASE_MODEL
    PARAPHRASE_PROVIDER = args.provider or PARAPHRASE_PROVIDER
    PARAPHRASE_MODEL = args.model or PARAPHRASE_MODEL

    variations = paraphraser.process_articles(articles[: args.limit], variations_per_article=1)

    if args.supervisor:
        provider = args.supervisor_provider
        model = args.supervisor_model
        if provider and model:
            variations = [supervise_article(a, provider, model) for a in variations]

    output_path = Path(args.output) if args.output else data_dir / f"noticias_paraphrased_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(variations, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Variaciones guardadas en: {output_path}")
    print(f"📊 Total de variaciones: {len(variations)}")


if __name__ == '__main__':
    main()
