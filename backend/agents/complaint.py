# =========================================================
# backend/agents/complaint.py
# -----------------------------------------------------------
# Module 5: Complaint Agent
# Handles: complaints, escalation, customer dissatisfaction.
# =========================================================

from backend.agents.llm_client import generate_response

SYSTEM_PROMPT = """You are the Complaints & Escalation Agent for TechMart Electronics.
Your job is to acknowledge the customer's frustration empathetically,
summarize their issue back to them, and explain the next steps
(including escalation to a human agent when appropriate).
Use the provided company knowledge base context for any policy details.
Never be dismissive. Always validate the customer's experience before
offering a resolution path.
"""


def handle(user_message: str, context: str) -> str:
    """Generate an empathetic complaint-handling answer grounded in RAG context."""
    return generate_response(SYSTEM_PROMPT, user_message, context)
