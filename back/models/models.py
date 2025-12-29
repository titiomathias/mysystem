from discord import Enum
from pydantic import BaseModel, EmailStr
from enum import Enum, IntEnum
from datetime import datetime, timedelta
from typing import Optional


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class Attributes(BaseModel):
    strength: int
    agility: int
    intelligence: int
    stamina: int
    wisdom: int
    charisma: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            "strength": "str",
            "agility": "agi",
            "intelligence": "int",
            "stamina": "con",
            "wisdom": "wis",
            "charisma": "cha",
        }


class UserProfile(BaseModel):
    username: str
    email: EmailStr
    level: int
    created_at: datetime
    attributes: Attributes
    class Config:
        orm_mode = True


class TaskFrequency(str, Enum):
    once = "once"
    daily = "daily"
    weekly = "weekly"
    habit = "habit"


class TaskStatus(IntEnum):
    PENDING = 0
    DONE = 1


class Task(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category: str
    frequency: TaskFrequency
    base_xp: int
    status: TaskStatus

    class Config:
        orm_mode = True


