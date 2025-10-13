FROM python:3.10-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml ./

RUN uv venv
# Install from pyproject.toml
RUN uv pip install --system --project rag-orchestrator .

# ✅ Verify uvicorn is installed and on $PATH
RUN which uvicorn && uvicorn --version

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
