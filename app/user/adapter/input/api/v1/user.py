from fastapi import APIRouter, Depends, Query

from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)
from app.user.adapter.input.api.v1.request import LoginRequest, CreateUserRequestDTO
from app.user.adapter.input.api.v1.response import LoginResponse
from app.user.application.dto import CreateUserResponseDTO
from app.user.application.dto import GetUserListResponseDTO
from app.user.application.service.user import UserService

user_router = APIRouter()


@user_router.get(
    "",
    response_model=list[GetUserListResponseDTO],
    response_model_exclude={"id"},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    return await UserService().get_user_list(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=CreateUserResponseDTO,
)
async def create_user(request: CreateUserRequestDTO):
    await UserService().create_user(**request.dict())
    return {"email": request.email, "nickname": request.nickname}


@user_router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(request: LoginRequest):
    token = await UserService().login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}
