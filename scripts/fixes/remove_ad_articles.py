#!/usr/bin/env python3
"""
Eliminar artículos con código de publicidad/ads (googletag, dailymotion, etc.)
"""
import subprocess
import json
import re

# Patrones que indican contenido de publicidad/ads no deseado
AD_PATTERNS = [
    r'googletag\.cmd\.push',
    r'googletag\.display',
    r'div-gpt-ad',
    r'#dailymotion-pip',
    r'googletag\.cmd',
    r'googletag\.display',
    r'googletag\.defineSlot',
    r'googletag\.pubads',
    r'googletag\.enableServices',
    r'gpt-ad',
    r'google_ads_iframe',
    r'/gpt/js/gpt\.js',
    r'/pagead/js/adsbygoogle\.js',
    r'adsbygoogle\.push',
    r'googlesyndication',
    r'doubleclick\.net',
    r'googletagservices',
]

def get_articles():
    """Fetch all articles from remote D1 database."""
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
                    CONTENIDO,
                    DESCRIPCION_PARAFRASEADA
                FROM ARTICULOS_PARAFRASEADOS
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
            print(f"  Fetched {len(all_articles)} articles...")
            
            if len(batch) < batch_size:
                break
                
            offset += batch_size
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            break
    
    return all_articles

def has_ad_content(content, description):
    """Check if content contains advertising code."""
    text = f"{content or ''} {description or ''}"
    
    for pattern in AD_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True, pattern
    
    return False, None

def delete_articles_batch(article_ids):
    """Delete multiple articles in a single batch."""
    if not article_ids:
        return True, 0
    
    # Also delete related original articles if they exist
    sql_parts = []
    
    for article_id in article_ids:
        safe_id = article_id.replace("'", "''")
        # Delete from paraphrased articles
        sql_parts.append(f"DELETE FROM ARTICULOS_PARAFRASEADOS WHERE ID = '{safe_id}';")
    
    sql_command = " ".join(sql_parts)
    
    cmd = [
        'wrangler', 'd1', 'execute', 'news_db', '--remote',
        '--command', sql_command
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd='/mnt/c/Users/soluc/cloudflare-news-project')
    return result.returncode == 0, len(article_ids)

def main():
    print("🔍 Fetching articles from remote database...")
    articles = get_articles()
    
    if not articles:
        print("❌ No articles found")
        return
    
    print(f"📊 Found {len(articles)} articles to analyze")
    
    # Find articles with ad content
    articles_to_delete = []
    
    for i, article in enumerate(articles):
        article_id = article.get('ID', '')
        title = article.get('TITULO_PARAFRASEADO', '')[:50]
        content = article.get('CONTENIDO', '')
        description = article.get('DESCRIPCION_PARAFRASEADA', '')
        
        has_ad, pattern = has_ad_content(content, description)
        
        if has_ad:
            articles_to_delete.append({
                'id': article_id,
                'title': title,
                'pattern': pattern
            })
        
        if (i + 1) % 50 == 0:
            print(f"  Analyzed {i + 1}/{len(articles)} articles...")
    
    print(f"\n⚠️  Found {len(articles_to_delete)} articles with advertising content")
    
    if articles_to_delete:
        print("\n📋 Articles to delete (showing first 20):")
        for i, article in enumerate(articles_to_delete[:20]):
            print(f"  {i+1}. \"{article['title']}...\"")
            print(f"     Pattern: {article['pattern']}")
        
        if len(articles_to_delete) > 20:
            print(f"  ... and {len(articles_to_delete) - 20} more")
        
        # Confirm deletion
        print(f"\n⚠️  WARNING: This will permanently delete {len(articles_to_delete)} articles!")
        response = input("Continue? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("❌ Operation cancelled")
            return
        
        print(f"\n🗑️  Deleting articles in batches...")
        batch_size = 20
        total_deleted = 0
        
        for i in range(0, len(articles_to_delete), batch_size):
            batch = articles_to_delete[i:i+batch_size]
            batch_ids = [a['id'] for a in batch]
            success, count = delete_articles_batch(batch_ids)
            
            if success:
                total_deleted += count
                print(f"  ✓ Batch {i//batch_size + 1}: Deleted {count} articles (total: {total_deleted}/{len(articles_to_delete)})")
            else:
                print(f"  ❌ Batch {i//batch_size + 1}: Failed to delete")
        
        print(f"\n✅ Completed! {total_deleted} articles deleted successfully")
        
        # Show pattern summary
        pattern_counts = {}
        for article in articles_to_delete:
            pattern = article['pattern']
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        print("\n📊 Deletion summary by pattern:")
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {pattern}: {count} articles")
    else:
        print("✅ No articles with advertising content found")

if __name__ == '__main__':
    main()
