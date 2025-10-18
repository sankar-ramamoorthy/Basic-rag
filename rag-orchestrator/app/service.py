import httpx
import logging
from app.config import VECTOR_STORE_URL, LLM_SERVICE_URL
from common.utils.embedding import get_embedding  # Use your shared embedding code

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to run the full RAG process (query -> search -> LLM)
async def run_rag(query: str, top_k: int = 5, provider=None, model=None):
    # Step 1: Embed query
    embedding = get_embedding(query)
    logger.debug(f"Query embedding: {embedding[:50]}...")  # Log the first 50 characters of the embedding for brevity

    # Step 2: Search vector DB
    async with httpx.AsyncClient() as client:
        search_url = f"{VECTOR_STORE_URL}/search"
        logger.debug(f"Searching vector store at URL: {search_url} with top_k={top_k}")
        
        search_resp = await client.post(search_url, json={
            "embedding": embedding,
            "top_k": top_k
        })
        
        try:
            search_resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        
        search_results = search_resp.json()["results"]
        logger.debug(f"Search results: {search_results}")

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

    async with httpx.AsyncClient(timeout=httpx.Timeout(240.0)) as client:
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
    logger.debug(f"Query embedding: {embedding[:50]}...")  # Log the first 50 characters of the embedding for brevity

    # Step 2: Search vector DB
    search_url = f"{VECTOR_STORE_URL}/search"
    logger.debug(f"Searching vector store at URL: {search_url} with top_k={top_k}")
    
    async with httpx.AsyncClient() as client:
        search_resp = await client.post(search_url, json={
            "embedding": embedding,
            "top_k": top_k
        })
        
        try:
            search_resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred while searching: {e}")
            raise
        
        search_results = search_resp.json()["results"]
        logger.debug(f"Search results: {search_results}")

    # Return the search results (only text and source)
    return [
        {"text": res["text"], "source": res.get("source", "N/A")}
        for res in search_results
    ]
