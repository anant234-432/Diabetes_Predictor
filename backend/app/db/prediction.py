"""
DB helpers for Prediction.
"""

from sqlalchemy.orm import Session

from app.models.prediction import Prediction


def create_prediction(
    db: Session,
    patient_id: int,
    prediction: int,
    probability: float,
    model_version: str,
    explanation: str,
) -> Prediction:
    pred = Prediction(
        patient_id=patient_id,
        prediction=prediction,
        probability=probability,
        model_version=model_version,
        explanation=explanation,
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred