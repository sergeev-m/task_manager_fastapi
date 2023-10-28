from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

# from src.task.schemas import Task


class AssignPermission(BaseModel):
    codename: str
    user_id: UUID


class CreatePermission(BaseModel):
    name: str
    codename: str


class UserNameMixin:
    username: Annotated[str, Field(pattern=r'^[A-Za-z1-9_-]+$', min_length=4, max_length=50)]


class PasswordMixin:
    password: Annotated[str, Field(pattern=r'^[A-Za-z1-9]+$', min_length=8, max_length=30)]


class EmailMixin:
    email: EmailStr


class UserCreate(BaseModel, UserNameMixin, EmailMixin, PasswordMixin):
    pass


class User(BaseModel, UserNameMixin, EmailMixin):
    id: UUID | None = None
    first_name: Annotated[str, Field(max_length=30)] | None = None
    last_name: Annotated[str, Field(max_length=30)] | None = None
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime
    permissions: list[AssignPermission]
    # tasks: list[Task]
