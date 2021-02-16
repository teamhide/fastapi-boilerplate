from typing import List

from fastapi import Request

from app.usecases import UserUsecase
from core.exceptions import UnauthorizedException


class PermissionDependency:
    def __init__(self, permissions: List):
        self.permissions = permissions

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission
            if not await cls.has_permission(request=request):
                raise cls.exception


class IsAuthenticated:
    exception = UnauthorizedException

    @classmethod
    async def has_permission(cls, request: Request):
        return request.user.id is not None


class IsAdmin:
    exception = UnauthorizedException

    @classmethod
    async def has_permission(cls, request: Request):
        user_id = request.user.id
        if not user_id:
            return False

        return await UserUsecase().is_admin(user_id=user_id)
