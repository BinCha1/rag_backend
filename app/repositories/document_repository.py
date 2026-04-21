from app.db.session import SessionLocal
from app.db.models.document import Document


class DocumentRepository:
    """
    Stores document metadata in PostgreSQL.
    """

    def save(self, filename: str, chunk_count: int, document_id: str, file_type: str):

        db = SessionLocal()

        try:
            doc = Document(
                document_id=document_id,
                filename=filename,
                chunk_count=chunk_count,
                file_type=file_type,
            )

            db.add(doc)
            db.commit()
            db.refresh(doc)

            return doc.id

        finally:
            db.close()
