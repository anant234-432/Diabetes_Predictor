"""
PatientRecord table:
- Stores a snapshot of input features used for prediction.
- Allows keeping history of measurements (useful for charts and drift analysis).
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PatientRecord(Base):
    __tablename__ = "patient_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)

    # Timestamp of when this record was captured
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Features (Pima Indians Diabetes dataset style)
    pregnancies: Mapped[int] = mapped_column(nullable=False)
    glucose: Mapped[int] = mapped_column(nullable=False)
    blood_pressure: Mapped[int] = mapped_column(nullable=False)
    skin_thickness: Mapped[int] = mapped_column(nullable=False)
    insulin: Mapped[int] = mapped_column(nullable=False)
    bmi: Mapped[float] = mapped_column(nullable=False)
    diabetes_pedigree_function: Mapped[float] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)

    patient = relationship("Patient", back_populates="records")
