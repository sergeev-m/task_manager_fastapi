from core.db.session import AsyncDatabaseSession
from core.repository import BaseRepository
from src.task.models import Task
from src.task.schemas import TaskCreate


class TaskRepository(BaseRepository):
    model = TaskCreate

    async def create_superuser(self, data: dict):
        data["is_superuser"] = True
        return await self.create(data)


user_repository = TaskRepository(db_session=AsyncDatabaseSession().session)
