import logging
from fastapi import APIRouter, HTTPException
from app.models import RAGQuery, RAGResponse, SearchQuery
from app.service import run_rag, search_documents
from pydantic import BaseModel
import httpx

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()

# /rag endpoint with structured RAGQuery and logging
@router.post("/rag", response_model=RAGResponse)
async def rag_endpoint(request: RAGQuery):
    # Log that we've entered the function and display parameters
    logger.debug(f"Entering /rag endpoint with parameters: {request.dict()}")
    
    try:
        # Run the RAG process using the structured parameters
        result = await run_rag(
            query=request.query,
            top_k=request.top_k,
            provider=request.provider,
            model=request.model
        )
        
        # Log the result from the RAG service
        logger.debug(f"RAG result: {result}")

        # Return the structured response
        return RAGResponse(**result)
    
    except httpx.HTTPStatusError as e:
        # Catch HTTP errors from the service layer and report them
        logger.error(f"HTTP error occurred in /rag: {str(e)}")
        raise HTTPException(status_code=500, detail=f"HTTP error occurred: {str(e)}")
    
    except httpx.ReadTimeout as e:
        # Catch timeout errors from the HTTP request
        logger.error(f"Timeout error occurred in /rag: {str(e)}")
        raise HTTPException(status_code=500, detail="The request to the LLM service timed out.")
    
    except Exception as e:
        # Catch any other generic errors and report them
        logger.error(f"Unexpected error occurred in /rag: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# /search endpoint for querying the vector store
@router.post("/search")
async def search_endpoint(request: SearchQuery):
    try:
        # Call the search_documents function from service.py to embed the question and search the vector store
        search_results = await search_documents(request.question, top_k=request.top_k)
        
        # Return the search results
        return {"results": search_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")


# Health check endpoint (no changes)
@router.get("/health")
def health_check():
    return {"status": "ok", "service": "rag-orchestrator"}


# Models for query validation

# SearchQuery class to handle input for the /search endpoint
class SearchQuery(BaseModel):
    question: str
    top_k: int = 5  # Default to top 5 search results


# RAGQuery class to handle input for the /rag endpoint
class RAGQuery(BaseModel):
    query: str  # The query string the user is asking
    top_k: int = 5  # Default to top 5 results from the RAG process
    provider: str = 'OpenAI'  # Provider for the LLM (e.g., OpenAI, Hugging Face)
    model: str = 'gpt-3.5'  # The model to be used (e.g., 'gpt-4', 'gpt-3.5', etc.)

    class Config:
        # Enforce strict validation and serialization
        min_anystr_length = 1
        anystr_strip_whitespace = True


# Response models for /rag endpoint

class RAGResponse(BaseModel):
    result: str  # The result of the RAG process, this can vary based on the LLM's response format
    source_documents: list  # A list of documents or references used in the RAG process

    class Config:
        # Configure the response model to ensure correct serialization and minimal errors
        anystr_strip_whitespace = True
        min_anystr_length = 1

