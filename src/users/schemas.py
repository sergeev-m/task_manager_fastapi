from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, PositiveInt, Field
from annotated_types import Le
from typing import Annotated


class AssignPermission(BaseModel):
    codename: str
    user_id: UUID


class CreatePermission(BaseModel):
    name: str
    codename: str


class User(BaseModel):
    id: UUID | None = None
    username: Annotated[str, Field(pattern=r'^[A-Za-z1-9_-]+$', min_length=6,
                                   max_length=50), None] = None
    email: EmailStr | None = None
    first_name: Annotated[str, Field(max_length=30)]
    last_name: Annotated[str, Field(max_length=30)]
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime
    permissions: list[AssignPermission]


class UserCreate(User):
    password: Annotated[str, Field(pattern=r'^[A-Za-z1-9]+$', min_length=2, max_length=30)]






