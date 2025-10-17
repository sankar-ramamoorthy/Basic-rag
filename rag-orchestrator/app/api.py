#api.py (EndPoints)

from fastapi import APIRouter
from app.models import RAGQuery, RAGResponse
from app.service import run_rag

router = APIRouter()

@router.post("/rag", response_model=RAGResponse)
async def rag_endpoint(request: RAGQuery):
    result = await run_rag(
        query=request.query,
        top_k=request.top_k,
        provider=request.provider,
        model=request.model
    )
    return RAGResponse(**result)

@router.get("/health")
def health_check():
    return {"status": "ok", "service": "rag-orchestrator"}

