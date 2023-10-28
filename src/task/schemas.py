from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Annotated

# from src.users.schemas import User


class TaskCreate(BaseModel):
    title: Annotated[str, Field(max_length=50)]
    description: str


class TaskUpdate(TaskCreate):
    completed: bool | None = False


class Task(TaskUpdate):
    id: UUID
    owner_id: UUID
    # owner: list[User]
    created_at: datetime
    updated_at: datetime
