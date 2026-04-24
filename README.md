# RAG-Backend

A FastAPI backend service combining **LLM-based intent routing**, **multi-turn conversational booking**, and **RAG (Retrieval-Augmented Generation)** for intelligent document search and question answering.

## Features

- **Intelligent Intent Routing** - LLM classifies user messages (booking vs question)
- **Multi-Turn Booking** - Guided appointment booking with Redis session state
- **RAG Pipeline** - Semantic document retrieval and LLM-generated answers
- **Vector Search** - Qdrant-based similarity search with all-MiniLM-L6-v2 embeddings
- **Flexible LLM Support** - Gemini, OpenAI, or Groq (configurable)
- **Session Management** - Redis for conversation state across turns
- **Persistent Storage** - PostgreSQL for booking records

## Prerequisites

- Python 3.10+
- PostgreSQL 12+
- Redis 6+
- Qdrant 1.0+
- LLM API key (Gemini/OpenAI/Groq)

## Installation

### 1. Setup Environment

```bash
# Clone repository
git clone <repo-url>
cd rag-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
pip install -e .
```

### 3. Configure Environment

Create `.env` file:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/rag_backend
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rag_backend

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=documents
EMBEDDING_MODEL=all-MiniLM-L6-v2

# LLM (choose one: gemini, openai, groq)
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key
```

### 4. Setup Database

```bash
python setup_db.py
```

### 5. Run Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access API at `http://localhost:8000`

## Project Structure

```
app/
├── main.py                    # FastAPI app
├── api/
│   ├── core/
│   │   ├── logger.py         # Logging setup
│   │   └── config.py         # Configuration
│   ├── chat.py               # Chat endpoint
│   └── ingestion.py          # Document upload
├── services/
│   ├── chat/                 # Chat orchestration
│   ├── router/               # Intent routing & tools
│   ├── rag/                  # RAG pipeline
│   ├── booking/              # Booking workflow
│   ├── ingestion/            # Document processing
│   └── memory/               # Session management
├── repositories/             # Database layer
├── providers/                # LLM providers
└── db/
    ├── session.py            # DB connection
    └── models/               # SQLAlchemy models
```

## Technology Stack

| Component     | Technology              |
| ------------- | ----------------------- |
| Framework     | FastAPI                 |
| LLM Tools     | LangChain               |
| Vector DB     | Qdrant                  |
| Database      | PostgreSQL + SQLAlchemy |
| Cache         | Redis                   |
| Embeddings    | all-MiniLM-L6-v2        |
| LLM Providers | Gemini, OpenAI, Groq    |

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       FastAPI Server                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Layer (/api/chat, /api/ingest)                 │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                           │
│  ┌────────────────▼─────────────────────────────────────┐   │
│  │  Intent Router (LLM Classification)                 │   │
│  │  ├─ Question Intent → RAG Service                   │   │
│  │  └─ Booking Intent → Booking Service                │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                           │
│  ┌────────────────┴─────────────────────────────────────┐   │
│  │                                                       │   │
│  │  ┌───────────────────┐    ┌─────────────────────┐  │   │
│  │  │  RAG Pipeline     │    │ Booking Workflow    │  │   │
│  │  ├─ Retriever       │    ├─ Extractor          │  │   │
│  │  ├─ Prompt Builder  │    ├─ Validator          │  │   │
│  │  └─ LLM Generation  │    └─ Repository         │  │   │
│  │                     │                           │  │   │
│  └─────────────────────┴───────────────────────────┘   │
│                                                         │
└────────┬──────────────────┬──────────────────┬──────────┘
         │                  │                  │
    ┌────▼────┐        ┌────▼────┐      ┌─────▼─────┐
    │ Qdrant  │        │ Redis   │      │ PostgreSQL│
    │(Vector  │        │(Session │      │(Bookings) │
    │ Search) │        │ State)  │      │           │
    └─────────┘        └─────────┘      └───────────┘
```

### Component Breakdown

#### 1. **Intent Router** (Brain of the system)

- Receives user message
- Uses LLM to classify: "booking" or "question"
- Routes to appropriate service based on intent
- Maintains tool registry for booking/question handlers

#### 2. **RAG Service** (Question Answering)

- **Retriever:** Searches Qdrant for relevant document chunks
- **Prompt Builder:** Constructs context + question → formatted prompt
- **LLM:** Generates user-friendly answer from retrieved context
- Returns formatted response without internal jargon

#### 3. **Booking Service** (Multi-Turn Workflow)

- **Extractor:** LLM pulls booking fields (name, email, date, time) from messages
- **Validator:** Ensures all required fields are present
- **Repository:** Saves confirmed bookings to PostgreSQL
- **Memory:** Uses Redis to maintain session state across turns

#### 4. **Data Layer**

- **PostgreSQL:** Persistent booking records
- **Redis:** Temporary session state (tracks conversation progress)
- **Qdrant:** Vector database for semantic document search

## User Flows

**Question (RAG):**

```
User Query → Intent Classification → Qdrant Search →
LLM Generation → Answer
```

**Booking (Multi-turn):**

```
"I want to book" → Extract Fields → Store State →
Ask Missing → Validate → Save → Confirm
```

## Troubleshooting

**Qdrant Connection Error:**

```bash
# Ensure Qdrant is running
docker run -p 6333:6333 qdrant/qdrant
```

**Redis Connection Error:**

```bash
# Start Redis
redis-server
```

**Database Migration Issues:**

```bash
# Re-setup database
python setup_db.py
```
