from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configuration for the application."""
    DB_HOST: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_SCHEMA: str | None = None

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

settings = Settings()