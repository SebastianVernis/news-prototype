import sys

sys.path.append("../..")
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from src.database import SessionLocal
from src.models import Article, Campaign, Publisher

load_dotenv()


def ingest_newsapi(campaign_id, publisher_id, api_key=None):
    """
    Adaptación de tu newsapi.py existente para guardar en PostgreSQL
    """
    session = SessionLocal()

    if not api_key:
        api_key = os.getenv("NEWSAPI_KEY")

    # Obtener publisher info
    publisher = session.query(Publisher).filter_by(id=publisher_id).first()
    if not publisher:
        print(f"❌ Publisher {publisher_id} not found")
        return

    # Fetch desde NewsAPI (TU CÓDIGO EXISTENTE)
    url = "https://newsapi.org/v2/everything"
    params = {
        "apiKey": api_key,
        "sources": publisher.page_name,  # Ejemplo: 'bbc-news'
        "pageSize": 20,
        "language": "en",
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        print(f"❌ API Error: {data.get('message')}")
        return

    articles = data.get("articles", [])
    saved_count = 0

    for article_data in articles:
        # Verificar si ya existe
        existing = session.query(Article).filter_by(url=article_data["url"]).first()
        if existing:
            continue

        # NUEVO: Crear registro en PostgreSQL
        article = Article(
            campaign_id=campaign_id,
            publisher_id=publisher_id,
            title=article_data.get("title", ""),
            content=article_data.get("content", ""),
            url=article_data.get("url", ""),
            analysis={
                "sentiment": "neutral",  # Temporal, después Gemini
                "urgency": "routine",
                "trending_score": 50,
            },
            ingested_at=datetime.utcnow(),
            processed=False,
        )

        session.add(article)
        saved_count += 1

    session.commit()
    session.close()

    print(f"✅ Ingested {saved_count} new articles from {publisher.page_name}")
    return saved_count


if __name__ == "__main__":
    # Test con campaign y publisher de ejemplo
    session = SessionLocal()

    # Crear campaign de prueba
    campaign = Campaign(name="Test Campaign S1", status="active")
    session.add(campaign)
    session.commit()

    # Crear publisher de prueba
    publisher = Publisher(
        campaign_id=campaign.id,
        page_name="bbc-news",
        rss_feed_url="http://feeds.bbci.co.uk/news/rss.xml",
        category="general",
    )
    session.add(publisher)
    session.commit()

    session.close()

    print(f"Campaign ID: {campaign.id}")
    print(f"Publisher ID: {publisher.id}")

    # Ingerir artículos
    ingest_newsapi(campaign.id, publisher.id)
