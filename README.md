# Document Ingestion API with RAG Capabilities

A FastAPI-based backend service for document ingestion with RAG (Retrieval-Augmented Generation) capabilities. Supports PDF and TXT file processing with multiple chunking strategies.

## Prerequisites

- Python 3.10+
- PostgreSQL (local or remote)
- Qdrant vector database (for embeddings storage)

## Installation

### 1. Clone and Setup Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -e .
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/rag_backend

# Qdrant Vector DB
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=documents

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## Running the Server

### Option 1: Direct Run

```bash
uvicorn app.main:app --reload
```

### Option 2: With Manual DB Init (if needed)

```bash
# First-time setup
python setup_db.py

# Then run the server
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Health Check

- **GET** `/` - Server status

### Document Ingestion

- **POST** `/api/v1/ingest` - Ingest a document
  - **Parameters:**
    - `file` (UploadFile): PDF or TXT file
    - `chunk_strategy` (str): `'recursive'` or `'sentence'`
  - **Returns:** Ingestion status and metadata

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── main.py                 # FastAPI entry point
├── api/
│   └── ingestion.py        # Ingestion endpoints
├── core/
│   ├── config.py           # Configuration
│   └── logger.py           # Logging setup
├── db/
│   ├── init_db.py          # Database initialization
│   ├── session.py          # SQLAlchemy session setup
│   └── models/
│       └── document.py     # Document ORM model
├── repositories/
│   └── document_repository.py  # Database operations
├── schemas/
│   └── ingestion.py        # Request/response schemas
└── services/
    └── ingestion/
        ├── chunker.py      # Text chunking strategies
        ├── embedder.py     # Embedding generation
        ├── parser.py       # File parsing
        ├── vector_store.py # Qdrant interactions
        └── ingestion_service.py  # Orchestration


```
