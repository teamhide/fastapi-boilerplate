from typing import Optional, List, Union, NoReturn

from sqlalchemy import or_

from app.models import User
from core.db import session
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
)


class UserUsecase:
    def __init__(self):
        pass


class GetUserListUsecase(UserUsecase):
    async def execute(self, limit: int, prev: Optional[int]) -> List[User]:
        query = session.query(User)

        if prev:
            query = query.filter(User.id < prev)

        if limit > 10:
            limit = 10

        return query.order_by(User.id.desc()).limit(limit).all()


class CreateUserUsecase(UserUsecase):
    async def execute(
        self, email: str, password1: str, password2: str, nickname: str,
    ) -> Union[User, NoReturn]:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        if (
            session.query(User)
            .filter(or_(User.email == email, User.nickname == nickname),)
            .first()
        ):
            raise DuplicateEmailOrNicknameException

        user = User(email=email, password=password1, nickname=nickname)
        session.add(user)
        session.commit()

        return user
