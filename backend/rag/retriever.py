# =========================================================
# backend/rag/retriever.py
# -----------------------------------------------------------
# Module 7 (Retrieval-Augmented Generation) — the "R" in RAG.
# Given a user question, embeds it and searches the vector store
# for the most relevant knowledge-base chunks, which are then
# passed to the LLM as grounding context.
# =========================================================

from backend.embeddings.embedder import embedder
from backend.vectorstore.faiss_store import vector_store
from typing import List, Dict


def retrieve_context(query: str, top_k: int = 4) -> List[Dict]:
    """
    Embed the user's query and return the top_k most similar
    knowledge-base chunks, each with its source document and score.
    """
    query_vector = embedder.embed_text(query)
    results = vector_store.search(query_vector, top_k=top_k)
    return results


def format_context_for_prompt(results: List[Dict]) -> str:
    """
    Turn retrieved chunks into a single string that gets injected
    into the LLM prompt, each chunk labeled with its source so the
    model (and the user) can trace where an answer came from.
    """
    if not results:
        return "No relevant company documents were found."

    formatted = []
    for r in results:
        formatted.append(f"[Source: {r['source']}]\n{r['text']}")
    return "\n\n".join(formatted)
