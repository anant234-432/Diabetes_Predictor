"""
Base class for SQLAlchemy ORM models.

All models should inherit from Base so Alembic can discover them and generate migrations.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
    