from sqlalchemy import (
    Column, Integer, String, MediumInteger, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(64), nullable=False)
    level = Column(MediumInteger, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    # Relationships
    tasks = relationship("Task", back_populates="user")
    attributes = relationship("Attribute", back_populates="user", uselist=False)
    task_logs = relationship("TaskLog", back_populates="user")
