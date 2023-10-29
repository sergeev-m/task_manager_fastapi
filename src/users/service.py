from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from core.errors import NoRowsFoundError, MultipleRowsFoundError
from core.service import BaseService
from src.users.repository import user_repository
from src.users.schemas import UserCreate


class UserService(BaseService):
    async def get_user_by_credentials(self, login: str):
        try:
            return await self.repository.get_one(email=login)
        except (NoRowsFoundError, MultipleRowsFoundError):
            raise HTTPException(HTTP_401_UNAUTHORIZED, 'Invalid credentials')

    async def create_user(self, user: UserCreate):
        return await self.create(user)


user_service = UserService(repository=user_repository)
