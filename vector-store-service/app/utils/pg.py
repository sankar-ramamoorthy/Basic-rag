import os
import psycopg
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# Postgres connection string
DB_URL = os.getenv("DATABASE_URL")

# Ensure pgvector extension is ready
TABLE_NAME = "documents"

async def store_vector(data: dict):
    text = data["text"]
    embedding = data["embedding"]
    source = data.get("source", "")
    doc_id = data.get("doc_id")

    embedding_str = "[" + ",".join([str(x) for x in embedding]) + "]"

    async with await psycopg.AsyncConnection.connect(DB_URL) as conn:
        async with conn.cursor() as cur:
            # Create table if it doesn't exist (idempotent)
            await cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                doc_id TEXT,
                text TEXT,
                source TEXT,
                embedding VECTOR(768)
            );
            """)

            await cur.execute(f"""
            INSERT INTO {TABLE_NAME} (doc_id, text, source, embedding)
            VALUES (%s, %s, %s, %s)
            """, (doc_id, text, source, embedding_str))

            await conn.commit()

async def search_vectors(query_embedding, top_k=10):
    embedding_str = "[" + ",".join([str(x) for x in query_embedding]) + "]"

    async with await psycopg.AsyncConnection.connect(DB_URL) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
            SELECT doc_id, text, source,
                   1 - (embedding <#> %s::vector) AS score
            FROM {TABLE_NAME}
            ORDER BY embedding <#> %s::vector
            LIMIT %s
            """, (embedding_str, embedding_str, top_k))

            rows = await cur.fetchall()

            return [
                {"doc_id": r[0], "text": r[1], "source": r[2], "score": round(float(r[3]), 4)}
                for r in rows
            ]
