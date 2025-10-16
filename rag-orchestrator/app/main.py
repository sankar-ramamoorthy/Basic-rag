from fastapi import FastAPI
from app import api

app = FastAPI(title="RAG Orchestrator")

app.include_router(api.router)
