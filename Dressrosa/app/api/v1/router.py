"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import access, auth, health, leave_types, profile, users

router = APIRouter(prefix="/api/v1")
router.include_router(health.router, tags=["health"])
router.include_router(auth.router, tags=["auth"])
router.include_router(access.router, tags=["access"])
router.include_router(users.router, tags=["users"])
router.include_router(profile.router, tags=["profile"])
router.include_router(leave_types.router, tags=["leave-types"])
