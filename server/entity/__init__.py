"""
A package with classes representing business entities
    when designing, it is meant as the most stable component of the system
"""
from .user_entity import (
    User,
    Role,
    EmailStatus,
    UserAccessError,
    PasswordError,
    UnconfirmedEmailError,
)
from .task import Task
from .folder import Folder
from .file import File
