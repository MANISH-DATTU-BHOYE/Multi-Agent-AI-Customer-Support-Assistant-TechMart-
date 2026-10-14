# =========================================================
# backend/agents/technical.py
# -----------------------------------------------------------
# Module 5: Technical Support Agent
# Handles: login, password reset, installation, errors, bugs.
# =========================================================

from backend.agents.llm_client import generate_response

SYSTEM_PROMPT = """You are the Technical Support Agent for TechMart Electronics.
You specialize in: login problems, password resets, installation issues,
software errors, and bugs.
Use ONLY the provided company knowledge base context to answer.
Give clear, numbered troubleshooting steps whenever possible.
If the issue looks like a bug requiring engineering, say you will
escalate it and create a support ticket.
"""


def handle(user_message: str, context: str) -> str:
    """Generate a technical-support answer grounded in the RAG context."""
    return generate_response(SYSTEM_PROMPT, user_message, context)
