from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import openai
import httpx
import logging

app = FastAPI(title="LLM Service")

# ------------------------------------------------------------------------------
# 🌐 Configuration
# ------------------------------------------------------------------------------

# Default provider from env or fallback
DEFAULT_LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

# Ollama (local LLM) config
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "Qwen3:1.7b")

# LM Studio / OpenAI-compatible config
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://host.docker.internal:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "not-needed")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "Qwen3:1.7b-chat")

# Configure OpenAI client (also works with LM Studio)
openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE

# ------------------------------------------------------------------------------
# 🛠️ Request Body Models
# ------------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    context: str = ""
    query: str

# ------------------------------------------------------------------------------
# 🧠 LLM Endpoint
# ------------------------------------------------------------------------------

@app.post("/generate")
async def generate(
    request: GenerateRequest,
    provider: str = Query(None, description="Optional LLM provider override"),
    model: str = Query(None, description="Optional model override")
):
    try:
        context = request.context
        query = request.query

        # Select provider (use default if not provided)
        active_provider = provider or DEFAULT_LLM_PROVIDER

        # Select model (use default if not provided)
        if active_provider == "ollama":
            active_model = model or OLLAMA_MODEL
        elif active_provider in ["lmstudio", "openai"]:
            active_model = model or OPENAI_MODEL
        else:
            raise ValueError(f"Unsupported LLM provider: {active_provider}")

        # Build the prompt
        prompt = f"Context:\n{context}\n\nQuestion:\n{query}"

        # ────────────────────────────────
        # 🐍 OLLAMA
        # ────────────────────────────────
        if active_provider == "ollama":
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": active_model,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=30
                )
                response.raise_for_status()
                answer = response.json()["message"]["content"]

        # ────────────────────────────────
        # 🤖 LM STUDIO or OPENAI
        # ────────────────────────────────
        elif active_provider in ["lmstudio", "openai"]:
            response = openai.completions.create(
                model=active_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            answer = response['choices'][0]['message']['content']

        else:
            raise ValueError(f"Unsupported LLM provider: {active_provider}")

        return {
            "provider": active_provider,
            "model": active_model,
            "response": answer.strip()
        }

    except Exception as e:
        logging.exception("Error in /generate")
        return JSONResponse(status_code=500, content={"error": str(e)})

# ------------------------------------------------------------------------------
# ✅ Health Check
# ------------------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "default_provider": DEFAULT_LLM_PROVIDER,
        "ollama_model": OLLAMA_MODEL,
        "openai_model": OPENAI_MODEL
    }
