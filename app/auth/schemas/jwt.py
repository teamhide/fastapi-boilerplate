from pydantic import BaseModel, Field


class RefreshTokenSchema(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
