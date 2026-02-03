from datetime import datetime

from flask import Flask, jsonify, render_template, request
from sqlalchemy import func

from src.database import SessionLocal
from src.models import Account, Article, Campaign, DistributionTask, Publisher

app = Flask(__name__)
app.config["SECRET_KEY"] = "meta-scale-secret-key-change-in-production"


@app.route("/")
def dashboard():
    """Dashboard principal"""
    session = SessionLocal()

    # Stats generales
    total_campaigns = session.query(Campaign).count()
    active_campaigns = session.query(Campaign).filter_by(status="active").count()

    # Artículos hoy
    today = datetime.utcnow().date()
    articles_today = (
        session.query(Article).filter(func.date(Article.ingested_at) == today).count()
    )

    # Tasks pendientes
    pending_tasks = session.query(DistributionTask).filter_by(status="pending").count()

    # Campaigns activas
    campaigns = session.query(Campaign).filter_by(status="active").all()

    session.close()

    return render_template(
        "dashboard.html",
        total_campaigns=total_campaigns,
        active_campaigns=active_campaigns,
        articles_today=articles_today,
        pending_tasks=pending_tasks,
        campaigns=campaigns,
    )


@app.route("/api/campaign/<campaign_id>")
def get_campaign(campaign_id):
    """API: detalles de campaña"""
    session = SessionLocal()
    campaign = session.query(Campaign).filter_by(id=campaign_id).first()

    if not campaign:
        return jsonify({"error": "Campaign not found"}), 404

    # Stats de la campaña
    total_articles = session.query(Article).filter_by(campaign_id=campaign_id).count()
    total_accounts = session.query(Account).filter_by(campaign_id=campaign_id).count()
    pending_tasks = (
        session.query(DistributionTask)
        .filter_by(campaign_id=campaign_id, status="pending")
        .count()
    )

    session.close()

    return jsonify(
        {
            "id": campaign.id,
            "name": campaign.name,
            "status": campaign.status,
            "fatigue_score": campaign.fatigue_score,
            "roi": campaign.roi_vs_baseline,
            "network_dependency": campaign.network_dependency,
            "stats": {
                "articles": total_articles,
                "accounts": total_accounts,
                "pending_tasks": pending_tasks,
            },
        }
    )


@app.route("/api/tasks")
def get_tasks():
    """API: tasks pendientes de aprobación"""
    session = SessionLocal()

    tasks = (
        session.query(DistributionTask)
        .filter_by(status="pending")
        .order_by(DistributionTask.matching_score.desc())
        .limit(50)
        .all()
    )

    result = []
    for task in tasks:
        article = session.query(Article).filter_by(id=task.article_id).first()
        account = session.query(Account).filter_by(id=task.account_id).first()

        result.append(
            {
                "id": task.id,
                "article_title": article.title if article else "N/A",
                "account_name": account.account_name if account else "N/A",
                "platform": account.platform if account else "N/A",
                "matching_score": task.matching_score,
                "created_at": task.created_at.isoformat(),
            }
        )

    session.close()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
