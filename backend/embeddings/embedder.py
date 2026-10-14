# =========================================================
# backend/embeddings/embedder.py
# -----------------------------------------------------------
# Wraps a sentence-transformers embedding model so the rest of
# the app never has to think about model loading or tokenization.
# Used both when ingesting knowledge-base documents (Module 6)
# and when embedding a live user query for retrieval (Module 7).
# =========================================================

from sentence_transformers import SentenceTransformer
from backend.config import settings
from typing import List
import numpy as np


class Embedder:
    """Thin wrapper around a SentenceTransformer model."""

    def __init__(self, model_name: str = None):
        # Loaded once and cached in memory - loading is the expensive part.
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.model = SentenceTransformer(self.model_name)

    def embed_text(self, text: str) -> np.ndarray:
        """Embed a single string -> 1D numpy vector."""
        return self.model.encode(text, normalize_embeddings=True)

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Embed many strings at once (much faster than looping) -> 2D numpy array."""
        return self.model.encode(texts, normalize_embeddings=True, batch_size=32)


# Shared singleton so the model is loaded only once per process
embedder = Embedder()
