"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import access, auth, health

router = APIRouter(prefix="/api/v1")
router.include_router(health.router, tags=["health"])
router.include_router(auth.router, tags=["auth"])
router.include_router(access.router, tags=["access"])
