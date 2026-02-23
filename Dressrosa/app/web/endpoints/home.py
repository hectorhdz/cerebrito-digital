"""Server-rendered page endpoints."""

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import get_web_user_from_session, require_web_roles

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db_session)) -> HTMLResponse:
    user = get_web_user_from_session(request, db)
    if user is None:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"title": "Dressrosa", "user": user},
    )


@router.get("/portal/employee", response_class=HTMLResponse)
def employee_portal(request: Request, user=Depends(require_web_roles("employee"))) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="role_page.html",
        context={"title": "Employee Portal", "user": user, "role_name": "employee"},
    )


@router.get("/portal/manager", response_class=HTMLResponse)
def manager_portal(request: Request, user=Depends(require_web_roles("manager"))) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="role_page.html",
        context={"title": "Manager Portal", "user": user, "role_name": "manager"},
    )


@router.get("/portal/hr", response_class=HTMLResponse)
def hr_portal(request: Request, user=Depends(require_web_roles("hr"))) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="role_page.html",
        context={"title": "HR Portal", "user": user, "role_name": "hr"},
    )


@router.get("/portal/admin", response_class=HTMLResponse)
def admin_portal(request: Request, user=Depends(require_web_roles("admin"))) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="role_page.html",
        context={"title": "Admin Portal", "user": user, "role_name": "admin"},
    )
