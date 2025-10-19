# config.py 

import os

# Ensure these match the service names and the ports exposed in docker-compose.yml
VECTOR_STORE_URL = os.getenv("VECTOR_STORE_URL", "http://vector-store-service:8000")
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://llm-service:8000")
EMBEDDING_MODE = os.getenv("EMBEDDING_MODE", "local")
