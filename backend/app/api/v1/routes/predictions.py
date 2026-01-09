"""
Prediction routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.db.patient import get_patient_by_user_id
from app.db.patient_record import list_records_for_patient
from app.db.prediction import create_prediction
from app.db.audit_log import write_audit_log
from app.models.user import User
from app.schemas.prediction import PredictionCreate, PredictionOut

router = APIRouter(prefix="/predictions", tags=["predictions"])


def _stub_predict(glucose: int, bmi: float, age: int) -> tuple[int, float, str]:
    """
    Deterministic placeholder model.
    """
    score = (glucose / 200.0) + (bmi / 50.0) + (age / 100.0)
    probability = min(1.0, score / 3.0)
    prediction = 1 if probability >= 0.5 else 0

    explanation = "Top factors: glucose, bmi, age"
    return prediction, probability, explanation


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PredictionOut)
def create_my_prediction(
    _: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")

    records = list_records_for_patient(db, patient_id=patient.id, limit=1, offset=0)
    if not records:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No patient records found")

    record = records[0]

    prediction, probability, explanation = _stub_predict(
        glucose=record.glucose,
        bmi=record.bmi,
        age=record.age,
    )

    pred = create_prediction(
        db,
        patient_id=patient.id,
        prediction=prediction,
        probability=probability,
        model_version="stub-v1",
        explanation=explanation,
    )

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        action="PREDICT",
        resource="prediction",
        resource_id=pred.id,
    )

    return pred
