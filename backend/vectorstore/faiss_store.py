# =========================================================
# backend/vectorstore/faiss_store.py
# -----------------------------------------------------------
# A small wrapper around a FAISS index (Module 7 / Technology
# Stack -> Vector Database -> FAISS). Stores document-chunk
# embeddings and supports fast nearest-neighbour search so the
# RAG retriever can find the most relevant chunks for a query.
# =========================================================

import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple
from backend.config import settings


class FaissVectorStore:
    def __init__(self, dimension: int = 384, index_path: str = None):
        """
        dimension: size of the embedding vectors produced by the
                   embedding model (384 for all-MiniLM-L6-v2).
        """
        self.dimension = dimension
        self.index_path = index_path or settings.FAISS_INDEX_PATH
        # IndexFlatIP = exact inner-product search; since embeddings are
        # normalized, inner product is equivalent to cosine similarity.
        self.index = faiss.IndexFlatIP(dimension)
        # Parallel list: index position -> (chunk_text, source_document)
        self.metadata: List[Tuple[str, str]] = []

    def add(self, vectors: np.ndarray, texts: List[str], sources: List[str]) -> None:
        """Add a batch of embeddings + their originating text/source to the index."""
        self.index.add(vectors.astype("float32"))
        for text, source in zip(texts, sources):
            self.metadata.append((text, source))

    def search(self, query_vector: np.ndarray, top_k: int = 4) -> List[dict]:
        """
        Return the top_k most similar chunks to the query vector.
        Each result contains the chunk text, its source document,
        and the similarity score.
        """
        query_vector = query_vector.reshape(1, -1).astype("float32")
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue  # FAISS pads with -1 when fewer than top_k results exist
            text, source = self.metadata[idx]
            results.append({"text": text, "source": source, "score": float(score)})
        return results

    def save(self) -> None:
        """Persist the FAISS index + metadata to disk so it survives a restart."""
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, f"{self.index_path}.index")
        with open(f"{self.index_path}.meta", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self) -> None:
        """Load a previously saved FAISS index + metadata from disk."""
        self.index = faiss.read_index(f"{self.index_path}.index")
        with open(f"{self.index_path}.meta", "rb") as f:
            self.metadata = pickle.load(f)


# Shared singleton used across the app
vector_store = FaissVectorStore()
