#!/usr/bin/env python3
"""
Sistema de Categorización Inteligente de Noticias
Usa IA para clasificar noticias en categorías relevantes
"""

import os
import json
import requests
from dotenv import load_dotenv
from typing import List, Dict, Tuple
import re

load_dotenv()

API_KEY = os.getenv('BLACKBOX_API_KEY')
API_URL = 'https://api.blackbox.ai/chat/completions'


class NewsCategorizador:
    """Categoriza noticias usando IA"""
    
    # Categorías políticas relevantes para México
    CATEGORIAS = {
        "política-nacional": {
            "nombre": "Política Nacional",
            "descripcion": "Política interna, gobierno federal, reformas, leyes",
            "keywords": ["gobierno", "presidente", "reforma", "congreso", "senado", "diputados", "legislativo", "ejecutivo"]
        },
        "política-internacional": {
            "nombre": "Política Internacional",
            "descripcion": "Relaciones exteriores, diplomacia, acuerdos internacionales",
            "keywords": ["internacional", "eeuu", "estados unidos", "diplomacia", "embajador", "otan", "onu"]
        },
        "economía-política": {
            "nombre": "Economía y Política",
            "descripcion": "Políticas económicas, presupuesto, inversión pública",
            "keywords": ["economía", "presupuesto", "fiscal", "impuestos", "inversión", "banco", "hacienda"]
        },
        "seguridad": {
            "nombre": "Seguridad y Justicia",
            "descripcion": "Seguridad pública, crimen, justicia, fuerzas armadas",
            "keywords": ["seguridad", "policía", "crimen", "narcotráfico", "ejército", "guardia", "delitos"]
        },
        "elecciones": {
            "nombre": "Elecciones y Partidos",
            "descripcion": "Procesos electorales, partidos políticos, campañas",
            "keywords": ["elecciones", "electoral", "partido", "voto", "campaña", "candidato", "ine"]
        },
        "derechos-sociales": {
            "nombre": "Derechos y Políticas Sociales",
            "descripcion": "Derechos humanos, políticas sociales, educación, salud",
            "keywords": ["derechos", "social", "educación", "salud", "pensiones", "bienestar", "igualdad"]
        },
        "medio-ambiente": {
            "nombre": "Medio Ambiente y Energía",
            "descripcion": "Políticas ambientales, energía, cambio climático",
            "keywords": ["ambiente", "energía", "pemex", "cfe", "clima", "ecología", "renovable"]
        },
        "judicial": {
            "nombre": "Poder Judicial",
            "descripcion": "Sistema judicial, cortes, tribunales, jueces",
            "keywords": ["judicial", "corte", "juez", "tribunal", "scjn", "suprema", "sentencia"]
        },
        "corrupción": {
            "nombre": "Anticorrupción y Transparencia",
            "descripcion": "Casos de corrupción, transparencia, fiscalización",
            "keywords": ["corrupción", "transparencia", "fiscalización", "asf", "auditoría", "soborno"]
        },
        "análisis-opinión": {
            "nombre": "Análisis y Opinión",
            "descripcion": "Columnas de opinión, análisis político, editoriales",
            "keywords": ["análisis", "opinión", "editorial", "columna", "perspectiva", "considera"]
        }
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("BLACKBOX_API_KEY no encontrada en .env")
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def categorizar_con_ia(self, article: Dict) -> Tuple[str, float]:
        """
        Categoriza un artículo usando IA
        
        Args:
            article: Diccionario con datos del artículo
            
        Returns:
            Tuple (categoría, confianza)
        """
        # Extraer información relevante
        title = article.get('title', '')
        description = article.get('description', '')
        content = article.get('content', article.get('full_text', ''))[:500]
        
        # Crear lista de categorías para el prompt
        categorias_texto = "\n".join([
            f"- {cat_id}: {cat_data['nombre']} - {cat_data['descripcion']}"
            for cat_id, cat_data in self.CATEGORIAS.items()
        ])
        
        prompt = f"""Analiza el siguiente artículo de noticias políticas y clasifícalo en UNA de las siguientes categorías:

{categorias_texto}

ARTÍCULO:
Título: {title}
Descripción: {description}
Contenido: {content}

INSTRUCCIONES:
1. Analiza el tema principal del artículo
2. Selecciona la categoría MÁS APROPIADA (solo una)
3. Responde ÚNICAMENTE con el ID de la categoría (ej: "política-nacional")
4. NO agregues explicaciones, solo el ID

Categoría:"""

        payload = {
            "model": "blackboxai/blackbox-pro",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un experto en clasificación de noticias políticas. Respondes únicamente con el ID de la categoría, sin explicaciones adicionales."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,  # Baja temperatura para respuestas más consistentes
            "max_tokens": 50
        }
        
        try:
            response = requests.post(API_URL, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            categoria = result['choices'][0]['message']['content'].strip().lower()
            
            # Limpiar la respuesta
            categoria = categoria.replace('"', '').replace("'", '').strip()
            
            # Verificar que sea una categoría válida
            if categoria in self.CATEGORIAS:
                return categoria, 0.9
            else:
                # Fallback a categorización por keywords
                return self.categorizar_por_keywords(article)
                
        except Exception as e:
            print(f"  ⚠️  Error en IA, usando keywords: {e}")
            return self.categorizar_por_keywords(article)
    
    def categorizar_por_keywords(self, article: Dict) -> Tuple[str, float]:
        """
        Categoriza usando keywords como fallback
        
        Args:
            article: Diccionario con datos del artículo
            
        Returns:
            Tuple (categoría, confianza)
        """
        # Combinar texto del artículo
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        content = article.get('content', article.get('full_text', ''))[:1000].lower()
        
        texto_completo = f"{title} {description} {content}"
        
        # Contar matches por categoría
        scores = {}
        for cat_id, cat_data in self.CATEGORIAS.items():
            score = 0
            for keyword in cat_data['keywords']:
                # Contar ocurrencias de cada keyword
                score += len(re.findall(r'\b' + re.escape(keyword) + r'\b', texto_completo))
            
            scores[cat_id] = score
        
        # Obtener categoría con mayor score
        if scores:
            best_category = max(scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:
                # Calcular confianza basada en score
                confianza = min(0.9, 0.3 + (best_category[1] * 0.1))
                return best_category[0], confianza
        
        # Default: análisis-opinión
        return "análisis-opinión", 0.3
    
    def categorizar_articulo(self, article: Dict, use_ai: bool = True) -> Dict:
        """
        Categoriza un artículo y retorna datos enriquecidos
        
        Args:
            article: Artículo a categorizar
            use_ai: Si True, usa IA; si False, usa keywords
            
        Returns:
            Artículo con categoría agregada
        """
        if use_ai:
            categoria, confianza = self.categorizar_con_ia(article)
        else:
            categoria, confianza = self.categorizar_por_keywords(article)
        
        # Agregar datos de categoría
        article_copy = article.copy()
        article_copy['category_id'] = categoria
        article_copy['category_name'] = self.CATEGORIAS[categoria]['nombre']
        article_copy['category_confidence'] = confianza
        
        return article_copy
    
    def categorizar_lote(self, articles: List[Dict], use_ai: bool = True, batch_delay: float = 0.5) -> List[Dict]:
        """
        Categoriza múltiples artículos
        
        Args:
            articles: Lista de artículos
            use_ai: Si True, usa IA
            batch_delay: Delay entre requests (rate limiting)
            
        Returns:
            Lista de artículos categorizados
        """
        import time
        
        print(f"\n{'='*70}")
        print(f"🏷️  CATEGORIZANDO {len(articles)} ARTÍCULOS")
        print(f"{'='*70}")
        print(f"Método: {'IA (Blackbox)' if use_ai else 'Keywords'}")
        print()
        
        categorized = []
        category_counts = {}
        
        for idx, article in enumerate(articles, 1):
            title = article.get('title', 'Sin título')[:60]
            print(f"[{idx}/{len(articles)}] {title}...", end=" ")
            
            try:
                result = self.categorizar_articulo(article, use_ai=use_ai)
                categorized.append(result)
                
                # Contar por categoría
                cat_name = result['category_name']
                category_counts[cat_name] = category_counts.get(cat_name, 0) + 1
                
                confidence_icon = "🟢" if result['category_confidence'] > 0.7 else "🟡"
                print(f"{confidence_icon} {result['category_name']}")
                
                # Rate limiting
                if use_ai and idx < len(articles):
                    time.sleep(batch_delay)
                    
            except Exception as e:
                print(f"❌ Error: {e}")
                # Agregar sin categoría
                article['category_id'] = 'análisis-opinión'
                article['category_name'] = 'Análisis y Opinión'
                article['category_confidence'] = 0.1
                categorized.append(article)
        
        print(f"\n{'='*70}")
        print(f"📊 DISTRIBUCIÓN DE CATEGORÍAS")
        print(f"{'='*70}")
        
        for cat_name, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat_name}: {count} artículos")
        
        print(f"{'='*70}")
        
        return categorized
    
    def agrupar_por_categoria(self, articles: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Agrupa artículos por categoría
        
        Args:
            articles: Lista de artículos categorizados
            
        Returns:
            Dict con categorías como keys y listas de artículos como values
        """
        grouped = {}
        
        for article in articles:
            cat_id = article.get('category_id', 'análisis-opinión')
            if cat_id not in grouped:
                grouped[cat_id] = []
            grouped[cat_id].append(article)
        
        return grouped


def main():
    """Test del categorizador"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║         🏷️  CATEGORIZADOR DE NOTICIAS CON IA                        ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Buscar archivo de noticias más reciente
    import glob
    from pathlib import Path
    
    patterns = ['noticias_parafraseadas_*.json', 'newsapi_*.json', 'noticias_originales_*.json']
    json_files = []
    for pattern in patterns:
        json_files.extend(glob.glob(pattern))
    
    if not json_files:
        print("❌ No se encontraron archivos de noticias")
        print("💡 Ejecuta primero: python3 scripts/generar_2_ejemplos.py")
        return
    
    latest_file = sorted(json_files)[-1]
    print(f"📂 Cargando: {latest_file}\n")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"📰 Artículos cargados: {len(articles)}")
    
    # Categorizar
    categorizador = NewsCategorizador()
    categorized = categorizador.categorizar_lote(articles, use_ai=True)
    
    # Agrupar por categoría
    grouped = categorizador.agrupar_por_categoria(categorized)
    
    # Guardar resultado
    output_file = 'noticias_categorizadas_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(categorized, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Guardado en: {output_file}")
    
    # Mostrar agrupación
    print(f"\n{'='*70}")
    print("📑 ARTÍCULOS POR CATEGORÍA")
    print(f"{'='*70}\n")
    
    for cat_id, cat_articles in grouped.items():
        cat_name = categorizador.CATEGORIAS.get(cat_id, {}).get('nombre', cat_id)
        print(f"\n📌 {cat_name} ({len(cat_articles)} artículos)")
        print("-" * 70)
        
        for article in cat_articles:
            conf = article.get('category_confidence', 0)
            conf_icon = "🟢" if conf > 0.7 else "🟡" if conf > 0.5 else "🔴"
            print(f"  {conf_icon} {article.get('title', 'Sin título')[:60]}...")


if __name__ == '__main__':
    main()
