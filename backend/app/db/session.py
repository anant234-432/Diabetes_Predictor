"""
Database session management.

- Creates the SQLAlchemy engine using DATABASE_URL.
- Provides SessionLocal factory.
- get_db() is used with FastAPI dependency injection to safely open/close sessions per request.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# pool_pre_ping=True helps detect stale connections and reconnect automatically
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# autocommit=False and autoflush=False are standard for explicit transaction control
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency to provide a DB session.

    Usage:
        def route(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
