"""
DB helpers for Patient.

Keeps route handlers thin and consistent with db/user.py style.
"""

from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


def get_patient_by_user_id(db: Session, user_id: int) -> Patient | None:
    return db.query(Patient).filter(Patient.user_id == user_id).first()


def create_patient_for_user(db: Session, user_id: int, payload: PatientCreate) -> Patient:
    patient = Patient(
        user_id=user_id,
        full_name=payload.full_name,
        age=payload.age,
        sex=payload.sex,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def update_patient(db: Session, patient: Patient, payload: PatientUpdate) -> Patient:
    if payload.full_name is not None:
        patient.full_name = payload.full_name
    if payload.age is not None:
        patient.age = payload.age
    if payload.sex is not None:
        patient.sex = payload.sex

    db.commit()
    db.refresh(patient)
    return patient


def delete_patient(db: Session, patient: Patient) -> None:
    db.delete(patient)
    db.commit()