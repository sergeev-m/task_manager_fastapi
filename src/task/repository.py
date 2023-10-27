from core.db.session import AsyncDatabaseSession
from core.repository import BaseRepository
from src.task.models import Task


class TaskRepository(BaseRepository):
    pass


task_repository = TaskRepository(model=Task, db_session=AsyncDatabaseSession().session)
