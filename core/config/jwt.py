from pydantic_settings import BaseSettings


class ConfigToken(BaseSettings):
    ALGORITHM: str
    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int
    REFRESH_TOKEN_ROTATE_MIN_LIFETIME: int


config_token = ConfigToken()
