#!/usr/bin/env python3
"""
Generador de Metadatos SEO y Open Graph
Genera metadatos completos para artículos y páginas
"""

from typing import Dict, List
from datetime import datetime
import os


class SEOMetadataGenerator:
    """Genera metadatos SEO completos para artículos y sitios"""
    
    def __init__(self):
        self.default_og_image = 'https://via.placeholder.com/1200x630/667eea/ffffff?text=Política+México'
    
    def generar_meta_tags_articulo(
        self,
        article: Dict,
        site_metadata: Dict,
        article_url: str,
        article_index: int = 1
    ) -> str:
        """
        Genera meta tags completos para un artículo
        
        Args:
            article: Datos del artículo
            site_metadata: Metadata del sitio
            article_url: URL del artículo
            article_index: Índice del artículo
            
        Returns:
            HTML con meta tags
        """
        # Extraer datos
        title = article.get('title', 'Sin título')
        description = article.get('description', '')[:300]
        author = article.get('author', 'Redacción')
        published_at = article.get('published_at', article.get('publishedAt', ''))
        category = article.get('category_name', 'Noticias')
        
        # URL de imagen
        image_url = article.get('image_url', article.get('ai_image_path', ''))
        if not image_url or not image_url.startswith('http'):
            image_url = self.default_og_image
        
        # Site name
        site_name = site_metadata.get('site_name', 'Noticias Políticas')
        site_url = site_metadata.get('site_url', 'https://ejemplo.com')
        
        # Keywords desde categoría y contenido
        keywords = self._generar_keywords(article)
        
        # Fecha formateada
        if published_at:
            try:
                if 'T' in published_at:
                    dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                else:
                    dt = datetime.strptime(published_at, '%Y-%m-%d')
                published_iso = dt.isoformat()
                modified_iso = datetime.now().isoformat()
            except:
                published_iso = datetime.now().isoformat()
                modified_iso = published_iso
        else:
            published_iso = datetime.now().isoformat()
            modified_iso = published_iso
        
        # Generar meta tags
        meta_tags = f'''
    <!-- SEO Meta Tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{self._escape_html(description)}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="{self._escape_html(author)}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="googlebot" content="index, follow">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{article_url}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{article_url}">
    <meta property="og:title" content="{self._escape_html(title)}">
    <meta property="og:description" content="{self._escape_html(description)}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="{self._escape_html(site_name)}">
    <meta property="og:locale" content="es_MX">
    <meta property="article:published_time" content="{published_iso}">
    <meta property="article:modified_time" content="{modified_iso}">
    <meta property="article:author" content="{self._escape_html(author)}">
    <meta property="article:section" content="{category}">
    <meta property="article:tag" content="{category}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{article_url}">
    <meta name="twitter:title" content="{self._escape_html(title)}">
    <meta name="twitter:description" content="{self._escape_html(description)}">
    <meta name="twitter:image" content="{image_url}">
    <meta name="twitter:creator" content="@{site_name.replace(' ', '')}">
    <meta name="twitter:site" content="@{site_name.replace(' ', '')}">
    
    <!-- Additional SEO -->
    <link rel="alternate" type="application/rss+xml" title="{site_name} RSS Feed" href="{site_url}/feed.xml">
    <meta name="theme-color" content="#667eea">
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "NewsArticle",
      "headline": "{self._escape_json(title)}",
      "description": "{self._escape_json(description)}",
      "image": ["{image_url}"],
      "datePublished": "{published_iso}",
      "dateModified": "{modified_iso}",
      "author": {{
        "@type": "Person",
        "name": "{self._escape_json(author)}"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "{self._escape_json(site_name)}",
        "url": "{site_url}",
        "logo": {{
          "@type": "ImageObject",
          "url": "{site_url}/assets/logo.png"
        }}
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{article_url}"
      }},
      "articleSection": "{category}",
      "keywords": "{keywords}",
      "inLanguage": "es-MX"
    }}
    </script>
'''
        
        return meta_tags
    
    def generar_meta_tags_home(self, site_metadata: Dict, total_articles: int = 0) -> str:
        """
        Genera meta tags para la página principal
        
        Args:
            site_metadata: Metadata del sitio
            total_articles: Total de artículos en el sitio
            
        Returns:
            HTML con meta tags
        """
        site_name = site_metadata.get('site_name', 'Noticias Políticas')
        site_url = site_metadata.get('site_url', 'https://ejemplo.com')
        tagline = site_metadata.get('tagline', 'Análisis político de México')
        description = site_metadata.get('description', f'{tagline}. Noticias políticas actualizadas.')
        
        # Imagen de portada
        og_image = site_metadata.get('og_image', self.default_og_image)
        
        meta_tags = f'''
    <!-- SEO Meta Tags -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{self._escape_html(description)}">
    <meta name="keywords" content="política méxico, noticias políticas, análisis político, gobierno méxico">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="googlebot" content="index, follow">
    
    <!-- Canonical URL -->
    <link rel="canonical" href="{site_url}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{site_url}">
    <meta property="og:title" content="{self._escape_html(site_name)} - {self._escape_html(tagline)}">
    <meta property="og:description" content="{self._escape_html(description)}">
    <meta property="og:image" content="{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="{self._escape_html(site_name)}">
    <meta property="og:locale" content="es_MX">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="{site_url}">
    <meta name="twitter:title" content="{self._escape_html(site_name)}">
    <meta name="twitter:description" content="{self._escape_html(description)}">
    <meta name="twitter:image" content="{og_image}">
    <meta name="twitter:site" content="@{site_name.replace(' ', '')}">
    
    <!-- RSS Feed -->
    <link rel="alternate" type="application/rss+xml" title="{site_name} RSS Feed" href="{site_url}/feed.xml">
    
    <!-- Theme -->
    <meta name="theme-color" content="#667eea">
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "{self._escape_json(site_name)}",
      "description": "{self._escape_json(description)}",
      "url": "{site_url}",
      "potentialAction": {{
        "@type": "SearchAction",
        "target": {{
          "@type": "EntryPoint",
          "urlTemplate": "{site_url}/search?q={{search_term_string}}"
        }},
        "query-input": "required name=search_term_string"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "{self._escape_json(site_name)}",
        "url": "{site_url}",
        "logo": {{
          "@type": "ImageObject",
          "url": "{site_url}/assets/logo.png"
        }}
      }}
    }}
    </script>
'''
        
        return meta_tags
    
    def _generar_keywords(self, article: Dict) -> str:
        """Genera keywords desde el artículo"""
        keywords = []
        
        # Agregar categoría
        if article.get('category_name'):
            keywords.append(article['category_name'].lower())
        
        # Keywords base
        keywords.extend(['política méxico', 'noticias políticas'])
        
        # Extraer del título
        title = article.get('title', '')
        # Palabras importantes del título (más de 5 caracteres)
        title_words = [w.lower() for w in title.split() if len(w) > 5 and w.lower() not in ['sobre', 'desde', 'hacia', 'contra']]
        keywords.extend(title_words[:5])
        
        return ', '.join(keywords[:10])
    
    def _escape_html(self, text: str) -> str:
        """Escapa HTML"""
        if not text:
            return ''
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
    
    def _escape_json(self, text: str) -> str:
        """Escapa para JSON"""
        if not text:
            return ''
        return (text
                .replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace('\r', '\\r')
                .replace('\t', '\\t'))


def main():
    """Demo del generador de metadatos"""
    import json
    import glob
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║           🎯 GENERADOR DE METADATOS SEO                              ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Cargar artículo de ejemplo
    json_files = glob.glob('noticias_parafraseadas*.json')
    if not json_files:
        print("❌ No se encontraron artículos")
        return
    
    with open(sorted(json_files)[-1], 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    if not articles:
        print("❌ No hay artículos en el archivo")
        return
    
    article = articles[0]
    
    # Metadata del sitio
    site_metadata = {
        'site_name': 'Política México Hoy',
        'site_url': 'https://politica-mexico.com',
        'tagline': 'Análisis político y noticias de México',
        'description': 'Portal de noticias políticas con análisis profundo de la actualidad mexicana'
    }
    
    # Generar metadatos
    generator = SEOMetadataGenerator()
    meta_tags = generator.generar_meta_tags_articulo(
        article,
        site_metadata,
        f"{site_metadata['site_url']}/article_1.html",
        article_index=1
    )
    
    print("📄 Meta Tags Generados:")
    print("="*70)
    print(meta_tags)
    
    # Guardar ejemplo
    with open('meta_tags_example.html', 'w', encoding='utf-8') as f:
        f.write(meta_tags)
    
    print("\n💾 Guardado en: meta_tags_example.html")


if __name__ == '__main__':
    main()
