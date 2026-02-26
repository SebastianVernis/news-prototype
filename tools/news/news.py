import os
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()  # Carga .env

API_KEY = os.getenv('NEWSAPI_KEY')
BASE_URL = 'https://newsapi.org/v2/everything'
HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'}

def fetch_news(query='política México', country='mx', language='es', page_size=20):
    params = {
        'q': query,
        'apiKey': API_KEY,
        'language': language,
        'sortBy': 'publishedAt',
        'pageSize': page_size
    }
    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Error API: {response.json()}")
    return response.json()['articles']

def get_full_text(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        # Remueve scripts y navega a párrafos principales (ajusta selectores por sitio)
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        text = ' '.join(p.get_text(strip=True) for p in soup.find_all('p')[:10])  # Primeros 10 párrafos
        return text[:5000]  # Límite razonable
    except:
        return "Texto no disponible"

if __name__ == '__main__':
    # Uso principal
    articles = fetch_news()
    enhanced_articles = []
    for art in articles:
        full_text = get_full_text(art['url']) if art['url'] else ''
        enhanced = {**art, 'full_text': full_text}
        enhanced_articles.append(enhanced)

    # Guardar
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    with open(f'noticias_mx_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(enhanced_articles, f, ensure_ascii=False, indent=2)

    df = pd.DataFrame(enhanced_articles)
    df.to_csv(f'noticias_mx_{timestamp}.csv', index=False, encoding='utf-8')

    print(f"Descargados {len(articles)} artículos guardados en JSON/CSV.")
