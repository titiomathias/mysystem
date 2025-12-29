from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Attribute(Base):
    __tablename__ = "attributes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    str = Column(Integer, nullable=False)
    agi = Column(Integer, nullable=False)
    con = Column(Integer, nullable=False)
    wis = Column(Integer, nullable=False)
    int = Column(Integer, nullable=False)
    cha = Column(Integer, nullable=False)

    # Relationships
    user = relationship("User", back_populates="attributes")
