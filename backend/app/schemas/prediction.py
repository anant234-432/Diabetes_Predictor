"""
Prediction schemas.
"""

from datetime import datetime
from pydantic import BaseModel


class PredictionCreate(BaseModel):
    """
    Run prediction using the latest patient record.
    (No payload required for now.)
    """
    pass


class PredictionOut(BaseModel):
    id: int
    patient_id: int
    created_at: datetime

    prediction: int
    probability: float
    model_version: str
    explanation: str

    class Config:
        from_attributes = True
