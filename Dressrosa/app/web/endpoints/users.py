"""Web user management endpoints for HR/Admin."""

from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import require_web_roles
from app.modules.users.service import UserAlreadyExistsError, create_user, delete_user, list_users

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/users", response_class=HTMLResponse)
def users_page(
    request: Request,
    current_user=Depends(require_web_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> HTMLResponse:
    users = list_users(db)
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"title": "User Management", "users": users, "current_user": current_user, "error": None},
    )


@router.post("/users", response_class=HTMLResponse)
def users_create(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    active: bool = Form(False),
    current_user=Depends(require_web_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> HTMLResponse:
    try:
        create_user(
            db,
            username=username,
            email=email,
            full_name=full_name,
            password=password,
            active=active,
        )
    except UserAlreadyExistsError as exc:
        users = list_users(db)
        return templates.TemplateResponse(
            request=request,
            name="users.html",
            context={
                "title": "User Management",
                "users": users,
                "current_user": current_user,
                "error": str(exc),
            },
            status_code=409,
        )

    return RedirectResponse(url="/users", status_code=303)


@router.post("/users/{user_id}/delete")
def users_delete(
    user_id: str,
    _: object = Depends(require_web_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> RedirectResponse:
    delete_user(db, user_id)
    return RedirectResponse(url="/users", status_code=303)
