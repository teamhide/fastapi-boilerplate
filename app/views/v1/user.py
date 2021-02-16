from typing import List

from fastapi import APIRouter, Depends

from app.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from app.usecases import UserUsecase
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)

user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
async def get_user_list(limit: int = 10, prev: int = None):
    return await UserUsecase().get_user_list(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(request: CreateUserRequestSchema):
    return await UserUsecase().create_user(**request.dict())
