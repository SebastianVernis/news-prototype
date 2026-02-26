#!/usr/bin/env python3
"""
Sintetizador de Múltiples Fuentes (Offline)
Combina información de varias fuentes sobre el mismo tema
sin usar IA generativa, mediante técnicas de extracción y fusión.
"""

import re
import json
from typing import List, Dict, Tuple, Set
from collections import Counter
from difflib import SequenceMatcher
import hashlib


class MultiSourceSynthesizer:
    """
    Sintetiza información de múltiples fuentes sobre el mismo tema.
    Funciona 100% offline usando técnicas de NLP básicas.
    """
    
    def __init__(self):
        # Palabras vacías en español
        self.stopwords = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'y', 'o', 'pero', 'sin', 'con', 'por', 'para', 'de', 'del',
            'al', 'en', 'a', 'ante', 'bajo', 'desde', 'hasta', 'hacia',
            'sobre', 'entre', 'durante', 'mediante', 'según', 'tras',
            'que', 'como', 'cuando', 'donde', 'quien', 'cuyo', 'cuya',
            'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
            'aquel', 'aquella', 'aquellos', 'aquellas', 'mi', 'tu', 'su',
            'nuestro', 'vuestro', 'suyo', 'mío', 'tuyo', 'suyo',
            'es', 'son', 'fue', 'fueron', 'era', 'eran', 'será', 'serán',
            'ha', 'han', 'había', 'habían', 'habrá', 'habrán',
            'está', 'están', 'estaba', 'estaban', 'estará', 'estarán',
            'tiene', 'tienen', 'tenía', 'tenían', 'tendrá', 'tendrán'
        }
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extrae palabras clave de un texto.
        
        Args:
            text: Texto a analizar
            top_n: Número de palabras clave a retornar
            
        Returns:
            Lista de palabras clave
        """
        # Limpiar y tokenizar
        words = re.findall(r'\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]{4,}\b', text.lower())
        
        # Filtrar stopwords y contar
        filtered = [w for w in words if w not in self.stopwords]
        word_counts = Counter(filtered)
        
        # Retornar las más frecuentes
        return [word for word, _ in word_counts.most_common(top_n)]
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calcula similitud entre dos textos.
        
        Args:
            text1: Primer texto
            text2: Segundo texto
            
        Returns:
            Score de similitud (0.0 - 1.0)
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def find_similar_articles(self, articles: List[Dict], threshold: float = 0.6) -> List[List[Dict]]:
        """
        Agrupa artículos similares sobre el mismo tema.
        
        Args:
            articles: Lista de artículos
            threshold: Umbral de similitud para agrupar
            
        Returns:
            Lista de grupos de artículos similares
        """
        groups = []
        used = set()
        
        for i, article1 in enumerate(articles):
            if i in used:
                continue
                
            group = [article1]
            used.add(i)
            
            title1 = article1.get('title', '')
            keywords1 = set(self.extract_keywords(title1))
            
            for j, article2 in enumerate(articles[i+1:], start=i+1):
                if j in used:
                    continue
                    
                title2 = article2.get('title', '')
                keywords2 = set(self.extract_keywords(title2))
                
                # Calcular similitud por keywords y título (índice Jaccard simétrico)
                intersection = keywords1 & keywords2
                union = keywords1 | keywords2
                keyword_sim = len(intersection) / max(len(union), 1)
                title_sim = self.calculate_similarity(title1, title2)
                
                # Score combinado
                combined_score = (keyword_sim * 0.6) + (title_sim * 0.4)
                
                if combined_score >= threshold:
                    group.append(article2)
                    used.add(j)
            
            if len(group) >= 2:  # Solo grupos con 2+ artículos
                groups.append(group)
        
        return groups
    
    def extract_facts(self, text: str) -> List[str]:
        """
        Extrae hechos/declaraciones de un texto.
        Busca oraciones con números, fechas, nombres propios, etc.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Lista de hechos extraídos
        """
        facts = []
        
        # Dividir en oraciones
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20:
                continue
            
            # Detectar hechos por patrones
            has_number = bool(re.search(r'\d+', sentence))
            has_date = bool(re.search(r'\b\d{1,2}[/-]\d{1,2}[/-](?:19|20)\d{2}\b|\b(?:19|20)\d{2}\b', sentence))
            has_percentage = bool(re.search(r'\d+%|\d+\s*por\s*ciento', sentence, re.I))
            has_money = bool(re.search(r'\$[\d,]+|\d+\s*(pesos|dólares|euros|millones|miles)', sentence, re.I))
            has_quote = bool(re.search(r'[""''"].*?[""''"]', sentence))
            
            # Puntuar la oración
            score = sum([has_number, has_date, has_percentage, has_money, has_quote])
            
            if score >= 2:  # Al menos 2 indicadores de hecho
                facts.append({
                    'text': sentence,
                    'score': score,
                    'has_number': has_number,
                    'has_date': has_date
                })
        
        # Ordenar por score y retornar textos
        facts.sort(key=lambda x: x['score'], reverse=True)
        return [f['text'] for f in facts[:5]]  # Top 5 hechos
    
    def synthesize_group(self, articles: List[Dict]) -> Dict:
        """
        Sintetiza un grupo de artículos similares en uno solo.
        
        Args:
            articles: Grupo de artículos sobre el mismo tema
            
        Returns:
            Artículo sintetizado
        """
        if not articles:
            return {}
        
        # Usar el artículo más largo como base
        base_article = max(articles, key=lambda a: len(a.get('description', '')))
        
        # Extraer todos los hechos de todos los artículos
        all_facts = []
        for article in articles:
            text = article.get('description', '') + ' ' + article.get('content', '')
            facts = self.extract_facts(text)
            all_facts.extend(facts)
        
        # Eliminar hechos duplicados (similares)
        unique_facts = []
        for fact in all_facts:
            is_duplicate = False
            for existing in unique_facts:
                if self.calculate_similarity(fact, existing) > 0.7:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_facts.append(fact)
        
        # Construir descripción sintetizada
        base_desc = base_article.get('description', '')
        
        # Agregar hechos adicionales si no están en la descripción base
        additional_facts = []
        for fact in unique_facts[:3]:  # Máximo 3 hechos adicionales
            if self.calculate_similarity(fact, base_desc) < 0.5:
                additional_facts.append(fact)
        
        # Crear descripción enriquecida
        synthesized_description = base_desc
        if additional_facts:
            synthesized_description += " " + " ".join(additional_facts)
        
        # Crear artículo sintetizado
        synthesized = {
            'title': base_article.get('title', ''),
            'description': synthesized_description,
            'content': base_article.get('content', ''),
            'url': base_article.get('url', ''),
            'image_url': base_article.get('image_url', ''),
            'published_at': base_article.get('published_at', ''),
            'source': 'synthesized',
            'sources_count': len(articles),
            'source_names': list(set(a.get('source_name', 'Desconocido') for a in articles)),
            'synthesis_method': 'multi_source_offline',
            'facts_extracted': len(unique_facts),
            'original_articles': [
                {
                    'title': a.get('title', ''),
                    'source': a.get('source_name', 'Desconocido')
                } for a in articles[:3]  # Guardar referencia a fuentes
            ]
        }
        
        return synthesized
    
    def synthesize_articles(self, articles: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        Proceso completo de síntesis de artículos.
        
        Args:
            articles: Lista de artículos de múltiples fuentes
            
        Returns:
            Tupla de (artículos sintetizados, estadísticas)
        """
        print(f"🔍 Analizando {len(articles)} artículos...")
        
        # Encontrar grupos similares
        groups = self.find_similar_articles(articles)
        print(f"📊 Encontrados {len(groups)} grupos de artículos similares")
        
        synthesized = []
        used_articles = set()
        
        # Sintetizar cada grupo
        for i, group in enumerate(groups, 1):
            print(f"  🔄 Sintetizando grupo {i}: {len(group)} artículos")
            
            synthesized_article = self.synthesize_group(group)
            if synthesized_article:
                synthesized.append(synthesized_article)
                
                # Marcar artículos como usados
                for article in group:
                    article_id = hashlib.md5(
                        article.get('title', '').encode()
                    ).hexdigest()[:10]
                    used_articles.add(article_id)
        
        # Agregar artículos únicos (no agrupados)
        for article in articles:
            article_id = hashlib.md5(
                article.get('title', '').encode()
            ).hexdigest()[:10]
            
            if article_id not in used_articles:
                article_copy = dict(article)
                article_copy['synthesis_method'] = 'original'
                article_copy['sources_count'] = 1
                synthesized.append(article_copy)
        
        stats = {
            'total_input': len(articles),
            'groups_found': len(groups),
            'synthesized': len(synthesized),
            'compression_ratio': len(synthesized) / max(len(articles), 1)
        }
        
        print(f"\n✅ Síntesis completada:")
        print(f"   Artículos de entrada: {stats['total_input']}")
        print(f"   Artículos de salida: {stats['synthesized']}")
        print(f"   Ratio de compresión: {stats['compression_ratio']:.2f}")
        
        return synthesized, stats


# Demo
if __name__ == "__main__":
    # Artículos de ejemplo sobre el mismo tema
    test_articles = [
        {
            'title': 'México anuncia nuevo plan económico para 2026',
            'description': 'El gobierno mexicano presentó un ambicioso plan económico que incluye reducción de impuestos y apoyo a pequeñas empresas. Se espera que el PIB crezca 3.5% el próximo año.',
            'source_name': 'El Economista',
            'published_at': '2026-01-20'
        },
        {
            'title': 'Gobierno federal lanza estrategia económica 2026',
            'description': 'La administración anunció medidas fiscales para impulsar la economía. Entre ellas, beneficios tributarios para PYMES y una proyección de crecimiento del 3.5%.',
            'source_name': 'Reforma',
            'published_at': '2026-01-20'
        },
        {
            'title': 'Nuevas políticas fiscales beneficiarán a empresas mexicanas',
            'description': 'El Ejecutivo presentó reformas tributarias orientadas a la reactivación económica. Las PYMES serán las principales beneficiadas con reducciones de impuestos.',
            'source_name': 'Milenio',
            'published_at': '2026-01-21'
        },
        {
            'title': 'Descubren nueva especie de dinosaurio en Argentina',
            'description': 'Paleontólogos argentinos encontraron restos fósiles de una especie desconocida de dinosaurio herbívoro en la Patagonia.',
            'source_name': 'National Geographic',
            'published_at': '2026-01-20'
        }
    ]
    
    synthesizer = MultiSourceSynthesizer()
    result, stats = synthesizer.synthesize_articles(test_articles)
    
    print("\n" + "="*70)
    print("RESULTADOS DE LA SÍNTESIS")
    print("="*70)
    
    for article in result:
        print(f"\n📰 {article['title']}")
        print(f"   Método: {article.get('synthesis_method', 'unknown')}")
        print(f"   Fuentes: {article.get('sources_count', 1)}")
        if article.get('source_names'):
            print(f"   Nombres: {', '.join(article['source_names'])}")
        print(f"   Descripción: {article['description'][:150]}...")