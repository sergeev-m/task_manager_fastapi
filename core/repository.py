from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete, insert
from sqlalchemy.exc import (
    IntegrityError,
    MultipleResultsFound,
    NoResultFound,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.errors import (
    AlreadyExistError,
    DBError,
    MultipleRowsFoundError,
    NoRowsFoundError,
)
from core.models import Base


class AbstractRepository(ABC):
    model = None

    @abstractmethod
    async def all(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def filter(self, **filters):
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, pk: UUID, **kwargs):
        raise NotImplementedError


class BaseRepository[AlchemyModel: Base](AbstractRepository):
    model: AlchemyModel = None

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, data: dict) -> object:
        async with self.db_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            try:
                await session.commit()
            except IntegrityError:
                raise AlreadyExistError(
                    f"object {self.model.__name__} already exist or no related tables with it"
                )
            return res.scalar_one()

    async def update(self, id: UUID, data: dict):
        async with self.db_session() as session:
            if not data:
                raise DBError(
                    f"Passed empty dictionary for update method in model {self.model.__name__}"
                )
            stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
            try:
                res = await self.session.execute(stmt)
            except IntegrityError:
                raise AlreadyExistError(
                    f'object {self.model.__name__} already exist or no related tables with it'
                )
            return res.scalar_one()

    async def delete_one(self, id: UUID):
        async with self.db_session() as session:
            stmt = delete(self.model).where(self.model.id == id)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                raise NoRowsFoundError(
                    f'For model {self.model.__name__} with id: {id}'
                )
            await session.commit()
            return

    async def filter(
        self,
        filters: dict | None = None,
        order: dict | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ):
        async with self.db_session() as session:
            stmt = select(self.model)
            if filters:
                stmt = stmt.filter_by(**filters)
            if order:
                stmt = stmt.order_by(order)
            if limit:
                stmt = stmt.limit(limit)
            if offset:
                stmt = stmt.offset(offset)
            row = await session.execute(stmt)
            return row.scalars().all()

    async def get_one(self, **filters):
        async with self.db_session() as session:
            stmt = select(self.model).filter_by(**filters)
            row = await self.session.execute(stmt)
            try:
                result = row.scalar_one()
            except NoResultFound:
                raise NoRowsFoundError(
                    f'For model {self.model.__name__} with next filters:{filters}'
                )
            except MultipleResultsFound:
                raise MultipleRowsFoundError(
                    f'For model {self.model.__name__} with next filters:{filters}'
                )
            return result

    async def all(self):
        return await self.filter()
