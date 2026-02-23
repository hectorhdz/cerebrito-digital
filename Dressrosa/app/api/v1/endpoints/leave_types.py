"""Leave type API endpoints for HR/Admin management."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import require_api_roles
from app.modules.leaves.service import (
    LeaveTypeAlreadyExistsError,
    create_leave_type,
    delete_leave_type,
    get_leave_type,
    list_leave_types,
    update_leave_type,
)

router = APIRouter(prefix="/leave-types")


class LeaveTypeCreateRequest(BaseModel):
    code: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool = True


class LeaveTypeUpdateRequest(BaseModel):
    code: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool


class LeaveTypeResponse(BaseModel):
    id: str
    code: str
    name: str
    description: str | None
    is_active: bool


def _to_response(leave_type) -> LeaveTypeResponse:
    return LeaveTypeResponse(
        id=leave_type.id,
        code=leave_type.code,
        name=leave_type.name,
        description=leave_type.description,
        is_active=leave_type.is_active,
    )


@router.get("", response_model=list[LeaveTypeResponse])
def api_list_leave_types(
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> list[LeaveTypeResponse]:
    return [_to_response(leave_type) for leave_type in list_leave_types(db)]


@router.post("", response_model=LeaveTypeResponse, status_code=status.HTTP_201_CREATED)
def api_create_leave_type(
    payload: LeaveTypeCreateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeaveTypeResponse:
    try:
        leave_type = create_leave_type(
            db,
            code=payload.code,
            name=payload.name,
            description=payload.description,
            is_active=payload.is_active,
        )
    except LeaveTypeAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return _to_response(leave_type)


@router.put("/{leave_type_id}", response_model=LeaveTypeResponse)
def api_update_leave_type(
    leave_type_id: str,
    payload: LeaveTypeUpdateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeaveTypeResponse:
    try:
        leave_type = update_leave_type(
            db,
            leave_type_id=leave_type_id,
            code=payload.code,
            name=payload.name,
            description=payload.description,
            is_active=payload.is_active,
        )
    except LeaveTypeAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    if leave_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found")

    return _to_response(leave_type)


@router.delete("/{leave_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_leave_type(
    leave_type_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> None:
    deleted = delete_leave_type(db, leave_type_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found")


@router.get("/{leave_type_id}", response_model=LeaveTypeResponse)
def api_get_leave_type(
    leave_type_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeaveTypeResponse:
    leave_type = get_leave_type(db, leave_type_id)
    if leave_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found")

    return _to_response(leave_type)
