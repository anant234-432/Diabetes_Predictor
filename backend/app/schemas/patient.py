"""
Patient schemas.

- PatientCreate: payload to create a patient profile (linked to current user)
- PatientUpdate: partial updates
- PatientOut: response model
"""

from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    full_name: str = Field(..., max_length=120)
    age: int = Field(..., ge=0, le=130)
    sex: str = Field(..., max_length=20)


class PatientUpdate(BaseModel):
    full_name: str | None = Field(None, max_length=120)
    age: int | None = Field(None, ge=0, le=130)
    sex: str | None = Field(None, max_length=20)


class PatientOut(BaseModel):
    id: int
    user_id: int
    full_name: str
    age: int
    sex: str

    class Config:
        from_attributes = True