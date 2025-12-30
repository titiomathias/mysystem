from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum, IntEnum
from datetime import datetime
from typing import Optional


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class Attributes(BaseModel):
    strength: int = Field(alias="str")
    agility: int = Field(alias="agi")
    intelligence: int = Field(alias="int")
    stamina: int = Field(alias="con")
    wisdom: int = Field(alias="wis")
    charisma: int = Field(alias="cha")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class UserProfile(BaseModel):
    username: str
    email: EmailStr
    level: int
    created_at: datetime
    attributes: Attributes

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True
    )


class TaskFrequency(str, Enum):
    once = "once"
    daily = "daily"
    weekly = "weekly"
    habit = "habit"


class TaskStatus(IntEnum):
    PENDING = 0
    DONE = 1


class TaskModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category: str
    frequency: TaskFrequency
    base_xp: int
    status: TaskStatus

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True
    )


