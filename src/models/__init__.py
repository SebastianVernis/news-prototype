from sqlalchemy import Column, String, Integer, DateTime, Float, JSON, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    status = Column(String(50), default='planning')  # planning | active | closed
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    fatigue_score = Column(Integer, default=20)
    network_dependency = Column(Float, default=0.0)
    roi_vs_baseline = Column(Float, default=1.66)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, nullable=False)
    page_name = Column(String(200))
    rss_feed_url = Column(String(500))
    category = Column(String(100))
    status = Column(String(50), default='active')
    metrics = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, nullable=False)
    platform = Column(String(50))  # facebook | instagram | x | linkedin | tiktok
    account_name = Column(String(200))
    prole = Column(JSON, default={})  # interests, activity_pattern, writing_style
    warmup_status = Column(String(50), default='warming')
    fatigue_score = Column(Integer, default=20)
    last_post_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Article(Base):
    __tablename__ = 'articles'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, nullable=False)
    publisher_id = Column(String, nullable=False)
    title = Column(String(500))
    content = Column(Text)
    url = Column(String(500))
    analysis = Column(JSON, default={})  # sentiment, urgency, trending_score, category
    ingested_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)

class DistributionTask(Base):
    __tablename__ = 'distribution_tasks'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, nullable=False)
    article_id = Column(String, nullable=False)
    account_id = Column(String, nullable=False)
    matching_score = Column(Integer)  # 0-100
    status = Column(String(50), default='pending')  # pending | approved | published | rejected
    generated_copies = Column(JSON, default=[])
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
