from abc import ABC, abstractmethod
from app.user.domain.entity.user import User


class UserRepo(ABC):
    @abstractmethod
    async def get_users(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        """Get user list"""

    @abstractmethod
    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> User | None:
        """Get user by email or nickname"""

    @abstractmethod
    async def get_user_by_id(self, *, user_id: int) -> User | None:
        """Get user by id"""

    @abstractmethod
    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> User | None:
        """Get user by email and password"""

    @abstractmethod
    async def save(self, *, user: User) -> None:
        """Save user"""
