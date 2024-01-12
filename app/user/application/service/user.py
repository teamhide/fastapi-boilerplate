from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import (
    LoginResponseDTO,
)
from app.user.application.exception import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from app.user.domain.entity.user import UserRead, User
from app.user.domain.usecase.user import UserUseCase
from core.db import Transactional
from core.helpers.token import TokenHelper


class UserService(UserUseCase):
    def __init__(self):
        self.repository = UserRepositoryAdapter()

    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserRead]:
        return await self.repository.get_users(limit=limit, prev=prev)

    @Transactional()
    async def create_user(
        self, *, email: str, password1: str, password2: str, nickname: str
    ) -> None:
        if password1 != password2:
            raise PasswordDoesNotMatchException

        is_exist = await self.repository.get_user_by_email_or_nickname(
            email=email,
            nickname=nickname,
        )
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User.create(email=email, password=password1, nickname=nickname)
        await self.repository.save(user=user)

    async def is_admin(self, *, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email_and_password(
            email=email,
            password=password,
        )
        if not user:
            raise UserNotFoundException

        response = LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response
