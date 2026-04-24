# app/services/rag/retriever.py

from typing import List
from app.api.core.logger import get_logger
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

logger = get_logger(__name__)


class Retriever:
    """Retrieves relevant document chunks from vector database."""

    def __init__(self) -> None:
        self.model: SentenceTransformer = SentenceTransformer("all-MiniLM-L6-v2")
        self.client: QdrantClient = QdrantClient(host="localhost", port=6333)
        self.collection: str = "documents"

    def get_relevant_chunks(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve relevant text chunks from vector store.

        Args:
            query: Search query string
            top_k: Number of top results to return

        Returns:
            List of relevant text chunks
        """
        # Convert query to vector
        query_vector: List[float] = self.model.encode(query).tolist()

        # Search in Qdrant
        response = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=top_k,
            with_payload=True,
        )

        # Extract text from result payload
        chunks: List[str] = [point.payload["text"] for point in response.points]
        logger.info(f"Retrieved {len(chunks)} chunks")

        return chunks
