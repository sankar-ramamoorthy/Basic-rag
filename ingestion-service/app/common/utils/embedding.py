import os
import logging
from sentence_transformers import SentenceTransformer
import openai

logging.basicConfig(level=logging.INFO)

EMBEDDING_MODE = os.getenv("EMBEDDING_MODE", "local")
_model = None

def _get_local_model():
    global _model
    if _model is None:
        logging.info("Loading local embedding model: all-MiniLM-L6-v2")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_embedding(text: str) -> list[float]:
    if EMBEDDING_MODE == "openai":
        try:
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            logging.error(f"OpenAI embedding failed: {e}")
            raise
    else:
        model = _get_local_model()
        return model.encode(text).tolist()
