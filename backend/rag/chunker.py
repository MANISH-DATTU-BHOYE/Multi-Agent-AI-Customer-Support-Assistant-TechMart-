# =========================================================
# backend/rag/chunker.py
# -----------------------------------------------------------
# Splits long documents (FAQ.pdf, RefundPolicy.pdf, etc.) into
# small overlapping text chunks. Small chunks retrieve more
# precisely; the overlap prevents cutting a sentence in half
# right at a chunk boundary.
# This is Step 1 of the RAG workflow described in Module 7:
#   Documents -> Split into chunks -> Generate embeddings -> ...
# =========================================================

from typing import List


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split `text` into chunks of roughly `chunk_size` characters,
    with `overlap` characters repeated between consecutive chunks.

    Args:
        text: raw document text (already extracted from PDF/txt).
        chunk_size: target number of characters per chunk.
        overlap: number of characters shared between adjacent chunks.

    Returns:
        List of chunk strings, cleaned of leading/trailing whitespace.
    """
    text = text.replace("\n", " ").strip()
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        # move the window forward, stepping back by `overlap`
        # so context carries over between chunks
        start += chunk_size - overlap

    return chunks


def load_and_chunk_file(file_path: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Read a .txt/.md knowledge-base file from disk and chunk it."""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    return chunk_text(raw_text, chunk_size, overlap)
