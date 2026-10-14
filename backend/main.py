# =========================================================
# backend/main.py
# -----------------------------------------------------------
# Application entrypoint. Wires together every module described
# in the project doc: auth, chat (multi-agent + RAG), analytics.
#
# Run locally with:
#   uvicorn backend.main:app --reload
# =========================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.api import auth_routes, chat_routes, analytics_routes

app = FastAPI(
    title="Multi-Agent AI Customer Support Assistant",
    description="RAG + multi-agent backend for customer support automation.",
    version="1.0.0",
)

# Allow the React/Next.js frontend (running on a different port/domain)
# to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register each feature's routes (kept in separate files for clarity)
app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(analytics_routes.router)


@app.get("/")
async def root():
    """Simple health-check endpoint."""
    return {"status": "ok", "service": "Multi-Agent AI Customer Support Assistant"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
