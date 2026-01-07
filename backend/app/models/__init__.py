"""
Model import aggregator.

Alembic autogenerate relies on models being imported so metadata is aware of them.
Import all models here, and ensure Alembic env.py imports app.models.
"""

from app.models.user import User
from app.models.patient import Patient
from app.models.patient_record import PatientRecord
from app.models.prediction import Prediction
from app.models.audit_log import AuditLog


__all__ = [
    "User",
    "Patient",
    "PatientRecord",
    "Prediction",
    "AuditLog"
]