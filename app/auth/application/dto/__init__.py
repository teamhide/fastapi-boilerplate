from pydantic import BaseModel, Field


class RefreshTokenResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
