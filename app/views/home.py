from fastapi import APIRouter, Depends
from core.fastapi.dependencies import IsAdmin, PermissionDependency

home_router = APIRouter()


@home_router.get("/", dependencies=[
    Depends(PermissionDependency([IsAdmin]))
])
def home():
    return {"status": True}
