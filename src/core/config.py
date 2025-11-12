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

    db_credentials = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "schema": DB_SCHEMA
    }

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

settings = Settings()