from fastapi import APIRouter, Response


home_router = APIRouter()


@home_router.get("/health")
async def home():
    return Response(status_code=200)
