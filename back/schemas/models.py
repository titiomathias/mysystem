from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum, IntEnum
from datetime import datetime
from typing import Optional


class AttributeType(str, Enum):
    cha = "cha"
    wis = "wis"
    int = "int"
    str = "str"
    agi = "agi"
    con = "con"


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

    current_xp: Optional[int] = None
    next_level_xp: Optional[int] = None

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
    PENDING = False
    DONE = True


class TaskAttributeCreate(BaseModel):
    attribute: AttributeType
    value: int


class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    frequency: TaskFrequency
    base_xp: int
    attributes: list[TaskAttributeCreate]


class TaskOut(BaseModel):
    id: int
    name: str
    description: str
    category: str
    frequency: TaskFrequency
    base_xp: int
    status: TaskStatus

    last_completed_at: Optional[datetime]
    streak_count: int
    best_streak: int

    attributes: list[TaskAttributeCreate]

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    frequency: Optional[TaskFrequency] = None
    base_xp: Optional[int] = None
    status: Optional[TaskStatus] = None
