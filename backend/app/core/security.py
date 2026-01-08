"""
Security helpers.

- Password hashing/verifying using bcrypt via passlib.
- JWT create/decode helpers.
- Dependency to get the current user from a Bearer token.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User

# bcrypt is a strong hashing algorithm suitable for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 bearer scheme (FastAPI will read Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(password: str) -> str:
    """Hash a plaintext password for storage."""
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password is too long (bcrypt limit is 72 bytes).")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """Create a JWT access token."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode a JWT token. Raises 401 if invalid."""
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise CREDENTIALS_EXCEPTION


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """FastAPI dependency: returns the authenticated User or raises 401."""
    payload = decode_access_token(token)

    sub = payload.get("sub")
    if sub is None:
        raise CREDENTIALS_EXCEPTION

    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        raise CREDENTIALS_EXCEPTION

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise CREDENTIALS_EXCEPTION

    return user
