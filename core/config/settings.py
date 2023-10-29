import os

from pathlib import Path
from pydantic_settings import BaseSettings


BASE_PATH = Path(__file__).resolve().parent.parent.parent
LOG_PATH = os.path.join(BASE_PATH, 'logs')


class Settings(BaseSettings):

    # FastAPI
    API_V1_STR: str = '/api/v1'
    TITLE: str = 'Task Manager'
    VERSION: str = '0.1'
    DESCRIPTION: str = 'Task Manager API'
    DOCS_URL: str | None = f'{API_V1_STR}/docs'
    REDOCS_URL: str | None = f'{API_V1_STR}/redocs'
    DEBUG: bool
    SECRET_KEY: str

    # Log
    LOG_FILENAME: str = 'task_manager_fastapi.log'


settings = Settings()
