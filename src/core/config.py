from typing import Any
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

BASE_DIR = Path(__file__).resolve().parent.parent.parent

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """Configuration for the application."""
    DB_HOST: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_SCHEMA: str | None = None
    SECRET_KEY: str | None = "super-secret-change-this"
    JWT_ALGORITHM: str | None = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int | None = 3600

    @property
    def db_credentials(self) -> dict[str, Any]:
        return {
            "host": self.DB_HOST,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "schema": self.DB_SCHEMA,
        }

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

settings = Settings()