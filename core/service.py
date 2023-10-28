from uuid import UUID
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from typing import NewType
from pydantic import BaseModel

from core.errors import (
    AlreadyExistError,
    DBError,
    MultipleRowsFoundError,
    NoRowsFoundError,
)
from core.repository import BaseRepository

PyModel = NewType('PyModel', BaseModel)


class BaseService:
    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository

    async def create(self, model: PyModel) -> object:
        try:
            return await self.repository.create(model.model_dump())
        except AlreadyExistError as e:
            raise HTTPException(HTTP_400_BAD_REQUEST, str(e))

    async def delete(self, pk: UUID):
        try:
            return await self.repository.delete_one(pk)
        except NoRowsFoundError as e:
            raise HTTPException(HTTP_404_NOT_FOUND, str(e))

    async def update(self, pk: UUID, model: PyModel):
        try:
            return await self.repository.update(pk, model.model_dump())
        except NoRowsFoundError as e:
            raise HTTPException(HTTP_404_NOT_FOUND, str(e))
        except (DBError, AlreadyExistError) as e:
            raise HTTPException(HTTP_400_BAD_REQUEST, str(e))

    async def retrieve(self, pk: UUID):
        try:
            return await self.repository.get_one(id=pk)
        except (NoRowsFoundError, MultipleRowsFoundError):
            raise HTTPException(HTTP_404_NOT_FOUND)

    async def filter(self, filters: dict = None):
        return await self.repository.filter(filters=filters)

    async def all(self):
        return await self.repository.all()
