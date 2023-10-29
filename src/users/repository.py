from src.core.db.session import AsyncDatabaseSession
from src.core.repository import BaseRepository
from src.users.models import User


class UserRepository(BaseRepository):
    async def create_superuser(self, data: dict):
        data["is_superuser"] = True
        return await self.create(data)


user_repository = UserRepository(model=User, db_session=AsyncDatabaseSession().session)
