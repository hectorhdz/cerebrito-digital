"""Web router composition."""

from fastapi import APIRouter

from app.web.endpoints import home

router = APIRouter()
router.include_router(home.router)
