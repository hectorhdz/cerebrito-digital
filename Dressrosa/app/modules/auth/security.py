"""Authentication utilities for password and JWT handling."""

from datetime import datetime, timedelta, UTC

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> tuple[str, int]:
    settings = get_settings()
    expire_minutes = settings.access_token_expire_minutes
    expire_at = datetime.now(UTC) + timedelta(minutes=expire_minutes)
    payload = {"sub": subject, "exp": expire_at}
    token = jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)
    return token, expire_minutes * 60


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
