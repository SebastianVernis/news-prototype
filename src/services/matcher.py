import sys
from datetime import datetime

sys.path.append("../..")
from src.database import SessionLocal
from src.models import Account, Article, DistributionTask


def calculate_matching_score(article, account):
    """
    Calcula score de compatibilidad entre artículo y cuenta (0-100)

    Factores:
    - Interest match (40 puntos)
    - Urgency boost (20 puntos)
    - Platform compatibility (20 puntos)
    - Account fatigue penalty (20 puntos)
    """
    score = 50  # Base score

    # 1. Interest matching
    article_category = article.analysis.get("category", "").lower()
    account_interests = [i.lower() for i in account.profile.get("interests", [])]

    if article_category in account_interests:
        score += 30
    elif any(interest in article_category for interest in account_interests):
        score += 15

    # 2. Urgency boost
    urgency = article.analysis.get("urgency", "routine")
    if urgency == "breaking":
        score += 20
    elif urgency == "trending":
        score += 10

    # 3. Platform compatibility
    platform = account.platform
    if platform == "x" and len(article.title) < 200:
        score += 10  # Twitter-friendly length
    elif platform == "facebook":
        score += 10  # Facebook acepta todo

    # 4. Account fatigue penalty
    fatigue = account.fatigue_score or 20
    if fatigue > 70:
        score -= 20
    elif fatigue > 50:
        score -= 10

    return min(100, max(0, score))


def match_articles_to_accounts(campaign_id, min_score=60):
    """
    Matching de artículos no procesados con cuentas activas
    """
    session = SessionLocal()

    # Obtener artículos sin procesar
    articles = (
        session.query(Article).filter_by(campaign_id=campaign_id, processed=False).all()
    )

    # Obtener cuentas listas
    accounts = (
        session.query(Account)
        .filter_by(campaign_id=campaign_id, warmup_status="ready")
        .all()
    )

    tasks_created = 0
    print(f" Matching {len(articles)} articles with {len(accounts)} accounts...")

    for article in articles:
        matches = []

        for account in accounts:
            score = calculate_matching_score(article, account)
            if score >= min_score:
                matches.append({"account": account, "score": score})

        # Ordenar por score (mayor primero)
        matches.sort(key=lambda x: x["score"], reverse=True)

        # Crear tasks para los mejores matches (top 5)
        for match in matches[:5]:
            task = DistributionTask(
                campaign_id=campaign_id,
                article_id=article.id,
                account_id=match["account"].id,
                matching_score=match["score"],
                status="pending",
            )

            session.add(task)
            tasks_created += 1

        # Marcar artículo como procesado
        article.processed = True

    session.commit()
    session.close()

    print(f"✅ Created {tasks_created} distribution tasks")
    return tasks_created


if __name__ == "__main__":
    session = SessionLocal()
    from src.models import Campaign

    campaign = session.query(Campaign).first()
    session.close()

    if campaign:
        match_articles_to_accounts(campaign.id)
    else:
        print("❌ No campaign found")
