# =========================================================
# backend/database/db.py
# -----------------------------------------------------------
# Handles the MongoDB connection and all read/write operations
# related to users and conversation memory (Module 8).
# Uses Motor (the async MongoDB driver) so DB calls never block
# FastAPI's event loop.
# =========================================================
from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings
from backend.models.schemas import ConversationTurn
from datetime import datetime
from typing import List
import certifi

# Single Mongo client shared by the whole app (created once at import time).
# tlsCAFile=certifi.where() fixes SSL handshake failures against MongoDB
# Atlas that are common on Linux systems with outdated/mismatched OpenSSL
# root certificates.
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
# Collections
users_collection = db["users"]
conversations_collection = db["conversations"]


async def save_conversation_turn(turn: ConversationTurn) -> None:
    """Persist a single message (user or assistant) tied to a session_id."""
    await conversations_collection.insert_one(turn.model_dump())


async def get_conversation_history(session_id: str, limit: int = 20) -> List[dict]:
    """
    Retrieve the most recent turns for a session, oldest first.
    Used to give the LLM short-term memory of the ongoing chat.
    """
    cursor = (
        conversations_collection.find({"session_id": session_id})
        .sort("timestamp", -1)
        .limit(limit)
    )
    turns = await cursor.to_list(length=limit)
    return list(reversed(turns))  # reverse so oldest comes first


async def create_user(name: str, email: str, hashed_password: str) -> str:
    """Insert a new user and return the inserted document's id as a string."""
    result = await users_collection.insert_one(
        {
            "name": name,
            "email": email,
            "hashed_password": hashed_password,
            "created_at": datetime.utcnow(),
        }
    )
    return str(result.inserted_id)


async def get_user_by_email(email: str):
    """Fetch a user document by email, or None if it doesn't exist."""
    return await users_collection.find_one({"email": email})
