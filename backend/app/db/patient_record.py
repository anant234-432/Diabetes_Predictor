"""
DB helpers for PatientRecord.
"""

from sqlalchemy.orm import Session

from app.models.patient_record import PatientRecord
from app.schemas.patient_record import PatientRecordCreate


def create_record(db: Session, patient_id: int, payload: PatientRecordCreate) -> PatientRecord:
    record = PatientRecord(
        patient_id=patient_id,
        pregnancies=payload.pregnancies,
        glucose=payload.glucose,
        blood_pressure=payload.blood_pressure,
        skin_thickness=payload.skin_thickness,
        insulin=payload.insulin,
        bmi=payload.bmi,
        diabetes_pedigree_function=payload.diabetes_pedigree_function,
        age=payload.age,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_record_by_id(db: Session, record_id: int) -> PatientRecord | None:
    return db.query(PatientRecord).filter(PatientRecord.id == record_id).first()


def list_records_for_patient(db: Session, patient_id: int, limit: int = 50, offset: int = 0) -> list[PatientRecord]:
    return (
        db.query(PatientRecord)
        .filter(PatientRecord.patient_id == patient_id)
        .order_by(PatientRecord.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def delete_record(db: Session, record: PatientRecord) -> None:
    db.delete(record)
    db.commit()
