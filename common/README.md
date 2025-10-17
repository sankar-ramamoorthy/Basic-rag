common.utils.embedding in multiple services, so it needs to live in a shared location that's:

Accessible across all services (e.g., ingestion, orchestrator, llm)

Mounted correctly via Docker

Structured in a way that allows Python to import it as common.utils.embedding

Recommended Directory Placement

├── common/
│   └── utils/
│       ├── __init__.py
│       └── embedding.py   👈 YOUR SHARED MODULE


place embedding.py here:

basic-rag/
├── common/
│   └── utils/
│       └── embedding.py   ✅


can import it in any service like:

from common.utils.embedding import get_embedding


Docker Compatibility
docker-compose.yml, you already mount this shared code in every service:

volumes:
  - ./common:/app/common



That means inside the container:
/app/common/utils/embedding.py


is available and importable as:
from common.utils.embedding import get_embedding


This will work as long as your PYTHONPATH includes /app, which it does by default in Python apps running from that directory (especially when WORKDIR is set to /app in your Dockerfile).

Put embedding.py in common/utils/embedding.py
Ensure there's an __init__.py in both common/ and common/utils/
Confirm your Dockerfile sets WORKDIR /app 
Mount ./common:/app/common 
