import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.domain.entity.user import User
from tests.support.user_fixture import make_user

user_repo = UserSQLAlchemyRepo()


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    user_1 = make_user(
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        lat=37.123,
        lng=127.123,
    )
    user_2 = make_user(
        password="password2",
        email="b@b.c",
        nickname="test",
        is_admin=False,
        lat=37.123,
        lng=127.123,
    )
    session.add_all([user_1, user_2])
    await session.commit()

    # When
    sut = await user_repo.get_users(limit=15, prev=12)

    # Then
    assert len(sut) == 2
    saved_user_1 = sut[0]
    assert saved_user_1.password == user_1.password
    assert saved_user_1.email == user_1.email
    assert saved_user_1.nickname == user_1.nickname
    assert saved_user_1.is_admin == user_1.is_admin
    assert saved_user_1.location.lat == user_1.location.lat
    assert saved_user_1.location.lng == user_1.location.lng

    saved_user_2 = sut[1]
    assert saved_user_2.password == user_2.password
    assert saved_user_2.email == user_2.email
    assert saved_user_2.nickname == user_2.nickname
    assert saved_user_2.is_admin == user_2.is_admin
    assert saved_user_2.location.lat == user_2.location.lat
    assert saved_user_2.location.lng == user_2.location.lng


@pytest.mark.asyncio
async def test_get_user_by_email_or_nickname(session: AsyncSession):
    # Given
    email = "a@b.c"
    nickname = "hide"
    user = make_user(
        password="password2",
        email=email,
        nickname=nickname,
        is_admin=False,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_email_or_nickname(email=email, nickname=nickname)

    # Then
    assert isinstance(sut, User)
    assert sut.id == user.id
    assert sut.email == email
    assert sut.nickname == nickname


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    # Given
    user_id = 1

    # When
    sut = await user_repo.get_user_by_id(user_id=user_id)

    # Then
    assert sut is None


@pytest.mark.asyncio
async def test_get_user_by_email_and_password(session: AsyncSession):
    # Given
    email = "b@c.d"
    password = "hide"
    user = make_user(
        password=password,
        email=email,
        nickname="hide",
        is_admin=False,
        lat=37.123,
        lng=127.123,
    )
    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_email_and_password(email=email, password=password)

    # Then
    assert isinstance(sut, User)
    assert sut.id == user.id
    assert sut.email == email
    assert sut.password == password


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    # Given
    email = "b@c.d"
    password = "hide"
    user = make_user(
        password=password,
        email=email,
        nickname="hide",
        is_admin=False,
        lat=37.123,
        lng=127.123,
    )

    # When, Then
    await user_repo.save(user=user)
