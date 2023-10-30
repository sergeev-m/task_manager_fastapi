from src.core.db.session import db
from src.core.repository import BaseRepository
from src.task.models import Task


class TaskRepository(BaseRepository):
    pass


task_repository = TaskRepository(model=Task, db_session=db.session)
