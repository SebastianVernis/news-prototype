#!/usr/bin/env python3
"""
Módulo para expandir artículos de noticias a versiones completas y detalladas
Genera artículos periodísticos profesionales con múltiples párrafos
"""

import json
import os
import time
from typing import Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BLACKBOX_API_KEY")
API_URL = "https://api.blackbox.ai/chat/completions"


class ArticleExpander:
    """Expande noticias cortas a artículos periodísticos completos"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        if not self.api_key:
            raise ValueError("BLACKBOX_API_KEY no encontrada en .env")

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        # Estructuras de artículo para variar
        self.structures = [
            "pirámide invertida clásica",  # Lo más importante primero
            "narrativa cronológica",  # Cuenta una historia temporal
            "enfoque analítico",  # Análisis profundo del tema
            "contexto histórico",  # Conecta con eventos pasados
            "impacto y consecuencias",  # Se enfoca en efectos
            "múltiples perspectivas",  # Presenta varios puntos de vista
            "datos y estadísticas",  # Enfoque en números y hechos
            "testimonios y voces",  # Citas y declaraciones
        ]

    def expand_article(
        self, article: Dict, target_words: int = 800, structure: str = None
    ) -> str:
        """
        Expande un artículo corto a uno completo y profesional

        Args:
            article: Diccionario con datos del artículo original
            target_words: Número objetivo de palabras (default: 800)
            structure: Estructura narrativa a usar

        Returns:
            Artículo expandido completo
        """
        # Extraer información del artículo
        title = article.get("title", "")
        description = article.get("description", "")
        content = article.get("content", "")
        full_text = article.get("full_text", "")

        # Manejar source que puede ser string o dict
        source = article.get("source_name", "")
        if not source:
            source_data = article.get("source", {})
            if isinstance(source_data, dict):
                source = source_data.get("name", "Fuente")
            elif isinstance(source_data, str):
                source = source_data
            else:
                source = "Fuente"

        # Compilar todo el contexto disponible
        context = f"""
Título: {title}

Descripción: {description}

{f"Contenido adicional: {content}" if content else ""}

{f"Texto completo: {full_text}" if full_text else ""}
        """.strip()

        structure = structure or self.structures[0]

        prompt = f"""Eres un periodista senior especializado en política. Tu tarea es expandir la siguiente noticia
a un artículo periodístico completo, profesional y creíble de aproximadamente {target_words} palabras.

INFORMACIÓN ORIGINAL:
{context}

INSTRUCCIONES CRÍTICAS DE FORMATO Y CALIDAD:

1. ESTRUCTURA DE PÁRRAFOS (MUY IMPORTANTE):
   - Usa un enfoque de {structure}
   - Escribe 8-10 párrafos SEPARADOS con doble salto de línea entre cada uno
   - Cada párrafo debe tener 3-5 oraciones (80-120 palabras)
   - NUNCA escribas todo el texto en un solo bloque
   - Usa puntos y comas correctamente
   - Separa ideas diferentes en párrafos diferentes

2. GRAMÁTICA Y PUNTUACIÓN:
   - Usa puntos (.) para terminar oraciones completas
   - Usa comas (,) correctamente para separar ideas
   - Usa punto y coma (;) para conectar ideas relacionadas
   - Usa dos puntos (:) antes de listas o explicaciones
   - Revisa concordancia de género y número
   - Evita oraciones excesivamente largas (máximo 30-35 palabras)

3. CONTENIDO DEL ARTÍCULO:
   - Mantén TODOS los hechos del original sin cambiarlos
   - Expande con contexto, antecedentes y análisis
   - Agrega implicaciones y consecuencias
   - Incluye contexto social, político o económico
   - Usa transiciones naturales entre párrafos
   - NO inventes cifras, nombres o fechas específicas
   - Mantén precisión factual absoluta

4. TONO PERIODÍSTICO:
   - Profesional y objetivo
   - Como si fuera para periódico de prestigio
   - NO uses "según el artículo" o "de acuerdo a la fuente"
   - Escribe con autoridad periodística directa
   - NO menciones que estás expandiendo algo

5. FORMATO DE RESPUESTA:

Primer párrafo con introducción clara. Debe contextualizar la noticia. Incluir 3-5 oraciones bien estructuradas.

Segundo párrafo desarrollando el punto principal. Separado del anterior con línea en blanco. Continuación lógica.

Tercer párrafo con nueva idea o aspecto. Mantener coherencia narrativa. Usar transiciones adecuadas.

[Continuar con 5-7 párrafos más de la misma manera]

Escribe SOLO el artículo expandido con PÁRRAFOS BIEN SEPARADOS:"""

        payload = {
            "model": "blackboxai/x-ai/grok-code-fast-1:free",
            "messages": [
                {
                    "role": "system",
                    "content": "Eres un periodista senior de un medio prestigioso con excelente dominio del español. Escribes artículos profundos, bien investigados y con autoridad. SIEMPRE separas el contenido en párrafos distintos usando doble salto de línea. Tienes impecable gramática, puntuación y estructura narrativa.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 3000,
        }

        try:
            response = requests.post(
                API_URL, headers=self.headers, json=payload, timeout=90
            )
            response.raise_for_status()

            result = response.json()
            expanded = result["choices"][0]["message"]["content"].strip()

            # Limpiar markdown headers si existen
            # Preservar dobles saltos de línea para mantener la estructura de párrafos
            lines = expanded.split("\n")
            cleaned_lines = []
            for line in lines:
                # Remover # del inicio de líneas (markdown headers)
                if line.strip().startswith("#"):
                    cleaned_lines.append(line.lstrip("#").strip())
                else:
                    cleaned_lines.append(line)

            # Reconstruir el texto preservando los dobles saltos de línea
            # para mantener la separación de párrafos
            expanded = "\n".join(cleaned_lines)

            # Asegurarse de que los párrafos estén separados por doble salto de línea
            # Reemplazar saltos de línea simples entre párrafos con dobles saltos
            # pero preservar saltos simples dentro del mismo párrafo
            if "\n\n" not in expanded and len(expanded.split("\n")) > 1:
                # Si no hay dobles saltos pero hay múltiples líneas,
                # asumir que cada línea es un párrafo separado
                expanded = "\n\n".join(
                    line.strip() for line in expanded.split("\n") if line.strip()
                )
            else:
                # Si ya hay dobles saltos, asegurarse de que sean consistentes
                expanded = "\n\n".join(
                    paragraph.strip()
                    for paragraph in expanded.split("\n\n")
                    if paragraph.strip()
                )

            return expanded

        except requests.exceptions.RequestException as e:
            print(f"❌ Error en API: {e}")
            return f"{title}\n\n{description}\n\n{content or full_text}"
        except (KeyError, IndexError) as e:
            print(f"❌ Error procesando respuesta: {e}")
            return f"{title}\n\n{description}\n\n{content or full_text}"

    def expand_with_variations(
        self, article: Dict, num_variations: int = 3
    ) -> List[Dict]:
        """
        Genera múltiples versiones expandidas del mismo artículo

        Args:
            article: Artículo original
            num_variations: Número de versiones a generar

        Returns:
            Lista de artículos expandidos con diferentes estructuras
        """
        variations = []

        print(
            f"\n📰 Expandiendo artículo: {article.get('title', 'Sin título')[:60]}..."
        )

        for i in range(num_variations):
            structure = self.structures[i % len(self.structures)]

            print(
                f"  [{i + 1}/{num_variations}] Estructura: {structure}...",
                end=" ",
                flush=True,
            )

            expanded_text = self.expand_article(
                article, target_words=800, structure=structure
            )

            # Extraer título y cuerpo del artículo expandido
            lines = expanded_text.split("\n\n", 1)
            if len(lines) >= 2:
                new_title = lines[0].strip()
                body = lines[1].strip()
            else:
                new_title = article.get("title", "")
                body = expanded_text

            # Crear nueva variación con artículo expandido
            variation = article.copy()
            variation["title"] = new_title
            variation["description"] = (
                body.split("\n\n")[0][:300] if "\n\n" in body else body[:300]
            )
            variation["full_text"] = body
            variation["content"] = body[:500]
            variation["expanded"] = True
            variation["expansion_structure"] = structure
            variation["variation_id"] = i + 1
            variation["word_count"] = len(body.split())
            variation["original_article_id"] = article.get(
                "id", article.get("url", hash(article.get("title", "")) % 10000)
            )

            variations.append(variation)
            print(f"✅ ({variation['word_count']} palabras)")

            # Pausa para no saturar la API
            if (i + 1) % 3 == 0:
                time.sleep(2)

        return variations

    def process_articles(
        self, articles: List[Dict], variations_per_article: int = 1
    ) -> List[Dict]:
        """
        Procesa múltiples artículos expandiéndolos.
        Genera UNA SOLA variación por artículo para asegurar que cada artículo
        se use en un solo sitio.

        Args:
            articles: Lista de artículos a expandir
            variations_per_article: Número de variaciones por artículo (default: 1)

        Returns:
            Lista de artículos expandidos (1 por artículo original)
        """
        all_expanded = []

        print(f"\n{'=' * 70}")
        print(f"📰 EXPANSIÓN DE ARTÍCULOS")
        print(f"{'=' * 70}")
        print(f"📊 Artículos a procesar: {len(articles)}")
        print(f"📊 Variaciones por artículo: 1 (forzado)")
        print(f"📊 Total artículos expandidos: {len(articles)}")

        for idx, article in enumerate(articles, 1):
            print(f"\n[{idx}/{len(articles)}] Procesando artículo...")

            try:
                # Forzar 1 variación por artículo
                expanded_variations = self.expand_with_variations(
                    article, num_variations=1
                )
                all_expanded.extend(expanded_variations)

            except Exception as e:
                print(f"❌ Error expandiendo artículo: {e}")
                # Agregar el artículo original si falla
                article_copy = article.copy()
                article_copy["expanded"] = False
                all_expanded.append(article_copy)

        print(f"\n{'=' * 70}")
        print(f"✅ Expansión completada: {len(all_expanded)} artículos generados")
        print(f"{'=' * 70}")

        return all_expanded


def main():
    """Demo del expansor de artículos"""
    import sys

    # Artículo de ejemplo para prueba
    sample_article = {
        "title": "Gobierno anuncia nuevas medidas económicas",
        "description": "El gobierno presentó hoy un paquete de medidas para impulsar la economía nacional.",
        "content": "Las medidas incluyen reducción de impuestos y programas de apoyo a empresas.",
        "source_name": "El Informador",
        "author": "Redacción",
        "url": "https://ejemplo.com/noticia",
    }

    # Cargar artículo desde JSON si se proporciona
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    sample_article = data[0]
        except Exception as e:
            print(f"⚠️ No se pudo cargar archivo: {e}")
            print("Usando artículo de ejemplo...")

    print("🧪 MODO DEMO - Expansor de Artículos")
    print("=" * 70)

    expander = ArticleExpander()
    expanded_articles = expander.expand_with_variations(
        sample_article, num_variations=3
    )

    # Guardar resultado
    output_file = "data/expanded_demo.json"
    os.makedirs("data", exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(expanded_articles, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Resultado guardado en: {output_file}")
    print("\n📄 Vista previa del primer artículo expandido:")
    print("=" * 70)
    print(expanded_articles[0]["full_text"][:500] + "...")


if __name__ == "__main__":
    main()
