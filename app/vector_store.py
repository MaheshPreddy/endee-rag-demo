from typing import List, Dict, Any, Optional
import numpy as np
import requests


class EndeeVectorStore:
    """Adapter for Endee: prefer Python SDK if installed, otherwise HTTP.

    This adapter will attempt to import and use the `endee` Python SDK. If
    the SDK is not installed, it will fall back to making HTTP requests to
    the Endee server using the provided `base_url`.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        collection: Optional[str] = None,
        upsert_path: str = "/vectors/upsert",
        query_path: str = "/vectors/query",
        timeout: int = 10,
        use_sdk: Optional[bool] = None,
    ):
        self.base_url = base_url.rstrip("/") if base_url else None
        self.api_key = api_key
        self.collection = collection
        self.upsert_path = upsert_path
        self.query_path = query_path
        self.timeout = timeout

        # Try to use the Endee Python SDK if available, unless explicitly disabled.
        self._sdk = None
        if use_sdk is None or use_sdk:
            try:
                import endee as _endee

                self._sdk = _endee
                # instantiate client with token if provided
                try:
                    if api_key:
                        self._client = _endee.Endee(api_key)
                    else:
                        self._client = _endee.Endee()
                except Exception:
                    # older/newer versions may accept different init; fallback to default
                    self._client = _endee.Endee()
                self._index = None
            except Exception:
                self._sdk = None

        # If SDK not available, ensure we have a base_url for HTTP adapter.
        if self._sdk is None and not self.base_url:
            raise ValueError("Either the Endee Python SDK must be installed or base_url must be provided")

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def upsert(self, doc_id: str, embedding: List[float], metadata: Dict[str, Any]):
        # If SDK available, use its index upsert
        if self._sdk is not None:
            # Ensure index exists
            if self._index is None:
                # Create or get index with dimension inferred from embedding
                dim = len(embedding)
                try:
                    self._index = self._client.get_index(name=self.collection) if self.collection else None
                except Exception:
                    # create index if not exists
                    if self.collection:
                        try:
                            self._client.create_index(name=self.collection, dimension=dim, space_type="cosine")
                            self._index = self._client.get_index(name=self.collection)
                        except Exception:
                            # If create/get fail, leave None and let SDK raise on upsert
                            self._index = None

            index = self._index or (self._client.get_index(name=self.collection) if self.collection else None)
            if index is not None:
                # Endee SDK expects list of vectors with id, vector and meta fields
                vec = {"id": doc_id, "vector": embedding, "meta": metadata}
                return index.upsert([vec])
            else:
                # Fallback to using client methods directly
                return self._client.upsert(doc_id, embedding, metadata)

        # Otherwise use HTTP adapter
        payload = {
            "id": doc_id,
            "embedding": embedding,
            "metadata": metadata,
        }
        if self.collection:
            payload["collection"] = self.collection

        url = f"{self.base_url}{self.upsert_path}"
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def query(self, embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        # If SDK available, use its query method
        if self._sdk is not None:
            index = self._index or (self._client.get_index(name=self.collection) if self.collection else None)
            if index is not None:
                results = index.query(vector=embedding, top_k=top_k)
                # Normalize to list of {id, score, metadata}
                out = []
                for r in results:
                    out.append({"id": r.get("id") or r.get("_id"), "score": r.get("score"), "metadata": r.get("meta") or r.get("metadata")})
                return out

        # Otherwise HTTP
        payload = {"embedding": embedding, "top_k": top_k}
        if self.collection:
            payload["collection"] = self.collection

        url = f"{self.base_url}{self.query_path}"
        resp = requests.post(url, json=payload, headers=self._headers(), timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()

        # Expecting a list of results like: [{"id":..., "score":..., "metadata": {...}}, ...]
        return data.get("results", data)


class InMemoryVectorStore:
    """Simple in-memory fallback for testing.

    Stored as list of tuples: (id, embedding, metadata)
    """

    def __init__(self):
        self._items = []

    def upsert(self, doc_id: str, embedding: List[float], metadata: Dict[str, Any]):
        self._items.append((doc_id, np.array(embedding, dtype=float), metadata))

    def query(self, embedding: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        if not self._items:
            return []
        q = np.array(embedding, dtype=float)
        sims = []
        for doc_id, emb, metadata in self._items:
            denom = (np.linalg.norm(q) * np.linalg.norm(emb))
            score = float(np.dot(q, emb) / denom) if denom != 0 else 0.0
            sims.append((doc_id, score, metadata))
        sims.sort(key=lambda x: x[1], reverse=True)
        results = []
        for doc_id, score, metadata in sims[:top_k]:
            results.append({"id": doc_id, "score": score, "metadata": metadata})
        return results
