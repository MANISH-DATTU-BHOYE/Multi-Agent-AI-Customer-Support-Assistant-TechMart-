# =========================================================
# backend/agents/intent_detector.py
# -----------------------------------------------------------
# Module 3: Intent Detection Agent.
# Classifies a customer message into one or more of:
#   billing, technical, product, complaint, faq
# A query CAN map to multiple intents at once, e.g.
#   "I paid yesterday but Premium is still locked."
#   -> ["billing", "technical"]   (matches Module 4's example)
#
# For simplicity/portability this uses fast keyword matching so
# the project runs with zero extra API calls. Swap the body of
# `detect_intent()` for an LLM-classification call if you want
# smarter detection - the function signature stays the same.
# =========================================================

from backend.models.schemas import IntentResult

# Keyword lexicon per agent domain - easy for students to extend
INTENT_KEYWORDS = {
    "billing": [
        "pay", "paid", "payment", "invoice", "subscription", "refund",
        "charge", "billing", "renew", "price", "premium", "plan",
    ],
    "technical": [
        "error", "bug", "crash", "login", "password", "install",
        "installation", "not working", "locked", "reset", "issue",
        "problem", "loading",
    ],
    "product": [
        "feature", "compare", "comparison", "available", "availability",
        "specs", "specification", "does it support", "pricing tier",
    ],
    "complaint": [
        "complain", "complaint", "unhappy", "disappointed", "angry",
        "escalate", "manager", "terrible", "worst", "unacceptable",
    ],
    "faq": [
        "policy", "hours", "contact", "location", "shipping",
        "warranty", "how do i", "what is your",
    ],
}


def detect_intent(message: str) -> IntentResult:
    """
    Scan the message for domain keywords and return every domain
    that matched (supports multi-agent routing), plus a confidence
    score based on how many keywords were found.
    """
    message_lower = message.lower()
    matched_intents = []
    total_hits = 0

    for domain, keywords in INTENT_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in message_lower)
        if hits > 0:
            matched_intents.append(domain)
            total_hits += hits

    # Fall back to the general FAQ agent if nothing matched
    if not matched_intents:
        matched_intents = ["faq"]
        confidence = 0.3
    else:
        # crude confidence heuristic: more keyword hits -> higher confidence
        confidence = min(0.5 + 0.1 * total_hits, 0.99)

    return IntentResult(intents=matched_intents, confidence=confidence)
