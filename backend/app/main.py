"""
FastAPI entrypoint.

- /health    : API liveness
- /health/db : DB connectivity (Postgres)
"""

from fastapi import FastAPI, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.api.v1.routes.patients import router as patients_router
from app.db.session import get_db
from app.schemas.health import HealthResponse, HealthDBResponse
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.patient_records import router as records_router



app = FastAPI(title="Diabetes Predictor API", version="0.1.0")

app.include_router(records_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(patients_router, prefix="/api/v1")

@app.get("/health", status_code=status.HTTP_200_OK, response_model=HealthResponse, tags=["health"])
def health():
    return {"status": "ok"}


@app.get("/health/db", status_code=status.HTTP_200_OK, response_model=HealthDBResponse, tags=["health"])
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "db": "connected"}
