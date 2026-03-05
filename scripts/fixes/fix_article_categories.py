#!/usr/bin/env python3
"""
Reorganize articles into proper categories based on content analysis.
Reads from remote D1 database and updates categories.
"""
import subprocess
import json
import re

# Categories available in the database
CATEGORIES = {
    'NACIONAL': {
        'keywords': ['méxico', 'mexico', 'nacional', 'local', 'estatal', 'regional', 'cdmx', 'ciudad de méxico'],
        'priority': 5
    },
    'INTERNACIONAL': {
        'keywords': ['internacional', 'eeuu', 'estados unidos', 'europa', 'china', 'rusia', 'trump', 'biden', 'putin', 'ucrania', 'israel', 'palestina', 'mundo', 'global', 'latinoamérica', 'america latina'],
        'priority': 1
    },
    'POLITICA': {
        'keywords': ['política', 'politica', 'presidente', 'gobierno', 'congreso', 'senado', 'diputado', 'elección', 'elecciones', 'voto', 'partido', 'morena', 'pan', 'pri', 'sheinbaum', 'amlo', 'garcía harfuch'],
        'priority': 2
    },
    'ECONOMIA': {
        'keywords': ['economía', 'economia', 'finanzas', 'peso', 'dólar', 'dolar', 'inflación', 'inflacion', 'pib', 'banco', 'banxico', 'bolsa', 'mercado', 'empresa', 'negocio', 'inversión', 'inversion', 'salario', 'empleo'],
        'priority': 3
    },
    'TECNOLOGIA': {
        'keywords': ['tecnología', 'tecnologia', 'ia', 'inteligencia artificial', 'digital', 'internet', 'app', 'aplicación', 'smartphone', 'celular', 'computadora', 'software', 'hardware', '5g', 'redes sociales', 'tiktok', 'facebook', 'google', 'apple', 'tesla', 'auto eléctrico', 'ev'],
        'priority': 4
    },
    'DEPORTES': {
        'keywords': ['deporte', 'deportes', 'fútbol', 'futbol', 'liga', 'mundial', 'olimpíadas', 'olimpiadas', 'nba', 'mlb', 'box', 'boxeo', 'fórmula 1', 'formula 1', 'tenis', 'gol', 'equipo', 'atleta', 'medalla'],
        'priority': 6
    },
    'CULTURA': {
        'keywords': ['cultura', 'arte', 'música', 'musica', 'cine', 'teatro', 'libro', 'literatura', 'concierto', 'festival', 'museo', 'exposición', 'pintura', 'artista', 'actor', 'actriz', 'canción', 'cancion', 'baile', 'danza'],
        'priority': 7
    },
    'SALUD': {
        'keywords': ['salud', 'médico', 'medico', 'hospital', 'clínica', 'clinica', 'enfermedad', 'vacuna', 'medicina', 'tratamiento', 'doctor', 'paciente', 'síntoma', 'sintoma', 'epidemia', 'pandemia', 'covid', 'cáncer', 'cancer', 'terapia'],
        'priority': 8
    },
    'ENTRETENIMIENTO': {
        'keywords': ['entretenimiento', 'espectáculos', 'famoso', 'celebridad', 'tv', 'televisión', 'television', 'serie', 'streaming', 'netflix', 'disney', 'hbo', 'premio', 'oscar', 'grammy', 'galardón'],
        'priority': 9
    },
    'CIENCIA': {
        'keywords': ['ciencia', 'científico', 'cientifica', 'investigación', 'investigacion', 'descubrimiento', 'nasa', 'espacio', 'astronomía', 'astronomia', 'física', 'fisica', 'química', 'quimica', 'biología', 'biologia', 'universo', 'planeta', 'cohete'],
        'priority': 10
    },
    'SOCIEDAD': {
        'keywords': ['sociedad', 'social', 'comunidad', 'familia', 'educación', 'educacion', 'escuela', 'universidad', 'trabajo', 'vivienda', 'transporte', 'seguridad', 'delito', 'narcotráfico', 'narco', 'cartel', 'violencia', 'migración', 'migracion'],
        'priority': 11
    }
}

def get_articles():
    """Fetch all articles from remote D1 database in batches."""
    all_articles = []
    batch_size = 100
    offset = 0
    
    while True:
        cmd = [
            'wrangler', 'd1', 'execute', 'news_db', '--remote', '--json',
            '--command', f'''
                SELECT 
                    ID, 
                    TITULO_PARAFRASEADO, 
                    DESCRIPCION_PARAFRASEADA, 
                    CONTENIDO, 
                    CATEGORIA 
                FROM ARTICULOS_PARAFRASEADOS
                LIMIT {batch_size} OFFSET {offset}
            '''
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='/mnt/c/Users/soluc/cloudflare-news-project')
        
        if result.returncode != 0:
            print(f"Error fetching articles: {result.stderr}")
            break
        
        try:
            # Parse the JSON output from wrangler
            output = json.loads(result.stdout)
            batch = []
            
            # Handle the nested structure: [{results: [...]}]
            if isinstance(output, list) and len(output) > 0:
                first_item = output[0]
                if isinstance(first_item, dict) and 'results' in first_item:
                    batch = first_item['results']
            elif isinstance(output, dict) and 'results' in output:
                batch = output['results']
            
            if not batch:
                break
                
            all_articles.extend(batch)
            print(f"  Fetched {len(all_articles)} articles...")
            
            if len(batch) < batch_size:
                break
                
            offset += batch_size
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON output: {e}")
            print(f"Raw output: {result.stdout[:500]}")
            break
    
    return all_articles

def analyze_category(title, description, content):
    """Analyze article content and determine the best category."""
    text = f"{title or ''} {description or ''} {content or ''}".lower()
    
    scores = {}
    
    for category, config in CATEGORIES.items():
        score = 0
        for keyword in config['keywords']:
            if keyword.lower() in text:
                score += 1
        
        if score > 0:
            # Adjust score by priority (lower priority number = higher priority)
            adjusted_score = score + (15 - config['priority']) * 0.1
            scores[category] = adjusted_score
    
    if not scores:
        return 'NACIONAL'  # Default category
    
    # Return category with highest score
    return max(scores, key=scores.get)

def update_articles_batch(updates):
    """Update multiple articles in a single batch."""
    if not updates:
        return True, 0
    
    # Build a single SQL statement with multiple updates
    sql_parts = []
    for update in updates:
        article_id = update['id'].replace("'", "''")
        new_category = update['new'].replace("'", "''")
        sql_parts.append(f"UPDATE ARTICULOS_PARAFRASEADOS SET CATEGORIA = '{new_category}' WHERE ID = '{article_id}';")
    
    sql_command = " ".join(sql_parts)
    
    cmd = [
        'wrangler', 'd1', 'execute', 'news_db', '--remote',
        '--command', sql_command
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd='/mnt/c/Users/soluc/cloudflare-news-project')
    return result.returncode == 0, len(updates)

def main():
    print("🔍 Fetching articles from remote database...")
    articles = get_articles()
    
    if not articles:
        print("❌ No articles found or error fetching data")
        return
    
    print(f"📊 Found {len(articles)} articles to analyze")
    
    # Analyze and categorize
    updates_needed = []
    category_counts = {cat: 0 for cat in CATEGORIES.keys()}
    
    for i, article in enumerate(articles):
        article_id = article.get('ID', '')
        current_category = article.get('CATEGORIA', 'NACIONAL')
        title = article.get('TITULO_PARAFRASEADO', '')
        description = article.get('DESCRIPCION_PARAFRASEADA', '')
        content = article.get('CONTENIDO', '')
        
        # Analyze and get new category
        new_category = analyze_category(title, description, content)
        
        if new_category != current_category:
            updates_needed.append({
                'id': article_id,
                'current': current_category,
                'new': new_category,
                'title': title[:50]
            })
        
        category_counts[new_category] = category_counts.get(new_category, 0) + 1
        
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(articles)} articles...")
    
    print(f"\n📈 Category distribution after reorganization:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {cat}: {count} articles")
    
    print(f"\n🔄 {len(updates_needed)} articles need category updates")
    
    if updates_needed:
        print("\n⚡ Starting category updates in batches...")
        batch_size = 20
        total_updated = 0
        
        for i in range(0, len(updates_needed), batch_size):
            batch = updates_needed[i:i+batch_size]
            success, count = update_articles_batch(batch)
            
            if success:
                total_updated += count
                print(f"  ✓ Batch {i//batch_size + 1}: Updated {count} articles (total: {total_updated}/{len(updates_needed)})")
            else:
                print(f"  ❌ Batch {i//batch_size + 1}: Failed to update")
        
        print(f"\n✅ Completed! {total_updated} articles recategorized successfully")
    
    # Show sample changes
    if updates_needed:
        print("\n📋 Sample changes (first 10):")
        for update in updates_needed[:10]:
            print(f"  • \"{update['title']}...\"")
            print(f"    {update['current']} → {update['new']}")

if __name__ == '__main__':
    main()
