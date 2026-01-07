"""
User table:
- Stores auth identity (email + password hash) and role.
- Patient profile is linked 1:1 via Patient.user_id.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Email is unique and indexed for fast login lookup
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)

    # Store only a secure password hash (never plaintext)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Simple RBAC: "patient" or "admin" (we’ll enforce permissions in routes)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="patient")

    # One-to-one relationship: a user may have a single patient profile
    patient = relationship("Patient", back_populates="user", uselist=False)
