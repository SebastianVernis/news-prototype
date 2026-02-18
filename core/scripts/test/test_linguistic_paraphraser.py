#!/usr/bin/env python3
"""
Test del Parafraseador Lingüístico
"""

import sys
from pathlib import Path

# Agregar directorio scripts al path
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))

from linguistic_paraphraser import LinguisticParaphraser

def main():
    print("🧪 Iniciando test del Parafraseador Lingüístico...")
    
    try:
        rewriter = LinguisticParaphraser()
        print("✅ Modelo cargado correctamente")
        
        examples = [
            "El presidente anunció nuevas medidas económicas para combatir la inflación.",
            "La selección nacional ganó el partido decisivo en el último minuto.",
            "Los científicos descubrieron una nueva especie en la selva amazónica."
        ]
        
        print("\n📝 Probando ejemplos:\n")
        
        for text in examples:
            result = rewriter.paraphrase_text(text)
            print(f"Original:  {text}")
            print(f"Reescrito: {result['text']}")
            print(f"Cambios:   {result['changes_count']} palabras")
            print("-" * 50)
            
        print("\n✅ Test completado")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
