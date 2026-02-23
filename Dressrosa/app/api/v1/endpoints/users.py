"""User API endpoints for HR/Admin user CRUD and role assignment management."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import require_api_roles
from app.modules.users.service import (
    RoleNotFoundError,
    UserAlreadyExistsError,
    assign_role_to_user,
    create_user,
    delete_user,
    get_user,
    get_user_role_names,
    list_roles,
    list_users,
    remove_role_from_user,
    update_user,
)

router = APIRouter(prefix="/users")


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=6, max_length=128)
    active: bool = True


class UserUpdateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str | None = Field(default=None, min_length=6, max_length=128)
    active: bool


class UserRoleAssignRequest(BaseModel):
    role_name: str = Field(min_length=2, max_length=50)


class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    full_name: str
    active: bool
    roles: list[str]


class RoleResponse(BaseModel):
    name: str


@router.get("", response_model=list[UserResponse])
def api_list_users(
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> list[UserResponse]:
    users = list_users(db)
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            active=user.active,
            roles=get_user_role_names(db, user.id),
        )
        for user in users
    ]


@router.get("/roles", response_model=list[RoleResponse])
def api_list_roles(
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> list[RoleResponse]:
    return [RoleResponse(name=role.name) for role in list_roles(db)]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def api_create_user(
    payload: UserCreateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> UserResponse:
    try:
        user = create_user(
            db,
            username=payload.username,
            email=str(payload.email),
            full_name=payload.full_name,
            password=payload.password,
            active=payload.active,
        )
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        active=user.active,
        roles=get_user_role_names(db, user.id),
    )


@router.get("/{user_id}", response_model=UserResponse)
def api_get_user(
    user_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> UserResponse:
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        active=user.active,
        roles=get_user_role_names(db, user.id),
    )


@router.put("/{user_id}", response_model=UserResponse)
def api_update_user(
    user_id: str,
    payload: UserUpdateRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> UserResponse:
    try:
        user = update_user(
            db,
            user_id=user_id,
            username=payload.username,
            email=str(payload.email),
            full_name=payload.full_name,
            active=payload.active,
            password=payload.password,
        )
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        active=user.active,
        roles=get_user_role_names(db, user.id),
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(
    user_id: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> None:
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.post("/{user_id}/roles", response_model=UserResponse)
def api_assign_role(
    user_id: str,
    payload: UserRoleAssignRequest,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> UserResponse:
    try:
        ok = assign_role_to_user(db, user_id=user_id, role_name=payload.role_name)
    except RoleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        active=user.active,
        roles=get_user_role_names(db, user.id),
    )


@router.delete("/{user_id}/roles/{role_name}", response_model=UserResponse)
def api_remove_role(
    user_id: str,
    role_name: str,
    _: object = Depends(require_api_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> UserResponse:
    try:
        ok = remove_role_from_user(db, user_id=user_id, role_name=role_name)
    except RoleNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        active=user.active,
        roles=get_user_role_names(db, user.id),
    )
