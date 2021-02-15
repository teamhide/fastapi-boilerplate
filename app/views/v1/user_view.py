from typing import List

from fastapi import APIRouter, Depends

from app.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from app.usecases import CreateUserUsecase, GetUserListUsecase
from core.fastapi.dependencies import extract_token

user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_user_list(
    limit: int = 10, prev: int = None, payload: dict = Depends(extract_token),
):
    return await GetUserListUsecase().execute(limit=limit, prev=prev)


@user_router.post(
    "",
    response_model=CreateUserResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def create_user(
    request: CreateUserRequestSchema, payload: dict = Depends(extract_token),
):
    return await CreateUserUsecase().execute(**request.dict())
