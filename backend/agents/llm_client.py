# =========================================================
# backend/agents/llm_client.py
# -----------------------------------------------------------
# Thin wrapper that calls a LOCAL Ollama model instead of OpenAI.
# This removes any API cost/quota/billing dependency entirely —
# the model runs on your own machine via the Ollama background
# server (default: http://localhost:11434).
#
# To switch back to OpenAI later, restore the previous version
# of this file (uses `from openai import OpenAI`).
# =========================================================

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"   # must match whatever you ran `ollama pull ` with


def generate_response(system_prompt: str, user_message: str, context: str = "") -> str:
    """
    Call the local Ollama server with a system prompt (defines the agent's
    persona/rules), the retrieved RAG context, and the user's message.
    """
    full_user_content = (
        f"Company knowledge base context:\n{context}\n\n"
        f"Customer question:\n{user_message}"
    )

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_user_content},
        ],
        "stream": False,          # get the full reply in one response, not token-by-token
        "options": {"temperature": 0.3},
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()   # raises an error if Ollama isn't running / request failed

    data = response.json()
    return data["message"]["content"]