from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.domain.repository.user import UserRepo
from tests.support.user_fixture import make_user

user_repo_mock = AsyncMock(spec=UserRepo)
repository_adapter = UserRepositoryAdapter(user_repo=user_repo_mock)


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    limit = 1
    prev = 1
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    user_repo_mock.get_users.return_value = [user]
    repository_adapter.user_repo = user_repo_mock

    # When
    sut = await repository_adapter.get_users(limit=limit, prev=prev)

    # Then
    assert len(sut) == 1
    result = sut[0]
    assert result.id == user.id
    assert result.email == user.email
    assert result.nickname == user.nickname
    repository_adapter.user_repo.get_users.assert_awaited_once_with(
        limit=limit, prev=prev
    )


@pytest.mark.asyncio
async def test_get_user_by_email_or_nickname(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    user_repo_mock.get_user_by_email_or_nickname.return_value = user
    repository_adapter.user_repo = user_repo_mock

    # When
    sut = await repository_adapter.get_user_by_email_or_nickname(
        email=user.email,
        nickname=user.nickname,
    )

    # Then
    assert sut is not None
    assert sut.id == user.id
    assert sut.password == user.password
    assert sut.email == user.email
    assert sut.nickname == user.nickname
    assert sut.is_admin == user.is_admin
    assert sut.location.lat == user.location.lat
    assert sut.location.lng == user.location.lng
    repository_adapter.user_repo.get_user_by_email_or_nickname.assert_awaited_once_with(
        email=user.email,
        nickname=user.nickname,
    )


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    user_repo_mock.get_user_by_id.return_value = user
    repository_adapter.user_repo = user_repo_mock

    # When
    sut = await repository_adapter.get_user_by_id(user_id=user.id)

    # Then
    assert sut is not None
    assert sut.id == user.id
    assert sut.password == user.password
    assert sut.email == user.email
    assert sut.nickname == user.nickname
    assert sut.is_admin == user.is_admin
    assert sut.location.lat == user.location.lat
    assert sut.location.lng == user.location.lng
    repository_adapter.user_repo.get_user_by_id.assert_awaited_once_with(
        user_id=user.id
    )


@pytest.mark.asyncio
async def test_get_user_by_email_and_password(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    user_repo_mock.get_user_by_email_and_password.return_value = user
    repository_adapter.user_repo = user_repo_mock

    # When
    sut = await repository_adapter.get_user_by_email_and_password(
        email=user.email, password=user.password
    )

    # Then
    assert sut is not None
    assert sut.id == user.id
    assert sut.password == user.password
    assert sut.email == user.email
    assert sut.nickname == user.nickname
    assert sut.is_admin == user.is_admin
    assert sut.location.lat == user.location.lat
    assert sut.location.lng == user.location.lng
    repository_adapter.user_repo.get_user_by_email_and_password.assert_awaited_once_with(
        email=user.email,
        password=user.password,
    )


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    user_repo_mock.save.return_value = None
    repository_adapter.user_repo = user_repo_mock

    # When
    await repository_adapter.save(user=user)

    # Then
    repository_adapter.user_repo.save.assert_awaited_once_with(user=user)
