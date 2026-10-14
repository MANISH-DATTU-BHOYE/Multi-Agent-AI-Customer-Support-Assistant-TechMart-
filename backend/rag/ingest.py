# =========================================================
# backend/rag/ingest.py
# -----------------------------------------------------------
# One-time (or on-demand) script that builds the vector database
# from the company knowledge base (Module 6 + Module 10).
# Run this whenever a document is added/changed:
#     python -m backend.rag.ingest
#
# Full pipeline implemented here (Module 7 workflow):
#   Documents -> Split into chunks -> Generate embeddings -> Store embeddings
# =========================================================

import os
import glob
from backend.rag.chunker import load_and_chunk_file
from backend.embeddings.embedder import embedder
from backend.vectorstore.faiss_store import vector_store

KNOWLEDGE_BASE_DIR = "knowledge_base"


def ingest_knowledge_base(kb_dir: str = KNOWLEDGE_BASE_DIR) -> None:
    """Read every .txt file in the knowledge base, chunk it, embed it, and store it."""
    file_paths = glob.glob(os.path.join(kb_dir, "*.txt"))

    if not file_paths:
        print(f"No knowledge base files found in '{kb_dir}'.")
        return

    all_chunks, all_sources = [], []

    for path in file_paths:
        doc_name = os.path.basename(path)
        chunks = load_and_chunk_file(path)
        print(f"  {doc_name}: {len(chunks)} chunks")
        all_chunks.extend(chunks)
        all_sources.extend([doc_name] * len(chunks))

    print(f"Embedding {len(all_chunks)} chunks total...")
    vectors = embedder.embed_batch(all_chunks)

    vector_store.add(vectors, all_chunks, all_sources)
    vector_store.save()
    print(f"Vector store saved to '{vector_store.index_path}'.")


if __name__ == "__main__":
    ingest_knowledge_base()
