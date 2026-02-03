import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/rotating_media")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Crear todas las tablas"""
    Base.metadata.create_all(engine)
    print("✅ Database tables created")


def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
