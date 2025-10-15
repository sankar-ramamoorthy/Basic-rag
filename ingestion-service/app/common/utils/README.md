chunking.py — Text Chunking for RAG

This module handles breaking documents into smaller chunks that can be embedded and stored efficiently.

Uses a token-aware chunker using tiktoken for OpenAI-style token counting, with overlap between chunks.

DEFAULT_MODEL = "gpt-3.5-turbo"  << What default mdel should we choose?

get_embedding(text) is now ready and pluggable
Supports sentence-transformers or OpenAI
All services can import it via the shared common/ volume