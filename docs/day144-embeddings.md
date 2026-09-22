# Day 144 — Embeddings

Part of the roadmap: Day 143 (Tool Calling + MCP) → **Day 144 (Embeddings)** → Day 145 (Vector DB) → Day 146 (RAG) → Day 147 (RAG mini project).

## Step 1 — Embedding basics ✅

**Files**

- [`app/schemas/embedding.py`](../app/schemas/embedding.py) — `EmbeddingRequest`
- [`app/services/embedding_service.py`](../app/services/embedding_service.py) — `create_embedding(text)`
- [`app/main.py`](../app/main.py) — `POST /api/embeddings`

**Flow**

```
text
  |
  v
client.embeddings.create(model="text-embedding-3-small", input=text)
  |
  v
1536-dim vector (list[float])
```

This is a different OpenAI API surface than `client.responses.create(...)` (used everywhere
else in this project for chat). An embedding model doesn't answer questions — it maps text
to a point in a high-dimensional space where semantic closeness ≈ vector closeness. The LLM
never sees the vector directly; the vector is only used to *find* relevant text, which is
then handed back to an LLM in later steps (RAG).

**Verified**

```
POST /api/embeddings
{ "text": "Chicken biryani costs 250 rupees" }

→ { "text": "...", "dimensions": 1536, "embedding": [-0.0108, -0.0235, ...] }
```

Confirmed live against the running server — dimensions = 1536 for `text-embedding-3-small`.

## Step 2 — Similarity search ⬜

Will add `POST /api/embeddings/similarity`: embed a query + candidate sentences in one batched
API call, score each with cosine similarity, return sorted by relevance. Needs `numpy`.

## Step 3 — Chunking ⬜

Will add `POST /api/embeddings/chunk`: split a long document into overlapping word-based
chunks, embed each chunk, return chunk + vector pairs. This is the ingestion half of RAG.

## Progress

- [x] What embeddings are
- [x] OpenAI Embeddings API (`client.embeddings.create`)
- [x] Vectors / dimensions
- [ ] Cosine similarity
- [ ] Batch embeddings
- [ ] Document chunking
- [ ] Chunk overlap
- [ ] Store embeddings (pgvector — Day 145)
- [ ] Vector similarity search (Day 145)
- [ ] RAG retrieval (Day 146)
