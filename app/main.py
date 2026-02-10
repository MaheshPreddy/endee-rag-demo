from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import openai
from typing import List, Optional

from app.vector_store import EndeeVectorStore, InMemoryVectorStore

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment or .env file")
openai.api_key = OPENAI_API_KEY

app = FastAPI(title="Endee RAG Demo")

# Choose a vector store implementation: prefer Endee if configured, else in-memory.
ENDEE_BASE_URL = os.getenv("ENDEE_BASE_URL")
ENDEE_API_KEY = os.getenv("ENDEE_API_KEY")
ENDEE_COLLECTION = os.getenv("ENDEE_COLLECTION")

if ENDEE_BASE_URL:
    vector_store = EndeeVectorStore(base_url=ENDEE_BASE_URL, api_key=ENDEE_API_KEY, collection=ENDEE_COLLECTION)
else:
    # For quick testing, use the in-memory store.
    vector_store = InMemoryVectorStore()

class IngestRequest(BaseModel):
    id: str
    text: str

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

@app.post("/ingest")
async def ingest(req: IngestRequest):
    # Create embedding via OpenAI
    try:
        resp = openai.Embedding.create(model="text-embedding-3-small", input=req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    embedding = resp["data"][0]["embedding"]
    metadata = {"text": req.text}
    vector_store.upsert(req.id, embedding, metadata)
    return {"status": "ingested", "id": req.id}

@app.post("/query")
async def query(req: QueryRequest):
    # Embed query
    try:
        resp = openai.Embedding.create(model="text-embedding-3-small", input=req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    q_emb = resp["data"][0]["embedding"]
    hits = vector_store.query(q_emb, top_k=req.top_k)

    # Build a prompt with retrieved context
    context_texts = "\n---\n".join([h["metadata"]["text"] for h in hits])
    prompt = f"Use the following context to answer the question. If the answer is not contained, say 'I don't know'.\n\nContext:\n{context_texts}\n\nQuestion: {req.query}\nAnswer:"

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.0,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    answer = completion["choices"][0]["message"]["content"].strip()
    return {"answer": answer, "retrieved": hits}
