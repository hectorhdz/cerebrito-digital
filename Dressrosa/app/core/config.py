"""Core application settings with environment separation."""

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    environment: str
    debug: bool
    api_v1_prefix: str
    database_url: str
    log_level: str
    secret_key: str
    access_token_expire_minutes: int
    session_cookie_name: str


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _environment_files(environment: str) -> list[Path]:
    files: list[Path] = [ROOT_DIR / ".env"]
    normalized = environment.lower()
    if normalized == "test":
        files.append(ROOT_DIR / ".env.test")
    elif normalized == "production":
        files.append(ROOT_DIR / ".env.prod")
    return files


def _load_environment_files() -> str:
    environment = os.getenv("ENVIRONMENT", "development").strip().lower()
    for env_file in _environment_files(environment):
        load_dotenv(dotenv_path=env_file, override=True)
    return os.getenv("ENVIRONMENT", environment).strip().lower()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    environment = _load_environment_files()

    return Settings(
        app_name=os.getenv("APP_NAME", "Dressrosa"),
        app_version=os.getenv("APP_VERSION", "0.1.0"),
        environment=environment,
        debug=_parse_bool(os.getenv("DEBUG"), default=(environment != "production")),
        api_v1_prefix=os.getenv("API_V1_PREFIX", "/api/v1"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./dressrosa.db"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        secret_key=os.getenv("SECRET_KEY", "dressrosa-dev-secret-key-change-me"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120")),
        session_cookie_name=os.getenv("SESSION_COOKIE_NAME", "dressrosa_session"),
    )


settings = get_settings()
