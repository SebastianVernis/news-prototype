#!/usr/bin/env python3
"""
Generador de Artículos Placeholder
Genera los últimos 20 artículos por categoría con parafraseo simple paralelo
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Agregar rutas
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / 'api'))

from newsapi import fetch_newsapi
from gemini_paraphraser import GeminiParaphraser
from categorizer import NewsCategorizador


class PlaceholderGenerator:
    """Genera artículos placeholder para cada categoría"""
    
    def __init__(self):
        self.gemini_paraphraser = GeminiParaphraser()
        self.categorizador = NewsCategorizador()
    
    def generar_placeholders_por_categoria(
        self,
        articulos_principales: List[Dict],
        num_placeholders_por_categoria: int = 20
    ) -> Dict[str, List[Dict]]:
        """
        Genera artículos placeholder para cada categoría
        
        Args:
            articulos_principales: Artículos ya procesados (con parafraseo completo)
            num_placeholders_por_categoria: Número de placeholders por categoría
            
        Returns:
            Dict con categoria_id -> lista de placeholders
        """
        print(f"\n{'='*70}")
        print("📑 GENERANDO PLACEHOLDERS POR CATEGORÍA")
        print(f"{'='*70}")
        print(f"Artículos principales: {len(articulos_principales)}")
        print(f"Placeholders por categoría: {num_placeholders_por_categoria}")
        
        # Agrupar artículos principales por categoría
        principales_agrupados = self.categorizador.agrupar_por_categoria(articulos_principales)
        
        print(f"\nCategorías encontradas: {len(principales_agrupados)}")
        for cat_id, arts in principales_agrupados.items():
            cat_name = self.categorizador.CATEGORIAS.get(cat_id, {}).get('nombre', cat_id)
            print(f"  • {cat_name}: {len(arts)} artículos principales")
        
        # Descargar noticias adicionales para placeholders
        print(f"\n{'='*70}")
        print("📥 DESCARGANDO NOTICIAS PARA PLACEHOLDERS")
        print(f"{'='*70}")
        
        total_necesarios = num_placeholders_por_categoria * len(principales_agrupados)
        print(f"Total necesarios: {total_necesarios}")
        print(f"Descargando {total_necesarios + 20} artículos (con margen)...\n")
        
        noticias_placeholder = fetch_newsapi(
            query='política México',
            language='es',
            page_size=min(total_necesarios + 20, 100),  # Máximo 100 de NewsAPI
            enrich=False,  # Sin enriquecimiento para mayor velocidad
            silent=False
        )
        
        print(f"\n✅ {len(noticias_placeholder)} noticias descargadas para placeholders")
        
        # Parafrasear en paralelo con Gemini (rápido)
        print(f"\n{'='*70}")
        print("🚀 PARAFRASEANDO PLACEHOLDERS CON GEMINI (PARALELO)")
        print(f"{'='*70}")
        
        noticias_parafraseadas = self.gemini_paraphraser.parafrasear_lote_paralelo(
            noticias_placeholder,
            max_workers=15  # 15 requests paralelos para máxima velocidad
        )
        
        # Categorizar placeholders
        print(f"\n{'='*70}")
        print("🏷️  CATEGORIZANDO PLACEHOLDERS")
        print(f"{'='*70}")
        
        placeholders_categorizados = self.categorizador.categorizar_lote(
            noticias_parafraseadas,
            use_ai=False,  # Usar keywords para mayor velocidad
            batch_delay=0
        )
        
        # Agrupar por categoría
        placeholders_agrupados = self.categorizador.agrupar_por_categoria(placeholders_categorizados)
        
        # Distribuir placeholders: tomar hasta 20 por categoría
        placeholders_finales = {}
        
        print(f"\n{'='*70}")
        print("📊 DISTRIBUCIÓN DE PLACEHOLDERS")
        print(f"{'='*70}")
        
        for cat_id in self.categorizador.CATEGORIAS.keys():
            cat_name = self.categorizador.CATEGORIAS[cat_id]['nombre']
            
            # Obtener placeholders de esta categoría
            cat_placeholders = placeholders_agrupados.get(cat_id, [])
            
            # Tomar hasta num_placeholders_por_categoria
            placeholders_finales[cat_id] = cat_placeholders[:num_placeholders_por_categoria]
            
            print(f"  {cat_name:30} {len(placeholders_finales[cat_id])} placeholders")
        
        print(f"{'='*70}")
        
        return placeholders_finales
    
    def generar_dataset_completo(
        self,
        articulos_principales: List[Dict],
        num_placeholders: int = 20
    ) -> Dict:
        """
        Genera dataset completo: principales + placeholders
        
        Args:
            articulos_principales: Artículos con parafraseo completo
            num_placeholders: Placeholders por categoría
            
        Returns:
            Dict con 'principales' y 'placeholders_por_categoria'
        """
        placeholders = self.generar_placeholders_por_categoria(
            articulos_principales,
            num_placeholders
        )
        
        total_placeholders = sum(len(p) for p in placeholders.values())
        
        return {
            'principales': articulos_principales,
            'placeholders_por_categoria': placeholders,
            'stats': {
                'total_principales': len(articulos_principales),
                'total_placeholders': total_placeholders,
                'categorias_con_placeholders': len(placeholders)
            }
        }


def main():
    """Test del generador de placeholders"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║     📑 GENERADOR DE PLACEHOLDERS POR CATEGORÍA                      ║
║     (Parafraseo rápido paralelo con Gemini)                          ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    import json
    import glob
    
    # Cargar artículos principales (simulados)
    json_files = glob.glob('noticias_parafraseadas*.json') or glob.glob('noticias_categorizadas*.json')
    
    if json_files:
        with open(sorted(json_files)[-1], 'r', encoding='utf-8') as f:
            articulos_principales = json.load(f)[:3]  # Solo 3 para test
    else:
        # Crear artículos de prueba
        articulos_principales = [
            {
                'title': 'Artículo principal 1',
                'description': 'Descripción del artículo 1',
                'category_id': 'política-nacional',
                'category_name': 'Política Nacional'
            }
        ]
    
    print(f"📰 Artículos principales: {len(articulos_principales)}")
    
    # Generar placeholders (solo 10 por categoría para test rápido)
    generator = PlaceholderGenerator()
    dataset = generator.generar_dataset_completo(
        articulos_principales,
        num_placeholders=10
    )
    
    # Guardar resultado
    output_file = 'dataset_con_placeholders_test.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print("✅ DATASET GENERADO")
    print(f"{'='*70}")
    print(f"📊 Estadísticas:")
    print(f"  • Artículos principales: {dataset['stats']['total_principales']}")
    print(f"  • Total placeholders: {dataset['stats']['total_placeholders']}")
    print(f"  • Categorías: {dataset['stats']['categorias_con_placeholders']}")
    print(f"\n💾 Guardado en: {output_file}")


if __name__ == '__main__':
    main()
