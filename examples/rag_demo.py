#!/usr/bin/env python3
"""
RAG Demo: Retrieval-Augmented Generation with Endee

This script demonstrates the complete RAG workflow:
1. Ingest sample documents and create embeddings
2. Query the vector store to retrieve relevant documents
3. Use a language model to generate answers augmented by retrieved context

Requirements:
- OPENAI_API_KEY must be set in .env or environment
- Run the FastAPI server: uvicorn app.main:app --reload
- Or run this script directly to use the in-memory store

Usage:
    python examples/rag_demo.py
"""

import os
import sys
from typing import List, Dict
from dotenv import load_dotenv
import requests

# Add workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from samples.dataset import SAMPLE_DOCUMENTS

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def ingest_documents(docs: List[Dict[str, str]]) -> int:
    """Ingest sample documents via the API."""
    count = 0
    for doc in docs:
        try:
            resp = requests.post(
                f"{API_BASE_URL}/ingest",
                json={"id": doc["id"], "text": doc["text"]},
                timeout=10,
            )
            resp.raise_for_status()
            print(f"✓ Ingested: {doc['id']}")
            count += 1
        except Exception as e:
            print(f"✗ Failed to ingest {doc['id']}: {e}")
    return count


def query_rag(query_text: str) -> Dict:
    """Query the RAG system and get an answer."""
    try:
        resp = requests.post(
            f"{API_BASE_URL}/query",
            json={"query": query_text, "top_k": 3},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error querying: {e}")
        return None


def main():
    """Run the demo."""
    print("=" * 70)
    print("RAG Demo: Retrieval-Augmented Generation with Endee")
    print("=" * 70)
    print()

    # Check API server
    try:
        requests.get(f"{API_BASE_URL}/docs", timeout=2)
        print(f"✓ FastAPI server is running at {API_BASE_URL}")
    except Exception:
        print(f"✗ Cannot reach API at {API_BASE_URL}")
        print("  Please start the server: uvicorn app.main:app --reload")
        sys.exit(1)

    if not OPENAI_API_KEY:
        print("✗ OPENAI_API_KEY is not set. Please set it in .env or environment.")
        sys.exit(1)

    print()
    print("Step 1: Ingesting Sample Documents")
    print("-" * 70)
    ingested = ingest_documents(SAMPLE_DOCUMENTS)
    print(f"Ingested {ingested}/{len(SAMPLE_DOCUMENTS)} documents")
    print()

    # Sample queries
    queries = [
        "What is Python used for?",
        "Explain how machine learning works",
        "What are embeddings in NLP?",
    ]

    print("Step 2: Running RAG Queries")
    print("-" * 70)

    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 70)
        result = query_rag(query)

        if result:
            answer = result.get("answer", "No answer")
            retrieved = result.get("retrieved", [])

            print(f"\nAnswer:\n{answer}")
            print(f"\nRetrieved {len(retrieved)} documents:")
            for i, doc in enumerate(retrieved, 1):
                print(
                    f"  {i}. {doc.get('id')} (score: {doc.get('score', 'N/A'):.3f})"
                )
        else:
            print("Failed to get answer")

        print()


if __name__ == "__main__":
    main()
