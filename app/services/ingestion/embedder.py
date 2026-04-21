from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from app.api.core.config import EMBEDDING_MODEL


class Embedder:
    """
    Converts text chunks into vector embeddings.
    """

    def __init__(self):
        self.model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    def embed(self, chunks: list[str]) -> list[list[float]]:
        """
        Generate embeddings for text chunks.

        Args:
            chunks (list[str])

        Returns:
            list[list[float]]
        """

        vectors = self.model.embed_documents(chunks)
        return vectors
