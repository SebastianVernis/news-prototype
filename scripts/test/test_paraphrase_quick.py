#!/usr/bin/env python3
"""Quick paraphrase test"""

from paraphrase import NewsParaphraser

# Test article
article = {
    'source': 'test',
    'title': 'México anuncia nuevas políticas económicas',
    'description': 'El gobierno presenta reformas importantes',
    'content': 'El presidente anunció reformas económicas significativas',
    'full_text': 'El presidente anunció reformas económicas significativas para el próximo año'
}

print("🧪 Test rápido de parafraseado\n")
print(f"Artículo original: {article['title']}")

paraphraser = NewsParaphraser()
print("\n📝 Generando 1 variación...")

variations = paraphraser.generate_variations(article, num_variations=1)

if variations:
    var = variations[0]
    print(f"\n✅ Resultado:")
    print(f"   Estilo: {var.get('style')}")
    print(f"   Título: {var['title'][:80]}...")
    print(f"   Descripción: {var['description'][:80]}...")
else:
    print("❌ No se generaron variaciones")
