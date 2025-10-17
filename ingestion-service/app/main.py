#main.py 
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
#from app.utils.chunking import chunk_text
#from app.utils.embedding import get_embedding

# ingestion-service/app/main.py

from common.utils.chunking import chunk_text
from common.utils.embedding import get_embedding


import httpx
import uuid
import logging

app = FastAPI(title="Ingestion Service")

logging.basicConfig(level=logging.INFO)

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    try:
        raw_text = (await file.read()).decode("utf-8")
        chunks = chunk_text(raw_text)

        doc_id = str(uuid.uuid4())  # Unique document ID
        source_name = file.filename

        async with httpx.AsyncClient(timeout=10.0) as client:
            for chunk in chunks:
                embedding = get_embedding(chunk)
                await client.post("http://vector-store:8000/store", json={
                    "doc_id": doc_id
                    "text": chunk,
                    "embedding": embedding,
                    "source_name": source_name,
                })

        logging.info(f"Ingested {len(chunks)} chunks from {source_name}")

        return {"status": "success", "chunks": len(chunks), "doc_id": doc_id}

    except Exception as e:
        logging.exception("Error during ingestion")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ingestion"}

@app.get("/test-chunking")
def test_chunking():
    text = "This is a long paragraph of text. " * 50
    chunks = chunk_text(text)
    return {"num_chunks": len(chunks), "sample": chunks[:2]}
