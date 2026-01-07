"""
Security helpers.

- Password hashing/verifying using bcrypt via passlib.
- JWT helpers will be added later (Step 5C) to keep changes small and reviewable.
"""

from passlib.context import CryptContext

# bcrypt is a strong hashing algorithm suitable for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password for storage."""
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password is too long (bcrypt limit is 72 bytes).")
    return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)
