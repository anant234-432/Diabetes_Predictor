"""
AuditLog table:
- Tracks important actions for security + traceability.
"""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    # Who performed the action (user id from users table)
    actor_user_id: Mapped[int] = mapped_column(nullable=False)

    # What happened (e.g., "LOGIN", "PREDICT", "UPDATE_PROFILE")
    action: Mapped[str] = mapped_column(String(100), nullable=False)

    # What resource was touched (e.g., "patient", "prediction")
    resource: Mapped[str] = mapped_column(String(100), nullable=False)

    # Which specific resource row (id)
    resource_id: Mapped[int] = mapped_column(nullable=False)

    # Optional request context (we’ll fill later from FastAPI request)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    user_agent: Mapped[str] = mapped_column(String(255), nullable=False, default="")
