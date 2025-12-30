from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship

from models.base import Base


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

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="tasks")
    attributes = relationship(
        "TaskAttribute",
        back_populates="task",
        cascade="all, delete-orphan"
    )
    logs = relationship("TaskLog", back_populates="task")
