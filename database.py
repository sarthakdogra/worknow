from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base
import os
from config import settings
#  Your PostgreSQL connection URL


#  Create Engine (connects Python ↔ PostgreSQL)
engine = create_engine(settings.DATABASE_URL)

#  SessionLocal (used for DB operations in FastAPI routes)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

#  Base class for all models (tables)
Base = declarative_base()


#  Dependency (VERY IMPORTANT for FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()