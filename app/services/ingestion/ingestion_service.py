import uuid
import os
from app.services.ingestion.parser import DocumentParser
from app.services.ingestion.chunker import TextChunker
from app.services.ingestion.embedder import Embedder
from app.services.ingestion.vector_store import VectorStore
from app.repositories.document_repository import DocumentRepository


class IngestionService:
    """
    Orchestrates full ingestion pipeline:
    parse → chunk → embed → store
    """

    def __init__(self):
        self.parser = DocumentParser()
        self.chunker = TextChunker()
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.repo = DocumentRepository()

    async def ingest(self, file, chunk_strategy: str):
        """
        Full ingestion pipeline.

        Args:
            file: uploaded file
            chunk_strategy: recursive | sentence

        Returns:
            dict
        """

        # Generate unique document ID
        document_id = str(uuid.uuid4())

        # Extract file type from extension
        _, file_type = os.path.splitext(file.filename)
        file_type = file_type.lstrip(".")  # Remove the dot (e.g., "pdf" not ".pdf")

        # 1. Parse document
        text = await self.parser.extract_text(file)

        # 2. Chunk text
        chunks = self.chunker.chunk(text, chunk_strategy)

        # 3. Generate embeddings
        vectors = self.embedder.embed(chunks)

        # 4. Store vectors in Qdrant
        self.vector_store.store(chunks, vectors, file.filename, document_id, file_type)

        # 5. Save metadata (PostgreSQL)
        self.repo.save(file.filename, len(chunks), document_id, file_type)

        return {
            "message": "Document ingested successfully",
            "document_id": document_id,
            "chunks_created": len(chunks),
        }
