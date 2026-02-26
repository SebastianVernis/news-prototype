#!/usr/bin/env python3
"""
Script interactivo para descargar y seleccionar noticias.
Descarga los últimos 50 títulos de noticias y permite seleccionar cuáles conservar.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

import requests

# Configuración
# Usamos la API KEY encontrada en wrangler.toml por defecto si no está en el ambiente
API_KEY = os.getenv("NEWSAPI_KEY", "YOUR_NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_50_news(query="México"):
    """Descarga las últimas 50 noticias de NewsAPI"""
    params = {
        "q": query,
        "apiKey": API_KEY,
        "language": "es",
        "sortBy": "publishedAt",
        "pageSize": 50,
    }
    
    print(f"📥 Descargando las últimas 50 noticias para: '{query}'...")
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            print(f"❌ Error de API: {data.get('message')}")
            return []
            
        articles = data.get("articles", [])
        print(f"✅ Se encontraron {len(articles)} noticias.")
        return articles
    except Exception as e:
        print(f"❌ Error al conectar con NewsAPI: {e}")
        return []

def interactive_selection(articles):
    """Interfaz interactiva para seleccionar noticias"""
    selected = []
    total = len(articles)
    
    print("
" + "="*80)
    print("SELECCIÓN INTERACTIVA DE NOTICIAS")
    print("Instrucciones: presiona 's' para conservar, 'n' para descartar, 'q' para terminar.")
    print("="*80 + "
")
    
    for i, art in enumerate(articles):
        title = art.get("title", "Sin título")
        source = art.get("source", {}).get("name", "Fuente desconocida")
        date = art.get("publishedAt", "")[:10]
        
        print(f"[{i+1}/{total}] {date} | {source}")
        print(f"TITULO: {title}")
        print("-" * 40)
        
        while True:
            choice = input("¿Conservar noticia? (s/n/q): ").lower().strip()
            if choice == 's':
                # Guardar en formato simple: solo título y contenido/descripción
                content = art.get("content") or art.get("description") or ""
                # Limpiar el rastro de "[+xxx chars]" de NewsAPI si existe
                if " [" in content and content.endswith("]"):
                    content = content[:content.rfind(" [")]
                
                selected_item = {
                    "titulo": title,
                    "texto": content,
                    "fecha": date,
                    "fuente": source,
                    "url": art.get("url")
                }
                selected.append(selected_item)
                print("✅ Agregada.")
                break
            elif choice == 'n':
                print("❌ Descartada.")
                break
            elif choice == 'q':
                print("⏹️ Terminando selección...")
                return selected
            else:
                print("Opción no válida. Usa 's', 'n' o 'q'.")
        print()
        
    return selected

def save_to_json(data):
    """Guarda la selección en un archivo JSON"""
    if not data:
        print("⚠️ No se seleccionaron noticias para guardar.")
        return
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"seleccion_noticias_{timestamp}.json"
    
    # Intentar guardar en la carpeta data si existe
    output_path = Path("data") / filename
    if not output_path.parent.exists():
        output_path = Path(filename)
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"
🎉 ¡Hecho! Se guardaron {len(data)} noticias en: {output_path}")

if __name__ == "__main__":
    # Pedir query al usuario o usar default
    user_query = input("Ingresa tema de búsqueda [México]: ").strip() or "México"
    
    news = fetch_50_news(user_query)
    if news:
        final_selection = interactive_selection(news)
        save_to_json(final_selection)
    else:
        print("No se pudieron obtener noticias. Verifica tu conexión o API Key.")
