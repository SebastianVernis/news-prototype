#!/usr/bin/env python3
"""
Gestor de Artículos Destacados
Prioriza artículos de calidad completa (Blackbox AI) como destacados
"""

from typing import List, Dict


class FeaturedManager:
    """Gestiona artículos destacados vs placeholders"""
    
    def __init__(self):
        pass
    
    def marcar_destacados(self, articles: List[Dict]) -> List[Dict]:
        """
        Marca artículos como destacados según su método de parafraseo
        
        Args:
            articles: Lista de artículos
            
        Returns:
            Lista con campo 'is_featured' agregado
        """
        for article in articles:
            paraphrase_method = article.get('paraphrase_method', '')
            
            # Artículos destacados: parafraseados con Blackbox (calidad completa)
            if 'blackbox' in paraphrase_method.lower():
                article['is_featured'] = True
                article['quality_tier'] = 'premium'
            # Placeholders: parafraseados con Gemini (rápido)
            elif 'gemini' in paraphrase_method.lower():
                article['is_featured'] = False
                article['quality_tier'] = 'standard'
            # No parafraseados
            else:
                article['is_featured'] = False
                article['quality_tier'] = 'basic'
        
        return articles
    
    def ordenar_destacados_primero(self, articles: List[Dict]) -> List[Dict]:
        """
        Ordena artículos poniendo destacados primero
        
        Args:
            articles: Lista de artículos con 'is_featured'
            
        Returns:
            Lista ordenada (destacados primero)
        """
        destacados = [a for a in articles if a.get('is_featured', False)]
        no_destacados = [a for a in articles if not a.get('is_featured', False)]
        
        return destacados + no_destacados
    
    def separar_destacados_y_placeholders(
        self,
        articles: List[Dict]
    ) -> Dict[str, List[Dict]]:
        """
        Separa artículos en destacados y placeholders
        
        Args:
            articles: Lista de artículos
            
        Returns:
            Dict con 'featured' y 'placeholders'
        """
        destacados = []
        placeholders = []
        
        for article in articles:
            if article.get('is_featured', False) or article.get('quality_tier') == 'premium':
                destacados.append(article)
            else:
                placeholders.append(article)
        
        return {
            'featured': destacados,
            'placeholders': placeholders,
            'stats': {
                'total_featured': len(destacados),
                'total_placeholders': len(placeholders),
                'ratio': f"{len(destacados)}:{len(placeholders)}"
            }
        }
    
    def generar_seccion_destacados_html(
        self,
        featured_articles: List[Dict],
        colores: Dict
    ) -> str:
        """
        Genera HTML para sección de artículos destacados
        
        Args:
            featured_articles: Artículos destacados
            colores: Paleta de colores del sitio
            
        Returns:
            HTML de la sección destacados
        """
        primary = colores.get('primary', '#667eea')
        
        if not featured_articles:
            return ""
        
        html = f'''
    <section class="featured-section">
        <div class="section-header">
            <h2>⭐ Artículos Destacados</h2>
            <p>Análisis completo y profundo de los temas más relevantes</p>
        </div>
        
        <div class="featured-grid">
'''
        
        for idx, article in enumerate(featured_articles[:6], 1):  # Máximo 6 destacados
            image_url = article.get('local_image_path', article.get('image_url', 'https://via.placeholder.com/600x400'))
            
            # Calcular índice real del artículo
            article_idx = article.get('_display_index', idx)
            
            html += f'''
            <article class="featured-card">
                <a href="article_{article_idx}.html">
                    <div class="featured-image-wrapper">
                        <img src="{image_url}" alt="{article['title']}" class="featured-image">
                        <span class="featured-badge">⭐ Destacado</span>
                    </div>
                    <div class="featured-content">
                        <span class="category-badge">{article.get('category_name', 'Noticias')}</span>
                        <h3>{article['title'][:120]}</h3>
                        <p class="featured-excerpt">{article.get('description', '')[:200]}...</p>
                        <div class="featured-meta">
                            <span>👤 {article.get('author', 'Redacción')}</span>
                            <span>📅 {article.get('published_at', '')[:10]}</span>
                            <span>📖 Lectura completa</span>
                        </div>
                    </div>
                </a>
            </article>
'''
        
        html += '''
        </div>
    </section>
    
    <style>
        .featured-section {
            max-width: 1200px;
            margin: 3rem auto;
            padding: 0 1rem;
        }
        
        .section-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .section-header h2 {
            font-size: 2rem;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        
        .section-header p {
            color: #6c757d;
            font-size: 1.1rem;
        }
        
        .featured-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }
        
        .featured-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 2px solid ''' + primary + ''';
        }
        
        .featured-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
        }
        
        .featured-card a {
            text-decoration: none;
            color: inherit;
        }
        
        .featured-image-wrapper {
            position: relative;
            height: 250px;
            overflow: hidden;
        }
        
        .featured-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .featured-card:hover .featured-image {
            transform: scale(1.05);
        }
        
        .featured-badge {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: ''' + primary + ''';
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 700;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .featured-content {
            padding: 1.5rem;
        }
        
        .featured-content h3 {
            font-size: 1.4rem;
            margin-bottom: 1rem;
            line-height: 1.4;
            color: #2c3e50;
        }
        
        .featured-excerpt {
            color: #6c757d;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        
        .featured-meta {
            display: flex;
            gap: 1rem;
            font-size: 0.85rem;
            color: #95a5a6;
            padding-top: 1rem;
            border-top: 1px solid #ecf0f1;
            flex-wrap: wrap;
        }
    </style>
'''
        
        return html


def main():
    """Test del gestor de destacados"""
    import json
    import glob
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║           ⭐ GESTOR DE ARTÍCULOS DESTACADOS                         ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Simular artículos con diferentes métodos
    articles = [
        {
            'title': 'Artículo Blackbox AI (Destacado)',
            'paraphrase_method': 'blackbox-grok',
            'description': 'Artículo con parafraseo completo de alta calidad'
        },
        {
            'title': 'Artículo Gemini (Placeholder)',
            'paraphrase_method': 'gemini-simple',
            'description': 'Artículo con parafraseo rápido para placeholder'
        },
        {
            'title': 'Artículo Blackbox Paralelo (Destacado)',
            'paraphrase_method': 'blackbox-parallel',
            'description': 'Artículo con parafraseo completo paralelo'
        },
        {
            'title': 'Artículo Original',
            'paraphrase_method': 'original',
            'description': 'Artículo sin parafrasear'
        }
    ]
    
    manager = FeaturedManager()
    
    # Marcar destacados
    articles_marked = manager.marcar_destacados(articles)
    
    print("\n" + "="*70)
    print("Artículos marcados:")
    print("="*70)
    
    for a in articles_marked:
        featured_icon = "⭐" if a['is_featured'] else "📄"
        print(f"{featured_icon} {a['title']}")
        print(f"   Método: {a['paraphrase_method']}")
        print(f"   Destacado: {a['is_featured']}")
        print(f"   Tier: {a['quality_tier']}")
        print()
    
    # Separar
    separated = manager.separar_destacados_y_placeholders(articles_marked)
    
    print("="*70)
    print("Separación:")
    print("="*70)
    print(f"Destacados: {separated['stats']['total_featured']}")
    print(f"Placeholders: {separated['stats']['total_placeholders']}")
    print(f"Ratio: {separated['stats']['ratio']}")


if __name__ == '__main__':
    main()
