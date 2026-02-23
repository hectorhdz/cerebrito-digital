"""User management service for HR/Admin CRUD operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.modules.auth.security import hash_password


class UserAlreadyExistsError(Exception):
    pass


def list_users(db: Session) -> list[User]:
    stmt = select(User).order_by(User.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def get_user(db: Session, user_id: str) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def _ensure_unique_fields(db: Session, username: str, email: str, exclude_user_id: str | None = None) -> None:
    username_stmt = select(User).where(User.username == username)
    email_stmt = select(User).where(User.email == email)

    if exclude_user_id:
        username_stmt = username_stmt.where(User.id != exclude_user_id)
        email_stmt = email_stmt.where(User.id != exclude_user_id)

    existing_username = db.execute(username_stmt).scalar_one_or_none()
    if existing_username is not None:
        raise UserAlreadyExistsError("Username already exists")

    existing_email = db.execute(email_stmt).scalar_one_or_none()
    if existing_email is not None:
        raise UserAlreadyExistsError("Email already exists")


def create_user(
    db: Session,
    username: str,
    email: str,
    full_name: str,
    password: str,
    active: bool = True,
) -> User:
    _ensure_unique_fields(db, username=username, email=email)

    user = User(
        username=username.strip(),
        email=email.strip().lower(),
        full_name=full_name.strip(),
        password_hash=hash_password(password),
        active=active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(
    db: Session,
    user_id: str,
    username: str,
    email: str,
    full_name: str,
    active: bool,
    password: str | None = None,
) -> User | None:
    user = get_user(db, user_id)
    if user is None:
        return None

    _ensure_unique_fields(db, username=username, email=email, exclude_user_id=user_id)

    user.username = username.strip()
    user.email = email.strip().lower()
    user.full_name = full_name.strip()
    user.active = active
    if password:
        user.password_hash = hash_password(password)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> bool:
    user = get_user(db, user_id)
    if user is None:
        return False

    db.delete(user)
    db.commit()
    return True
