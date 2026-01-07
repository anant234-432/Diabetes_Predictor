"""
Patient table:
- Stores patient profile information.
- Links to users table via user_id (1:1).
- Holds relationships to records (features snapshots) and predictions history.
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Unique constraint ensures one patient profile per user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Basic profile fields (keep minimal for demo; avoid sensitive PHI in public repos)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    sex: Mapped[str] = mapped_column(String(20), nullable=False)  # male/female/other

    # Relationships
    user = relationship("User", back_populates="patient")

    # Cascade delete: if patient is deleted, delete their records/predictions
    records = relationship("PatientRecord", back_populates="patient", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="patient", cascade="all, delete-orphan")
