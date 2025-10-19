#config.py 

import os

VECTOR_STORE_URL = os.getenv("VECTOR_STORE_URL", "http://vector-store:8000")
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://llm:8000")
EMBEDDING_MODE = os.getenv("EMBEDDING_MODE", "local")


