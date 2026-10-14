# Multi-Agent AI Customer Support Assistant (RAG + LLMs)[TECHMART ASSISTANT]


A web-based customer support assistant that routes customer queries to
specialized AI agents (Billing, Technical, Product, Complaint, FAQ),
grounded in a company knowledge base via Retrieval-Augmented Generation (RAG).

# Purpose of the Project

Modern businesses receive customer queries across many different concerns — billing disputes, technical failures, product questions, complaints, and routine policy questions — but most support systems still treat every query the same way, either routing everything to overworked human agents or to a single generic chatbot that lacks the accuracy and grounding to be trusted.

The purpose of this project is to demonstrate a realistic, working alternative: an AI support system that behaves the way a well-run support department already does — different specialists for different problems, all coordinated by someone who reads the ticket first and sends it to the right desk. Concretely, the purpose is to:

Automatically understand what a customer actually needs, even when a single message spans more than one issue.
Ground every answer in real company documentation, not the model's general/guessed knowledge, so responses are accurate and auditable.
Provide this as a working, deployable full-stack system (not just a prototype notebook), proving the architecture holds up end-to-end — from browser, to API, to database, to AI pipeline, and back.


# Project Aim

The project aims to answer one central question:

Can a coordinated system of specialized AI agents, combined with retrieval-augmented generation, resolve customer support queries more accurately and more scalably than a single general-purpose chatbot?

To answer that, the system was built with four specific aims:

Accuracy through specialization — each agent (Billing, Technical, Product, Complaint, FAQ) only needs to be good at one narrow domain, which is easier to prompt, easier to evaluate, and easier to improve than one agent trying to do everything.
Trustworthiness through grounding — by retrieving actual company documents before generating an answer (RAG), the system reduces hallucinated or made-up information, a critical requirement for anything customer-facing that touches money, warranties, or policy.
Continuity through memory — conversations are stored per session, so the assistant doesn't treat every message as if it's meeting the customer for the first time.
Scalability through architecture — the system is built with the same components a production company would use (FastAPI, a vector database, a document store, a real frontend), so the aim isn't just "does this work as a demo" but "does this design generalize to a real deployment."

# 3. Business Impact & Insights

3.1 Cost impact

Support teams typically spend the majority of their time on repetitive, low-complexity queries — refund status, shipping timelines, password resets, plan comparisons. A system like this can resolve a large share of those automatically, meaning human agents spend their time only on genuinely complex or emotionally sensitive cases (which the Complaint Agent is specifically designed to route toward escalation). This directly reduces cost-per-ticket and support staffing pressure, especially during demand spikes (e.g. sales events, product launches).

3.2 Consistency and compliance

Human agents vary in how they phrase policies, and mistakes in stated refund windows or warranty terms create real liability. Because every specialized agent answers using the same retrieved knowledge-base text, answers stay consistent across every conversation and every time of day — an operational insight most businesses value as much as raw cost savings.

3.3 Faster resolution, better customer experience

Multi-intent routing (e.g. a payment problem and a locked feature in the same sentence) means the customer doesn't have to split their issue into separate tickets or repeat themselves to different departments. This shortens time-to-resolution and reduces the frustration of being bounced between support queues — a common driver of poor customer satisfaction scores (CSAT/NPS).

3.4 Data as a byproduct — analytics insight

Because every conversation and every agent-invocation is logged (see the optional Analytics module), the business gains a continuously growing dataset of what customers actually struggle with most. Which agent gets invoked most often? Which queries get escalated most frequently? This turns a support tool into a feedback loop that can inform product fixes, clearer documentation, or pricing-page changes — insight that's normally invisible without instrumenting support conversations this way.

3.5 24/7 availability without proportional headcount growth

Unlike human support, this system doesn't need shifts, breaks, or overtime. For companies expanding into new time zones or scaling user volume, this decouples "hours of support coverage" from "headcount," which is a meaningful strategic and financial advantage as a company grows.

## Architecture

```
Customer → Web Chat Interface → Backend API Server
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                                ▼
             Intent Detection                 Conversation Memory
                     │
                     ▼
               Agent Router
                     │
   ┌─────────────┬───┴────────┬──────────────┐
   ▼              ▼           ▼              ▼
Billing       Technical    Product       Complaint     (+ FAQ fallback)
   │
   ▼
Retrieval System (RAG) → Vector Database (FAISS) → Company Documents
   │
   ▼
Response Aggregator → Final Response
```

## Folder Structure

```
customer-support-ai/
├── frontend/            React / Next.js chat UI
│   ├── components/       ChatWindow, MessageInput
│   ├── pages/             chat.jsx, login.jsx
│   ├── hooks/              useChat.js
│   ├── services/            api.js (Axios client)
│   └── styles/               Tailwind globals
│
├── backend/              FastAPI application
│   ├── api/               auth & chat & analytics routes
│   ├── agents/             billing, technical, product, complaint, faq, router
│   ├── rag/                 chunker, retriever, ingest script
│   ├── embeddings/            sentence-transformers wrapper
│   ├── vectorstore/            FAISS wrapper
│   ├── database/                 MongoDB (Motor) access layer
│   ├── models/                    Pydantic schemas
│   └── main.py                     app entrypoint
│
├── knowledge_base/       Sample TechMart Electronics company documents
├── datasets/             Optional public datasets (see datasets/README.md)
├── requirements.txt
├── .env.example
└── README.md
```

## Frontend — where it starts

frontend/pages/chat.jsx
Renders the main chat page and generates a unique session ID per browser tab.
Loads ChatWindow and MessageInput and connects them via the useChat hook.

frontend/components/MessageInput.jsx
Captures what the user types and detects the Send click or Enter key.
Passes the typed text up to useChat.js to begin the send process.

frontend/hooks/useChat.js
Adds the user's message to the UI instantly and calls the backend API.
Waits for the reply, then updates the chat state so ChatWindow can render it.

frontend/services/api.js
Holds the single Axios client and the exact backend URL for every network call.
Sends the POST /chat/ request and returns the parsed JSON response back to the hook.

frontend/components/ChatWindow.jsx
Displays every message bubble, the typing indicator, and auto-scrolls to the latest one.
Shows which agent(s) answered and which knowledge-base sources were used.

2. Backend entry — where the request lands

backend/main.py
Starts the FastAPI server and enables CORS so the frontend can call it.
Registers every route file (auth, chat, analytics) into one running app.

backend/config.py
Loads .env once at startup into a single shared settings object.
Every other backend file reads config through settings, never os.getenv() directly.

backend/models/schemas.py
Defines the exact structure of every request and response using Pydantic.
FastAPI uses these to validate incoming data and auto-build the /docs page.

backend/api/chat_routes.py
Receives the incoming chat message and is the true entry point of the pipeline.
Saves the user's message, calls the agent router, saves the reply, returns it.

3. The multi-agent core — where the "thinking" happens

backend/agents/intent_detector.py
Scans the message for keywords to decide which domain(s) it belongs to.
Can return multiple intents at once, enabling true multi-agent routing.

backend/rag/retriever.py
Embeds the user's question into a vector using the same model as the documents.
Searches the FAISS index and returns the most relevant knowledge-base chunks.

backend/agents/router.py
Calls intent detection and RAG retrieval, then invokes every matched agent.
Merges all agent answers into one final reply and decides if escalation is needed.

backend/agents/billing.py / technical.py / product.py / complaint.py / faq.py
Each holds one specialized system prompt (persona) for its own domain.
Each calls llm_client.py with that persona plus the RAG context and the question.

backend/agents/llm_client.py
The only file that actually talks to the AI model (currently local Ollama).
Sends the prompt and returns the generated text back to whichever agent called it.

4. RAG setup — runs before any of the above, done once (or on update)

backend/rag/chunker.py
Splits a long knowledge-base document into small, overlapping text pieces.
Smaller chunks let the retriever find precise matches instead of whole-document noise.

backend/embeddings/embedder.py
Converts any text (document chunk or live question) into a numeric vector.
Uses the same model for both, so meaning can be compared accurately.

backend/vectorstore/faiss_store.py
Stores every document chunk's vector plus its original text and source file.
Performs the actual fast "find closest match" search during retrieval.

backend/rag/ingest.py
Reads every file in knowledge_base/, chunks it, embeds it, and saves it to FAISS.
Run manually once, and again any time a knowledge-base document changes.

5. Memory layer — runs alongside every request

backend/database/db.py
Connects to MongoDB and defines save/read functions for messages and users.
Called twice per chat turn — once for the user's message, once for the reply.

6. Supporting layer — not in the main chat flow

backend/api/auth_routes.py + auth_utils.py
Handles account registration and login, issuing JWT tokens for sessions.
Hashes passwords with bcrypt so raw passwords are never stored.

backend/api/analytics_routes.py
Reads the conversations collection to count total messages and agent usage.
Powers an optional dashboard showing which agents get invoked most often.

7. Knowledge source — not code, but essential

knowledge_base/*.txt
Plain text files containing TechMart's actual policies, pricing, and FAQs.
This is the "ground truth" that ingest.py turns into the searchable vector databas

## Setup Instructions

### 1. Backend (Python 3.11+)

```bash
cd customer-support-ai
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # then fill in OPENAI_API_KEY, MONGO_URI, etc.

# Make sure MongoDB is running locally, or point MONGO_URI at MongoDB Atlas.

# Build the vector database from the knowledge_base/ documents:
python -m backend.rag.ingest

# Start the API server:
uvicorn backend.main:app --reload
```

The API will be live at `http://localhost:8000`, with interactive docs at
`http://localhost:8000/docs`.

### 2. Frontend (Node.js 20+)

```bash
cd customer-support-ai/frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

The chat UI will be live at `http://localhost:3000/chat`.

## Key Concepts Demonstrated

- **Multi-Agent Systems** – `backend/agents/router.py` dispatches a query to
  one or more specialized agents based on detected intent.
- **RAG** – `backend/rag/` chunks documents, embeds them, stores them in FAISS,
  and retrieves relevant context at query time.
- **Vector Databases** – `backend/vectorstore/faiss_store.py`.
- **LLM Integration** – `backend/agents/llm_client.py` (OpenAI by default;
  swap for Gemini/Llama/Hugging Face).
- **Full-Stack Development** – FastAPI backend + Next.js/React frontend.
- **Cloud Deployment** – see the "Deployment" section of the project brief
  (Vercel for frontend, Railway/Render for backend, MongoDB Atlas for the DB).

## Running Tests / Sanity Checks

```bash
# Confirm the backend boots and health check responds:
curl http://localhost:8000/health

# Confirm the vector store was built:
python -c "from backend.vectorstore.faiss_store import vector_store; vector_store.load(); print(vector_store.index.ntotal, 'vectors loaded')"
```

# Future Scope

The current system is a solid foundation; the following are natural next steps that would meaningfully increase its business value:

Smarter intent detection — replace keyword matching with a fine-tuned or LLM-based classifier trained on real historical support tickets, improving accuracy on ambiguous or informally worded queries.

Sentiment-aware routing — detect frustration or urgency in the message itself and prioritize/escalate accordingly, rather than relying only on keyword-based confidence.

Human-in-the-loop handoff — a live handoff mechanism where an escalated conversation transfers seamlessly to a human agent, including full conversation context, instead of just flagging escalation.

Multilingual support — extending the agents and RAG pipeline to operate in multiple languages would let one system serve global customer bases without duplicating support infrastructure per region.

Voice channel integration — connecting this same agent/RAG backbone to a voice interface (phone support) would extend the same architecture to a channel that currently drives a large share of support costs.

Continuous knowledge-base syncing — instead of manually re-running ingestion, connect this pipeline directly to a company's live CMS, product database, or policy documents so the knowledge base updates automatically as company information changes.

Feedback-driven agent improvement — using customer satisfaction ratings per conversation to identify which agent's prompts or retrieved context are underperforming, and iterating on those specifically.

Ticketing system integration — auto-creating tickets in tools like Zendesk or Freshdesk directly from escalated conversations, so nothing falls through the cracks between the AI layer and the human support team.

Enterprise-grade deployment — containerizing the system (Docker), adding rate-limiting, and deploying with horizontal scaling would move this from "capstone project" to something closer to production-ready infrastructure.

