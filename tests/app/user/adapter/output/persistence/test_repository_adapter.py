import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from unittest.mock import patch, AsyncMock

from app.user.domain.repository.user import UserRepo

repository_adapter = UserRepositoryAdapter()


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    limit = 1
    prev = 1
    user_repo_mock = AsyncMock(spec=UserRepo)
    user_repo_mock.get_users.return_value = []
    repository_adapter.user_repo = user_repo_mock

    # When
    sut = await repository_adapter.get_users(limit=limit, prev=prev)

    # Then
    print(user_repo_mock.__dict__)
    # repository_adapter.user_repo.assert_awaited_once_with(limit=limit, prev=prev)


@pytest.mark.asyncio
async def test_get_user_by_email_or_nickname(session: AsyncSession):
    ...


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    ...


@pytest.mark.asyncio
async def test_get_user_by_email_and_password(session: AsyncSession):
    ...


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    pass
