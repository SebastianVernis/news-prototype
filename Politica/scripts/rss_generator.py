#!/usr/bin/env python3
"""
Generador de RSS Feeds
Crea feeds RSS 2.0 completos para el sitio y por categoría
"""

import os
from datetime import datetime
from typing import List, Dict
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


class RSSGenerator:
    """Genera RSS feeds para noticias"""
    
    def __init__(self):
        self.encoding = 'utf-8'
    
    def _prettify_xml(self, elem: Element) -> str:
        """Convierte Element a string XML formateado"""
        rough_string = tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding=self.encoding).decode(self.encoding)
    
    def _limpiar_html(self, texto: str) -> str:
        """Limpia HTML del texto para RSS"""
        import re
        # Remover tags HTML
        texto = re.sub(r'<[^>]+>', '', texto)
        # Escapar caracteres especiales
        texto = texto.replace('&', '&amp;')
        texto = texto.replace('<', '&lt;')
        texto = texto.replace('>', '&gt;')
        texto = texto.replace('"', '&quot;')
        texto = texto.replace("'", '&#39;')
        return texto
    
    def generar_rss(
        self,
        articles: List[Dict],
        site_metadata: Dict,
        categoria: str = None,
        output_file: str = 'feed.xml'
    ) -> str:
        """
        Genera un RSS feed
        
        Args:
            articles: Lista de artículos
            site_metadata: Metadata del sitio
            categoria: Categoría específica (None para feed general)
            output_file: Nombre del archivo de salida
            
        Returns:
            Path del archivo generado
        """
        # Crear elemento raíz
        rss = Element('rss')
        rss.set('version', '2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
        rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
        rss.set('xmlns:content', 'http://purl.org/rss/1.0/modules/content/')
        
        channel = SubElement(rss, 'channel')
        
        # Metadata del canal
        site_name = site_metadata.get('site_name', 'Sitio de Noticias')
        site_url = site_metadata.get('site_url', 'https://ejemplo.com')
        site_description = site_metadata.get('tagline', 'Noticias políticas de México')
        
        if categoria:
            title_text = f"{site_name} - {categoria.replace('-', ' ').title()}"
            description_text = f"Noticias de {categoria.replace('-', ' ')} en {site_name}"
            link_text = f"{site_url}/categoria/{categoria}"
        else:
            title_text = site_name
            description_text = site_description
            link_text = site_url
        
        SubElement(channel, 'title').text = title_text
        SubElement(channel, 'link').text = link_text
        SubElement(channel, 'description').text = description_text
        SubElement(channel, 'language').text = 'es-MX'
        SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
        SubElement(channel, 'generator').text = 'News Prototype Generator'
        
        # Atom self link
        atom_link = SubElement(channel, 'atom:link')
        atom_link.set('href', f"{site_url}/{output_file}")
        atom_link.set('rel', 'self')
        atom_link.set('type', 'application/rss+xml')
        
        # Agregar items (artículos)
        for idx, article in enumerate(articles[:50], 1):  # Máximo 50 artículos en RSS
            item = SubElement(channel, 'item')
            
            # Datos básicos
            title = article.get('title', 'Sin título')
            SubElement(item, 'title').text = title
            
            # Link al artículo
            article_url = article.get('url', f"{site_url}/article_{idx}.html")
            if not article_url.startswith('http'):
                article_url = f"{site_url}/article_{idx}.html"
            SubElement(item, 'link').text = article_url
            SubElement(item, 'guid').text = article_url
            
            # Descripción
            description = article.get('description', '')[:500]
            description_clean = self._limpiar_html(description)
            SubElement(item, 'description').text = description_clean
            
            # Contenido completo (opcional)
            content = article.get('full_text', article.get('content', ''))[:2000]
            if content:
                content_clean = self._limpiar_html(content)
                SubElement(item, 'content:encoded').text = f"<![CDATA[{content}]]>"
            
            # Fecha de publicación
            pub_date = article.get('published_at', article.get('publishedAt', ''))
            if pub_date:
                try:
                    if 'T' in pub_date:
                        dt = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    else:
                        dt = datetime.strptime(pub_date, '%Y-%m-%d')
                    pub_date_formatted = dt.strftime('%a, %d %b %Y %H:%M:%S +0000')
                    SubElement(item, 'pubDate').text = pub_date_formatted
                except:
                    pass
            
            # Autor
            author = article.get('author', article.get('source_name', ''))
            if author:
                SubElement(item, 'dc:creator').text = author
            
            # Categoría
            if article.get('category_name'):
                SubElement(item, 'category').text = article['category_name']
            
            # Imagen (enclosure)
            image_url = article.get('image_url', article.get('ai_image_path', ''))
            if image_url and image_url.startswith('http'):
                enclosure = SubElement(item, 'enclosure')
                enclosure.set('url', image_url)
                enclosure.set('type', 'image/jpeg')
        
        # Convertir a string XML formateado
        xml_string = self._prettify_xml(rss)
        
        # Guardar archivo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_string)
        
        return output_file
    
    def generar_feeds_por_categoria(
        self,
        articles: List[Dict],
        site_metadata: Dict,
        output_dir: str = '.'
    ) -> Dict[str, str]:
        """
        Genera múltiples RSS feeds: uno general y uno por cada categoría
        
        Args:
            articles: Lista de artículos categorizados
            site_metadata: Metadata del sitio
            output_dir: Directorio de salida
            
        Returns:
            Dict con categoría -> path del feed
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        feeds = {}
        
        # Feed general
        print(f"\n📡 Generando feed general...")
        general_feed = os.path.join(output_dir, 'feed.xml')
        self.generar_rss(articles, site_metadata, categoria=None, output_file=general_feed)
        feeds['general'] = general_feed
        print(f"  ✅ {general_feed}")
        
        # Agrupar por categoría
        from categorizer import NewsCategorizador
        categorizador = NewsCategorizador()
        grouped = categorizador.agrupar_por_categoria(articles)
        
        # Feed por categoría
        print(f"\n📡 Generando feeds por categoría...")
        for cat_id, cat_articles in grouped.items():
            if len(cat_articles) > 0:
                cat_feed = os.path.join(output_dir, f'feed_{cat_id}.xml')
                self.generar_rss(cat_articles, site_metadata, categoria=cat_id, output_file=cat_feed)
                feeds[cat_id] = cat_feed
                print(f"  ✅ {cat_id}: {cat_feed} ({len(cat_articles)} artículos)")
        
        return feeds


def main():
    """Test del generador RSS"""
    import json
    import glob
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              📡 GENERADOR DE RSS FEEDS                               ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Buscar archivo de noticias categorizadas
    json_files = glob.glob('noticias_categorizadas*.json')
    if not json_files:
        json_files = glob.glob('noticias_parafraseadas*.json')
    if not json_files:
        json_files = glob.glob('newsapi*.json')
    
    if not json_files:
        print("❌ No se encontraron archivos de noticias")
        return
    
    latest_file = sorted(json_files)[-1]
    print(f"📂 Cargando: {latest_file}\n")
    
    with open(latest_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Metadata de ejemplo
    site_metadata = {
        'site_name': 'Política México Hoy',
        'site_url': 'https://politica-mexico.com',
        'tagline': 'Análisis político y noticias de México'
    }
    
    # Generar RSS
    generator = RSSGenerator()
    
    # Feed general
    feed_path = generator.generar_rss(articles, site_metadata, output_file='feed_test.xml')
    print(f"\n✅ Feed generado: {feed_path}")
    
    # Mostrar preview
    print(f"\n{'='*70}")
    print("📄 PREVIEW DEL RSS")
    print(f"{'='*70}\n")
    
    with open(feed_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[:30]:
            print(line.rstrip())
    
    print(f"\n... ({len(lines) - 30} líneas más)\n")
    print(f"{'='*70}")
    print(f"✅ RSS Feed generado exitosamente")
    print(f"{'='*70}")


if __name__ == '__main__':
    main()
