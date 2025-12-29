from sqlalchemy import (
    Column, Integer, Enum, ForeignKey, SmallInteger
)
from sqlalchemy.orm import relationship

from base import Base


class TaskAttribute(Base):
    __tablename__ = "task_attributes"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    attribute = Column(
        Enum("cha", "wis", "int", "str", "agi", "con", name="attribute_type"),
        primary_key=True
    )
    value = Column(SmallInteger, nullable=False)

    # Relationships
    task = relationship("Task", back_populates="attributes")
