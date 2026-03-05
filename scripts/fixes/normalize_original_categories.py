#!/usr/bin/env python3
"""
Normalize category names in ARTICULOS_ORIGINALES table to uppercase.
"""
import subprocess
import json

# Category name mappings (various formats -> standard uppercase)
CATEGORY_MAPPING = {
    'nacional': 'NACIONAL',
    'Nacional': 'NACIONAL',
    'NACIONAL': 'NACIONAL',
    'internacional': 'INTERNACIONAL',
    'Internacional': 'INTERNACIONAL',
    'INTERNACIONAL': 'INTERNACIONAL',
    'politica': 'POLITICA',
    'Política': 'POLITICA',
    'politica': 'POLITICA',
    'POLITICA': 'POLITICA',
    'economia': 'ECONOMIA',
    'Economía': 'ECONOMIA',
    'economia': 'ECONOMIA',
    'ECONOMIA': 'ECONOMIA',
    'tecnologia': 'TECNOLOGIA',
    'Tecnología': 'TECNOLOGIA',
    'tecnologia': 'TECNOLOGIA',
    'TECNOLOGIA': 'TECNOLOGIA',
    'deportes': 'DEPORTES',
    'Deportes': 'DEPORTES',
    'DEPORTES': 'DEPORTES',
    'cultura': 'CULTURA',
    'Cultura': 'CULTURA',
    'CULTURA': 'CULTURA',
    'salud': 'SALUD',
    'Salud': 'SALUD',
    'SALUD': 'SALUD',
    'entretenimiento': 'ENTRETENIMIENTO',
    'Entretenimiento': 'ENTRETENIMIENTO',
    'ENTRETENIMIENTO': 'ENTRETENIMIENTO',
    'ciencia': 'CIENCIA',
    'Ciencia': 'CIENCIA',
    'CIENCIA': 'CIENCIA',
    'sociedad': 'SOCIEDAD',
    'Sociedad': 'SOCIEDAD',
    'SOCIEDAD': 'SOCIEDAD',
}

def get_original_articles():
    """Fetch all original articles from remote D1 database."""
    all_articles = []
    batch_size = 100
    offset = 0
    
    while True:
        cmd = [
            'wrangler', 'd1', 'execute', 'news_db', '--remote', '--json',
            '--command', f'''
                SELECT ID, CATEGORIA FROM ARTICULOS_ORIGINALES
                LIMIT {batch_size} OFFSET {offset}
            '''
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='/mnt/c/Users/soluc/cloudflare-news-project')
        
        if result.returncode != 0:
            print(f"Error fetching articles: {result.stderr}")
            break
        
        try:
            output = json.loads(result.stdout)
            batch = []
            
            if isinstance(output, list) and len(output) > 0:
                first_item = output[0]
                if isinstance(first_item, dict) and 'results' in first_item:
                    batch = first_item['results']
            elif isinstance(output, dict) and 'results' in output:
                batch = output['results']
            
            if not batch:
                break
                
            all_articles.extend(batch)
            print(f"  Fetched {len(all_articles)} original articles...")
            
            if len(batch) < batch_size:
                break
                
            offset += batch_size
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            break
    
    return all_articles

def normalize_categories_batch(updates):
    """Update multiple articles with normalized categories."""
    if not updates:
        return True, 0
    
    sql_parts = []
    for update in updates:
        article_id = update['id'].replace("'", "''")
        new_category = update['new'].replace("'", "''")
        sql_parts.append(f"UPDATE ARTICULOS_ORIGINALES SET CATEGORIA = '{new_category}' WHERE ID = '{article_id}';")
    
    sql_command = " ".join(sql_parts)
    
    cmd = [
        'wrangler', 'd1', 'execute', 'news_db', '--remote',
        '--command', sql_command
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd='/mnt/c/Users/soluc/cloudflare-news-project')
    return result.returncode == 0, len(updates)

def main():
    print("🔍 Fetching original articles from remote database...")
    articles = get_original_articles()
    
    if not articles:
        print("❌ No articles found")
        return
    
    print(f"📊 Found {len(articles)} original articles")
    
    # Find articles needing normalization
    updates_needed = []
    category_counts = {}
    
    for article in articles:
        article_id = article.get('ID', '')
        current_category = article.get('CATEGORIA', '')
        
        # Normalize to uppercase
        new_category = CATEGORY_MAPPING.get(current_category, current_category.upper())
        
        if new_category != current_category:
            updates_needed.append({
                'id': article_id,
                'current': current_category,
                'new': new_category
            })
        
        category_counts[new_category] = category_counts.get(new_category, 0) + 1
    
    print(f"\n📈 Category distribution after normalization:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {cat}: {count} articles")
    
    print(f"\n🔄 {len(updates_needed)} articles need category normalization")
    
    if updates_needed:
        print("\n⚡ Starting normalization in batches...")
        batch_size = 20
        total_updated = 0
        
        for i in range(0, len(updates_needed), batch_size):
            batch = updates_needed[i:i+batch_size]
            success, count = normalize_categories_batch(batch)
            
            if success:
                total_updated += count
                print(f"  ✓ Batch {i//batch_size + 1}: Normalized {count} articles (total: {total_updated}/{len(updates_needed)})")
            else:
                print(f"  ❌ Batch {i//batch_size + 1}: Failed to update")
        
        print(f"\n✅ Completed! {total_updated} articles normalized successfully")
        
        # Show sample changes
        print("\n📋 Sample changes (first 10):")
        for update in updates_needed[:10]:
            print(f"  {update['current']} → {update['new']}")

if __name__ == '__main__':
    main()
