#README.md

The RAG Orchestrator is the service that:
Accepts user queries.
Embeds the query.
Sends it to the vector store to retrieve relevant chunks.
Builds a context window.
Sends context + query to the LLM service.
Returns a final answer.

rag-orchestrator/
├── app/
│ ├── main.py
│ ├── api.py # Endpoints
│ ├── service.py # Core logic (RAG flow)
│ ├── models.py # Request/response models
│ └── config.py # Settings loader


Use common.utils.embedding across both ingestion and orchestrator to ensure consistency.

add to .env

VECTOR_STORE_URL=http://vector-store:8000
LLM_SERVICE_URL=http://llm:8000

Flow

[ User uploads document ]
│
▼
[ Ingestion Service: /ingest ]
│
│ 1. Reads + chunks text
│ 2. For each chunk:
│ a. get_embedding(chunk)
│ b. POST to vector-store /store
▼
[ Vector Store ]
│
▼
[ Vector DB (Postgres + pgvector) ]

[ User / Frontend ]
│
▼
[ Orchestrator: /rag endpoint ]
│
│ 1. Receives query
▼
[ get_embedding(query) ]
│
▼
[ Vector Store: /search ]
│ 2. Sends embedding
│
▼
[ Vector DB (e.g., Supabase/Postgres) ]
│
│ 3. Returns top-k matching chunks
▼
[ Orchestrator ]
│
│ 4. Builds prompt:
│ "Context: \n\nQuestion: "
▼
[ LLM Service: /generate ]
│
│ 5. Forwards prompt to selected provider (Ollama, LM Studio, OpenAI)
▼
[ Local LLM (Ollama/LM Studio) or OpenAI API ]
│
│ 6. Receives generated answer
▼
[ LLM Service ]
▼
[ Orchestrator ]
│
│ 7. Assembles response:
│ { answer, sources }
▼
[ User ]

Clear separation of concerns

api.py: handles request/response (can be extended with versioning, logging, etc.)
service.py: clean, testable function like run_rag(query)
config.py: single source of truth for env vars and URLs
models.py: reusable Pydantic schemas across services

rag-orchestrator/
├── app/
│ ├── main.py
│ ├── api.py
│ ├── service.py
│ ├── config.py
│ └── models.py
├── pyproject.toml
└── init.py (optional, if needed)


sample request  to RAG

POST /rag
{
  "query": "What is the capital of France?",
  "top_k": 3,
  "provider": "lmstudio",
  "model": "Qwen3:1.7b"
}
