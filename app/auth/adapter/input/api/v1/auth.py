from fastapi import APIRouter, Response

from app.auth.adapter.input.api.v1.request import RefreshTokenRequest, VerifyTokenRequest
from app.auth.adapter.input.api.v1.response import RefreshTokenResponse
from app.auth.application.service.jwt import JwtService

auth_router = APIRouter()


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
async def refresh_token(request: RefreshTokenRequest):
    token = await JwtService().create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return {"token": token.token, "refresh_token": token.refresh_token}


@auth_router.post("/verify")
async def verify_token(request: VerifyTokenRequest):
    await JwtService().verify_token(token=request.token)
    return Response(status_code=200)
