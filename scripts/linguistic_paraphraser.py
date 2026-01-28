#!/usr/bin/env python3
"""
Parafraseador Lingüístico (Sin IA Generativa)
Utiliza Spacy, vectores de palabras y bases de datos de sinónimos (WordNet)
para reescribir textos conservando entidades y gramática.
"""

import os
import sys
import random
import subprocess
from typing import List, Dict, Optional

# Intentar importar spacy y nltk
try:
    import spacy
    from spacy.tokens import Token
    import nltk
    from nltk.corpus import wordnet as wn
except ImportError:
    print("⚠️  Instalando dependencias necesarias (spacy, nltk)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy", "nltk"])
    import spacy
    from spacy.tokens import Token
    import nltk
    from nltk.corpus import wordnet as wn

class LinguisticParaphraser:
    """
    Sistema de parafraseo basado en reglas lingüísticas y vectores.
    No requiere API keys ni modelos generativos costosos.
    """
    
    def __init__(self, model_size: str = "md"):
        """
        Inicializa el parafraseador.
        Args:
            model_size: 'sm' (rápido), 'md' (balanceado, con vectores), 'lg' (preciso)
        """
        self.model_name = f"es_core_news_{model_size}"
        self.nlp = self._load_spacy_model()
        self._ensure_nltk_data()
        
        # Cache de sinónimos para velocidad
        self.synonym_cache = {}
        
        # Palabras protegidas adicionales (además de entidades)
        self.protected_words = {
            'año', 'años', 'día', 'días', 'mes', 'meses', 'semana', 'semanas',
            'hora', 'horas', 'minuto', 'minutos', 'segundo', 'segundos',
            'ayer', 'hoy', 'mañana', 'país', 'mundo', 'gobierno'
        }
        
    def _load_spacy_model(self):
        """Carga el modelo de Spacy, descargándolo si es necesario"""
        try:
            return spacy.load(self.model_name)
        except OSError:
            print(f"⬇️  Descargando modelo de lenguaje: {self.model_name}...")
            subprocess.check_call([sys.executable, "-m", "spacy", "download", self.model_name])
            return spacy.load(self.model_name)

    def _ensure_nltk_data(self):
        """Descarga recursos de NLTK necesarios"""
        try:
            wn.synsets('perro', lang='spa')
        except (LookupError, AttributeError):
            print("⬇️  Descargando WordNet (Open Multilingual WordNet)...")
            nltk.download('wordnet')
            nltk.download('omw-1.4')

    def get_synonyms_wordnet(self, word: str, pos_tag: str) -> List[str]:
        """
        Obtiene sinónimos usando NLTK WordNet en español.
        Args:
            word: Palabra a buscar
            pos_tag: Etiqueta gramatical de Spacy (NOUN, VERB, ADJ, ADV)
        """
        # Mapeo de Spacy POS a WordNet POS
        wn_pos_map = {
            'NOUN': wn.NOUN,
            'VERB': wn.VERB,
            'ADJ': wn.ADJ,
            'ADV': wn.ADV
        }
        wn_pos = wn_pos_map.get(pos_tag)
        if not wn_pos:
            return []

        synonyms = set()
        # Buscar en WordNet español ('spa')
        for synset in wn.synsets(word, pos=wn_pos, lang='spa'):
            for lemma in synset.lemmas(lang='spa'):
                synonym = lemma.name().replace('_', ' ')
                if synonym.lower() != word.lower():
                    synonyms.add(synonym)
        
        return list(synonyms)

    def get_synonyms_vectors(self, token: Token, limit: int = 5) -> List[str]:
        """
        Encuentra palabras similares usando vectores de Spacy (embeddings).
        Requiere modelo 'md' o 'lg'.
        """
        if not token.has_vector or self.nlp.vocab.vectors.n_keys == 0:
            return []
            
        # Encontrar palabras más similares en el vocabulario
        # Nota: La API de 'most_similar' de Spacy varía, esta es una implementación segura usando vectores
        queries = [token.vector]
        try:
            # Esta operación puede ser costosa, usamos el método interno de best_match si existe
            most_similar = self.nlp.vocab.vectors.most_similar(queries, n=10)
            candidate_keys = most_similar[0][0]
            
            candidates = []
            for key in candidate_keys:
                candidate_word = self.nlp.vocab.strings[key]
                if candidate_word.lower() != token.text.lower():
                    # Verificar si realmente parece una palabra válida
                    if candidate_word.isalpha():
                        candidates.append(candidate_word)
            return candidates
        except:
            return []

    def filter_synonyms_by_similarity(self, token: Token, candidates: List[str], threshold: float = 0.45) -> List[str]:
        """
        Filtra candidatos usando similitud de vectores con la palabra original.
        """
        if not token.has_vector or not candidates:
            return candidates
            
        filtered = []
        for cand in candidates:
            # Crear doc temporal para el candidato
            cand_doc = self.nlp(cand)
            if cand_doc and cand_doc.vector_norm:
                similarity = token.similarity(cand_doc)
                if similarity >= threshold:
                    filtered.append(cand)
        
        return filtered if filtered else candidates  # Fallback si filtra todos

    def paraphrase_text(self, text: str, change_threshold: float = 0.4) -> Dict:
        """
        Parafrasea un texto completo.
        
        Args:
            text: Texto original
            change_threshold: Porcentaje de palabras 'sustituibles' que intentaremos cambiar (0.0 a 1.0)
            
        Returns:
            Dict con 'text' (nuevo texto) y stats
        """
        doc = self.nlp(text)
        new_tokens = []
        changes_made = 0
        
        # Identificar entidades para protegerlas (No cambiar nombres de Personas, Org, Lugares)
        protected_indices = set()
        for ent in doc.ents:
            for i in range(ent.start, ent.end):
                protected_indices.add(i)
        
        for token in doc:
            # Conservar puntuación, espacios y palabras protegidas tal cual
            if (token.i in protected_indices or 
                token.is_punct or 
                token.is_space or 
                token.is_stop or
                token.lemma_.lower() in self.protected_words or
                token.pos_ not in ['NOUN', 'VERB', 'ADJ', 'ADV']):
                
                new_tokens.append(token.text_with_ws)
                continue
            
            # Decidir aleatoriamente si cambiar esta palabra (basado en threshold)
            if random.random() > change_threshold:
                new_tokens.append(token.text_with_ws)
                continue
                
            # Intentar buscar sinónimos
            # Estrategia: Preferir WordNet por ser sinónimos "reales", usar vectores como fallback
            synonyms = self.get_synonyms_wordnet(token.lemma_, token.pos_)
            
            # Filtrar por similitud vectorial para evitar sinónimos fuera de contexto
            if synonyms:
                synonyms = self.filter_synonyms_by_similarity(token, synonyms)

            if synonyms:
                # Seleccionar un sinónimo aleatorio
                choice = random.choice(synonyms)
                
                # Intentar igualar la morfología (básico)
                # Si la palabra original es mayúscula
                if token.text[0].isupper():
                    choice = choice.capitalize()
                
                # TODO: Implementar lógica avanzada de inflexión (género/número)
                # Esto es difícil sin librerías pesadas, así que por ahora confiamos en el lemma
                # Para verbos, esto suele devolver el infinitivo, lo cual puede sonar "robotico"
                # Estrategia simple: Si es verbo, intentar no cambiarlo si no podemos conjugar
                if token.pos_ == 'VERB' and token.text != token.lemma_:
                    # Si no tenemos un conjugador, mejor conservamos el original para no romper gramática
                    new_tokens.append(token.text_with_ws)
                else:
                    changes_made += 1
                    # Añadir espacio si el original lo tenía
                    ws = token.whitespace_
                    new_tokens.append(choice + ws)
            else:
                new_tokens.append(token.text_with_ws)
                
        result_text = "".join(new_tokens)
        
        return {
            "title": "Parafraseado Lingüístico",
            "text": result_text,
            "original_text": text,
            "changes_count": changes_made
        }

    def paraphrase_article(self, article: Dict) -> Dict:
        """
        Procesa un artículo completo (título y descripción/contenido)
        """
        new_article = article.copy()
        
        # Parafrasear título (con cuidado, menos agresivo)
        if 'title' in article:
            res = self.paraphrase_text(article['title'], change_threshold=0.3)
            new_article['title'] = res['text']
            
        # Parafrasear contenido/descripción
        content_key = 'content' if 'content' in article and article['content'] else 'description'
        if content_key in article and article[content_key]:
            res = self.paraphrase_text(article[content_key], change_threshold=0.5)
            # Guardamos el resultado como 'full_text' o sobreescribimos
            new_article['description'] = res['text'] # Actualizar descripción
            
            # Generar "cuerpo" si no existe
            if 'full_text' not in new_article:
                new_article['full_text'] = res['text'] # Usar el texto parafraseado
                
        new_article['is_paraphrased'] = True
        new_article['paraphrase_method'] = 'linguistic_associations'
        
        return new_article

# Demo simple
if __name__ == "__main__":
    print("Cargando modelo lingüístico...")
    rewriter = LinguisticParaphraser()
    
    texto_orig = "El presidente anunció nuevas medidas económicas para combatir la inflación creciente en el país."
    print(f"\nOriginal: {texto_orig}")
    
    res = rewriter.paraphrase_text(texto_orig)
    print(f"Reescrito: {res['text']}")
