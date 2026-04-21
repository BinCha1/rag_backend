import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from app.api.core.config import QDRANT_HOST, QDRANT_PORT


class VectorStore:
    """
    Handles storing document embeddings into Qdrant.
    """

    def __init__(self):
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        self.collection = "documents"

    def store(
        self,
        chunks: list[str],
        vectors: list[list[float]],
        filename: str,
        document_id: str,
        file_type: str,
    ):
        """
        Store chunk embeddings + metadata into Qdrant.
        """

        points = []

        for index, (chunk, vector) in enumerate(zip(chunks, vectors)):

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        #  core data
                        "text": chunk,
                        "document_id": document_id,
                        "chunk_index": index,
                        "filename": filename,
                        "file_type": file_type,
                    },
                )
            )

        self.client.upsert(collection_name=self.collection, points=points)
