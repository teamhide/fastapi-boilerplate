from fastapi import APIRouter

from api.user.v1.user import user_router as user_v1_router

router = APIRouter()
router.include_router(user_v1_router, prefix="/api/v1/users", tags=["User"])


__all__ = ["router"]
