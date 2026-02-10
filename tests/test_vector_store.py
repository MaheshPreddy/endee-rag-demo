from app.vector_store import InMemoryVectorStore


def test_inmemory_upsert_and_query():
    s = InMemoryVectorStore()
    s.upsert("d1", [1.0, 0.0, 0.0], {"text": "hello world"})
    s.upsert("d2", [0.0, 1.0, 0.0], {"text": "goodbye world"})

    # Query near d1
    res = s.query([0.9, 0.1, 0.0], top_k=1)
    assert len(res) == 1
    assert res[0]["id"] == "d1"

    # Query top2
    res2 = s.query([0.5, 0.5, 0.0], top_k=2)
    assert len(res2) == 2
    ids = {r["id"] for r in res2}
    assert ids == {"d1", "d2"}
