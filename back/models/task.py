from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, Boolean, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    description = Column(String(512), nullable=False)

    category = Column(String(32), nullable=False, default="common")

    frequency = Column(
        Enum("once", "daily", "weekly", "habit", name="task_frequency"),
        nullable=False,
        default="once"
    )

    base_xp = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)

    last_completed_at = Column(TIMESTAMP, nullable=True)

    streak_count = Column(Integer, nullable=False, default=0)
    best_streak = Column(Integer, nullable=False, default=0)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="tasks")

    attributes = relationship(
        "TaskAttribute",
        back_populates="task",
        cascade="all, delete-orphan"
    )

    logs = relationship(
        "TaskLog",
        back_populates="task",
        cascade="all, delete-orphan"
    )
