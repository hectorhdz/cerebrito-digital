"""User management service for HR/Admin CRUD, role assignment, and org mapping."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.modules.auth.security import hash_password


class UserAlreadyExistsError(Exception):
    pass


class RoleNotFoundError(Exception):
    pass


class ManagerAssignmentError(Exception):
    pass


def list_users(db: Session) -> list[User]:
    stmt = select(User).order_by(User.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def list_roles(db: Session) -> list[Role]:
    stmt = select(Role).order_by(Role.name.asc())
    return list(db.execute(stmt).scalars().all())


def get_user(db: Session, user_id: str) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def get_user_roles(db: Session, user_id: str) -> list[Role]:
    stmt = (
        select(Role)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
        .order_by(Role.name.asc())
    )
    return list(db.execute(stmt).scalars().all())


def get_user_role_names(db: Session, user_id: str) -> list[str]:
    return [role.name for role in get_user_roles(db, user_id)]


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
    manager_id: str | None = None,
) -> User:
    _ensure_unique_fields(db, username=username, email=email)

    user = User(
        username=username.strip(),
        email=email.strip().lower(),
        full_name=full_name.strip(),
        password_hash=hash_password(password),
        active=active,
        manager_id=manager_id,
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
    manager_id: str | None,
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
    user.manager_id = manager_id
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


def assign_role_to_user(db: Session, user_id: str, role_name: str) -> bool:
    user = get_user(db, user_id)
    if user is None:
        return False

    role = db.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
    if role is None:
        raise RoleNotFoundError(f"Role '{role_name}' not found")

    existing = db.execute(
        select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role.id)
    ).scalar_one_or_none()
    if existing is not None:
        return True

    db.add(UserRole(user_id=user_id, role_id=role.id))
    db.commit()
    return True


def remove_role_from_user(db: Session, user_id: str, role_name: str) -> bool:
    user = get_user(db, user_id)
    if user is None:
        return False

    role = db.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
    if role is None:
        raise RoleNotFoundError(f"Role '{role_name}' not found")

    mapping = db.execute(
        select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role.id)
    ).scalar_one_or_none()
    if mapping is None:
        return True

    db.delete(mapping)
    db.commit()
    return True


def assign_manager_to_user(db: Session, user_id: str, manager_id: str | None) -> bool:
    user = get_user(db, user_id)
    if user is None:
        return False

    if manager_id in (None, ""):
        user.manager_id = None
        db.commit()
        return True

    if manager_id == user_id:
        raise ManagerAssignmentError("User cannot be their own manager")

    manager = get_user(db, manager_id)
    if manager is None or not manager.active:
        raise ManagerAssignmentError("Manager user not found or inactive")

    user.manager_id = manager.id
    db.commit()
    return True


def set_user_active_status(db: Session, user_id: str, active: bool) -> User | None:
    user = get_user(db, user_id)
    if user is None:
        return None

    user.active = active
    db.commit()
    db.refresh(user)
    return user
