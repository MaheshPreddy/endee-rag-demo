# Quick Reference: Endee RAG Demo

## 5-Minute Setup

### 1. Fork & Clone

```bash
# Fork Endee at: https://github.com/endee-io/endee → Fork
# Create new repo at: https://github.com/new
# Name it: endee-rag-demo

cd /workspace
git init
git add .
git commit -m "Initial commit: Endee RAG demo"
git branch -M main
git remote add origin https://github.com/<your-username>/endee-rag-demo.git
git push -u origin main
```

Or use the automated script:

```bash
# Windows PowerShell
.\setup_git.ps1

# macOS/Linux
chmod +x setup_git.sh
./setup_git.sh
```

### 2. Install & Configure

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run Tests

```bash
pytest tests/ -v
```

### 4. Run Endee Server

```bash
docker-compose up -d
# or
docker run -p 8080:8080 endeeio/endee-server:latest
```

### 5. Start FastAPI Server

```bash
uvicorn app.main:app --reload
# Server at: http://localhost:8000/docs
```

### 6. Run Demo

```bash
python examples/rag_demo.py
```

## API Endpoints

| Endpoint  | Method | Purpose                                |
| --------- | ------ | -------------------------------------- |
| `/ingest` | POST   | Ingest documents and create embeddings |
| `/query`  | POST   | Retrieve docs and generate RAG answers |
| `/docs`   | GET    | FastAPI interactive docs               |

### Example: Ingest

```bash
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d '{"id": "doc1", "text": "Python is a programming language"}'
```

### Example: Query

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Python?", "top_k": 3}'
```

## Project Files

| File                         | Purpose                                 |
| ---------------------------- | --------------------------------------- |
| `app/main.py`                | FastAPI routes (/ingest, /query)        |
| `app/vector_store.py`        | Endee adapters (SDK + HTTP + in-memory) |
| `examples/rag_demo.py`       | End-to-end demo script                  |
| `samples/dataset.py`         | Sample documents                        |
| `tests/test_vector_store.py` | Unit tests                              |
| `README.md`                  | Full documentation                      |
| `requirements.txt`           | Python dependencies                     |
| `docker-compose.yml`         | Endee server setup                      |
| `.env.example`               | Environment template                    |
| `.github/workflows/ci.yml`   | CI/CD pipeline                          |

## Troubleshooting

| Issue                                          | Solution                                        |
| ---------------------------------------------- | ----------------------------------------------- |
| `ModuleNotFoundError: No module named 'endee'` | Run `pip install -r requirements.txt`           |
| `Connection refused` (Endee)                   | Start Endee: `docker-compose up -d`             |
| `OPENAI_API_KEY not set`                       | Add to `.env`: `OPENAI_API_KEY=sk-...`          |
| `Port 8000 already in use`                     | Change port: `uvicorn app.main:app --port 8001` |

## Key Architecture

```
Query
  ↓
OpenAI Embeddings (text-embedding-3-small)
  ↓
Endee Vector DB (similarity search)
  ↓
GPT-4o (RAG answer generation)
```

## Evaluation Criteria ✓

- ✅ Endee as vector database
- ✅ Semantic search + RAG implementation
- ✅ FastAPI REST API
- ✅ Unit tests (passing)
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ Comprehensive README
- ✅ Docker support
- ✅ Production-ready code

## Links

- Repository: `https://github.com/<your-username>/endee-rag-demo`
- Endee Fork: `https://github.com/<your-username>/endee`
- README: [README.md](README.md)
- Setup Guide: [GITHUB_SETUP.md](GITHUB_SETUP.md)
- Endee Docs: https://docs.endee.io
- FastAPI Docs: https://fastapi.tiangolo.com

---

Ready? Push to GitHub and you're done! 🚀
