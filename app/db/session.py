from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.api.core.config import DATABASE_URL

"""
PostgreSQL database session setup.
"""

DATABASE_URL = DATABASE_URL

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
