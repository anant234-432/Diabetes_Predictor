"""
Patient record routes.

Ownership rule:
- user can only manage records for their own patient profile
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.db.patient import get_patient_by_user_id
from app.db.patient_record import create_record, get_record_by_id, list_records_for_patient, delete_record
from app.models.user import User
from app.schemas.patient_record import PatientRecordCreate, PatientRecordOut

router = APIRouter(prefix="/records", tags=["patient-records"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PatientRecordOut)
def create_patient_record(payload: PatientRecordCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patient = get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    return create_record(db, patient_id=patient.id, payload=payload)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[PatientRecordOut])
def list_my_records(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    patient = get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    return list_records_for_patient(db, patient_id=patient.id, limit=limit, offset=offset)


@router.get("/{record_id}", status_code=status.HTTP_200_OK, response_model=PatientRecordOut)
def get_my_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patient = get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")

    record = get_record_by_id(db, record_id)
    if not record or record.patient_id != patient.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_record(record_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    patient = get_patient_by_user_id(db, current_user.id)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")

    record = get_record_by_id(db, record_id)
    if not record or record.patient_id != patient.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    delete_record(db, record)
    return None
