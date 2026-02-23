"""Web router composition."""

from fastapi import APIRouter

from app.web.endpoints import auth, home

router = APIRouter()
router.include_router(auth.router)
router.include_router(home.router)
