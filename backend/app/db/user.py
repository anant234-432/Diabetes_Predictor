"""
DB helpers for users.

Keeping DB logic here avoids fat endpoints and makes testing easier later.
"""

from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password_hash: str) -> User:
    """Create a new user."""
    new_user = User(email=email, password_hash=password_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

