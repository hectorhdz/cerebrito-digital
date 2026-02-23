"""Leave type service for configurable leave taxonomy management."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.leave_type import LeaveType

DEFAULT_LEAVE_TYPES: tuple[dict[str, str], ...] = (
    {"code": "paid", "name": "Paid Leave", "description": "Paid leave allocations such as vacation and sick leave."},
    {"code": "unpaid", "name": "Unpaid Leave", "description": "Approved leave without salary payment."},
    {
        "code": "holiday_substitution",
        "name": "Holiday Substitution",
        "description": "Time-off taken in exchange for work performed on a holiday.",
    },
)


class LeaveTypeAlreadyExistsError(Exception):
    pass


def list_leave_types(db: Session) -> list[LeaveType]:
    stmt = select(LeaveType).order_by(LeaveType.created_at.asc())
    return list(db.execute(stmt).scalars().all())


def get_leave_type(db: Session, leave_type_id: str) -> LeaveType | None:
    stmt = select(LeaveType).where(LeaveType.id == leave_type_id)
    return db.execute(stmt).scalar_one_or_none()


def get_leave_type_by_code(db: Session, code: str) -> LeaveType | None:
    stmt = select(LeaveType).where(LeaveType.code == code.strip().lower())
    return db.execute(stmt).scalar_one_or_none()


def create_leave_type(
    db: Session,
    code: str,
    name: str,
    description: str | None = None,
    is_active: bool = True,
) -> LeaveType:
    normalized_code = code.strip().lower()
    if get_leave_type_by_code(db, normalized_code) is not None:
        raise LeaveTypeAlreadyExistsError(f"Leave type '{normalized_code}' already exists")

    leave_type = LeaveType(
        code=normalized_code,
        name=name.strip(),
        description=(description.strip() if description else None),
        is_active=is_active,
    )
    db.add(leave_type)
    db.commit()
    db.refresh(leave_type)
    return leave_type


def update_leave_type(
    db: Session,
    leave_type_id: str,
    code: str,
    name: str,
    description: str | None,
    is_active: bool,
) -> LeaveType | None:
    leave_type = get_leave_type(db, leave_type_id)
    if leave_type is None:
        return None

    normalized_code = code.strip().lower()
    existing_with_code = get_leave_type_by_code(db, normalized_code)
    if existing_with_code is not None and existing_with_code.id != leave_type_id:
        raise LeaveTypeAlreadyExistsError(f"Leave type '{normalized_code}' already exists")

    leave_type.code = normalized_code
    leave_type.name = name.strip()
    leave_type.description = description.strip() if description else None
    leave_type.is_active = is_active
    db.commit()
    db.refresh(leave_type)
    return leave_type


def delete_leave_type(db: Session, leave_type_id: str) -> bool:
    leave_type = get_leave_type(db, leave_type_id)
    if leave_type is None:
        return False

    db.delete(leave_type)
    db.commit()
    return True


def ensure_default_leave_types(db: Session, defaults: Sequence[dict[str, str]] | None = None) -> None:
    catalog = defaults or DEFAULT_LEAVE_TYPES

    for default in catalog:
        code = default["code"].strip().lower()
        existing = get_leave_type_by_code(db, code)
        if existing is not None:
            existing.name = default["name"].strip()
            existing.description = default.get("description", "").strip() or None
            existing.is_active = True
            continue

        db.add(
            LeaveType(
                code=code,
                name=default["name"].strip(),
                description=default.get("description", "").strip() or None,
                is_active=True,
            )
        )

    db.commit()
