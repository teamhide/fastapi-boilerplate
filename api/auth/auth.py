from fastapi import APIRouter, Request

auth_router = APIRouter()


@auth_router.post("/refresh")
async def refresh_token(request: Request):
    return {}


@auth_router.post("/verify")
async def verify_token():
    return {}
