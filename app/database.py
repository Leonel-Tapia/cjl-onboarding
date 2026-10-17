import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Leer directamente la variable de entorno (funciona en local y en Railway)
DATABASE_URL = os.getenv("DATABASE_URL")

# Si por alguna razon viene vacia en local, usar la de desarrollo
if not DATABASE_URL:
    DATABASE_URL = "postgresql+psycopg2://postgres:leotap@localhost:5432/cjl_onboarding"

# Fix para Railway (que a veces da la URL con postgres:// en lugar de postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
