# =========================================================
# backend/agents/product.py
# -----------------------------------------------------------
# Module 5: Product Agent
# Handles: features, pricing, comparisons, availability.
# =========================================================

from backend.agents.llm_client import generate_response

SYSTEM_PROMPT = """You are the Product Information Agent for TechMart Electronics.
You specialize in: product features, pricing tiers, product comparisons,
and stock/availability.
Use ONLY the provided company knowledge base context to answer.
Present comparisons as short bullet points when the customer asks
about more than one product or plan.
"""


def handle(user_message: str, context: str) -> str:
    """Generate a product-information answer grounded in the RAG context."""
    return generate_response(SYSTEM_PROMPT, user_message, context)
