from fastapi import FastAPI
from app.api.ingestion import router as ingestion_router
from app.db.init_db import init_db

"""
Main entry point of the Document Ingestion Service.
"""

app = FastAPI(title="Document Ingestion API")


# Create DB tables on startup
@app.on_event("startup")
def startup():
    init_db()


# Routes
app.include_router(ingestion_router, prefix="/api/v1", tags=["Ingestion"])


@app.get("/")
def root():
    return {"message": "Document Ingestion Service is running"}
