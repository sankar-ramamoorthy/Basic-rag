FROM python:3.10-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./        # ✅ will silently skip if not present

RUN uv pip install

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
