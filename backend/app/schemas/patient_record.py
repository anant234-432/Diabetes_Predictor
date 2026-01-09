"""
PatientRecord schemas.

- PatientRecordCreate: input feature snapshot
- PatientRecordOut: response model
"""

from datetime import datetime
from pydantic import BaseModel, Field


class PatientRecordCreate(BaseModel):
    pregnancies: int = Field(..., ge=0, le=50)
    glucose: int = Field(..., ge=0, le=500)
    blood_pressure: int = Field(..., ge=0, le=300)
    skin_thickness: int = Field(..., ge=0, le=200)
    insulin: int = Field(..., ge=0, le=2000)
    bmi: float = Field(..., ge=0, le=100)
    diabetes_pedigree_function: float = Field(..., ge=0, le=10)
    age: int = Field(..., ge=0, le=130)


class PatientRecordOut(BaseModel):
    id: int
    patient_id: int
    created_at: datetime

    pregnancies: int
    glucose: int
    blood_pressure: int
    skin_thickness: int
    insulin: int
    bmi: float
    diabetes_pedigree_function: float
    age: int

    class Config:
        from_attributes = True
