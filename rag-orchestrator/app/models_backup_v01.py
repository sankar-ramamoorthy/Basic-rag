#model.py (pydantic models)

from pydantic import BaseModel

class RAGQuery(BaseModel):
    query: str
    top_k: int = 5
    provider: str = None
    model: str = None

class RAGResponse(BaseModel):
    answer: str
    sources: list
