"""Auth API endpoints for token issuance and identity."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import get_current_api_user
from app.modules.auth.security import create_access_token
from app.modules.auth.service import authenticate_user, get_user_role_names

router = APIRouter(prefix="/auth")


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
) -> dict[str, str | int]:
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token, expires_in = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer", "expires_in": expires_in}


@router.get("/me")
def read_current_user(
    user=Depends(get_current_api_user),
    db: Session = Depends(get_db_session),
) -> dict[str, str | bool | list[str]]:
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "active": user.active,
        "roles": sorted(get_user_role_names(db, user.id)),
    }
