from typing import List

from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas import (
    ExceptionResponseSchema,
    GetUserListResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)
from app.usecases import CreateUserUsecase, GetUserListUsecase
from core.utils import extract_payload_from_token

user_router = APIRouter()
security = HTTPBearer()


@user_router.get(
    '',
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={'id'},
    responses={
        '400': {'model': ExceptionResponseSchema},
    },
)
async def get_user_list(
    limit: int = 10,
    prev: int = None,
    authorization: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    extract_payload_from_token(token=authorization.credentials)
    return await GetUserListUsecase().execute(limit=limit, prev=prev)


@user_router.post(
    '',
    response_model=CreateUserResponseSchema,
    responses={
        '400': {'model': ExceptionResponseSchema},
    },
)
async def create_user(
    request: CreateUserRequestSchema,
    authorization: HTTPAuthorizationCredentials = Security(HTTPBearer()),
):
    extract_payload_from_token(token=authorization.credentials)
    return await CreateUserUsecase().execute(**request.dict())
