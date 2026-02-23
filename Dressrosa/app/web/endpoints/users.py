"""Web user management endpoints for HR/Admin."""

from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import require_web_roles
from app.modules.users.service import (
    RoleNotFoundError,
    UserAlreadyExistsError,
    assign_role_to_user,
    create_user,
    delete_user,
    get_user_role_names,
    list_roles,
    list_users,
    remove_role_from_user,
)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


def _users_page_context(db: Session, current_user, error: str | None = None) -> dict:
    users = list_users(db)
    roles = list_roles(db)
    user_roles = {user.id: get_user_role_names(db, user.id) for user in users}
    return {
        "title": "User Management",
        "users": users,
        "roles": roles,
        "user_roles": user_roles,
        "current_user": current_user,
        "error": error,
    }


@router.get("/users", response_class=HTMLResponse)
def users_page(
    request: Request,
    current_user=Depends(require_web_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context=_users_page_context(db, current_user),
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
        return templates.TemplateResponse(
            request=request,
            name="users.html",
            context=_users_page_context(db, current_user, error=str(exc)),
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


@router.post("/users/{user_id}/roles")
def users_assign_role(
    request: Request,
    user_id: str,
    role_name: str = Form(...),
    current_user=Depends(require_web_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> HTMLResponse | RedirectResponse:
    try:
        ok = assign_role_to_user(db, user_id=user_id, role_name=role_name)
    except RoleNotFoundError as exc:
        return templates.TemplateResponse(
            request=request,
            name="users.html",
            context=_users_page_context(db, current_user, error=str(exc)),
            status_code=404,
        )

    if not ok:
        return templates.TemplateResponse(
            request=request,
            name="users.html",
            context=_users_page_context(db, current_user, error="User not found"),
            status_code=404,
        )

    return RedirectResponse(url="/users", status_code=303)


@router.post("/users/{user_id}/roles/{role_name}/remove")
def users_remove_role(
    request: Request,
    user_id: str,
    role_name: str,
    current_user=Depends(require_web_roles("hr", "admin")),
    db: Session = Depends(get_db_session),
) -> HTMLResponse | RedirectResponse:
    try:
        ok = remove_role_from_user(db, user_id=user_id, role_name=role_name)
    except RoleNotFoundError as exc:
        return templates.TemplateResponse(
            request=request,
            name="users.html",
            context=_users_page_context(db, current_user, error=str(exc)),
            status_code=404,
        )

    if not ok:
        return templates.TemplateResponse(
            request=request,
            name="users.html",
            context=_users_page_context(db, current_user, error="User not found"),
            status_code=404,
        )

    return RedirectResponse(url="/users", status_code=303)
