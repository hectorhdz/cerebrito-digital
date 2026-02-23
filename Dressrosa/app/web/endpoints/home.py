"""Server-rendered page endpoints."""

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.modules.auth.dependencies import get_web_user_from_session

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
