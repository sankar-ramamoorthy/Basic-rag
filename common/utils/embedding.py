# common/utils/embedding.py

import os
from sentence_transformers import SentenceTransformer
import openai

# Choose mode via env var
EMBEDDING_MODE = os.getenv("EMBEDDING_MODE", "local")  # "openai" or "local"

# Lazy init
_model = None


def _get_local_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_embedding(text: str) -> list[float]:
    if EMBEDDING_MODE == "openai":
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response["data"][0]["embedding"]
    else:
        model = _get_local_model()
        return model.encode(text).tolist()
