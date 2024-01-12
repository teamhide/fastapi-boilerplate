from app.auth.application.dto import RefreshTokenResponseDTO
from app.auth.application.exception import DecodeTokenException
from app.auth.domain.usecase.jwt import JwtUseCase
from core.helpers.token import (
    TokenHelper,
    DecodeTokenException as JwtDecodeTokenException,
    ExpiredTokenException as JwtExpiredTokenException,
)


class JwtService(JwtUseCase):
    async def verify_token(self, token: str) -> None:
        try:
            TokenHelper.decode(token=token)
        except (JwtDecodeTokenException, JwtExpiredTokenException):
            raise DecodeTokenException

    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenResponseDTO:
        decoede_created_token = TokenHelper.decode(token=token)
        decoded_refresh_token = TokenHelper.decode(token=refresh_token)
        if decoded_refresh_token.get("sub") != "refresh":
            raise DecodeTokenException

        return RefreshTokenResponseDTO(
            token=TokenHelper.encode(
                payload={"user_id": decoede_created_token.get("user_id")}
            ),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
