"""Authentication dependencies for API and web routes."""

from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models.user import User
from app.modules.auth.security import decode_access_token
from app.modules.auth.service import get_user_by_id, get_user_role_names

bearer_scheme = HTTPBearer(auto_error=False)

ROLE_INHERITANCE: dict[str, set[str]] = {
    "admin": {"hr", "manager", "employee"},
    "hr": {"manager", "employee"},
    "manager": {"employee"},
    "employee": set(),
}


def expand_roles(role_names: set[str]) -> set[str]:
    expanded = set(role_names)
    queue = list(role_names)

    while queue:
        role = queue.pop()
        inherited = ROLE_INHERITANCE.get(role, set())
        new_roles = inherited - expanded
        expanded.update(new_roles)
        queue.extend(new_roles)

    return expanded


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


def require_api_roles(*required_roles: str) -> Callable:
    required = set(required_roles)

    def _dependency(
        user: User = Depends(get_current_api_user),
        db: Session = Depends(get_db_session),
    ) -> User:
        user_roles = get_user_role_names(db, user.id)
        effective_roles = expand_roles(user_roles)

        if required and effective_roles.isdisjoint(required):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")

        return user

    return _dependency


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


def require_web_roles(*required_roles: str) -> Callable:
    required = set(required_roles)

    def _dependency(
        user: User = Depends(get_current_web_user),
        db: Session = Depends(get_db_session),
    ) -> User:
        user_roles = get_user_role_names(db, user.id)
        effective_roles = expand_roles(user_roles)

        if required and effective_roles.isdisjoint(required):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")

        return user

    return _dependency
