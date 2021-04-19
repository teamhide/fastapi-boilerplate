from fastapi import APIRouter

home_router = APIRouter()


@home_router.get("/")
async def home():
    return {"status": True}
