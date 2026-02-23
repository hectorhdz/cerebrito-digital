"""Profile and account status endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import get_current_api_user, require_api_roles
from app.modules.users.service import get_user, get_user_role_names, set_user_active_status

router = APIRouter(prefix="/profile")


class ProfileResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: str
    active: bool
    account_status: str
    manager_id: str | None
    manager_name: str | None
    roles: list[str]


class AccountStatusUpdateRequest(BaseModel):
    active: bool


class AccountStatusResponse(BaseModel):
    user_id: str
    username: str
    active: bool
    account_status: str


def _profile_response(db: Session, user) -> ProfileResponse:
    manager_name = None
    if user.manager_id:
        manager = get_user(db, user.manager_id)
        manager_name = manager.full_name if manager else None

    return ProfileResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        active=user.active,
        account_status="active" if user.active else "inactive",
        manager_id=user.manager_id,
        manager_name=manager_name,
        roles=get_user_role_names(db, user.id),
    )


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    current_user=Depends(get_current_api_user),
    db: Session = Depends(get_db_session),
) -> ProfileResponse:
    user = get_user(db, current_user.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return _profile_response(db, user)


@router.get("/{user_id}/status", response_model=AccountStatusResponse)
def get_user_account_status(
    user_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> AccountStatusResponse:
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return AccountStatusResponse(
        user_id=user.id,
        username=user.username,
        active=user.active,
        account_status="active" if user.active else "inactive",
    )


@router.put("/{user_id}/status", response_model=AccountStatusResponse)
def update_user_account_status(
    user_id: str,
    payload: AccountStatusUpdateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> AccountStatusResponse:
    user = set_user_active_status(db, user_id, payload.active)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return AccountStatusResponse(
        user_id=user.id,
        username=user.username,
        active=user.active,
        account_status="active" if user.active else "inactive",
    )
