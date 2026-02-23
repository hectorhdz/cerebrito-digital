"""Core application settings."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Dressrosa")
    environment: str = os.getenv("ENVIRONMENT", "development")
    api_v1_prefix: str = "/api/v1"


settings = Settings()
