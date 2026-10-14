# =========================================================
# backend/api/auth_routes.py
# -----------------------------------------------------------
# Module 1: User Authentication -> Login, Register, Session mgmt.
# =========================================================

from fastapi import APIRouter, HTTPException
from backend.models.schemas import UserRegister, UserLogin, Token
from backend.database.db import create_user, get_user_by_email
from backend.api.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token)
async def register(user: UserRegister):
    """Create a new account. Rejects duplicate emails."""
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed = hash_password(user.password)
    await create_user(user.name, user.email, hashed)

    token = create_access_token(subject=user.email)
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Validate credentials and issue a JWT session token."""
    user = await get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token(subject=credentials.email)
    return Token(access_token=token)
