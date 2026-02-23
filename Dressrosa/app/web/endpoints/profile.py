"""Web profile endpoints."""

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import get_current_web_user
from app.modules.users.service import get_user, get_user_role_names

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/profile", response_class=HTMLResponse)
def profile_page(
    request: Request,
    current_user=Depends(get_current_web_user),
    db: Session = Depends(get_db_session),
) -> HTMLResponse:
    manager_name = None
    if current_user.manager_id:
        manager = get_user(db, current_user.manager_id)
        manager_name = manager.full_name if manager else None

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "title": "My Profile",
            "user": current_user,
            "roles": get_user_role_names(db, current_user.id),
            "account_status": "active" if current_user.active else "inactive",
            "manager_name": manager_name,
        },
    )
