"""
Patient routes.

Ownership rule:
- a user can only manage their own patient profile (patients.user_id == current_user.id)
- one patient profile per user (enforced by DB unique constraint)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.db.patient import (
    get_patient_by_user_id,
    create_patient_for_user,
    update_patient,
    delete_patient,
)
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientUpdate, PatientOut

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PatientOut)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = get_patient_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Patient profile already exists for this user")

    return create_patient_for_user(db, user_id=current_user.id, payload=payload)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=PatientOut)
def get_my_patient(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patient = get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    return patient


@router.put("/me", status_code=status.HTTP_200_OK, response_model=PatientOut)
def update_my_patient(payload: PatientUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patient = get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    return update_patient(db, patient, payload)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_patient(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patient = get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    delete_patient(db, patient)
    return None