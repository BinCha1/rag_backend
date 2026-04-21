from fastapi import APIRouter, UploadFile, File, Form
from app.services.ingestion.ingestion_service import IngestionService

router = APIRouter()
service = IngestionService()


@router.post("/ingest")
async def ingest(file: UploadFile = File(...), chunk_strategy: str = Form(...)):
    """
    Ingestion API endpoint.

    Args:
        file (UploadFile): PDF or TXT file
        chunk_strategy (str): 'recursive' or 'sentence'

    Returns:
        dict: ingestion status and metadata
    """
    return await service.ingest(file, chunk_strategy)
