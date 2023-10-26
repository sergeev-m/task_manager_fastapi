from core.db.session import AsyncDatabaseSession
from core.repository import BaseRepository
from src.users.models import User


class UserRepository(BaseRepository):
    model: User = User

    async def create_superuser(self, data: dict):
        data["is_superuser"] = True
        return await self.create(data)


user_repository = UserRepository(db_session=AsyncDatabaseSession().session)
