"""
FastAPI entrypoint.

- /health    : API liveness
- /health/db : DB connectivity (Postgres)
"""

from fastapi import FastAPI, Depends, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.health import HealthResponse, HealthDBResponse

app = FastAPI(title="Diabetes Predictor API", version="0.1.0")


@app.get("/health", status_code=status.HTTP_200_OK, response_model=HealthResponse, tags=["health"])
def health():
    return {"status": "ok"}


@app.get("/health/db", status_code=status.HTTP_200_OK, response_model=HealthDBResponse, tags=["health"])
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "db": "connected"}
