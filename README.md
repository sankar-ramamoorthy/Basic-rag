This README is a work in progress.
---

# Basic-RAG: Retrieval-Augmented Generation with FastAPI, Docker, and Supabase

A modular, containerized backend system using **FastAPI**, **Docker**, and **Supabase (pgvector)** to implement a **Retrieval-Augmented Generation (RAG)** pipeline.

The system supports:

* Document ingestion
* Embedding generation
* Vector storage
* Semantic search
* LLM-based answer generation (Ollama: `Qwen3:1.7b`)

---

## 🚀 Prerequisites

* Docker & Docker Compose installed
* Ollama installed and running, serving model: `Qwen3:1.7b`

  ```bash
  ollama serve Qwen3:1.7b
  ```
* Clone this repository:

  ```bash
  git clone https://github.com/sankar-ramamoorthy/Basic-rag
  cd Basic-rag
  ```

---

## 🐳 Running the Project

1. Build and start all services:

   ```bash
   docker compose build
   docker compose up
   ```

2. Check service health with `curl`:

   ```bash
   curl http://localhost:8001/health  # ingestion
   curl http://localhost:8002/health  # vector-store
   curl http://localhost:8003/health  # LLM
   curl http://localhost:8004/health  # RAG orchestrator
   ```

   Expected output:

   ```json
   {"status":"ok","service":"ingestion"}
   {"status":"ok","service":"vector-store"}
   {"status":"ok","default_provider":"ollama","ollama_model":"Qwen3:1.7b","openai_model":"gpt-4"}
   {"status":"ok","service":"rag-orchestrator"}
   ```

---

## 📄 Document Ingestion

### Step 1: Chunk a sample document

```bash
curl http://localhost:8001/test-chunking
```

### Step 2: Ingest a text file

**Single-line curl (Windows/Linux/macOS):**

```bash
curl -X POST http://localhost:8001/ingest -F "file=@Basic-rag.txt" -H "Accept: application/json"
```

You can replace `Basic-rag.txt` with any text file, e.g., `the_colors_of_old_calcutta_story.txt`.

---

## 🔍 Semantic Search / RAG Queries

After ingestion, you can ask questions directly via the **orchestrator**.

**Example 1 – Search the ingested `Basic-rag.txt` file:**

```bash
curl -X POST http://localhost:8004/search -H "Content-Type: application/json" -d "{\"question\": \"What is the name of the project?\", \"top_k\": 3}"
```

**Example 2 – Using LLM directly through the orchestrator:**

```bash
curl -X POST "http://localhost:8003/generate?provider=ollama&model=Qwen3:1.7b" -H "Content-Type: application/json" -d "{\"context\":\"daisy lived in a colorful home in what used to be Calcutta in India\",\"query\":\"Where was Daisy's home?\"}"
```

---

## 🐍 Python Usage Examples

**Search via Python:**

```python
import httpx

payload = {"question": "What is the name of the project?", "top_k": 3}
response = httpx.post("http://localhost:8004/search", json=payload)
print(response.json())
```

**Ingest via Python:**

```python
import httpx

with open("Basic-rag.txt", "rb") as f:
    files = {"file": f}
    response = httpx.post("http://localhost:8001/ingest", files=files)
    print(response.json())
```

---

## 📊 API Documentation (Swagger UI)

Once services are running:

* **Ingestion service:** [http://localhost:8001/docs](http://localhost:8001/docs)
* **Vector-store service:** [http://localhost:8002/docs](http://localhost:8002/docs)
* **LLM service:** [http://localhost:8003/docs](http://localhost:8003/docs)
* **RAG orchestrator:** [http://localhost:8004/docs](http://localhost:8004/docs)

---

## 🗄️ Supabase Backend

* PostgreSQL is preconfigured with pgvector for embeddings.
* Database health check:

```bash
docker exec -it supabase-db pg_isready -U postgres
```

---

## ⚡ Notes

* Ensure **Ollama** is serving `Qwen3:1.7b` before starting queries.
* The orchestrator handles both semantic search and LLM-based answer generation.
* All services are containerized for easy deployment.

---

