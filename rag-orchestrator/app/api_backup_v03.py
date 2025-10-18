# api.py (Endpoints)

from fastapi import APIRouter, HTTPException
from app.models import RAGQuery, RAGResponse
from app.service import run_rag, search_documents  # Import the search_documents function
from pydantic import BaseModel

router = APIRouter()

# Existing /rag endpoint
@router.post("/rag", response_model=RAGResponse)
async def rag_endpoint(request: RAGQuery):
    result = await run_rag(
        query=request.query,
        top_k=request.top_k,
        provider=request.provider,
        model=request.model
    )
    return RAGResponse(**result)

# New /search endpoint for querying the vector store
class SearchQuery(BaseModel):
    question: str
    top_k: int = 5  # Default to top 5 search results

@router.post("/search")
async def search_endpoint(request: SearchQuery):
    try:
        # Call the search_documents function from service.py to embed the question and search the vector store
        search_results = await search_documents(request.question, top_k=request.top_k)
        
        # Return the search results
        return {"results": search_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint (no changes)
@router.get("/health")
def health_check():
    return {"status": "ok", "service": "rag-orchestrator"}

