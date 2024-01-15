import pytest

from app.auth.application.service.jwt import JwtService, DecodeTokenException
from tests.support.token import INVALID_REFRESH_TOKEN, USER_ID_1_TOKEN

jwt_service = JwtService()


@pytest.mark.asyncio
async def test_verify_token():
    # Given, When, Then
    with pytest.raises(DecodeTokenException):
        await jwt_service.verify_token(token="abc")


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_refresh_token():
    # Given
    token = INVALID_REFRESH_TOKEN

    # When, Then
    with pytest.raises(DecodeTokenException):
        await jwt_service.create_refresh_token(token=token, refresh_token=token)


@pytest.mark.asyncio
async def test_create_refresh_token():
    # Given
    token = USER_ID_1_TOKEN

    # When
    sut = await jwt_service.create_refresh_token(token=token, refresh_token=token)

    # Then
    assert sut.token
    assert sut.refresh_token
