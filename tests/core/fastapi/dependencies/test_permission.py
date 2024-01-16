from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import Request

from app.user.application.service.user import UserService
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
    IsAuthenticated,
    AllowAll,
)
from core.fastapi.dependencies import permission
from core.fastapi.dependencies.permission import UnauthorizedException


@pytest.mark.asyncio
async def test_permission_dependency_is_authenticated():
    # Given
    dependency = PermissionDependency(permissions=[IsAuthenticated])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    # When, Then
    with pytest.raises(UnauthorizedException):
        await dependency(request=request)


@pytest.mark.asyncio
@patch.object(permission, "UserService", spec=UserService)
async def test_permission_dependency_is_admin_user_is_not_admin(user_service_mock):
    # Given
    dependency = PermissionDependency(permissions=[IsAdmin])
    request = AsyncMock(spec=Request)
    user_id = 1
    request.user = Mock(id=user_id)
    user_service_mock.is_admin.return_value = False

    # When, Then
    await dependency(request=request)


@pytest.mark.asyncio
@patch.object(permission, "UserService", spec=UserService)
async def test_permission_dependency_is_admin_user_id_is_none(user_service_mock):
    # Given
    dependency = PermissionDependency(permissions=[IsAdmin])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)
    user_service_mock.is_admin.return_value = False

    # When, Then
    with pytest.raises(UnauthorizedException):
        await dependency(request=request)


@pytest.mark.asyncio
async def test_permission_dependency_allow_all():
    # Given
    dependency = PermissionDependency(permissions=[AllowAll])
    request = AsyncMock(spec=Request)

    # When
    sut = await dependency(request=request)

    # Then
    assert sut is None
