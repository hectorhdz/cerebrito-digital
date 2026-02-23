"""Web router composition."""

from fastapi import APIRouter

from app.web.endpoints import auth, home, profile, users

router = APIRouter()
router.include_router(auth.router)
router.include_router(home.router)
router.include_router(users.router)
router.include_router(profile.router)
