#!/usr/bin/env python3
"""
Script para limpiar contenido corrupto de artículos en la base de datos D1.
Elimina:
- Google Tag Manager scripts
- CSS variables corruptas
- Caracteres especiales ()
- HTML entities escapadas

Uso:
  python3 clean_articles_db.py

Requiere:
  - wrangler CLI instalado
"""

import subprocess
import json
import re
import html

def run_wrangler_query(query):
    """Ejecuta una query en D1 y retorna los resultados"""
    cmd = f'wrangler d1 execute news_db --command "{query}" --remote --json'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except:
        return None

def clean_text(text):
    """Limpia texto corrupto"""
    if not text:
        return text
    
    # 1. Decodificar HTML entities
    text = html.unescape(text)
    
    # 2. Eliminar Google Tag Manager scripts
    text = re.sub(r'googletag\.cmd\.push\([^)]*\);', '', text)
    text = re.sub(r'googletag\.display\([^)]*\);', '', text)
    text = re.sub(r'googletag\.display\([\'"][^\'"]*[\'"]\);', '', text)
    
    # 3. Eliminar CSS variables corruptas
    text = re.sub(r'\s*--[\w-]+:\s*[^;]*;\s*', '', text)
    
    # 4. Eliminar caracteres especiales ()
    text = text.replace('', '')
    text = text.replace('', '')
    
    # 5. Eliminar bloques CSS corruptos
    text = re.sub(r'\{[^}]*--[\w-]+:[^}]*\}', '', text)
    
    # 6. Eliminar caracteres de control
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    
    # 7. Limpieza final de espacios
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_articles_from_table(table, id_col, content_col):
    """Obtiene artículos de una tabla"""
    query = f"SELECT {id_col}, {content_col} as content FROM {table} WHERE {content_col} LIKE '%googletag%' OR {content_col} LIKE '%div-gpt-ad%' OR {content_col} LIKE '%%' LIMIT 100"
    result = run_wrangler_query(query)
    if result and 'results' in result:
        return result['results']
    return []

def update_article(table, id_col, article_id, clean_content):
    """Actualiza un artículo con contenido limpio"""
    # Escapar comillas simples
    clean_content_escaped = clean_content.replace("'", "''")
    query = f"UPDATE {table} SET CONTENIDO = '{clean_content_escaped}' WHERE {id_col} = '{article_id}'"
    result = run_wrangler_query(query)
    return result is not None

def main():
    print("="*60)
    print("Limpieza de Contenido Corrupto - Artículos D1")
    print("="*60)
    print()
    
    tables = [
        ('ARTICULOS_PARAFRASEADOS', 'ID'),
        ('ARTICULOS_CMS', 'ID')
    ]
    
    total_cleaned = 0
    total_errors = 0
    
    for table, id_col in tables:
        print(f"Procesando tabla: {table}")
        print("-" * 40)
        
        articles = get_articles_from_table(table, id_col, 'CONTENIDO')
        
        if not articles:
            print(f"  No se encontraron artículos corruptos en {table}")
            print()
            continue
        
        print(f"  Encontrados {len(articles)} artículos con contenido corrupto")
        
        cleaned_count = 0
        error_count = 0
        
        for article in articles:
            article_id = article[id_col]
            content = article['content']
            
            # Limpiar contenido
            clean_content = clean_text(content)
            
            # Actualizar en DB
            if update_article(table, id_col, article_id, clean_content):
                cleaned_count += 1
                print(f"  ✓ Limpiado artículo {article_id[:8]}...")
            else:
                error_count += 1
                print(f"  ✗ Error al limpiar artículo {article_id[:8]}...")
        
        print(f"  Resultado: {cleaned_count} limpiados, {error_count} errores")
        print()
        
        total_cleaned += cleaned_count
        total_errors += error_count
    
    print("="*60)
    print(f"Resumen Final")
    print("="*60)
    print(f"Total limpiados: {total_cleaned}")
    print(f"Total errores: {total_errors}")
    print()
    
    if total_errors == 0:
        print("✅ ¡Limpieza completada exitosamente!")
    else:
        print(f"⚠️  Limpieza completada con {total_errors} errores")
    
    print()
    print("Para verificar el resultado:")
    print("  wrangler d1 execute news_db --command \"SELECT COUNT(*) FROM ARTICULOS_PARAFRASEADOS WHERE CONTENIDO LIKE '%googletag%'\" --remote")
    print()

if __name__ == "__main__":
    main()
