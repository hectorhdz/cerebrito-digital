"""FastAPI app entrypoint."""

from fastapi import FastAPI

from app.api.router import router as api_router
from app.core.config import settings
from app.web.router import router as web_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.include_router(web_router)
    app.include_router(api_router)

    return app


app = create_app()
