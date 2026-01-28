#!/usr/bin/env python3
"""
Script maestro para el sistema automatizado de noticias
Orquesta: descarga, parafraseado y generación de imágenes con IA
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Importar módulos del proyecto
from news import fetch_news, get_full_text
sys.path.insert(0, 'scripts')
from paraphrase import NewsParaphraser
from site_name_manager import SiteNameManager

# Importar expansor de artículos (opcional)
try:
    spec_expander = importlib.util.spec_from_file_location("article_expander", "scripts/article-expander.py")
    article_expander_module = importlib.util.module_from_spec(spec_expander)
    spec_expander.loader.exec_module(article_expander_module)
    ArticleExpander = article_expander_module.ArticleExpander
    EXPANDER_AVAILABLE = True
except Exception:
    EXPANDER_AVAILABLE = False

# Importar nuevos scrapers de APIs
sys.path.insert(0, 'scripts/api')
try:
    from newsapi import fetch_newsapi
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False

try:
    from apitube import fetch_apitube
    APITUBE_AVAILABLE = True
except ImportError:
    APITUBE_AVAILABLE = False

try:
    from newsdata import fetch_newsdata
    NEWSDATA_AVAILABLE = True
except ImportError:
    NEWSDATA_AVAILABLE = False

try:
    from worldnews import fetch_worldnews
    WORLDNEWS_AVAILABLE = True
except ImportError:
    WORLDNEWS_AVAILABLE = False

# Importar con nombre correcto del archivo
import importlib.util
spec = importlib.util.spec_from_file_location("generate_images_ai", "scripts/generate-images-ai.py")
generate_images_ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generate_images_ai)
AIImageGenerator = generate_images_ai.AIImageGenerator

load_dotenv()


class NewsAutomationSystem:
    """Sistema automatizado de noticias con IA"""
    
    def __init__(self, num_articles: int = 5, variations_per_article: int = 1, api_source: str = 'newsapi', expand_articles: bool = False, site_name_mode: str = 'automatico'):
        self.num_articles = num_articles
        # Forzar 1 variación por artículo - cada artículo se usa en un sitio diferente
        self.variations_per_article = 1
        self.api_source = api_source.lower()
        self.expand_articles = expand_articles
        self.site_name_mode = site_name_mode  # 'manual' o 'automatico'
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        
        # Verificar API keys
        self._check_api_keys()
        
        # Inicializar componentes
        self.paraphraser = NewsParaphraser()
        self.image_generator = AIImageGenerator()
        self.site_name_manager = SiteNameManager()
        
        # Configurar modo de nombres de sitios
        self.site_name_manager.set_modo_asignacion(self.site_name_mode)
        
        # Inicializar expansor si está habilitado
        if self.expand_articles and EXPANDER_AVAILABLE:
            self.expander = ArticleExpander()
            print("✅ Expansor de artículos activado")
        elif self.expand_articles and not EXPANDER_AVAILABLE:
            print("⚠️ Expansor no disponible, usando parafraseado normal")
            self.expand_articles = False
    
    def _check_api_keys(self):
        """Verifica que las API keys estén configuradas"""
        newsapi_key = os.getenv('NEWSAPI_KEY')
        blackbox_key = os.getenv('BLACKBOX_API_KEY')
        
        if not newsapi_key:
            raise ValueError("❌ NEWSAPI_KEY no encontrada en .env")
        
        if not blackbox_key:
            raise ValueError("❌ BLACKBOX_API_KEY no encontrada en .env")
        
        print("✅ API keys verificadas")
    
    def step1_download_news(self) -> list:
        """
        Paso 1: Descargar noticias de política usando la API seleccionada
        
        Returns:
            Lista de artículos descargados
        """
        print(f"\n{'='*70}")
        print(f"📥 PASO 1: Descargando noticias de política (API: {self.api_source.upper()})")
        print(f"{'='*70}")
        
        try:
            # Seleccionar fuente de API
            if self.api_source == 'newsapi':
                if not NEWSAPI_AVAILABLE:
                    raise ImportError("Módulo newsapi.py no disponible")
                print(f"🔍 Consultando NewsAPI.org...")
                articles = fetch_newsapi(
                    query='política México',
                    language='es',
                    page_size=self.num_articles,
                    enrich=True,
                    silent=True
                )
            
            elif self.api_source == 'apitube':
                if not APITUBE_AVAILABLE:
                    raise ImportError("Módulo apitube.py no disponible")
                print(f"🔍 Consultando APITube.io...")
                articles = fetch_apitube(
                    country='mx',
                    category='politics',
                    language='es',
                    page_size=self.num_articles,
                    silent=True
                )
            
            elif self.api_source == 'newsdata':
                if not NEWSDATA_AVAILABLE:
                    raise ImportError("Módulo newsdata.py no disponible")
                print(f"🔍 Consultando Newsdata.io...")
                articles = fetch_newsdata(
                    query='política México',
                    country='mx',
                    language='es',
                    category='politics',
                    page_size=min(self.num_articles, 10),  # Newsdata limita a 10 en plan gratuito
                    silent=True
                )
            
            elif self.api_source == 'worldnews':
                if not WORLDNEWS_AVAILABLE:
                    raise ImportError("Módulo worldnews.py no disponible")
                print(f"🔍 Consultando WorldNewsAPI...")
                articles = fetch_worldnews(
                    query='política México',
                    source_country='mx',
                    language='es',
                    number=self.num_articles,
                    silent=True
                )
            
            elif self.api_source == 'legacy':
                # Usar el método antiguo (news.py original)
                articles = fetch_news(
                    query='política México',
                    language='es',
                    page_size=self.num_articles
                )
                
                # Obtener texto completo de cada artículo
                enhanced_articles = []
                for idx, art in enumerate(articles, 1):
                    print(f"[{idx}/{len(articles)}] Procesando: {art.get('title', 'Sin título')[:60]}...")
                    
                    full_text = get_full_text(art['url']) if art.get('url') else ''
                    enhanced = {**art, 'full_text': full_text}
                    enhanced_articles.append(enhanced)
                
                articles = enhanced_articles
            
            else:
                raise ValueError(f"API source desconocida: {self.api_source}. Usa: newsapi, apitube, newsdata, worldnews, legacy")
            
            # Guardar artículos originales
            original_file = f'data/noticias_{self.api_source}_{self.timestamp}.json'
            Path('data').mkdir(exist_ok=True)
            with open(original_file, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Descargados {len(articles)} artículos")
            print(f"💾 Guardados en: {original_file}")
            
            return articles
            
        except Exception as e:
            print(f"❌ Error descargando noticias: {e}")
            sys.exit(1)
    
    def step2_paraphrase_articles(self, articles: list) -> list:
        """
        Paso 2: Parafrasear artículos para generar variaciones
        Opcionalmente expande a artículos completos si está habilitado
        
        Args:
            articles: Lista de artículos originales
            
        Returns:
            Lista de artículos con variaciones (1 por artículo)
        """
        print(f"\n{'='*70}")
        if self.expand_articles:
            print(f"📰 PASO 2: Expandiendo artículos completos (1 variación por artículo)")
        else:
            print(f"📝 PASO 2: Parafraseando artículos (1 variación por artículo)")
        print(f"{'='*70}")
        
        try:
            if self.expand_articles:
                # Usar el expansor de artículos completos - SIEMPRE 1 variación
                variations = self.expander.process_articles(
                    articles,
                    variations_per_article=1
                )
                file_prefix = 'expanded'
            else:
                # Usar el parafraseador normal - SIEMPRE 1 variación
                variations = self.paraphraser.process_articles(
                    articles,
                    variations_per_article=1
                )
                file_prefix = 'paraphrased'
            
            # Asignar nombre de sitio a cada variación
            for i, variation in enumerate(variations):
                sitio_info = self.site_name_manager.obtener_siguiente_nombre(f"articulo_{i+1}")
                variation['site_name'] = sitio_info.get('nombre')
                variation['site_tagline'] = sitio_info.get('tagline')
                variation['site_domain'] = sitio_info.get('dominio_completo')
                variation['site_mode'] = sitio_info.get('modo')
            
            # Guardar variaciones
            output_file = f'data/noticias_{file_prefix}_{self.timestamp}.json'
            Path('data').mkdir(exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(variations, f, ensure_ascii=False, indent=2)
            
            print(f"\n✅ Generadas {len(variations)} variaciones")
            print(f"💾 Guardadas en: {output_file}")
            
            return variations
            
        except Exception as e:
            print(f"❌ Error procesando artículos: {e}")
            sys.exit(1)
    
    def step3_generate_images(self, articles: list) -> list:
        """
        Paso 3: Generar imágenes con IA para cada artículo
        
        Args:
            articles: Lista de artículos con variaciones
            
        Returns:
            Lista de artículos con imágenes
        """
        print(f"\n{'='*70}")
        print("🎨 PASO 3: Generando imágenes con IA (Flux Schnell)")
        print(f"{'='*70}")
        
        try:
            articles_with_images = self.image_generator.process_articles(articles)
            
            # Guardar resultados finales
            final_file = f'data/noticias_final_{self.timestamp}.json'
            Path('data').mkdir(exist_ok=True)
            with open(final_file, 'w', encoding='utf-8') as f:
                json.dump(articles_with_images, f, ensure_ascii=False, indent=2)
            
            successful_images = sum(1 for a in articles_with_images if a.get('ai_image_path'))
            
            print(f"\n✅ Proceso completado")
            print(f"💾 Resultados finales en: {final_file}")
            print(f"📊 Imágenes generadas: {successful_images}/{len(articles_with_images)}")
            
            return articles_with_images
            
        except Exception as e:
            print(f"❌ Error generando imágenes: {e}")
            sys.exit(1)
    
    def run(self):
        """Ejecuta el flujo completo del sistema"""
        mode = "Artículos expandidos" if self.expand_articles else "Parafraseado rápido"
        print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  🤖 SISTEMA AUTOMATIZADO DE NOTICIAS CON IA                      ║
║                                                                   ║
║  • Descarga automática de noticias de política                   ║
║  • {mode:<58} ║
║  • Generación de imágenes con Flux Schnell                       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
        """)
        
        start_time = datetime.now()
        
        # Paso 1: Descargar noticias
        articles = self.step1_download_news()
        
        # Paso 2: Parafrasear artículos
        variations = self.step2_paraphrase_articles(articles)
        
        # Paso 3: Generar imágenes
        final_articles = self.step3_generate_images(variations)
        
        # Resumen final
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"\n{'='*70}")
        print("🎉 PROCESO COMPLETADO EXITOSAMENTE")
        print(f"{'='*70}")
        print(f"⏱️  Tiempo total: {duration:.2f} segundos")
        print(f"📰 Artículos originales: {len(articles)}")
        print(f"📝 Variaciones generadas: {len(variations)}")
        print(f"🎨 Imágenes creadas: {sum(1 for a in final_articles if a.get('ai_image_path'))}")
        print(f"📂 Directorio de imágenes: {self.image_generator.output_dir.absolute()}")
        print(f"{'='*70}")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sistema automatizado de noticias con IA')
    parser.add_argument('--articles', type=int, default=5,
                       help='Número de artículos a descargar (default: 5)')
    # El parámetro --variations se mantiene por compatibilidad pero se ignora
    parser.add_argument('--variations', type=int, default=1,
                       help='DEPRECATED: Siempre se usa 1 variación por artículo')
    parser.add_argument('--api', type=str, default='newsapi',
                       choices=['newsapi', 'apitube', 'newsdata', 'worldnews', 'legacy'],
                       help='API source a usar (default: newsapi)')
    parser.add_argument('--test', action='store_true',
                       help='Modo prueba: 2 artículos, 1 variación')
    parser.add_argument('--expand', action='store_true',
                       help='Expandir artículos a versiones completas (~800 palabras)')
    parser.add_argument('--site-name-mode', type=str, default='automatico',
                       choices=['manual', 'automatico'],
                       help='Modo de asignación de nombres de sitios (default: automatico)')
    
    args = parser.parse_args()
    
    # Modo prueba
    if args.test:
        print("⚠️  MODO PRUEBA ACTIVADO")
        args.articles = 2
        args.variations = 1
    
    # Crear y ejecutar sistema
    # Nota: variations_per_article siempre es 1 (ignora el parámetro)
    system = NewsAutomationSystem(
        num_articles=args.articles,
        variations_per_article=1,  # Forzar 1 variación por artículo
        api_source=args.api,
        expand_articles=args.expand,
        site_name_mode=args.site_name_mode
    )
    
    system.run()


if __name__ == '__main__':
    main()
