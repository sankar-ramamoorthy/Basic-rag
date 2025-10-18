# service.py (Core RAG Logic)

import httpx
from app.config import VECTOR_STORE_URL, LLM_SERVICE_URL
from common.utils.embedding import get_embedding  # Use your shared embedding code

# Function to run the full RAG process (query -> search -> LLM)
async def run_rag(query: str, top_k: int = 5, provider=None, model=None):
    # Step 1: Embed query
    embedding = get_embedding(query)

    # Step 2: Search vector DB
    async with httpx.AsyncClient() as client:
        search_resp = await client.post(f"{VECTOR_STORE_URL}/search", json={
            "embedding": embedding,
            "top_k": top_k
        })
        search_resp.raise_for_status()
        search_results = search_resp.json()["results"]

    # Step 3: Build context for LLM
    context = "\n\n".join([res["text"] for res in search_results])

    # Step 4: Send to LLM
    llm_payload = {
        "context": context,
        "query": query
    }
    params = {}
    if provider:
        params["provider"] = provider
    if model:
        params["model"] = model

    llm_resp = await client.post(f"{LLM_SERVICE_URL}/generate", json=llm_payload, params=params)
    llm_resp.raise_for_status()
    llm_result = llm_resp.json()

    return {
        "answer": llm_result["response"],
        "sources": [res.get("source") for res in search_results]
    }

# New function to search the vector store and return search results without invoking the LLM
async def search_documents(query: str, top_k: int = 5):
    # Step 1: Embed query
    embedding = get_embedding(query)

    # Step 2: Search vector DB
    async with httpx.AsyncClient() as client:
        search_resp = await client.post(f"{VECTOR_STORE_URL}/search", json={
            "embedding": embedding,
            "top_k": top_k
        })
        search_resp.raise_for_status()
        search_results = search_resp.json()["results"]

    # Return the search results (only text and source)
    return [
        {"text": res["text"], "source": res.get("source", "N/A")}
        for res in search_results
    ]
