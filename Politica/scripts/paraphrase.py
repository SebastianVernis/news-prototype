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

load_dotenv()

API_KEY = os.getenv('BLACKBOX_API_KEY')
API_URL = 'https://api.blackbox.ai/chat/completions'

class NewsParaphraser:
    """Genera variaciones de artículos usando IA"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("BLACKBOX_API_KEY no encontrada en .env")
        
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
        Parafrasea un texto usando la API de Blackbox
        
        Args:
            text: Texto original a parafrasear
            style: Estilo de escritura deseado
            
        Returns:
            Texto parafraseado
        """
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

3. CONTENIDO DEL ARTÍCULO (MÁS DE 1000 PALABRAS):
   - Párrafo 1: Introducción sólida que contextualice la noticia
   - Párrafos 2-3: Desarrollo de los hechos principales
   - Párrafos 4-5: Antecedentes relevantes y contexto político
   - Párrafos 6-7: Análisis de implicaciones políticas, sociales y económicas
   - Párrafo 8: Perspectivas de expertos o análisis comparativo
   - Párrafos 9-10: Impacto potencial en ciudadanos e instituciones
   - Párrafo 11: Consideraciones adicionales importantes
   - Párrafo 12: Conclusión que sintetice los puntos clave

4. GRAMÁTICA Y PUNTUACIÓN:
   - Usa puntos (.) para terminar oraciones completas
   - Usa comas (,) correctamente para separar ideas dentro de oraciones
   - Usa punto y coma (;) cuando conectes ideas relacionadas
   - Usa dos puntos (:) antes de listas o explicaciones
   - Revisa concordancia de género y número
   - Evita oraciones excesivamente largas (máximo 30-35 palabras)

5. FORMATO DE RESPUESTA:
   [TÍTULO]
   Título informativo y descriptivo aquí
   
   [ARTÍCULO]
   
   Primer párrafo con introducción clara y concisa. Debe contextualizar la noticia principal. Incluir 3-5 oraciones bien estructuradas.
   
   Segundo párrafo desarrollando el primer punto importante. Separado del anterior con línea en blanco. Continuación lógica del tema.
   
   Tercer párrafo con nueva idea o aspecto. Mantener coherencia narrativa. Usar transiciones adecuadas.
   
   [Continuar con 9 párrafos más de la misma manera]

6. CALIDAD PERIODÍSTICA:
   - Tono profesional apropiado para lectores informados
   - NO inventes datos específicos, pero SÍ expande contexto y análisis
   - Mantén todos los hechos del original
   - Desarrolla profundamente el contexto histórico y político
   - Usa vocabulario rico pero accesible

Artículo original:
{text}

Artículo expandido con PÁRRAFOS BIEN SEPARADOS:"""

        payload = {
            "model": "blackboxai/x-ai/grok-code-fast-1:free",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un periodista senior especializado en política con excelente dominio del español. Escribes artículos profundos, detallados y políticamente precisos de más de 1000 palabras. Tu especialidad es expandir noticias breves en análisis completos manteniendo rigor periodístico. SIEMPRE separas el contenido en párrafos distintos usando doble salto de línea. Tienes impecable gramática, puntuación y estructura narrativa."
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
            response = requests.post(API_URL, headers=self.headers, json=payload, timeout=90)
            response.raise_for_status()
            
            result = response.json()
            paraphrased = result['choices'][0]['message']['content'].strip()
            return paraphrased
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error en API: {e}")
            return text  # Retornar texto original si falla
        except (KeyError, IndexError) as e:
            print(f"❌ Error procesando respuesta: {e}")
            return text
    
    def paraphrase_article(self, article: Dict, style: str = "neutral") -> Dict:
        """
        Parafrasea un artículo completo
        
        Args:
            article: Diccionario con datos del artículo
            style: Estilo de escritura deseado
            
        Returns:
            Diccionario con artículo parafraseado
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
        
        # Texto base para parafrasear
        text_parts = [title, description]
        if full_text:
            text_parts.append(full_text[:1000])
        elif content:
            text_parts.append(content[:1000])
        
        base_text = '\n\n'.join(filter(None, text_parts))
        
        # Parafrasear
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
            
            variations.append(variation)
            print("✅")
            
            # Pequeña pausa para no saturar la API
            if (i + 1) % 5 == 0:
                time.sleep(1)
        
        return variations
    
    def process_articles(self, articles: List[Dict], variations_per_article: int = 40) -> List[Dict]:
        """
        Procesa múltiples artículos generando variaciones
        
        Args:
            articles: Lista de artículos originales
            variations_per_article: Número de variaciones por artículo
            
        Returns:
            Lista con todos los artículos y sus variaciones
        """
        all_variations = []
        
        print(f"\n{'='*70}")
        print(f"🎯 Procesando {len(articles)} artículos con {variations_per_article} variaciones cada uno")
        print(f"{'='*70}")
        
        for idx, article in enumerate(articles, 1):
            print(f"\n[{idx}/{len(articles)}] Artículo: {article.get('title', 'Sin título')[:60]}...")
            
            variations = self.generate_variations(article, variations_per_article)
            all_variations.extend(variations)
            
            print(f"✅ Generadas {len(variations)} variaciones")
        
        print(f"\n{'='*70}")
        print(f"✨ Total de artículos generados: {len(all_variations)}")
        print(f"{'='*70}")
        
        return all_variations


def main():
    """Función principal para pruebas"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  📝 Parafraseador de Noticias con IA                     ║
    ║  Blackbox API - Generación de Variaciones                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Cargar artículos de prueba
    import glob
    
    # Buscar archivos de diferentes patrones
    patterns = ['noticias_mx_*.json', 'newsapi_*.json', 'newsdata_*.json', 'worldnews_*.json', 'apitube_*.json']
    json_files = []
    for pattern in patterns:
        json_files.extend(glob.glob(pattern))
    
    if not json_files:
        print("❌ No se encontraron archivos de noticias")
        print("💡 Ejecuta primero: python3 api/newsapi.py --size 5")
        return
    
    latest_file = sorted(json_files)[-1]
    print(f"📂 Cargando: {latest_file}")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Procesar solo los primeros 2 artículos para prueba
    print(f"\n⚠️  MODO PRUEBA: Procesando solo 2 artículos con 5 variaciones cada uno")
    
    paraphraser = NewsParaphraser()
    variations = paraphraser.process_articles(articles[:2], variations_per_article=5)
    
    # Guardar resultados
    output_file = 'noticias_paraphrased_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Variaciones guardadas en: {output_file}")
    print(f"📊 Total de variaciones: {len(variations)}")


if __name__ == '__main__':
    main()
