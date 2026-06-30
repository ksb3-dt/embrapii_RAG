from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_version: str = "0.1.0"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    redis_url: str = ""
    qdrant_url: str = ""
    documents_dir: str = "/app/data/documents"


@lru_cache
def get_settings() -> Settings:
    return Settings()
