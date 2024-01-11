from abc import ABC, abstractmethod

from app.auth.application.dto import RefreshTokenResponseDTO


class JwtUseCase(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> None:
        """Verify token"""

    @abstractmethod
    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenResponseDTO:
        """Create refresh token"""
