from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.session import Base


class Document(Base):
    """
    Stores only document-level metadata.
    No page/chunk duplication here.
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    # unique id used across vector DB + API
    document_id = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    chunk_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
