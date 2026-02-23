"""Leave policy API endpoints for HR/Admin placeholders."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import require_api_roles
from app.modules.leaves.service import (
    LeavePolicyAlreadyExistsError,
    LeaveSubtypeNotFoundError,
    LeaveTypeNotFoundError,
    create_leave_policy,
    delete_leave_policy,
    get_leave_policy,
    list_leave_policies,
    update_leave_policy,
)

router = APIRouter(prefix="/leave-policies")


class LeavePolicyCreateRequest(BaseModel):
    code: str = Field(min_length=2, max_length=80)
    name: str = Field(min_length=2, max_length=120)
    leave_type_id: str = Field(min_length=1, max_length=36)
    leave_subtype_id: str | None = Field(default=None, max_length=36)
    entitlement_days: float | None = None
    accrual_rate_per_month: float | None = None
    max_carryover_days: float | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    rules_json: str | None = Field(default=None, max_length=2000)
    is_active: bool = True


class LeavePolicyUpdateRequest(BaseModel):
    code: str = Field(min_length=2, max_length=80)
    name: str = Field(min_length=2, max_length=120)
    leave_type_id: str = Field(min_length=1, max_length=36)
    leave_subtype_id: str | None = Field(default=None, max_length=36)
    entitlement_days: float | None = None
    accrual_rate_per_month: float | None = None
    max_carryover_days: float | None = None
    effective_from: date | None = None
    effective_to: date | None = None
    rules_json: str | None = Field(default=None, max_length=2000)
    is_active: bool


class LeavePolicyResponse(BaseModel):
    id: str
    code: str
    name: str
    leave_type_id: str
    leave_subtype_id: str | None
    entitlement_days: float | None
    accrual_rate_per_month: float | None
    max_carryover_days: float | None
    effective_from: date | None
    effective_to: date | None
    rules_json: str | None
    is_active: bool


def _to_response(policy) -> LeavePolicyResponse:
    return LeavePolicyResponse(
        id=policy.id,
        code=policy.code,
        name=policy.name,
        leave_type_id=policy.leave_type_id,
        leave_subtype_id=policy.leave_subtype_id,
        entitlement_days=policy.entitlement_days,
        accrual_rate_per_month=policy.accrual_rate_per_month,
        max_carryover_days=policy.max_carryover_days,
        effective_from=policy.effective_from,
        effective_to=policy.effective_to,
        rules_json=policy.rules_json,
        is_active=policy.is_active,
    )


@router.get("", response_model=list[LeavePolicyResponse])
def api_list_leave_policies(
    leave_type_id: str | None = Query(default=None),
    leave_subtype_id: str | None = Query(default=None),
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> list[LeavePolicyResponse]:
    return [
        _to_response(policy)
        for policy in list_leave_policies(db, leave_type_id=leave_type_id, leave_subtype_id=leave_subtype_id)
    ]


@router.post("", response_model=LeavePolicyResponse, status_code=status.HTTP_201_CREATED)
def api_create_leave_policy(
    payload: LeavePolicyCreateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeavePolicyResponse:
    try:
        policy = create_leave_policy(
            db,
            code=payload.code,
            name=payload.name,
            leave_type_id=payload.leave_type_id,
            leave_subtype_id=payload.leave_subtype_id,
            entitlement_days=payload.entitlement_days,
            accrual_rate_per_month=payload.accrual_rate_per_month,
            max_carryover_days=payload.max_carryover_days,
            effective_from=payload.effective_from,
            effective_to=payload.effective_to,
            rules_json=payload.rules_json,
            is_active=payload.is_active,
        )
    except LeavePolicyAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (LeaveTypeNotFoundError, LeaveSubtypeNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return _to_response(policy)


@router.get("/{leave_policy_id}", response_model=LeavePolicyResponse)
def api_get_leave_policy(
    leave_policy_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeavePolicyResponse:
    policy = get_leave_policy(db, leave_policy_id)
    if policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave policy not found")

    return _to_response(policy)


@router.put("/{leave_policy_id}", response_model=LeavePolicyResponse)
def api_update_leave_policy(
    leave_policy_id: str,
    payload: LeavePolicyUpdateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeavePolicyResponse:
    try:
        policy = update_leave_policy(
            db,
            leave_policy_id=leave_policy_id,
            code=payload.code,
            name=payload.name,
            leave_type_id=payload.leave_type_id,
            leave_subtype_id=payload.leave_subtype_id,
            entitlement_days=payload.entitlement_days,
            accrual_rate_per_month=payload.accrual_rate_per_month,
            max_carryover_days=payload.max_carryover_days,
            effective_from=payload.effective_from,
            effective_to=payload.effective_to,
            rules_json=payload.rules_json,
            is_active=payload.is_active,
        )
    except LeavePolicyAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (LeaveTypeNotFoundError, LeaveSubtypeNotFoundError) as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    if policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave policy not found")

    return _to_response(policy)


@router.delete("/{leave_policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_leave_policy(
    leave_policy_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> None:
    deleted = delete_leave_policy(db, leave_policy_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave policy not found")
