FROM python:3.10-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml ./

RUN uv venv
# Install from pyproject.toml
RUN uv pip install --project ingestion-service  . 

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
