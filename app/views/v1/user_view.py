from typing import List

from fastapi import APIRouter

from app.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from app.usecases import CreateUserUsecase, GetUserListUsecase

user_router = APIRouter()


@user_router.get('/', response_model=List[GetUserListResponseSchema])
async def get_user_list(limit: int = 10, prev: int = None):
    return await GetUserListUsecase().execute(limit=limit, prev=prev)


@user_router.post(
    '/',
    response_model=CreateUserResponseSchema,
    responses={
        '400': {'model': ExceptionResponseSchema},
    },
)
async def create_user(request: CreateUserRequestSchema):
    return await CreateUserUsecase().execute(**request.dict())
