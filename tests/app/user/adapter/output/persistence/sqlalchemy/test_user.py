import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.domain.entity.user import User
from app.user.domain.vo.location import Location

user_repo = UserSQLAlchemyRepo()


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    user_1 = User(
        password="password",
        email="a@b.c",
        nickname="hide",
        is_admin=True,
        location=Location(lat=37.123, lng=127.123),
    )
    user_2 = User(
        password="password2",
        email="b@b.c",
        nickname="test",
        is_admin=False,
        location=Location(lat=37.123, lng=127.123),
    )
    session.add_all([user_1, user_2])
    await session.commit()

    # When
    sut = await user_repo.get_users(limit=12, prev=12)

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
