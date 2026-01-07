"""
Pydantic schemas for health endpoints.

Keeping response models here keeps app/main.py clean and scalable as the API grows.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class HealthDBResponse(BaseModel):
    status: str
    db: str
