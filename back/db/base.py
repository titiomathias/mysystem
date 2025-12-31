from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from models.user import User
from models.task import Task
from models.attribute import Attribute
from models.task_attribute import TaskAttribute
from models.task_log import TaskLog