"""Leave subtype API endpoints for HR/Admin management."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import require_api_roles
from app.modules.leaves.service import (
    LeaveSubtypeAlreadyExistsError,
    LeaveTypeNotFoundError,
    create_leave_subtype,
    delete_leave_subtype,
    get_leave_subtype,
    list_leave_subtypes,
    update_leave_subtype,
)

router = APIRouter(prefix="/leave-subtypes")


class LeaveSubtypeCreateRequest(BaseModel):
    leave_type_id: str = Field(min_length=1, max_length=36)
    code: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool = True


class LeaveSubtypeUpdateRequest(BaseModel):
    leave_type_id: str = Field(min_length=1, max_length=36)
    code: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool


class LeaveSubtypeResponse(BaseModel):
    id: str
    leave_type_id: str
    code: str
    name: str
    description: str | None
    is_active: bool


def _to_response(subtype) -> LeaveSubtypeResponse:
    return LeaveSubtypeResponse(
        id=subtype.id,
        leave_type_id=subtype.leave_type_id,
        code=subtype.code,
        name=subtype.name,
        description=subtype.description,
        is_active=subtype.is_active,
    )


@router.get("", response_model=list[LeaveSubtypeResponse])
def api_list_leave_subtypes(
    leave_type_id: str | None = Query(default=None),
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> list[LeaveSubtypeResponse]:
    return [_to_response(subtype) for subtype in list_leave_subtypes(db, leave_type_id=leave_type_id)]


@router.post("", response_model=LeaveSubtypeResponse, status_code=status.HTTP_201_CREATED)
def api_create_leave_subtype(
    payload: LeaveSubtypeCreateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeaveSubtypeResponse:
    try:
        subtype = create_leave_subtype(
            db,
            leave_type_id=payload.leave_type_id,
            code=payload.code,
            name=payload.name,
            description=payload.description,
            is_active=payload.is_active,
        )
    except LeaveSubtypeAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except LeaveTypeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return _to_response(subtype)


@router.get("/{leave_subtype_id}", response_model=LeaveSubtypeResponse)
def api_get_leave_subtype(
    leave_subtype_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeaveSubtypeResponse:
    subtype = get_leave_subtype(db, leave_subtype_id)
    if subtype is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave subtype not found")

    return _to_response(subtype)


@router.put("/{leave_subtype_id}", response_model=LeaveSubtypeResponse)
def api_update_leave_subtype(
    leave_subtype_id: str,
    payload: LeaveSubtypeUpdateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> LeaveSubtypeResponse:
    try:
        subtype = update_leave_subtype(
            db,
            leave_subtype_id=leave_subtype_id,
            leave_type_id=payload.leave_type_id,
            code=payload.code,
            name=payload.name,
            description=payload.description,
            is_active=payload.is_active,
        )
    except LeaveSubtypeAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except LeaveTypeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    if subtype is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave subtype not found")

    return _to_response(subtype)


@router.delete("/{leave_subtype_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_leave_subtype(
    leave_subtype_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> None:
    deleted = delete_leave_subtype(db, leave_subtype_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave subtype not found")
