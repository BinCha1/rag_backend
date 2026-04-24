from fastapi import FastAPI
from app.api.ingestion import router as ingestion_router
from app.api.chat import router as chat_router
from app.db.init_db import init_db
from app.api.core.logger import setup_logging, get_logger

"""
Main entry point of the Document Ingestion Service.
"""

# Configure logging
setup_logging()
logger = get_logger("Main")
app = FastAPI(title="Document Ingestion API")


# Create DB tables on startup
@app.on_event("startup")
def startup():
    init_db()


# Routes
app.include_router(ingestion_router, prefix="/api/v1", tags=["Ingestion"])
app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])


@app.get("/")
def root():
    return {"message": "Document Ingestion Service is running"}
