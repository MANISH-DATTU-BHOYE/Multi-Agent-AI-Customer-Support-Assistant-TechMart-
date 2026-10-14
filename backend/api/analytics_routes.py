# =========================================================
# backend/api/analytics_routes.py
# -----------------------------------------------------------
# Module 9 (Optional): Analytics Dashboard.
# Aggregates simple metrics from the conversations collection:
# total conversations, agent usage breakdown, and escalation rate.
# =========================================================

from fastapi import APIRouter
from backend.database.db import conversations_collection

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
async def analytics_summary():
    """Return high-level usage stats for the admin dashboard."""
    total_conversations = len(
        await conversations_collection.distinct("session_id")
    )
    total_messages = await conversations_collection.count_documents({})

    # Count how many assistant replies were handled by each agent
    agent_usage = {}
    async for doc in conversations_collection.find({"role": "assistant"}):
        agents = (doc.get("agent") or "").split(",")
        for agent in agents:
            if agent:
                agent_usage[agent] = agent_usage.get(agent, 0) + 1

    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "agent_usage": agent_usage,
    }
