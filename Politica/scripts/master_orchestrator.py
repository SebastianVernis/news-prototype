#!/usr/bin/env python3
"""
Master Orchestrator - Flujo Completo de Generación de Sitios
Orquesta todo el proceso desde descarga de noticias hasta sitios completos
"""

import os
import json
import sys
import time
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Importar módulos del proyecto
try:
    import importlib.util
    
    def import_module_from_file(module_name, file_path):
        """Importa un módulo desde un archivo con guiones en el nombre"""
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        raise ImportError(f"No se pudo importar {module_name} desde {file_path}")
    
    # Obtener directorio actual
    current_dir = Path(__file__).parent
    
    # Importar módulos con guiones
    article_expander_module = import_module_from_file(
        'article_expander',
        current_dir / 'article-expander.py'
    )
    ArticleExpander = article_expander_module.ArticleExpander
    
    # Usar generador unificado (IA + fallback Unsplash)
    generate_images_unified_module = import_module_from_file(
        'generate_images_unified',
        current_dir / 'generate-images-unified.py'
    )
    UnifiedImageGenerator = generate_images_unified_module.UnifiedImageGenerator
    
    # Importar módulos con guiones bajos normalmente
    from paraphrase import NewsParaphraser
    from site_name_generator import SiteNameGenerator
    from domain_verifier import DomainVerifier
    from site_pre_creation import SitePreCreation
    from legal_pages_generator import LegalPagesGenerator
    from template_combiner import TemplateCombiner
    from layout_generator import LayoutGenerator, HTMLLayoutBuilder
    from logo_generator_svg import LogoGeneratorSVG, generar_logo_svg
    from categorizer import NewsCategorizador
    from rss_generator import RSSGenerator
    from seo_metadata_generator import SEOMetadataGenerator
    from section_generator import SectionGenerator
    from og_image_generator import OGImageGenerator
    from preloader_generator import PreloaderGenerator
    from gemini_paraphraser import GeminiParaphraser
    from blackbox_parallel import BlackboxParallelParaphraser
    from placeholder_generator import PlaceholderGenerator
    from featured_manager import FeaturedManager
    from enhanced_components import EnhancedComponents
    from multi_layout_generator import MultiLayoutGenerator
    from advanced_layout_generator import AdvancedLayoutGenerator
    from linguistic_paraphraser import LinguisticParaphraser
    
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print(f"Directorio actual: {Path(__file__).parent}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

load_dotenv()


class MasterOrchestrator:
    """Orquestador principal del flujo completo de generación"""
    
    def __init__(self, output_base_dir: str = None, usar_api_whois: bool = False):
        """
        Inicializa el orquestador
        
        Args:
            output_base_dir: Directorio base para sitios generados
            usar_api_whois: Si True, usa APILayer WHOIS API. Si False, usa whois local
        """
        # Usar rutas absolutas basadas en la ubicación del script
        script_dir = Path(__file__).parent
        base_dir = script_dir.parent
        
        if output_base_dir is None:
            self.output_base_dir = base_dir / "generated_sites"
        else:
            self.output_base_dir = Path(output_base_dir)
        
        self.output_base_dir.mkdir(parents=True, exist_ok=True)
        
        # Directorios de trabajo con rutas absolutas
        self.data_dir = base_dir / "data"
        self.templates_dir = base_dir / "templates"
        
        # Detectar siguiente número de sitio disponible
        self.next_site_number = self._get_next_site_number()
        
        # Inicializar componentes
        self.paraphraser = NewsParaphraser()
        self.article_expander = ArticleExpander()
        self.name_generator = SiteNameGenerator()
        self.domain_verifier = DomainVerifier(usar_api=usar_api_whois)
        self.template_combiner = TemplateCombiner()
        # Usar generador unificado (NewsAPI Original primero, luego fallbacks)
        # IMPORTANTE: use_cache=False para siempre descargar imágenes nuevas
        self.image_generator = UnifiedImageGenerator(prefer_ai=False, use_cache=False)
        self.layout_generator = LayoutGenerator()
        
        # Componentes SEO y categorización
        self.categorizador = NewsCategorizador()
        self.rss_generator = RSSGenerator()
        self.seo_generator = SEOMetadataGenerator()
        self.section_generator = SectionGenerator()
        self.og_image_generator = OGImageGenerator()
        self.preloader_generator = PreloaderGenerator()
        
        # Componentes de sistema paralelo
        self.gemini_paraphraser = GeminiParaphraser()
        self.blackbox_parallel = BlackboxParallelParaphraser()
        self.placeholder_generator = PlaceholderGenerator()
        self.featured_manager = FeaturedManager()
        self.enhanced_components = EnhancedComponents()
        self.layout_generator_multi = MultiLayoutGenerator()
        self.advanced_layout = AdvancedLayoutGenerator()
        self.legal_generator = LegalPagesGenerator()
        self.logo_generator = LogoGeneratorSVG()
        self.linguistic_paraphraser = None  # Lazy init
        
        # Timestamp para esta ejecución
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Estadísticas
        self.stats = {
            "noticias_descargadas": 0,
            "articulos_principales": 0,
            "placeholders_generados": 0,
            "noticias_parafraseadas": 0,
            "imagenes_generadas": 0,
            "sitios_creados": 0,
            "tiempo_inicio": time.time()
        }
    
    def _get_next_site_number(self) -> int:
        """
        Detecta sitios existentes y retorna el siguiente número disponible
        
        Returns:
            Próximo número de sitio a crear
        """
        existing_sites = list(self.output_base_dir.glob("site_*"))
        if not existing_sites:
            return 1
        
        # Extraer números de los directorios existentes
        site_numbers = []
        for site_dir in existing_sites:
            try:
                num = int(site_dir.name.split('_')[1])
                site_numbers.append(num)
            except (IndexError, ValueError):
                continue
        
        if not site_numbers:
            return 1
        
        return max(site_numbers) + 1
    
    def log(self, message: str, level: str = "INFO"):
        """Log con timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "PROGRESS": "🔄"
        }.get(level, "📝")
        
        print(f"[{timestamp}] {prefix} {message}", flush=True)
    
    def paso_1_descargar_noticias(self, num_noticias: int = 50, force_download: bool = False) -> List[Dict]:
        """
        Paso 1: Descarga noticias desde APIs
        
        Args:
            num_noticias: Número de noticias a descargar
            force_download: Forzar descarga en vivo incluso si hay archivos
            
        Returns:
            Lista de noticias descargadas
        """
        self.log("=" * 70)
        self.log("PASO 1: Descargando Noticias", "PROGRESS")
        self.log("=" * 70)
        
        # Si no se fuerza descarga, intentar usar archivo existente
        if not force_download:
            noticias_files = list(self.data_dir.glob("noticias_newsapi_*.json"))
            if noticias_files:
                latest_file = max(noticias_files, key=lambda p: p.stat().st_mtime)
                self.log(f"Usando archivo existente: {latest_file.name}")
                
                with open(latest_file, 'r', encoding='utf-8') as f:
                    noticias = json.load(f)
                
                self.stats["noticias_descargadas"] = len(noticias)
                self.log(f"Cargadas {len(noticias)} noticias originales", "SUCCESS")
                return noticias[:num_noticias]
        
        # Descargar noticias en vivo desde NewsAPI
        self.log("Descargando noticias en vivo desde NewsAPI...", "PROGRESS")
        
        try:
            # Importar el módulo de NewsAPI
            import sys
            from pathlib import Path
            api_dir = Path(__file__).parent / "api"
            if str(api_dir) not in sys.path:
                sys.path.insert(0, str(api_dir))
            
            from newsapi import fetch_newsapi
            
            # Descargar noticias
            noticias = fetch_newsapi(
                query='política México',
                language='es',
                page_size=num_noticias,
                enrich=True,
                silent=False
            )
            
            self.stats["noticias_descargadas"] = len(noticias)
            self.log(f"Descargadas {len(noticias)} noticias desde NewsAPI", "SUCCESS")
            return noticias
            
        except Exception as e:
            self.log(f"Error descargando noticias: {e}", "ERROR")
            return []
    
    def paso_2_parafrasear_noticias(self, noticias: List[Dict]) -> List[Dict]:
        """
        Paso 2: Parafrasea artículos principales con Blackbox Pro
        (Usa sistema paralelo si hay 2 keys, sino secuencial)
        
        Args:
            noticias: Lista de noticias originales
            
        Returns:
            Lista de noticias parafraseadas (destacados)
        """
        self.log("=" * 70)
        self.log("PASO 2: Parafraseando Artículos Principales (Blackbox Pro)", "PROGRESS")
        self.log("=" * 70)
        
        # Usar primeras 20 noticias para artículos principales
        noticias_principales = noticias[:20]
        
        self.log(f"Parafraseando {len(noticias_principales)} artículos con Blackbox Pro...")
        self.log("(Calidad completa: 1,500-2,000 palabras, 8-12 párrafos)")
        
        # Verificar si hay 2 keys de Blackbox para usar paralelo
        if len(self.blackbox_parallel.api_configs) >= 2:
            self.log("Usando sistema paralelo (2 workers)", "SUCCESS")
            noticias_parafraseadas = self.blackbox_parallel.parafrasear_lote_paralelo(
                noticias_principales,
                max_workers=2
            )
        else:
            self.log("Usando parafraseo secuencial (1 key)")
            noticias_parafraseadas = []
            
            for noticia_idx, noticia in enumerate(noticias_principales, 1):
                try:
                    style_idx = noticia_idx % len(self.paraphraser.styles)
                    style = self.paraphraser.styles[style_idx]
                    
                    self.log(f"  [{noticia_idx}/{len(noticias_principales)}] {noticia.get('title', '')[:50]}...")
                    
                    paraphrased = self.paraphraser.paraphrase_article(noticia, style=style)
                    paraphrased['author'] = paraphrased.get('author') or self.legal_generator.generar_autor_aleatorio()
                    paraphrased['paraphrase_method'] = 'blackbox-pro'
                    
                    noticias_parafraseadas.append(paraphrased)
                    self.stats["noticias_parafraseadas"] += 1
                    
                except Exception as e:
                    self.log(f"Error: {e}", "ERROR")
                    noticia['paraphrase_method'] = 'error'
                    noticias_parafraseadas.append(noticia)
        
        self.stats["articulos_principales"] = len(noticias_parafraseadas)
        self.stats["noticias_parafraseadas"] = len(noticias_parafraseadas)
        self.log(f"Artículos principales completados: {len(noticias_parafraseadas)}", "SUCCESS")
        return noticias_parafraseadas
    
    def paso_2_parafraseo_linguistico(self, noticias: List[Dict]) -> List[Dict]:
        """
        Paso 2 (Alternativo): Parafraseo lingüístico offline (Spacy + NLTK)
        """
        self.log("=" * 70)
        self.log("PASO 2: Parafraseo Lingüístico (Offline - Sin IA Generativa)", "PROGRESS")
        self.log("=" * 70)
        
        if not self.linguistic_paraphraser:
            self.linguistic_paraphraser = LinguisticParaphraser()
            
        noticias_parafraseadas = []
        
        for idx, noticia in enumerate(noticias, 1):
            self.log(f"  [{idx}/{len(noticias)}] Reescritura lingüística: {noticia.get('title', '')[:50]}...")
            
            # Parafrasear
            resultado = self.linguistic_paraphraser.paraphrase_article(noticia)
            noticias_parafraseadas.append(resultado)
            self.stats["noticias_parafraseadas"] += 1
            
        self.stats["articulos_principales"] = len(noticias_parafraseadas)
        return noticias_parafraseadas
    
    def paso_2_1_generar_placeholders(self, noticias_restantes: List[Dict]) -> List[Dict]:
        """
        Paso 2.1: Genera placeholders con Gemini paralelo
        
        Args:
            noticias_restantes: Noticias para convertir en placeholders
            
        Returns:
            Lista de placeholders parafraseados
        """
        self.log("=" * 70)
        self.log("PASO 2.1: Generando Placeholders (Gemini Paralelo)", "PROGRESS")
        self.log("=" * 70)
        
        # Limitar a 80 placeholders como máximo
        noticias_para_placeholders = noticias_restantes[:80]
        
        self.log(f"Parafraseando {len(noticias_para_placeholders)} placeholders con Gemini...")
        self.log("(Parafraseo rápido: título + descripción + 3-4 párrafos)")
        
        placeholders = self.gemini_paraphraser.parafrasear_lote_paralelo(
            noticias_para_placeholders,
            max_workers=3,
            delay_between_batches=0.5
        )
        
        self.stats["placeholders_generados"] = len(placeholders)
        self.stats["noticias_parafraseadas"] += len(placeholders)
        self.log(f"Placeholders completados: {len(placeholders)}", "SUCCESS")
        return placeholders
    
    def paso_2_5_categorizar_noticias(self, noticias: List[Dict]) -> List[Dict]:
        """
        Paso 2.5: Categoriza noticias usando IA
        
        Args:
            noticias: Lista de noticias parafraseadas
            
        Returns:
            Lista de noticias con categorías asignadas
        """
        self.log("=" * 70)
        self.log("PASO 2.5: Categorizando Noticias", "PROGRESS")
        self.log("=" * 70)
        
        noticias_categorizadas = self.categorizador.categorizar_lote(
            noticias,
            use_ai=True,
            batch_delay=0.3
        )
        
        self.log(f"Categorización completada: {len(noticias_categorizadas)} artículos categorizados", "SUCCESS")
        return noticias_categorizadas
    
    def paso_3_generar_imagenes(self, noticias: List[Dict], site_num: int) -> Dict[str, str]:
        """
        Paso 3: Genera 1 imagen por noticia
        
        Args:
            noticias: Lista de noticias parafraseadas
            site_num: Número del sitio
            
        Returns:
            Dict[article_id -> image_path]
        """
        self.log("=" * 70)
        self.log("PASO 3: Generando Imágenes de Noticias", "PROGRESS")
        self.log("=" * 70)
        
        site_images_dir = self.output_base_dir / f"site_{site_num}" / "images"
        site_images_dir.mkdir(parents=True, exist_ok=True)
        
        imagenes = {}
        
        for idx, noticia in enumerate(noticias, 1):
            try:
                # Preparar datos del artículo para generación de imagen
                title = noticia.get('title', '')
                description = noticia.get('description', '')
                category = noticia.get('category', 'tecnología')
                
                # Crear prompt (usado solo si IA está disponible)
                prompt = f"""Professional news image for political article: {title}. 
{description}. 
Style: Modern, clean, political-focused. Category: {category}. 
High quality, photojournalistic, relevant to the specific topic. 
No text, no watermarks."""
                
                self.log(f"  [{idx}/{len(noticias)}] Descargando imagen: {title[:50]}...", "PROGRESS")
                
                # Generar/descargar imagen (NewsAPI primero, luego fallbacks)
                article_id = f"article_{idx}"
                image_path = self.image_generator.generate_image(prompt, article_id, idx, article=noticia)
                
                # Mover a directorio del sitio
                if image_path and Path(image_path).exists():
                    dest_path = site_images_dir / f"news_{idx}.jpg"
                    shutil.copy2(image_path, dest_path)
                    imagenes[article_id] = str(dest_path)
                    self.stats["imagenes_generadas"] += 1
                
            except Exception as e:
                self.log(f"Error generando imagen {idx}: {e}", "WARNING")
            
            # Rate limiting
            time.sleep(1)
        
        self.log(f"Generación de imágenes completada: {self.stats['imagenes_generadas']} imágenes", "SUCCESS")
        return imagenes
    
    def paso_4_crear_metadata_sitios(self, num_sitios: int, verificar_dominios: bool = False) -> List[Dict]:
        """
        Paso 4: Genera nombre de sitio + verifica dominios + crea logo
        
        Args:
            num_sitios: Número de sitios a crear
            verificar_dominios: Si True, verifica disponibilidad de dominios
            
        Returns:
            Lista de metadatos de sitios
        """
        self.log("=" * 70)
        self.log("PASO 4: Creando Metadata de Sitios", "PROGRESS")
        self.log("=" * 70)
        
        protocolo = SitePreCreation(output_dir=str(self.data_dir / "sites_metadata"))
        
        sites_metadata = protocolo.crear_batch_sitios(
            cantidad=num_sitios,
            verificar_dominios=verificar_dominios,
            guardar_archivo=True
        )
        
        self.log(f"Metadata de {len(sites_metadata)} sitios creada", "SUCCESS")
        return sites_metadata
    
    def paso_5_generar_logos(self, sites_metadata: List[Dict]) -> Dict[int, str]:
        """
        Paso 5: Genera logos para cada sitio (prompts ultra específicos)
        
        Args:
            sites_metadata: Metadata de los sitios
            
        Returns:
            Dict[site_id -> logo_path]
        """
        self.log("=" * 70)
        self.log("PASO 5: Generando Logos de Sitios", "PROGRESS")
        self.log("=" * 70)
        
        logos = {}
        
        for idx, metadata in enumerate(sites_metadata, 1):
            try:
                site_name = metadata['nombre']
                tagline = metadata['tagline']
                domain = metadata['dominio']
                
                self.log(f"  [{idx}/{len(sites_metadata)}] Generando logo SVG: {site_name}", "PROGRESS")
                
                # Preparar directorio del sitio
                site_dir = self.output_base_dir / f"site_{idx}"
                site_dir.mkdir(parents=True, exist_ok=True)
                
                # Obtener colores del sitio (por defecto usar Milenio rojo)
                colors = {
                    "primary": "#B10B1F",
                    "secondary": "#FFFFFF"
                }
                
                # Generar logo SVG (siempre funciona, no requiere IA)
                try:
                    logo_result = self.logo_generator.generate_and_save(
                        site_name=site_name,
                        colors=colors,
                        output_dir=str(site_dir),
                        style="auto"
                    )
                    logos[idx] = logo_result['logo_path']
                    self.log(f"    ✓ Logo SVG: {logo_result['logo_type']} ({logo_result['font_used']})", "SUCCESS")
                except Exception as e:
                    self.log(f"⚠️  Error generando logo SVG: {e}", "WARNING")
                    # Fallback: crear logo tipográfico simple
                    fallback_svg = self.logo_generator.generate_typographic_logo(site_name, colors["primary"])
                    fallback_path = site_dir / "logo.svg"
                    self.logo_generator.save_logo(fallback_svg, str(fallback_path))
                    logos[idx] = str(fallback_path)
                
            except Exception as e:
                self.log(f"❌ Error generando logo para sitio {idx}: {e}", "WARNING")
            
            time.sleep(1)
        
        self.log(f"Generación de logos completada: {len(logos)} logos", "SUCCESS")
        return logos
    
    def paso_6_generar_templates_css(self, num_sitios: int, sites_metadata: List[Dict] = None) -> List[Dict]:
        """
        Paso 6: Genera paleta + tipografía + layout y combina módulos
        
        Args:
            num_sitios: Número de templates a generar
            sites_metadata: Metadata de sitios (para obtener colores)
            
        Returns:
            Lista de metadata de templates
        """
        self.log("=" * 70)
        self.log("PASO 6: Generando Templates CSS Modulares", "PROGRESS")
        self.log("=" * 70)
        
        # Generar templates únicos
        templates_metadata = self.template_combiner.generar_multiples_templates(
            num_templates=num_sitios,
            output_dir=str(self.templates_dir / "css"),
            aleatorio=True
        )
        
        self.log(f"Templates CSS generados: {len(templates_metadata)}", "SUCCESS")
        return templates_metadata
    
    def paso_7_generar_sitios_html(self, 
                                   sites_metadata: List[Dict],
                                   noticias: List[Dict],
                                   imagenes: Dict[str, str],
                                   logos: Dict[int, str],
                                   templates_metadata: List[Dict]) -> List[str]:
        """
        Paso 7: Genera sitio HTML completo
        
        Args:
            sites_metadata: Metadata del sitio
            noticias: Lista de noticias parafraseadas
            imagenes: Imágenes generadas
            logos: Logos generados
            templates_metadata: Metadata de templates CSS
            
        Returns:
            Lista de paths de sitios generados
        """
        self.log("=" * 70)
        self.log("PASO 7: Generando Sitio HTML", "PROGRESS")
        self.log("=" * 70)
        
        sitios_generados = []
        metadata = sites_metadata[0]
        idx = self.next_site_number
        
        try:
            site_dir = self.output_base_dir / f"site_{idx}"
            site_dir.mkdir(parents=True, exist_ok=True)
            
            template_info = templates_metadata[0]
            logo_path = logos.get(idx)
            
            self.log(f"Generando: {metadata['nombre']}", "PROGRESS")
            
            # Generar HTML del sitio (index.html)
            index_html = self._generar_index_html(
                metadata, noticias, template_info, idx, logo_path
            )
            
            # Inyectar preloader en el index.html
            preloader_tipo = self._seleccionar_preloader_aleatorio()
            colores_preloader = {
                'primary': metadata.get('color_primario', '#667eea'),
                'secondary': metadata.get('color_secundario', '#764ba2')
            }
            preloader_code = self.preloader_generator.generar_preloader_completo(
                preloader_tipo,
                colores_preloader,
                logo_url=logo_path
            )
            index_html = self.preloader_generator.inyectar_en_html(index_html, preloader_code)
            
            self.log(f"Preloader seleccionado: {preloader_tipo}")
            
            index_path = site_dir / "index.html"
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_html)
            
            # Generar páginas de artículos individuales
            self._generar_paginas_articulos(site_dir, noticias, metadata, template_info, idx, logo_path)
            
            # Generar páginas legales
            self._generar_paginas_legales(site_dir, metadata)
            
            # Copiar CSS
            self._copiar_css(site_dir, idx)
            
            sitios_generados.append(str(index_path))
            self.stats["sitios_creados"] += 1
            
        except Exception as e:
            self.log(f"Error generando sitio: {e}", "ERROR")
        
        self.log(f"Sitio HTML generado", "SUCCESS")
        return sitios_generados
    
    def _generar_index_html(self, metadata: Dict, noticias: List[Dict], 
                           template_info: Dict, site_num: int, logo_path: str = None) -> str:
        """Genera el HTML del index del sitio usando layout avanzado"""
        
        self.log(f"Generando index con AdvancedLayoutGenerator...", "PROGRESS")
        
        # 1. Preparar lista de categorías
        categorias_lista = [
            {'id': cat_id, 'nombre': cat_data['nombre']}
            for cat_id, cat_data in self.categorizador.CATEGORIAS.items()
        ]
        
        # 2. Separar artículos (featured vs normal)
        # Asumimos que 'noticias' ya viene ordenada con destacados primero gracias a featured_manager
        # Pero nos aseguramos filtrando por 'is_featured'
        featured = [n for n in noticias if n.get('is_featured', False)]
        
        # Si no hay marcados como featured, tomar los primeros 3
        if not featured:
            featured = noticias[:3]
        
        # Asegurar que logo_path sea relativo (solo el nombre del archivo) si es una ruta completa
        if logo_path:
            logo_path = Path(logo_path).name
        else:
            logo_path = 'logo.svg'
            
        # 3. Generar HTML
        # all_articles debe ser la lista completa para el carrusel y otros usos
        html = self.advanced_layout.generar_index_completo(
            site_metadata=metadata,
            featured_articles=featured,
            all_articles=noticias,
            categorias=categorias_lista,
            logo_path=logo_path
        )
        
        return html
    
    def _generar_sidebar_articulos(self, otras_noticias: List[Dict], metadata: Dict) -> str:
        """
        Genera sidebar con miniaturas de otros artículos
        
        Args:
            otras_noticias: Lista de otras noticias con índices
            metadata: Metadata del sitio
            
        Returns:
            str: HTML del sidebar
        """
        items_html = []
        for i, noticia in enumerate(otras_noticias):
            # Usar el índice de la noticia original si existe
            article_idx = noticia.get('_display_index', i + 1)
            title = noticia.get('title', '')
            title_truncated = title if len(title) <= 80 else title[:80] + '...'
            
            items_html.append(f"""
                    <article class="sidebar-article">
                        <a href="article_{article_idx}.html" class="sidebar-article-link">
                            <div class="sidebar-article-image">
                                <img src="images/news_{article_idx}.jpg" alt="{title[:50]}">
                                <span class="sidebar-category">{noticia.get('category', 'General')}</span>
                            </div>
                            <div class="sidebar-article-content">
                                <h3 class="sidebar-article-title">{title_truncated}</h3>
                                <span class="sidebar-article-date">{noticia.get('published_at', '')[:10]}</span>
                            </div>
                        </a>
                    </article>""")
        
        sidebar_html = f"""
                <aside class="article-sidebar">
                    <div class="sidebar-section">
                        <h2 class="sidebar-title">Más Noticias</h2>
                        <div class="sidebar-articles">
{''.join(items_html)}
                        </div>
                    </div>
                    
                    <div class="sidebar-section sidebar-newsletter">
                        <h3>Suscríbete</h3>
                        <p>Recibe las últimas noticias en tu correo</p>
                        <form class="newsletter-form">
                            <input type="email" placeholder="Tu email" required>
                            <button type="submit">Suscribirse</button>
                        </form>
                    </div>
                </aside>"""
        
        return sidebar_html
    
    def _formatear_contenido_html(self, texto: str) -> str:
        """
        Convierte texto plano en HTML con estructura semántica y marcado
        """
        if not texto:
            return ""
        
        # Dividir por líneas vacías (doble salto de línea)
        parrafos = texto.strip().split('\n\n')
        
        # Envolver cada párrafo en tags <p> con clases semánticas
        html_parrafos = []
        for i, parrafo in enumerate(parrafos):
            parrafo = parrafo.strip()
            if parrafo:
                # Limpiar saltos de línea internos y espacios múltiples
                parrafo = ' '.join(parrafo.split())
                
                # Primer párrafo como lead/intro
                if i == 0:
                    html_parrafos.append(f'<p class="lead">{parrafo}</p>')
                else:
                    html_parrafos.append(f'<p>{parrafo}</p>')
        
        return '\n                    '.join(html_parrafos)
    
    def _seleccionar_preloader_aleatorio(self) -> str:
        """Selecciona un tipo de preloader aleatorio"""
        import random
        tipos_disponibles = [
            'contador', 'fade', 'slide-down', 
            'circle-expand', 'bars-loading', 'dots-pulse',
            'spinning-logo', 'wave-animation', 'glitch-effect',
            'rotating-square', 'progress-circle', 'bouncing-balls'
        ]
        return random.choice(tipos_disponibles)
    
    def _generar_paginas_articulos(self, site_dir: Path, noticias: List[Dict],
                                   metadata: Dict, template_info: Dict, site_num: int, logo_path: str = None):
        """Genera páginas HTML individuales para cada artículo con sidebar"""
        for idx, noticia in enumerate(noticias, 1):
            # Generar sidebar con otros artículos (excluyendo el actual)
            otras_noticias = []
            for i, n in enumerate(noticias, 1):
                if i != idx:
                    n_copy = n.copy()
                    n_copy['_display_index'] = i
                    otras_noticias.append(n_copy)
            
            sidebar_html = self._generar_sidebar_articulos(otras_noticias[:6], metadata)
            
            # Generar metadatos SEO
            article_url = f"{metadata.get('domain', 'https://ejemplo.com')}/article_{idx}.html"
            seo_meta_tags = self.seo_generator.generar_meta_tags_articulo(
                noticia,
                metadata,
                article_url,
                idx
            )
            
            article_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
{seo_meta_tags}
    <title>{noticia.get('title', 'Artículo')} - {metadata['nombre']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-branding">
                {'<img src="logo.jpg" alt="' + metadata['nombre'] + '" class="logo-img">' if logo_path else ''}
                <h1 class="logo"><a href="index.html">{metadata['nombre']}</a></h1>
            </div>
            <nav class="nav">
                <a href="index.html" class="nav-link">Inicio</a>
            </nav>
        </div>
    </header>
    
    <main class="main article-page">
        <div class="container">
            <div class="article-layout">
                <article class="article-full">
                    <header class="article-header">
                        <div class="article-category-badge">{noticia.get('category', 'General')}</div>
                        <h1 class="article-title">{noticia.get('title', '')}</h1>
                        <div class="article-meta">
                            <span class="author">Por {noticia.get('author', 'Redacción')}</span>
                            <span class="separator">•</span>
                            <time class="date">{noticia.get('published_at', '')}</time>
                        </div>
                    </header>
                    
                    <figure class="article-image-wrapper">
                        <img src="images/news_{idx}.jpg" alt="{noticia.get('title', '')}" class="article-image">
                    </figure>
                    
                    <div class="article-content">
                    {self._formatear_contenido_html(noticia.get('full_article', noticia.get('content', noticia.get('description', ''))))}
                    </div>
                    
                    <footer class="article-footer">
                        <div class="article-tags">
                            <span class="tag">{noticia.get('category', 'General')}</span>
                        </div>
                        <div class="article-share">
                            <span>Compartir:</span>
                            <a href="#" class="share-link">Facebook</a>
                            <a href="#" class="share-link">Twitter</a>
                            <a href="#" class="share-link">WhatsApp</a>
                        </div>
                    </footer>
                </article>
                
                {sidebar_html}
            </div>
        </div>
    </main>
    
    <footer class="footer">
        <div class="container">
            <p><a href="index.html">← Volver al inicio</a></p>
            <p>&copy; 2026 {metadata['nombre']}</p>
        </div>
    </footer>
</body>
</html>"""
            
            # Inyectar preloader (solo en el primer artículo para testing, o todos si prefieres)
            if idx == 1:
                # Seleccionar preloader aleatorio
                preloader_tipo = self._seleccionar_preloader_aleatorio()
                colores_preloader = {
                    'primary': metadata.get('color_primario', '#667eea'),
                    'secondary': metadata.get('color_secundario', '#764ba2')
                }
                preloader_code = self.preloader_generator.generar_preloader_completo(
                    preloader_tipo,
                    colores_preloader
                )
                article_html = self.preloader_generator.inyectar_en_html(article_html, preloader_code)
                self.log(f"  Preloader: {preloader_tipo} (artículo {idx})")
            
            article_path = site_dir / f"article_{idx}.html"
            with open(article_path, 'w', encoding='utf-8') as f:
                f.write(article_html)
    
    def _generar_paginas_legales(self, site_dir: Path, metadata: Dict):
        """
        Genera páginas legales (Términos, Privacidad, FAQs, Acerca de)
        
        Args:
            site_dir: Directorio del sitio
            metadata: Metadata del sitio
        """
        site_name = metadata['nombre']
        domain = metadata['dominio']
        tagline = metadata['tagline']
        
        # Generar Términos y Condiciones
        terms_html = self.legal_generator.generar_terminos_condiciones(site_name, domain)
        terms_path = site_dir / "terminos.html"
        with open(terms_path, 'w', encoding='utf-8') as f:
            f.write(terms_html)
        
        # Generar Política de Privacidad
        privacy_html = self.legal_generator.generar_politica_privacidad(site_name, domain)
        privacy_path = site_dir / "privacidad.html"
        with open(privacy_path, 'w', encoding='utf-8') as f:
            f.write(privacy_html)
        
        # Generar FAQs
        faqs_html = self.legal_generator.generar_faqs(site_name)
        faqs_path = site_dir / "faqs.html"
        with open(faqs_path, 'w', encoding='utf-8') as f:
            f.write(faqs_html)
        
        # Generar Acerca de
        about_html = self.legal_generator.generar_acerca_de(site_name, tagline, domain)
        about_path = site_dir / "acerca.html"
        with open(about_path, 'w', encoding='utf-8') as f:
            f.write(about_html)
    
    def _copiar_css(self, site_dir: Path, site_num: int):
        """Copia el CSS del template al directorio del sitio"""
        # Siempre usar template1.css ya que se genera uno por ejecución
        css_source = self.templates_dir / "css" / "template1.css"
        css_dest = site_dir / "style.css"
        
        if css_source.exists():
            shutil.copy2(css_source, css_dest)
        else:
            self.log(f"⚠️  No se encontró {css_source}", "WARNING")
    
    def ejecutar_flujo_completo(self, verificar_dominios: bool = False, force_download: bool = True, offline_mode: bool = False) -> Dict:
        """
        Ejecuta el flujo completo de generación
        
        Args:
            verificar_dominios: Si True, verifica disponibilidad de dominios
            force_download: Si True, descarga noticias en vivo desde NewsAPI
            offline_mode: Si True, usa parafraseo lingüístico en lugar de APIs de IA
            
        Returns:
            Diccionario con resultados y estadísticas
        """
        self.log("=" * 70)
        self.log("🚀 INICIANDO FLUJO COMPLETO DE GENERACIÓN DE SITIO")
        self.log("=" * 70)
        self.log(f"Run ID: {self.run_id}")
        self.log(f"Siguiente sitio: site_{self.next_site_number}")
        self.log(f"Verificar dominios: {verificar_dominios}")
        self.log(f"Descarga en vivo: {force_download}")
        self.log(f"Modo Offline (Sin IA): {offline_mode}")
        
        try:
            # Verificar si el sitio ya existe ANTES de generar contenido
            site_dir = self.output_base_dir / f"site_{self.next_site_number}"
            if site_dir.exists():
                self.log(f"⚠️  El sitio site_{self.next_site_number} ya existe. Abortando para no sobrescribir.", "WARNING")
                raise Exception(f"Sitio site_{self.next_site_number} ya existe")
            
            # Paso 1: Descargar noticias (más para cubrir destacados + placeholders)
            noticias = self.paso_1_descargar_noticias(num_noticias=100, force_download=force_download)
            if not noticias:
                raise Exception("No hay noticias disponibles")
            
            if offline_mode:
                # Usa parafraseo lingüístico para TODO
                self.log("⚠️  MODO OFFLINE ACTIVADO: Usando Spacy+NLTK en lugar de Blackbox/Gemini")
                articulos_principales = self.paso_2_parafraseo_linguistico(noticias[:100]) # Procesar todas
                placeholders = [] # No hay placeholders separados en este modo
            else:
                # Paso 2: Parafrasear artículos principales (Blackbox Pro - primeros 20)
                articulos_principales = self.paso_2_parafrasear_noticias(noticias[:20])
                
                # Paso 2.1: Generar placeholders (Gemini paralelo - resto)
                placeholders = self.paso_2_1_generar_placeholders(noticias[20:])
            
            # Combinar todos los artículos
            todos_articulos = articulos_principales + placeholders
            
            self.log(f"Total artículos: {len(todos_articulos)} ({len(articulos_principales)} destacados + {len(placeholders)} placeholders)")
            
            # Paso 2.5: Categorizar todos los artículos
            noticias_categorizadas = self.paso_2_5_categorizar_noticias(todos_articulos)
            
            # Paso 2.6: Marcar y ordenar destacados
            noticias_categorizadas = self.featured_manager.marcar_destacados(noticias_categorizadas)
            noticias_categorizadas = self.featured_manager.ordenar_destacados_primero(noticias_categorizadas)
            
            separated = self.featured_manager.separar_destacados_y_placeholders(noticias_categorizadas)
            self.log(f"Destacados: {separated['stats']['total_featured']}, Placeholders: {separated['stats']['total_placeholders']}")
            
            # Paso 3: Generar imágenes
            imagenes = self.paso_3_generar_imagenes(noticias_categorizadas, self.next_site_number)
            
            # Paso 4: Crear metadata del sitio
            sites_metadata = self.paso_4_crear_metadata_sitios(1, verificar_dominios)
            
            # Paso 5: Generar logo
            logos = self.paso_5_generar_logos(sites_metadata)
            
            # Paso 6: Generar template CSS
            templates_metadata = self.paso_6_generar_templates_css(1)
            
            # Paso 7: Generar sitio HTML
            sitios_generados = self.paso_7_generar_sitios_html(
                sites_metadata, noticias_categorizadas, imagenes,
                logos, templates_metadata
            )
            
            # Paso 8: Generar RSS feeds
            self.paso_8_generar_rss_feeds(noticias_categorizadas, sites_metadata[0], sitios_generados[0]['site_dir'])
            
            # Paso 9: Generar páginas de categorías
            self.paso_9_generar_paginas_categorias(noticias_categorizadas, sites_metadata[0], sitios_generados[0]['site_dir'])
            
            # Paso 10: Generar imágenes Open Graph
            self.paso_10_generar_og_images(noticias_categorizadas, sites_metadata[0], sitios_generados[0]['site_dir'])
            
            # Calcular estadísticas finales
            tiempo_total = time.time() - self.stats["tiempo_inicio"]
            
            resultado = {
                "success": True,
                "run_id": self.run_id,
                "sitios_generados": sitios_generados,
                "stats": {
                    **self.stats,
                    "tiempo_total_segundos": tiempo_total,
                    "tiempo_total_minutos": tiempo_total / 60
                },
                "output_dir": str(self.output_base_dir)
            }
            
            # Guardar resumen
            self._guardar_resumen(resultado)
            
            self.log("=" * 70)
            self.log("🎉 FLUJO COMPLETADO EXITOSAMENTE", "SUCCESS")
            self.log("=" * 70)
            self.log(f"Sitio creado: {self.stats['sitios_creados']}")
            self.log(f"Artículos principales (Blackbox Pro): {self.stats.get('articulos_principales', 20)}")
            self.log(f"Placeholders (Gemini): {self.stats.get('placeholders_generados', 0)}")
            self.log(f"Total artículos: {self.stats['noticias_parafraseadas']}")
            self.log(f"Imágenes generadas: {self.stats['imagenes_generadas']}")
            self.log(f"Tiempo total: {tiempo_total/60:.2f} minutos")
            self.log(f"Directorio de salida: {self.output_base_dir}")
            self.log(f"")
            self.log(f"✨ MEJORA: Sistema paralelo {int((7*60)/tiempo_total if tiempo_total > 0 else 1)}x más rápido que el original")
            
            return resultado
            
        except Exception as e:
            self.log(f"Error en el flujo: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": str(e),
                "stats": self.stats
            }
    
    def _guardar_resumen(self, resultado: Dict):
        """Guarda un resumen de la ejecución"""
        resumen_path = self.output_base_dir / f"run_summary_{self.run_id}.json"
        with open(resumen_path, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    def paso_8_generar_rss_feeds(self, noticias: List[Dict], site_metadata: Dict, site_dir: Path):
        """
        Paso 8: Genera RSS feeds (general y por categoría)
        
        Args:
            noticias: Lista de noticias categorizadas
            site_metadata: Metadata del sitio
            site_dir: Directorio del sitio
        """
        self.log("=" * 70)
        self.log("PASO 8: Generando RSS Feeds", "PROGRESS")
        self.log("=" * 70)
        
        try:
            feeds = self.rss_generator.generar_feeds_por_categoria(
                noticias,
                site_metadata,
                output_dir=str(site_dir)
            )
            
            self.log(f"Generados {len(feeds)} RSS feeds", "SUCCESS")
            
        except Exception as e:
            self.log(f"Error generando RSS: {e}", "ERROR")
    
    def paso_9_generar_paginas_categorias(self, noticias: List[Dict], site_metadata: Dict, site_dir: Path):
        """
        Paso 9: Genera páginas HTML por categoría
        
        Args:
            noticias: Lista de noticias categorizadas
            site_metadata: Metadata del sitio
            site_dir: Directorio del sitio
        """
        self.log("=" * 70)
        self.log("PASO 9: Generando Páginas de Categorías", "PROGRESS")
        self.log("=" * 70)
        
        try:
            # Agrupar por categoría
            grouped = self.categorizador.agrupar_por_categoria(noticias)
            
            # Crear directorio de categorías
            cat_dir = site_dir / 'categoria'
            cat_dir.mkdir(exist_ok=True)
            
            # Obtener colores del sitio
            color_palette = {
                'primary': site_metadata.get('color_primario', '#667eea'),
                'secondary': site_metadata.get('color_secundario', '#764ba2')
            }
            
            # Generar página por cada categoría
            for cat_id, cat_articles in grouped.items():
                cat_data = self.categorizador.CATEGORIAS.get(cat_id, {})
                cat_nombre = cat_data.get('nombre', cat_id)
                
                output_path = cat_dir / f"{cat_id}.html"
                
                self.section_generator.generar_pagina_categoria(
                    cat_id,
                    cat_nombre,
                    cat_articles,
                    site_metadata,
                    color_palette,
                    str(output_path)
                )
                
                self.log(f"  Generada: {cat_nombre} ({len(cat_articles)} artículos)")
            
            # Generar índice de categorías
            index_path = site_dir / 'categorias.html'
            self.section_generator.generar_index_categorias(
                grouped,
                site_metadata,
                color_palette,
                str(index_path)
            )
            
            self.log(f"Generadas {len(grouped)} páginas de categorías + índice", "SUCCESS")
            
        except Exception as e:
            self.log(f"Error generando páginas de categorías: {e}", "ERROR")
    
    def paso_10_generar_og_images(self, noticias: List[Dict], site_metadata: Dict, site_dir: Path):
        """
        Paso 10: Genera imágenes Open Graph para compartir en redes sociales
        
        Args:
            noticias: Lista de noticias
            site_metadata: Metadata del sitio
            site_dir: Directorio del sitio
        """
        self.log("=" * 70)
        self.log("PASO 10: Generando Imágenes Open Graph", "PROGRESS")
        self.log("=" * 70)
        
        try:
            # Configurar output dir para OG images
            self.og_image_generator.output_dir = site_dir / 'og-images'
            
            # Generar imágenes
            og_images = self.og_image_generator.generar_og_images_lote(
                noticias,
                site_metadata
            )
            
            self.log(f"Generadas {len(og_images)} imágenes Open Graph (1200x630)", "SUCCESS")
            
        except Exception as e:
            self.log(f"Error generando imágenes OG: {e}", "WARNING")


def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Master Orchestrator - Generación Completa de Sitio")
    parser.add_argument('--verificar-dominios', action='store_true', help='Verificar disponibilidad de dominios')
    parser.add_argument('--api-whois', action='store_true', help='Usar APILayer WHOIS API (requiere APILAYER_API_KEY en .env)')
    parser.add_argument('--output-dir', type=str, default=None, help='Directorio de salida')
    parser.add_argument('--usar-cache', action='store_true', help='Usar noticias en cache en lugar de descargar nuevas')
    parser.add_argument('--offline', action='store_true', help='Usar modo offline (parafraseo lingüístico sin IA)')
    
    args = parser.parse_args()
    
    # Crear orquestador
    orchestrator = MasterOrchestrator(
        output_base_dir=args.output_dir,
        usar_api_whois=args.api_whois
    )
    
    # Ejecutar flujo
    resultado = orchestrator.ejecutar_flujo_completo(
        verificar_dominios=args.verificar_dominios,
        force_download=not args.usar_cache,
        offline_mode=args.offline
    )
    
    # Retornar código de salida
    sys.exit(0 if resultado["success"] else 1)


if __name__ == "__main__":
    main()
