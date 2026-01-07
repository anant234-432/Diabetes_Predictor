"""
Prediction table:
- Stores the output of model inference for a patient.
- Stores model_version so results remain traceable after future retraining.
- explanation is a short text for "why" (we’ll populate later).
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Binary prediction: 0 = not diabetic, 1 = diabetic (for demo model)
    prediction: Mapped[int] = mapped_column(nullable=False)

    # Probability/confidence score (0.0 - 1.0)
    probability: Mapped[float] = mapped_column(nullable=False)

    # Model version/hash stored for traceability
    model_version: Mapped[str] = mapped_column(String(50), nullable=False, default="0.1.0")

    # Lightweight explanation (e.g., "Top factors: glucose, bmi, age")
    explanation: Mapped[str] = mapped_column(String(500), nullable=False, default="")

    patient = relationship("Patient", back_populates="predictions")
