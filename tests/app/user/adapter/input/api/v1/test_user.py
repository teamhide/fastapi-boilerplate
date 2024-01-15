import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.exception import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from tests.support.token import USER_ID_1_TOKEN
from tests.support.user_fixture import make_user

HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
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
    session.add(user)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/user", headers=HEADERS)

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {"id": 1, "email": "a@b.c", "nickname": "hide"}


@pytest.mark.asyncio
async def test_create_user_password_does_not_match(session: AsyncSession):
    # Given
    body = {
        "email": "h@id.e",
        "password1": "a",
        "password2": "b",
        "nickname": "hide",
        "lat": 37.123,
        "lng": 127.123,
    }
    exc = PasswordDoesNotMatchException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user_duplicated_user(session: AsyncSession):
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
    session.add(user)
    await session.commit()

    body = {
        "email": "a@b.c",
        "password1": "a",
        "password2": "a",
        "nickname": "hide",
        "lat": 37.123,
        "lng": 127.123,
    }
    exc = DuplicateEmailOrNicknameException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    # Given
    email = "h@id.e"
    nickname = "hide"
    body = {
        "email": email,
        "password1": "a",
        "password2": "a",
        "nickname": nickname,
        "lat": 37.123,
        "lng": 127.123,
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user", headers=HEADERS, json=body)

    # Then
    assert response.json() == {"email": email, "nickname": nickname}

    user_repo = UserSQLAlchemyRepo()
    sut = await user_repo.get_user_by_email_or_nickname(nickname=nickname, email=email)
    assert sut is not None
    assert sut.email == email
    assert sut.nickname == nickname


@pytest.mark.asyncio
async def test_login_user_not_found(session: AsyncSession):
    # Given
    email = "h@id.e"
    password = "password"
    body = {"email": email, "password": password}
    exc = UserNotFoundException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user/login", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_login(session: AsyncSession):
    # Given
    email = "h@id.e"
    password = "password"
    user = make_user(
        id=1,
        password=password,
        email=email,
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    body = {"email": email, "password": password}

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/user/login", headers=HEADERS, json=body)

    # Then
    sut = response.json()
    assert "token" in sut
    assert "refresh_token" in sut
