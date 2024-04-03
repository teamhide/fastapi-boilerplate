from sqlalchemy import and_, or_, select

from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepo
from core.db.session import session, session_factory


class UserSQLAlchemyRepo(UserRepo):
    async def get_users(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        query = select(User)

        if prev:
            query = query.where(User.id < prev)

        if limit > 12:
            limit = 12

        query = query.limit(limit)
        async with session_factory() as read_session:
            result = await read_session.execute(query)

        return result.scalars().all()

    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> User | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(
                select(User).where(or_(User.email == email, User.nickname == nickname)),
            )
            return stmt.scalars().first()

    async def get_user_by_id(self, *, user_id: int) -> User | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(select(User).where(User.id == user_id))
            return stmt.scalars().first()

    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> User | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(
                select(User).where(and_(User.email == email, password == password))
            )
            return stmt.scalars().first()

    async def save(self, *, user: User) -> None:
        session.add(user)
