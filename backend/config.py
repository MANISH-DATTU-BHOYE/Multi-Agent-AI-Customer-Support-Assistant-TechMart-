# =========================================================
# backend/config.py
# -----------------------------------------------------------
# Central place where every environment variable is read once
# and exposed as a typed "settings" object. Every other module
# imports `settings` from here instead of calling os.getenv()
# everywhere — this keeps configuration consistent and testable.
# =========================================================

import os
from dotenv import load_dotenv

# Load variables from the .env file into the process environment
load_dotenv()


class Settings:
    """Typed container for all configuration values used by the app."""

    # ----- LLM -----
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

    # ----- Embeddings -----
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # ----- Vector store -----
    VECTOR_STORE: str = os.getenv("VECTOR_STORE", "faiss")
    FAISS_INDEX_PATH: str = os.getenv(
        "FAISS_INDEX_PATH", "backend/vectorstore/faiss_index"
    )

    # ----- Database -----
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "customer_support_ai")

    # ----- Auth -----
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

    # ----- App -----
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")


# Single shared instance imported across the whole backend
settings = Settings()
