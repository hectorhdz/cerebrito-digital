"""Authentication dependencies for API and web routes."""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.user import User
from app.modules.auth.security import decode_access_token
from app.modules.auth.service import get_user_by_id

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_api_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db_session),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = str(payload.get("sub", ""))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user = get_user_by_id(db, user_id)
    if user is None or not user.active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    return user


def get_web_user_from_session(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None

    user = get_user_by_id(db, str(user_id))
    if user is None or not user.active:
        return None

    return user


def get_current_web_user(request: Request, db: Session = Depends(get_db_session)) -> User:
    user = get_web_user_from_session(request, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return user
