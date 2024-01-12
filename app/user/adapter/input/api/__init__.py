from fastapi import APIRouter

from app.user.adapter.input.api.v1.user import user_router as user_v1_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/user", tags=["User"])


__all__ = ["router"]
