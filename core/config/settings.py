from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "task_manager"
    debug: bool
    secret_key: str
    version: str = "0.1"


settings = Settings()
