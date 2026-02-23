"""Leave taxonomy service for types and scalable subtype management."""

from collections.abc import Sequence
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.leave_policy import LeavePolicy
from app.models.leave_subtype import LeaveSubtype
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

DEFAULT_LEAVE_SUBTYPES: dict[str, tuple[dict[str, str], ...]] = {
    "paid": (
        {"code": "vacation", "name": "Vacation", "description": "Planned annual paid vacation days."},
        {"code": "sick_leave", "name": "Sick Leave", "description": "Paid leave for medical conditions."},
        {"code": "parent_leave", "name": "Parent Leave", "description": "Paid parenthood-related leave."},
    ),
    "unpaid": (
        {"code": "personal_unpaid", "name": "Personal Unpaid", "description": "Unpaid personal time off."},
        {"code": "medical_unpaid", "name": "Medical Unpaid", "description": "Unpaid medical recovery leave."},
    ),
    "holiday_substitution": (
        {
            "code": "comp_day",
            "name": "Compensation Day",
            "description": "Time off granted in exchange for working on a holiday.",
        },
    ),
}

DEFAULT_LEAVE_POLICIES: tuple[dict[str, str | float | None], ...] = (
    {
        "code": "paid-default",
        "name": "Paid Leave Default Policy",
        "leave_type_code": "paid",
        "leave_subtype_code": None,
        "entitlement_days": 20.0,
        "accrual_rate_per_month": 1.67,
        "max_carryover_days": 5.0,
        "rules_json": '{"accrual_model":"monthly","requires_approval":true}',
    },
    {
        "code": "unpaid-default",
        "name": "Unpaid Leave Default Policy",
        "leave_type_code": "unpaid",
        "leave_subtype_code": None,
        "entitlement_days": None,
        "accrual_rate_per_month": None,
        "max_carryover_days": None,
        "rules_json": '{"requires_approval":true}',
    },
)


class LeaveTypeAlreadyExistsError(Exception):
    pass


class LeaveSubtypeAlreadyExistsError(Exception):
    pass


class LeaveTypeNotFoundError(Exception):
    pass


class LeaveSubtypeNotFoundError(Exception):
    pass


class LeavePolicyAlreadyExistsError(Exception):
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


def list_leave_subtypes(db: Session, leave_type_id: str | None = None) -> list[LeaveSubtype]:
    stmt = select(LeaveSubtype)
    if leave_type_id:
        stmt = stmt.where(LeaveSubtype.leave_type_id == leave_type_id)
    stmt = stmt.order_by(LeaveSubtype.created_at.asc())
    return list(db.execute(stmt).scalars().all())


def get_leave_subtype(db: Session, leave_subtype_id: str) -> LeaveSubtype | None:
    stmt = select(LeaveSubtype).where(LeaveSubtype.id == leave_subtype_id)
    return db.execute(stmt).scalar_one_or_none()


def get_leave_subtype_by_code(db: Session, leave_type_id: str, code: str) -> LeaveSubtype | None:
    stmt = select(LeaveSubtype).where(
        LeaveSubtype.leave_type_id == leave_type_id,
        LeaveSubtype.code == code.strip().lower(),
    )
    return db.execute(stmt).scalar_one_or_none()


def create_leave_subtype(
    db: Session,
    leave_type_id: str,
    code: str,
    name: str,
    description: str | None = None,
    is_active: bool = True,
) -> LeaveSubtype:
    leave_type = get_leave_type(db, leave_type_id)
    if leave_type is None:
        raise LeaveTypeNotFoundError("Leave type not found")

    normalized_code = code.strip().lower()
    if get_leave_subtype_by_code(db, leave_type_id=leave_type.id, code=normalized_code) is not None:
        raise LeaveSubtypeAlreadyExistsError(
            f"Leave subtype '{normalized_code}' already exists for leave type '{leave_type.code}'"
        )

    subtype = LeaveSubtype(
        leave_type_id=leave_type.id,
        code=normalized_code,
        name=name.strip(),
        description=(description.strip() if description else None),
        is_active=is_active,
    )
    db.add(subtype)
    db.commit()
    db.refresh(subtype)
    return subtype


def update_leave_subtype(
    db: Session,
    leave_subtype_id: str,
    leave_type_id: str,
    code: str,
    name: str,
    description: str | None,
    is_active: bool,
) -> LeaveSubtype | None:
    subtype = get_leave_subtype(db, leave_subtype_id)
    if subtype is None:
        return None

    leave_type = get_leave_type(db, leave_type_id)
    if leave_type is None:
        raise LeaveTypeNotFoundError("Leave type not found")

    normalized_code = code.strip().lower()
    existing = get_leave_subtype_by_code(db, leave_type_id=leave_type.id, code=normalized_code)
    if existing is not None and existing.id != leave_subtype_id:
        raise LeaveSubtypeAlreadyExistsError(
            f"Leave subtype '{normalized_code}' already exists for leave type '{leave_type.code}'"
        )

    subtype.leave_type_id = leave_type.id
    subtype.code = normalized_code
    subtype.name = name.strip()
    subtype.description = description.strip() if description else None
    subtype.is_active = is_active
    db.commit()
    db.refresh(subtype)
    return subtype


def delete_leave_subtype(db: Session, leave_subtype_id: str) -> bool:
    subtype = get_leave_subtype(db, leave_subtype_id)
    if subtype is None:
        return False

    db.delete(subtype)
    db.commit()
    return True


def list_leave_policies(
    db: Session,
    leave_type_id: str | None = None,
    leave_subtype_id: str | None = None,
) -> list[LeavePolicy]:
    stmt = select(LeavePolicy)
    if leave_type_id:
        stmt = stmt.where(LeavePolicy.leave_type_id == leave_type_id)
    if leave_subtype_id:
        stmt = stmt.where(LeavePolicy.leave_subtype_id == leave_subtype_id)
    stmt = stmt.order_by(LeavePolicy.created_at.asc())
    return list(db.execute(stmt).scalars().all())


def get_leave_policy(db: Session, leave_policy_id: str) -> LeavePolicy | None:
    stmt = select(LeavePolicy).where(LeavePolicy.id == leave_policy_id)
    return db.execute(stmt).scalar_one_or_none()


def get_leave_policy_by_code(db: Session, code: str) -> LeavePolicy | None:
    stmt = select(LeavePolicy).where(LeavePolicy.code == code.strip().lower())
    return db.execute(stmt).scalar_one_or_none()


def _validate_policy_refs(
    db: Session,
    leave_type_id: str,
    leave_subtype_id: str | None,
) -> tuple[LeaveType, LeaveSubtype | None]:
    leave_type = get_leave_type(db, leave_type_id)
    if leave_type is None:
        raise LeaveTypeNotFoundError("Leave type not found")

    if not leave_subtype_id:
        return leave_type, None

    subtype = get_leave_subtype(db, leave_subtype_id)
    if subtype is None:
        raise LeaveSubtypeNotFoundError("Leave subtype not found")
    if subtype.leave_type_id != leave_type.id:
        raise LeaveSubtypeNotFoundError("Leave subtype does not belong to the selected leave type")

    return leave_type, subtype


def create_leave_policy(
    db: Session,
    code: str,
    name: str,
    leave_type_id: str,
    leave_subtype_id: str | None = None,
    entitlement_days: float | None = None,
    accrual_rate_per_month: float | None = None,
    max_carryover_days: float | None = None,
    effective_from: date | None = None,
    effective_to: date | None = None,
    rules_json: str | None = None,
    is_active: bool = True,
) -> LeavePolicy:
    normalized_code = code.strip().lower()
    if get_leave_policy_by_code(db, normalized_code) is not None:
        raise LeavePolicyAlreadyExistsError(f"Leave policy '{normalized_code}' already exists")

    _, subtype = _validate_policy_refs(db, leave_type_id=leave_type_id, leave_subtype_id=leave_subtype_id)

    policy = LeavePolicy(
        code=normalized_code,
        name=name.strip(),
        leave_type_id=leave_type_id,
        leave_subtype_id=subtype.id if subtype else None,
        entitlement_days=entitlement_days,
        accrual_rate_per_month=accrual_rate_per_month,
        max_carryover_days=max_carryover_days,
        effective_from=effective_from,
        effective_to=effective_to,
        rules_json=rules_json.strip() if rules_json else None,
        is_active=is_active,
    )
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy


def update_leave_policy(
    db: Session,
    leave_policy_id: str,
    code: str,
    name: str,
    leave_type_id: str,
    leave_subtype_id: str | None,
    entitlement_days: float | None,
    accrual_rate_per_month: float | None,
    max_carryover_days: float | None,
    effective_from: date | None,
    effective_to: date | None,
    rules_json: str | None,
    is_active: bool,
) -> LeavePolicy | None:
    policy = get_leave_policy(db, leave_policy_id)
    if policy is None:
        return None

    normalized_code = code.strip().lower()
    existing = get_leave_policy_by_code(db, normalized_code)
    if existing is not None and existing.id != leave_policy_id:
        raise LeavePolicyAlreadyExistsError(f"Leave policy '{normalized_code}' already exists")

    _, subtype = _validate_policy_refs(db, leave_type_id=leave_type_id, leave_subtype_id=leave_subtype_id)

    policy.code = normalized_code
    policy.name = name.strip()
    policy.leave_type_id = leave_type_id
    policy.leave_subtype_id = subtype.id if subtype else None
    policy.entitlement_days = entitlement_days
    policy.accrual_rate_per_month = accrual_rate_per_month
    policy.max_carryover_days = max_carryover_days
    policy.effective_from = effective_from
    policy.effective_to = effective_to
    policy.rules_json = rules_json.strip() if rules_json else None
    policy.is_active = is_active
    db.commit()
    db.refresh(policy)
    return policy


def delete_leave_policy(db: Session, leave_policy_id: str) -> bool:
    policy = get_leave_policy(db, leave_policy_id)
    if policy is None:
        return False

    db.delete(policy)
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


def ensure_default_leave_subtypes(
    db: Session,
    defaults: dict[str, tuple[dict[str, str], ...]] | None = None,
) -> None:
    catalog = defaults or DEFAULT_LEAVE_SUBTYPES

    for leave_type_code, subtypes in catalog.items():
        leave_type = get_leave_type_by_code(db, leave_type_code)
        if leave_type is None:
            continue

        for subtype_data in subtypes:
            normalized_code = subtype_data["code"].strip().lower()
            existing = get_leave_subtype_by_code(db, leave_type.id, normalized_code)
            if existing is not None:
                existing.name = subtype_data["name"].strip()
                existing.description = subtype_data.get("description", "").strip() or None
                existing.is_active = True
                continue

            db.add(
                LeaveSubtype(
                    leave_type_id=leave_type.id,
                    code=normalized_code,
                    name=subtype_data["name"].strip(),
                    description=subtype_data.get("description", "").strip() or None,
                    is_active=True,
                )
            )

    db.commit()


def ensure_default_leave_policies(
    db: Session,
    defaults: Sequence[dict[str, str | float | None]] | None = None,
) -> None:
    catalog = defaults or DEFAULT_LEAVE_POLICIES

    for policy_data in catalog:
        code = str(policy_data["code"]).strip().lower()
        leave_type_code = str(policy_data["leave_type_code"]).strip().lower()
        leave_subtype_code_raw = policy_data.get("leave_subtype_code")
        leave_subtype_code = str(leave_subtype_code_raw).strip().lower() if leave_subtype_code_raw else None

        leave_type = get_leave_type_by_code(db, leave_type_code)
        if leave_type is None:
            continue

        leave_subtype_id = None
        if leave_subtype_code:
            subtype = get_leave_subtype_by_code(db, leave_type.id, leave_subtype_code)
            if subtype is None:
                continue
            leave_subtype_id = subtype.id

        existing = get_leave_policy_by_code(db, code)
        if existing is not None:
            existing.name = str(policy_data["name"]).strip()
            existing.leave_type_id = leave_type.id
            existing.leave_subtype_id = leave_subtype_id
            existing.entitlement_days = policy_data.get("entitlement_days")  # type: ignore[assignment]
            existing.accrual_rate_per_month = policy_data.get("accrual_rate_per_month")  # type: ignore[assignment]
            existing.max_carryover_days = policy_data.get("max_carryover_days")  # type: ignore[assignment]
            existing.rules_json = str(policy_data.get("rules_json", "")).strip() or None
            existing.is_active = True
            continue

        db.add(
            LeavePolicy(
                code=code,
                name=str(policy_data["name"]).strip(),
                leave_type_id=leave_type.id,
                leave_subtype_id=leave_subtype_id,
                entitlement_days=policy_data.get("entitlement_days"),  # type: ignore[arg-type]
                accrual_rate_per_month=policy_data.get("accrual_rate_per_month"),  # type: ignore[arg-type]
                max_carryover_days=policy_data.get("max_carryover_days"),  # type: ignore[arg-type]
                rules_json=str(policy_data.get("rules_json", "")).strip() or None,
                is_active=True,
            )
        )

    db.commit()
