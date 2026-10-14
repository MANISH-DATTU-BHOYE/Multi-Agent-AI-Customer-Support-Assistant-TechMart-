# =========================================================
# backend/agents/router.py
# -----------------------------------------------------------
# Module 4: Agent Router
# This is the orchestrator described in the architecture diagram:
#
#   Customer -> Web Chat -> Backend API -> Intent Detection
#            -> Agent Router -> [Billing | Technical | Product | Complaint | FAQ]
#            -> Retrieval System (RAG) -> Vector DB -> Company Documents
#            -> Response Aggregator -> Final Response
#
# Given a user's message, it:
#   1. Detects intent(s) via the Intent Detection Agent
#   2. Retrieves RAG context relevant to the message
#   3. Invokes every matched specialized agent
#   4. Aggregates their answers into one final response
#   5. Decides whether to escalate to a human
# =========================================================

from backend.agents.intent_detector import detect_intent
from backend.rag.retriever import retrieve_context, format_context_for_prompt
from backend.agents import billing, technical, product, complaint, faq
from backend.models.schemas import ChatResponse

# Maps an intent name to the function that handles it
AGENT_MAP = {
    "billing": billing.handle,
    "technical": technical.handle,
    "product": product.handle,
    "complaint": complaint.handle,
    "faq": faq.handle,
}

# Below this confidence, the router treats the query as unresolved
# and flags it for human escalation (Module 4 / Project Objective).
ESCALATION_CONFIDENCE_THRESHOLD = 0.35


def route_query(session_id: str, message: str) -> ChatResponse:
    """
    Main orchestration entrypoint used by the /chat API route.
    Returns a fully-formed ChatResponse ready to send to the frontend.
    """
    # Step 1: figure out which domain(s) this query belongs to
    intent_result = detect_intent(message)

    # Step 2: retrieve supporting context from the vector database (RAG)
    retrieved_chunks = retrieve_context(message, top_k=4)
    context_text = format_context_for_prompt(retrieved_chunks)
    sources = sorted({chunk["source"] for chunk in retrieved_chunks})

    # Step 3: invoke every matched agent and collect their answers
    agent_answers = []
    for intent in intent_result.intents:
        agent_fn = AGENT_MAP.get(intent, faq.handle)
        answer = agent_fn(message, context_text)
        agent_answers.append(f"**{intent.capitalize()} Agent:** {answer}")

    # Step 4: aggregate multiple agent answers into a single response
    #         (Response Aggregator in the architecture diagram)
    final_answer = "\n\n".join(agent_answers)

    # Step 5: decide whether this should be escalated to a human
    escalated = intent_result.confidence < ESCALATION_CONFIDENCE_THRESHOLD

    return ChatResponse(
        session_id=session_id,
        agent_used=intent_result.intents,
        answer=final_answer,
        sources=sources,
        escalated=escalated,
    )
