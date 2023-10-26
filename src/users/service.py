from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import AsyncDatabaseSession
from core.service import BaseService
from src.users.models import User
from src.users.user_repository import user_repository


class UserService(BaseService):
    async def get_user_by_credentials(self, login: str) -> User:
        if "@" in login:
            return await self.retrieve(email=login)
        else:
            return await self.retrieve(username=login)


user_service = UserService(repository=user_repository)
