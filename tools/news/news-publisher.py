#!/usr/bin/env python3
"""
Sistema de Publicación Automática de Noticias
Publica 1 noticia por hora con contenido único y parafraseado
"""

import os
import json
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import hashlib

# Configuración
NEWS_API_KEY = os.getenv('NEWSAPI_KEY', 'YOUR_NEWSAPI_KEY')
BLACKBOX_API_KEY = os.getenv('BLACKBOX_API_KEY', '')
SUPERVISOR_PROVIDER = os.getenv("SUPERVISOR_PROVIDER", "")
SUPERVISOR_MODEL = os.getenv("SUPERVISOR_MODEL", "")
REPO_ROOT = Path(__file__).resolve().parents[2]
SITES_DIR = Path(os.getenv("SITES_DIR", REPO_ROOT / "sites"))
DATA_DIR = Path(os.getenv("NEWS_DATA_DIR", REPO_ROOT / "data"))
QUEUE_DIR = DATA_DIR / 'news_queue'
PUBLISHED_DIR = DATA_DIR / 'published_news'
LOGS_DIR = DATA_DIR / 'logs'

# Crear directorios
for dir_path in [DATA_DIR, QUEUE_DIR, PUBLISHED_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Archivos de control
QUEUE_FILE = QUEUE_DIR / 'news_queue.json'
PUBLISHED_FILE = PUBLISHED_DIR / 'published_news.json'
CONFIG_FILE = DATA_DIR / 'publisher_config.json'
LOG_FILE = LOGS_DIR / f'publisher_{datetime.now().strftime("%Y%m%d")}.log'

from text_supervisor import supervise_article


class NewsParaphraser:
    """Parafrasea noticias de forma ligera y supervisa gramática"""
    
    def __init__(self, supervisor_provider=None, supervisor_model=None):
        self.api_key = BLACKBOX_API_KEY
        self.api_url = 'https://api.blackbox.ai/chat/completions'
        self.styles = [
            "formal y periodístico",
            "narrativo y descriptivo",
            "analítico y detallado",
            "directo y conciso",
            "editorial con contexto"
        ]
        self.supervisor_provider = supervisor_provider or SUPERVISOR_PROVIDER
        self.supervisor_model = supervisor_model or SUPERVISOR_MODEL
    
    def paraphrase_article(self, article: Dict, style_index: int = 0) -> Dict:
        """Parafrasea un artículo completo"""
        # Parafraseo básico sin IA generativa
        paraphrased_article = self.basic_paraphrase(article, style_index)

        # Supervisión gramatical opcional con LLM
        if self.supervisor_provider and self.supervisor_model:
            paraphrased_article = supervise_article(paraphrased_article, self.supervisor_provider, self.supervisor_model)

        return paraphrased_article
    
    def basic_paraphrase(self, article: Dict, style_index: int) -> Dict:
        """Parafraseo básico sin IA"""
        paraphrased = article.copy()
        
        # Parafrasear título (cambiar estructura)
        title = article.get('title', '')
        paraphrased['title'] = self.rewrite_title(title)
        
        # Parafrasear descripción
        description = article.get('description', '')
        paraphrased['description'] = self.rewrite_description(description)
        
        # Marcar como parafraseado
        paraphrased['paraphrased'] = True
        paraphrased['paraphrase_style'] = self.styles[style_index % len(self.styles)]
        paraphrased['paraphrased_at'] = datetime.now().isoformat()
        
        return paraphrased
    
    def rewrite_title(self, title: str) -> str:
        """Reescribe el título"""
        # Sinónimos comunes
        replacements = {
            'anuncia': 'revela',
            'revela': 'anuncia',
            'confirma': 'confirman',
            'investiga': 'investigan',
            'presenta': 'presentan',
            'lanza': 'lanzan',
            'inicia': 'inician',
            'México': 'el país',
            'Gobierno': 'El Ejecutivo',
            'Presidente': 'El mandatario'
        }
        
        rewritten = title
        for old, new in replacements.items():
            if old in rewritten and len(rewritten) > 50:
                rewritten = rewritten.replace(old, new, 1)
                break
        
        return rewritten if rewritten != title else f"[ANÁLISIS] {title}"
    
    def rewrite_description(self, description: str) -> str:
        """Reescribe la descripción"""
        if len(description) < 50:
            return description
        
        # Dividir y reorganizar
        sentences = description.split('. ')
        if len(sentences) > 1:
            # Invertir orden de las primeras dos oraciones
            sentences[0], sentences[1] = sentences[1], sentences[0]
            return '. '.join(sentences)
        
        return description
    
    def extract_title(self, text: str, default: str) -> str:
        """Extrae el título del texto parafraseado"""
        lines = text.strip().split('\n')
        for line in lines:
            if len(line) > 20 and len(line) < 150:
                return line.strip()
        return default
    
    def extract_description(self, text: str, default: str) -> str:
        """Extrae la descripción del texto parafraseado"""
        # Tomar primeras 200 palabras
        words = text.split(' ')
        description = ' '.join(words[:30])
        return description if len(description) > 50 else default
    
    def log(self, message: str):
        """Registra un mensaje en el log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")


class NewsPublisher:
    """Publica una noticia por hora en los 10 sitios"""
    
    def __init__(self):
        self.paraphraser = NewsParaphraser()
        self.load_config()
    
    def load_config(self):
        """Carga la configuración del publisher"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'publish_interval_hours': 1,
                'last_published': None,
                'total_published': 0,
                'sites_count': 10
            }
            self.save_config()
    
    def save_config(self):
        """Guarda la configuración"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def load_queue(self) -> List[Dict]:
        """Carga la cola de noticias"""
        if QUEUE_FILE.exists():
            with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_queue(self, queue: List[Dict]):
        """Guarda la cola de noticias"""
        with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
    
    def load_published(self) -> List[Dict]:
        """Carga el historial de noticias publicadas"""
        if PUBLISHED_FILE.exists():
            with open(PUBLISHED_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_published(self, published: List[Dict]):
        """Guarda el historial de noticias publicadas"""
        with open(PUBLISHED_FILE, 'w', encoding='utf-8') as f:
            json.dump(published, f, ensure_ascii=False, indent=2)
    
    def download_news(self, query='México', page_size=10) -> List[Dict]:
        """Descarga noticias nuevas"""
        print(f"📡 Descargando noticias para: {query}")
        
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': query,
            'apiKey': NEWS_API_KEY,
            'language': 'es',
            'sortBy': 'publishedAt',
            'pageSize': page_size
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            print(f"✅ {len(articles)} noticias descargadas")
            return articles
            
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return []
    
    def add_to_queue(self, articles: List[Dict]):
        """Agrega noticias a la cola"""
        queue = self.load_queue()
        published_urls = set([p.get('url', '') for p in self.load_published()])
        
        added_count = 0
        for article in articles:
            if article.get('url') not in published_urls:
                queue.append(article)
                added_count += 1
        
        self.save_queue(queue)
        print(f"✅ {added_count} noticias agregadas a la cola (total: {len(queue)})")
    
    def publish_next_news(self):
        """Publica la siguiente noticia de la cola"""
        queue = self.load_queue()
        
        if not queue:
            print("⚠️ Cola vacía, descargando noticias...")
            new_news = self.download_news()
            self.add_to_queue(new_news)
            queue = self.load_queue()
        
        if not queue:
            print("❌ No hay noticias disponibles")
            return False
        
        # Tomar la primera noticia de la cola
        article = queue.pop(0)
        
        # Parafrasear con estilo único
        style_index = self.config.get('total_published', 0)
        paraphrased_article = self.paraphraser.paraphrase_article(article, style_index)
        
        # Agregar metadata de publicación
        paraphrased_article['published_at'] = datetime.now().isoformat()
        paraphrased_article['publication_number'] = self.config.get('total_published', 0) + 1
        
        # Publicar en los 10 sitios
        print(f"📰 Publicando noticia #{paraphrased_article['publication_number']}: {paraphrased_article['title'][:50]}...")
        
        self.update_sites(paraphrased_article)
        
        # Guardar en historial
        published = self.load_published()
        published.append(paraphrased_article)
        self.save_published(published)
        
        # Actualizar cola
        self.save_queue(queue)
        
        # Actualizar config
        self.config['last_published'] = datetime.now().isoformat()
        self.config['total_published'] = self.config.get('total_published', 0) + 1
        self.save_config()
        
        print(f"✅ Noticia publicada exitosamente")
        self.paraphraser.log(f"Noticia #{self.config['total_published']} publicada: {paraphrased_article['title'][:100]}")
        
        return True
    
    def update_sites(self, article: Dict):
        """Actualiza los 10 sitios con la nueva noticia"""
        for site_num in range(1, 11):
            site_file = SITES_DIR / f'site{site_num}.html'
            
            if not site_file.exists():
                continue
            
            with open(site_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Crear HTML de la noticia
            news_html = f"""
    <article class="breaking-news-item" style="background:#fff3cd;border-left:4px solid #ffc107;padding:20px;margin:20px 0;border-radius:8px;">
        <span style="background:#ffc107;color:#000;padding:4px 12px;border-radius:20px;font-size:0.8em;font-weight:bold;">ÚLTIMA HORA</span>
        <h2 style="margin:15px 0 10px 0;font-size:1.5em;color:#333;">{article.get('title', 'Noticia')}</h2>
        <p style="color:#666;line-height:1.7;margin-bottom:15px;">{article.get('description', '')}</p>
        <div style="background:#f9f9f9;padding:20px;border-radius:8px;margin:15px 0;">
            <p style="line-height:1.8;color:#333;">{article.get('full_text', article.get('content', ''))[:800]}...</p>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;padding-top:15px;border-top:1px solid #ddd;">
            <span style="color:#888;font-size:0.9em;">Por {article.get('author', 'Redacción')}</span>
            <span style="color:#888;font-size:0.9em;">{article.get('published_at', datetime.now().isoformat())[:10]}</span>
        </div>
    </article>
"""
            
            # Insertar después del header principal o antes del footer
            if '<section class="breaking-news"' in content:
                content = content.replace('<section class="breaking-news"', news_html + '\n    <section class="breaking-news"')
            elif '</footer>' in content:
                content = content.replace('</footer>', news_html + '\n    </footer>')
            
            # Guardar sitio actualizado
            with open(site_file, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"   ✅ 10 sitios actualizados")
    
    def run_scheduler(self):
        """Ejecuta el scheduler continuo"""
        print("🕐 Iniciando scheduler de publicación (1 noticia/hora)...")
        print(f"📊 Total publicadas: {self.config.get('total_published', 0)}")
        print(f"🕐 Última publicación: {self.config.get('last_published', 'Nunca')}")
        
        while True:
            try:
                # Verificar si es hora de publicar
                last_published = self.config.get('last_published')
                
                if last_published:
                    last_pub_time = datetime.fromisoformat(last_published)
                    hours_since_last = (datetime.now() - last_pub_time).total_seconds() / 3600
                    
                    if hours_since_last < self.config.get('publish_interval_hours', 1):
                        next_pub_in = self.config.get('publish_interval_hours', 1) - hours_since_last
                        print(f"⏰ Próxima publicación en {next_pub_in:.1f} horas...")
                        time.sleep(3600)  # Esperar 1 hora
                        continue
                
                # Publicar noticia
                self.publish_next_news()
                
                # Esperar 1 hora
                time.sleep(3600)
                
            except KeyboardInterrupt:
                print("\n⏹️ Scheduler detenido por usuario")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                self.paraphraser.log(f"ERROR: {e}")
                time.sleep(300)  # Esperar 5 minutos en caso de error
    
    def get_status(self) -> Dict:
        """Obtiene el estado actual del sistema"""
        queue = self.load_queue()
        published = self.load_published()
        
        return {
            'total_published': self.config.get('total_published', 0),
            'last_published': self.config.get('last_published', 'Nunca'),
            'queue_size': len(queue),
            'published_today': len([p for p in published if p.get('published_at', '')[:10] == datetime.now().strftime('%Y-%m-%d')]),
            'next_publish_in': '1 hora'
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="News Publisher")
    parser.add_argument("command", nargs="?", default="publish", help="publish|status|add|queue|run")
    parser.add_argument("--supervisor-provider", default=SUPERVISOR_PROVIDER)
    parser.add_argument("--supervisor-model", default=SUPERVISOR_MODEL)
    parser.add_argument("--query", default="México")
    parser.add_argument("--count", type=int, default=10)
    args = parser.parse_args()

    publisher = NewsPublisher(
        supervisor_provider=args.supervisor_provider,
        supervisor_model=args.supervisor_model,
    )

    command = args.command
        
        if command == 'publish':
            # Publicar una noticia inmediatamente
            publisher.publish_next_news()
        
        elif command == 'status':
            # Mostrar estado
            status = publisher.get_status()
            print("\n📊 ESTADO DEL SISTEMA")
            print("="*60)
            print(f"📰 Total publicadas: {status['total_published']}")
            print(f"🕐 Última publicación: {status['last_published']}")
            print(f"📋 Cola de espera: {status['queue_size']} noticias")
            print(f"📅 Publicado hoy: {status['published_today']}")
            print(f"⏰ Próxima publicación: {status['next_publish_in']}")
            print("="*60)
        
        elif command == 'add':
            # Agregar noticias a la cola
            new_news = publisher.download_news(args.query, args.count)
            publisher.add_to_queue(new_news)
        
        elif command == 'queue':
            # Mostrar cola
            queue = publisher.load_queue()
            print(f"\n📋 COLA DE NOTICIAS ({len(queue)} noticias)")
            print("="*60)
            for i, article in enumerate(queue[:10], 1):
                print(f"{i}. {article.get('title', 'Sin título')[:80]}")
            if len(queue) > 10:
                print(f"... y {len(queue) - 10} más")
            print("="*60)
        
        elif command == 'run':
            # Ejecutar scheduler continuo
            publisher.run_scheduler()
        
        else:
            print("Comandos disponibles:")
            print("  publish  - Publicar una noticia inmediatamente")
            print("  status   - Mostrar estado del sistema")
            print("  add --query \"México\" --count 10 - Agregar noticias a la cola")
            print("  queue    - Mostrar cola de noticias")
            print("  run      - Ejecutar scheduler continuo (1 noticia/hora)")


if __name__ == "__main__":
    main()
