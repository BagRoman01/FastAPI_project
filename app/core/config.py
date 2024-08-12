import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="C:/Users/roman/Desktop/Python_projects/WEB_Project/.env")
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    CURRENCY_API_KEY: str
    MODE: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def __init__(self):
        super().__init__()
        if not self.SECRET_KEY:
            self.generate_secret_key()

    def generate_secret_key(self) -> None:
        self.SECRET_KEY = secrets.token_urlsafe(32)


settings = Settings()
