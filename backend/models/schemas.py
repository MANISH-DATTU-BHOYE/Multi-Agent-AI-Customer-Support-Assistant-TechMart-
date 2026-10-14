# =========================================================
# backend/models/schemas.py
# -----------------------------------------------------------
# Pydantic models define the shape of every request/response
# that flows through the API. FastAPI uses these for automatic
# validation, serialization, and OpenAPI (Swagger) docs.
# =========================================================

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ---------- Auth ----------

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Chat ----------

class ChatRequest(BaseModel):
    """What the frontend sends every time the user hits 'send'."""
    session_id: str
    message: str


class ChatResponse(BaseModel):
    """What the backend returns after routing + RAG + LLM generation."""
    session_id: str
    agent_used: List[str]          # e.g. ["billing", "technical"] for multi-intent queries
    answer: str
    sources: List[str] = []        # knowledge-base documents used to ground the answer
    escalated: bool = False        # true if no agent was confident enough and a human is needed
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationTurn(BaseModel):
    """A single stored turn in the conversation-memory database."""
    session_id: str
    role: str          # "user" or "assistant"
    content: str
    agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ---------- Intent detection ----------

class IntentResult(BaseModel):
    intents: List[str]     # possible multiple simultaneous intents
    confidence: float
