"""FastAPI app entrypoint."""

import logging

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.router import router as api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.web.router import router as web_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings)

    app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secret_key,
        session_cookie=settings.session_cookie_name,
        max_age=settings.access_token_expire_minutes * 60,
        same_site="lax",
        https_only=(settings.environment == "production"),
    )

    app.include_router(web_router)
    app.include_router(api_router)

    logger.info(
        "app_started name=%s version=%s environment=%s api_prefix=%s",
        settings.app_name,
        settings.app_version,
        settings.environment,
        settings.api_v1_prefix,
    )

    return app


app = create_app()
