"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Base Database Model

Responsibilities:
- Common fields for all tables
- ID generation
- Timestamp management
═══════════════════════════════════════════════════════════════════════
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_mixin

from database.engine import Base


# ==========================================================
# BASE MODEL MIXIN
# ==========================================================

@declarative_mixin
class TimestampMixin:
    """
    Adds created_at & updated_at to all models
    """

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==========================================================
# BASE ENTITY
# ==========================================================

class BaseModel(Base, TimestampMixin):
    """
    Base class for all database models
    """

    __abstract__ = True

    # Unique ID for all tables
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True,
        unique=True,
        nullable=False
    )

    def to_dict(self):
        """
        Convert model to dictionary
        """

        data = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, datetime):
                value = value.isoformat()

            data[column.name] = value

        return data
