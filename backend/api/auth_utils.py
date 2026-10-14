# =========================================================
# backend/api/auth_utils.py
# -----------------------------------------------------------
# Module 1: User Authentication.
# Password hashing (passlib/bcrypt) and JWT creation/validation
# (python-jose), kept separate from the route handlers so they
# can be unit-tested in isolation.
# =========================================================

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from backend.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """One-way hash a plaintext password before storing it."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a login attempt's password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """Issue a signed JWT for a logged-in user (subject = user email/id)."""
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """Return the token's subject (user identifier) if valid, else None."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
