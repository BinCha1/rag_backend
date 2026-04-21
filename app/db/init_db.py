from app.db.session import engine, Base
from app.db.models.document import Document

"""
Creates all database tables.
"""


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    print(" Database tables initialized")
