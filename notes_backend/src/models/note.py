from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from src.core.database import Base


class Note(Base):
    """SQLAlchemy model for a note entity."""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
