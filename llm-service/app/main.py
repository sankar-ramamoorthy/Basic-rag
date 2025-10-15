from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import openai
import httpx
import logging

app = FastAPI(title="LLM Service")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # openai or ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

@app.post("/generate")
async def generate(req: Request):
    try:
        body = await req.json()
        context = body["context"]
        query = body["query"]

        prompt = f"Context:\n{context}\n\nQuestion:\n{query}"

        if LLM_PROVIDER == "openai":
            response = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            answer = response.choices[0].message["content"]
        elif LLM_PROVIDER == "ollama":
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": OLLAMA_MODEL,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                answer = response.json()["message"]["content"]
        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")

        return {"response": answer}

    except Exception as e:
        logging.exception("Error in /generate")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/health")
def health_check():
    return {"status": "ok", "provider": LLM_PROVIDER}
