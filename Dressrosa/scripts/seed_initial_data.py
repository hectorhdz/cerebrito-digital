"""Seed default roles and initial admin user.

Usage:
    py -3 scripts/seed_initial_data.py
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.models.user_role import UserRole
from app.modules.auth.security import hash_password
from app.modules.leaves.service import (
    ensure_default_leave_policies,
    ensure_default_leave_subtypes,
    ensure_default_leave_types,
)

DEFAULT_ROLES = ["employee", "manager", "hr", "admin"]
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = "admin@dressrosa.local"
DEFAULT_ADMIN_FULL_NAME = "System Administrator"
DEFAULT_ADMIN_PASSWORD = "Test123"


def ensure_role(db: Session, role_name: str) -> Role:
    existing_role = db.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
    if existing_role is not None:
        return existing_role

    role = Role(name=role_name)
    db.add(role)
    db.flush()
    return role


def ensure_admin_user(db: Session) -> User:
    existing_user = db.execute(select(User).where(User.username == DEFAULT_ADMIN_USERNAME)).scalar_one_or_none()
    if existing_user is not None:
        return existing_user

    admin_user = User(
        username=DEFAULT_ADMIN_USERNAME,
        email=DEFAULT_ADMIN_EMAIL,
        full_name=DEFAULT_ADMIN_FULL_NAME,
        password_hash=hash_password(DEFAULT_ADMIN_PASSWORD),
        active=True,
    )
    db.add(admin_user)
    db.flush()
    return admin_user


def ensure_user_role(db: Session, user_id: str, role_id: str) -> None:
    mapping = db.execute(
        select(UserRole).where(UserRole.user_id == user_id, UserRole.role_id == role_id)
    ).scalar_one_or_none()
    if mapping is None:
        db.add(UserRole(user_id=user_id, role_id=role_id))


def seed() -> None:
    db: Session = SessionLocal()
    try:
        roles = {role_name: ensure_role(db, role_name) for role_name in DEFAULT_ROLES}
        admin_user = ensure_admin_user(db)
        ensure_user_role(db, admin_user.id, roles["admin"].id)
        ensure_default_leave_types(db)
        ensure_default_leave_subtypes(db)
        ensure_default_leave_policies(db)
        db.commit()

        print("Seed completed successfully.")
        print(f"Admin username: {DEFAULT_ADMIN_USERNAME}")
        print(f"Admin email: {DEFAULT_ADMIN_EMAIL}")
        print("Admin password: Test123")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
