from fastapi import FastAPI, UploadFile, File
from common.utils.chunking import chunk_text
from common.utils.embedding import get_embedding

import httpx

app = FastAPI(title="Ingestion Service")

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8")
    chunks = chunk_text(text)

    async with httpx.AsyncClient() as client:
        for chunk in chunks:
            embedding = get_embedding(chunk)
            await client.post("http://vector-store:8000/store", json={
                "text": chunk,
                "embedding": embedding,
            })

    return {"status": "success", "chunks": len(chunks)}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ingestion"}

#Start the ingestion service and test from bash  curl http://localhost:8001/test-chunking    
@app.get("/test-chunking")
def test_chunking():
    text = "This is a long paragraph of text. " * 50
    chunks = chunk_text(text)
    return {"num_chunks": len(chunks), "sample": chunks[:2]}    