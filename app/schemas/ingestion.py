from pydantic import BaseModel


class IngestionResponse(BaseModel):
    """
    Response schema for ingestion API
    """

    message: str
    document_id: int
    chunks_created: int
