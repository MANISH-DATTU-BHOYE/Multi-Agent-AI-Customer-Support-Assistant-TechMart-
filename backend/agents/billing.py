# =========================================================
# backend/agents/billing.py
# -----------------------------------------------------------
# Module 5: Billing Agent
# Handles: payment issues, subscription, invoice, refund.
# =========================================================

from backend.agents.llm_client import generate_response

SYSTEM_PROMPT = """You are the Billing Support Agent for TechMart Electronics.
You specialize in: payments, subscriptions, invoices, and refunds.
Use ONLY the provided company knowledge base context to answer.
If the context does not contain the answer, say you will escalate
the issue to a human billing specialist. Be concise, polite, and precise
about amounts, dates, and policy terms.
"""


def handle(user_message: str, context: str) -> str:
    """Generate a billing-specific answer grounded in the RAG context."""
    return generate_response(SYSTEM_PROMPT, user_message, context)
