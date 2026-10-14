# =========================================================
# backend/agents/faq.py
# -----------------------------------------------------------
# Module 5: FAQ Agent
# Handles: company policies, general questions, contact info.
# This is also the default/fallback agent when intent detection
# can't confidently match a specialized domain.
# =========================================================

from backend.agents.llm_client import generate_response

SYSTEM_PROMPT = """You are the General FAQ Agent for TechMart Electronics.
You answer general questions about company policies, shipping,
warranty, business hours, and how to contact the company.
Use ONLY the provided company knowledge base context to answer.
If the question is outside this scope, politely say so and suggest
which department could help.
"""


def handle(user_message: str, context: str) -> str:
    """Generate a general FAQ answer grounded in the RAG context."""
    return generate_response(SYSTEM_PROMPT, user_message, context)
