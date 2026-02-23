"""Authentication web endpoints."""

from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.service import authenticate_user

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"title": "Login - Dressrosa", "error": None},
    )


@router.post("/login", response_class=HTMLResponse)
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db_session),
) -> HTMLResponse:
    user = authenticate_user(db, username, password)

    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"title": "Login - Dressrosa", "error": "Invalid username or password."},
            status_code=401,
        )

    request.session["user_id"] = user.id
    response = RedirectResponse(url="/", status_code=303)
    return response


@router.post("/logout")
def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
