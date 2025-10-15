# common/utils/chunking.py

import tiktoken

DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_CHUNK_SIZE = 300
DEFAULT_CHUNK_OVERLAP = 50


def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    model: str = DEFAULT_MODEL
) -> list[str]:
    """
    Split text into overlapping token-based chunks.

    Args:
        text: Input text.
        chunk_size: Max tokens per chunk.
        chunk_overlap: Overlap between chunks (in tokens).
        model: Model to determine tokenizer.

    Returns:
        List of chunked text strings.
    """
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    chunks = []

    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk = tokens[start:end]
        decoded = enc.decode(chunk)
        chunks.append(decoded)

        start += chunk_size - chunk_overlap  # Slide forward with overlap

    return chunks
