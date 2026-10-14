# =========================================================
# backend/api/chat_routes.py
# -----------------------------------------------------------
# Module 2 (Chat Interface backend) + Module 8 (Conversation Memory).
# This is the single endpoint the React frontend calls on every
# "send message" action. It saves the user's message, routes it
# through the multi-agent system, saves the assistant's reply,
# and returns the final aggregated answer.
# =========================================================

from fastapi import APIRouter
from backend.models.schemas import ChatRequest, ChatResponse, ConversationTurn
from backend.agents.router import route_query
from backend.database.db import save_conversation_turn, get_conversation_history

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Full request lifecycle:
      1. Persist the incoming user message (conversation memory)
      2. Route the query through the intent detector + specialized agents + RAG
      3. Persist the assistant's aggregated answer
      4. Return the answer to the frontend
    """
    # 1. store user turn
    await save_conversation_turn(
        ConversationTurn(session_id=request.session_id, role="user", content=request.message)
    )

    # 2. run the multi-agent + RAG pipeline
    response: ChatResponse = route_query(request.session_id, request.message)

    # 3. store assistant turn
    await save_conversation_turn(
        ConversationTurn(
            session_id=request.session_id,
            role="assistant",
            content=response.answer,
            agent=",".join(response.agent_used),
        )
    )

    # 4. return to frontend
    return response


@router.get("/history/{session_id}")
async def chat_history(session_id: str):
    """Return the full stored conversation for a given session (for reload/refresh)."""
    history = await get_conversation_history(session_id, limit=100)
    # Convert Mongo's ObjectId to string so it's JSON-serializable
    for turn in history:
        turn["_id"] = str(turn["_id"])
    return {"session_id": session_id, "history": history}
