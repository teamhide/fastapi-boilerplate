from fastapi import APIRouter, Depends, Query

from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)
from app.user.adapter.input.api.v1.request import LoginRequest, CreateUserRequest
from app.user.adapter.input.api.v1.response import LoginResponse
from app.user.application.dto import CreateUserResponseDTO
from app.user.application.dto import GetUserListResponseDTO
from app.user.application.service.user import UserService
from app.user.domain.command import CreateUserCommand

user_router = APIRouter()


@user_router.get(
    "",
    response_model=list[GetUserListResponseDTO],
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
async def create_user(request: CreateUserRequest):
    command = CreateUserCommand(**request.model_dump())
    await UserService().create_user(command=command)
    return {"email": request.email, "nickname": request.nickname}


@user_router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(request: LoginRequest):
    token = await UserService().login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}
