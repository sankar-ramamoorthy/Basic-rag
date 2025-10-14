vector-store-service/
├── app/
│   ├── main.py
│   └── utils/
│       └── pg.py


pg.py: connects to Supabase (Postgres with pgvector), stores embeddings, and does cosine search

pgvector distance operator

using <#> → cosine distance (1 - cosine_similarity)

So lower scores = more similar — we invert it for easier interpretation

Test JSON (for /store):

```
{
  "text": "This is a sample document about vector databases.",
  "embedding": [0.1, 0.2, 0.3, ...],  // your 768-dim embedding
  "source": "example.txt",
  "doc_id": "abc123"
}
```


TBD. Make sure your embeddings are 768-dim (if using bge-small-en-v1.5)
May have moved the table schema setup to a migration or init script
TBD. Log output can be added using Python’s logging module for observability