#!/usr/bin/env python3
"""
Servidor HTTP simple para servir los 2 ejemplos de noticias parafraseadas
Puerto 8001: Noticia 1
Puerto 8002: Noticia 2
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import threading

# Buscar el archivo más reciente de noticias parafraseadas
data_dir = Path(__file__).parent.parent
paraphrased_files = list(data_dir.glob("noticias_parafraseadas_*.json"))

if not paraphrased_files:
    print("❌ No se encontraron archivos de noticias parafraseadas")
    sys.exit(1)

latest_file = max(paraphrased_files, key=lambda p: p.stat().st_mtime)
print(f"📄 Cargando: {latest_file.name}")

with open(latest_file, 'r', encoding='utf-8') as f:
    noticias = json.load(f)

if len(noticias) < 2:
    print("❌ Se necesitan al menos 2 noticias en el archivo")
    sys.exit(1)

# Separar las dos noticias
noticia_1 = noticias[0]
noticia_2 = noticias[1]


class ArticleHandler(BaseHTTPRequestHandler):
    """Handler para servir un artículo específico"""
    
    article_data = None
    article_number = None
    
    def log_message(self, format, *args):
        """Silenciar logs del servidor"""
        pass
    
    def do_GET(self):
        """Manejar requests GET"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = self.generate_html()
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/json':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            
            self.wfile.write(json.dumps(self.article_data, ensure_ascii=False, indent=2).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def generate_html(self):
        """Generar HTML para mostrar el artículo"""
        article = self.article_data
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article.get('title', 'Sin título')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.8;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem 1rem;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }}
        
        .article-number {{
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            opacity: 0.9;
            margin-bottom: 1rem;
        }}
        
        .title {{
            font-size: 2.5rem;
            font-weight: bold;
            line-height: 1.2;
            margin-bottom: 1rem;
        }}
        
        .metadata {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            font-size: 0.9rem;
            opacity: 0.9;
            margin-top: 1.5rem;
        }}
        
        .metadata-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .content {{
            padding: 3rem 2.5rem;
        }}
        
        .original-title {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 1rem 1.5rem;
            margin-bottom: 2rem;
            border-radius: 4px;
        }}
        
        .original-title-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #667eea;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .original-title-text {{
            color: #495057;
            font-size: 1rem;
        }}
        
        .article-text {{
            font-size: 1.125rem;
            line-height: 1.9;
            color: #2c3e50;
        }}
        
        .article-text p {{
            margin-bottom: 1.5rem;
            text-align: justify;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            padding: 2rem 2.5rem;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }}
        
        .stat-card {{
            text-align: center;
            padding: 1rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .actions {{
            padding: 2rem 2.5rem;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 0.75rem 2rem;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}
        
        .btn-secondary {{
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }}
        
        .btn-secondary:hover {{
            background: #667eea;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .title {{
                font-size: 1.75rem;
            }}
            
            .content {{
                padding: 2rem 1.5rem;
            }}
            
            .article-text {{
                font-size: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="article-number">📰 Ejemplo {self.article_number}</div>
            <h1 class="title">{article.get('title', 'Sin título')}</h1>
            <div class="metadata">
                <div class="metadata-item">
                    <span>📅</span>
                    <span>{article.get('published_at', 'N/A')[:10]}</span>
                </div>
                <div class="metadata-item">
                    <span>✍️</span>
                    <span>{article.get('author', 'Sin autor')}</span>
                </div>
                <div class="metadata-item">
                    <span>🏢</span>
                    <span>{article.get('source_name', 'Sin fuente')}</span>
                </div>
                <div class="metadata-item">
                    <span>🎨</span>
                    <span>{article.get('style', 'Sin estilo')}</span>
                </div>
            </div>
        </div>
        
        <div class="content">
            <div class="original-title">
                <div class="original-title-label">Título Original</div>
                <div class="original-title-text">{article.get('original_title', 'N/A')}</div>
            </div>
            
            <div class="article-text">
                {''.join(f'<p>{para.strip()}</p>' for para in article.get('full_text', 'Sin contenido').split('\n\n') if para.strip())}
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{len(article.get('full_text', '').split())}</div>
                <div class="stat-label">Palabras</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(article.get('full_text', ''))}</div>
                <div class="stat-label">Caracteres</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(article.get('full_text', '').split('\\n\\n'))}</div>
                <div class="stat-label">Párrafos</div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/json" class="btn btn-primary" target="_blank">📄 Ver JSON</a>
            <a href="{article.get('url', '#')}" class="btn btn-secondary" target="_blank">🔗 Artículo Original</a>
        </div>
    </div>
</body>
</html>"""
        return html


def create_handler(article, number):
    """Factory para crear handlers con artículo específico"""
    class CustomHandler(ArticleHandler):
        article_data = article
        article_number = number
    return CustomHandler


def start_server(port, handler, article_num):
    """Iniciar servidor en puerto específico"""
    server = HTTPServer(('0.0.0.0', port), handler)
    print(f"✅ Servidor {article_num} iniciado en http://localhost:{port}")
    server.serve_forever()


def main():
    """Iniciar ambos servidores"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     🌐 SERVIDORES HTTP - EJEMPLOS DE NOTICIAS           ║
╚══════════════════════════════════════════════════════════╝
""")
    
    print(f"📰 Noticia 1: {noticia_1.get('title', 'N/A')[:60]}...")
    print(f"📰 Noticia 2: {noticia_2.get('title', 'N/A')[:60]}...")
    print()
    
    # Crear handlers
    handler_1 = create_handler(noticia_1, 1)
    handler_2 = create_handler(noticia_2, 2)
    
    # Iniciar servidores en threads separados
    thread_1 = threading.Thread(target=start_server, args=(8001, handler_1, 1), daemon=True)
    thread_2 = threading.Thread(target=start_server, args=(8002, handler_2, 2), daemon=True)
    
    thread_1.start()
    thread_2.start()
    
    print()
    print("━" * 62)
    print("📡 SERVIDORES ACTIVOS")
    print("━" * 62)
    print("  🔗 Ejemplo 1: http://localhost:8001")
    print("  🔗 Ejemplo 2: http://localhost:8002")
    print()
    print("  📄 JSON 1:    http://localhost:8001/json")
    print("  📄 JSON 2:    http://localhost:8002/json")
    print("━" * 62)
    print()
    print("💡 Presiona Ctrl+C para detener los servidores")
    print()
    
    try:
        # Mantener el programa vivo
        thread_1.join()
        thread_2.join()
    except KeyboardInterrupt:
        print("\n\n👋 Servidores detenidos")
        sys.exit(0)


if __name__ == '__main__':
    main()
