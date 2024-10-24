import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    AnyHttpUrl,
    field_validator,
    ValidationError
)
from typing import (
    List,
    Union
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="C:/Users/roman/Desktop/Python_projects/WEB_Project/.env")

    # DATABASE
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # REDIS
    REDIS_HOST: str

    # AUTHENTICATION
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    def generate_secret_key(self) -> None:
        self.SECRET_KEY = secrets.token_urlsafe(32)

    # FRONTEND COMMUNICATION
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v

    # API SETTINGS
    CURRENCY_API_KEY: str

    # USING MODE
    MODE: str

    # DEPLOYMENT
    HOST: str
    PORT: int

    def __init__(self):
        super().__init__()
        if not self.SECRET_KEY:
            self.generate_secret_key()


try:
    settings = Settings()
except ValidationError as e:
    print(e)
