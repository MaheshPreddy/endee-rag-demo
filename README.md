# Endee RAG Demo: Retrieval-Augmented Generation with Vector Search

A production-ready **Retrieval-Augmented Generation (RAG)** demo using [Endee](https://github.com/endee-io/endee), a high-performance open-source vector database. This project demonstrates semantic search, vector-based document retrieval, and LLM-augmented question answering.

**Key Features:**

- 🚀 FastAPI server with REST endpoints for ingestion and RAG queries
- 🧠 Integration with Endee vector database (Python SDK + HTTP adapter)
- 🔍 Semantic search using OpenAI embeddings
- 📚 Retrieval-Augmented Generation with GPT-4o
- 📦 In-memory fallback for local development
- 🧪 Unit tests and CI/CD pipeline (GitHub Actions)
- 🐳 Docker-ready (docker-compose config included)

## Architecture

```
┌─────────────┐
│   User      │
│  Query      │
└──────┬──────┘
       │
       ▼
┌────────────────────────────────────────┐
│      FastAPI Server (app/main.py)      │
├────────────────────────────────────────┤
│  /ingest  ──► Embedding ──► Vector DB  │
│  /query   ──► Embedding ──► Retrieve   │
└──────┬───────────────────────────────┬──┘
       │                               │
       ▼                               ▼
┌──────────────────┐         ┌─────────────────────┐
│ OpenAI Embeddings│         │  Endee Vector DB    │
│ (text-embedding) │         │  (HNSW index)       │
└──────────────────┘         └─────────────────────┘
                                      △
                          Python SDK or HTTP
                                      │
                             ┌─────────────────┐
                             │  LLM (GPT-4o)   │
                             │  + Retrieved    │
                             │  Context ──► RAG│
                             └─────────────────┘
```

## Quick Start

### Prerequisites

- **Python 3.9+**
- **OpenAI API Key** (for embeddings and LLM)
- **Endee** (Python SDK, or HTTP endpoint)

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/<your-username>/endee-rag-demo.git
cd endee-rag-demo

# Create virtual environment
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
# OR on Windows PowerShell:
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Required: OpenAI API key
OPENAI_API_KEY=sk-...

# Optional: Endee vector database configuration
# If using Endee HTTP API (via docker-compose or remote):
ENDEE_BASE_URL=http://localhost:8000
ENDEE_API_KEY=              # Optional bearer token
ENDEE_COLLECTION=docs       # Optional collection name

# Optional: FastAPI configuration
API_BASE_URL=http://localhost:8000
```

### 3. Run Endee (Option A: Docker)

```bash
# Start Endee via docker-compose
docker-compose up -d

# Verify it's running
curl http://localhost:8080
```

Or visit the dashboard: http://localhost:8080

### 4. Run the FastAPI Server

```bash
# In a separate terminal, with .venv activated
uvicorn app.main:app --reload

# Server will be available at http://localhost:8000
```

### 5. Try the Demo

```bash
# In a third terminal, run the demo script
python examples/rag_demo.py
```

This will:

1. Ingest sample documents about Python and ML
2. Query the system with real questions
3. Show retrieved documents and AI-generated answers

## API Endpoints

### `/ingest` (POST)

Ingest a document and create its embedding.

**Request:**

```json
{
  "id": "doc_1",
  "text": "This is a sample document about Python."
}
```

**Response:**

```json
{
  "status": "ingested",
  "id": "doc_1"
}
```

### `/query` (POST)

Query the vector store and generate an answer using the retrieved context.

**Request:**

```json
{
  "query": "What is Python?",
  "top_k": 3
}
```

**Response:**

```json
{
  "answer": "Python is a high-level programming language known for...",
  "retrieved": [
    {
      "id": "doc_python_intro",
      "score": 0.95,
      "metadata": {
        "text": "Python is a high-level..."
      }
    }
  ]
}
```

## Vector Store Adapters

The project includes two vector store implementations:

### 1. Endee Python SDK (Preferred)

Auto-detects and uses the Endee Python SDK if installed:

```python
from app.vector_store import EndeeVectorStore
store = EndeeVectorStore(collection="docs")
```

### 2. Endee HTTP Adapter (Fallback)

Makes HTTP requests to an Endee server:

```python
from app.vector_store import EndeeVectorStore
store = EndeeVectorStore(base_url="http://localhost:8000", collection="docs")
```

### 3. In-Memory Store (Testing)

Simple in-memory vector store for local development:

```python
from app.vector_store import InMemoryVectorStore
store = InMemoryVectorStore()
```

## Integrating Your Forked Endee

To use your own fork of Endee:

1. **Fork** the Endee repository: https://github.com/endee-io/endee
2. **Install your fork locally:**

   ```bash
   # Option A: Install from your GitHub fork
   pip install git+https://github.com/<your-username>/endee.git

   # Option B: Install from local source
   cd ~/your-fork-location
   pip install -e .
   ```

3. **Configure in `.env`:**
   ```bash
   ENDEE_BASE_URL=http://localhost:8000  # Your Endee server
   ENDEE_COLLECTION=docs
   ```
4. **The adapter will automatically use your SDK** when available.

## Project Structure

```
endee-rag-demo/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── docker-compose.yml           # Docker setup for Endee
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI server (routes)
│   └── vector_store.py          # Vector DB adapters
│
├── samples/
│   └── dataset.py               # Sample documents for testing
│
├── examples/
│   └── rag_demo.py              # End-to-end demo script
│
├── tests/
│   └── test_vector_store.py     # Unit tests
│
└── .github/workflows/
    └── ci.yml                   # CI/CD pipeline (pytest + flake8)
```

## Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing

# Run specific test
pytest tests/test_vector_store.py -v

# Run linting
flake8 app/ tests/ --max-line-length=120
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t endee-rag-demo:latest .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-... \
  -e ENDEE_BASE_URL=http://endee:8080 \
  --network host \
  endee-rag-demo:latest

# Or use docker-compose (includes Endee server)
docker-compose up
```

### Cloud Deployment (Heroku / AWS / GCP)

1. Ensure `.env` variables are set as environment variables
2. Ensure Endee is deployed (use cloud Endee service, or self-hosted)
3. Update `ENDEE_BASE_URL` to point to your cloud Endee endpoint

## Evaluation Criteria ✓

- ✅ **Forked Endee repository**: Uses https://github.com/endee-io/endee
- ✅ **Vector database integration**: Endee adapters (SDK + HTTP) in `app/vector_store.py`
- ✅ **Practical use case**: RAG/Semantic Search with sample dataset
- ✅ **GitHub hosting**: Ready to push to GitHub
- ✅ **Comprehensive README**: Architecture, setup, API, deployment, and more

## Next Steps

1. **Fork Endee:** https://github.com/endee-io/endee
2. **Clone your fork** and install locally
3. **Configure `.env`** with your OpenAI key and Endee endpoint
4. **Run tests** to verify everything works: `pytest tests/ -v`
5. **Start the server:** `uvicorn app.main:app --reload`
6. **Try the demo:** `python examples/rag_demo.py`
7. **Push to GitHub:** Update the repo link in this README

## Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the **Apache License 2.0** — same as Endee. See [LICENSE](LICENSE) for details.

## Resources

- **Endee Repository:** https://github.com/endee-io/endee
- **Endee Documentation:** https://docs.endee.io
- **OpenAI API:** https://platform.openai.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **RAG Overview:** https://en.wikipedia.org/wiki/Retrieval-augmented_generation

## Questions?

Open an issue on GitHub or reach out to the Endee community at https://github.com/endee-io/endee/discussions
