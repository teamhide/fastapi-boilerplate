import pytest

from app.auth.application.service.jwt import JwtService, DecodeTokenException

jwt_service = JwtService()


@pytest.mark.asyncio
async def test_verify_token():
    # Given, When, Then
    with pytest.raises(DecodeTokenException):
        await jwt_service.verify_token(token="abc")


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_refresh_token():
    # Given
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhIjoxfQ.VF_eJEtfxZ9PEOqWunr26x0jF2n0o2dyKpmMwisIISY"

    # When, Then
    with pytest.raises(DecodeTokenException):
        await jwt_service.create_refresh_token(token=token, refresh_token=token)


@pytest.mark.asyncio
async def test_create_refresh_token():
    # Given
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyZWZyZXNoIiwidXNlcl9pZCI6MX0.p3PLbILjOq4-i2OmkH2uARu6UQun01dxPArSribeQ8w"

    # When
    sut = await jwt_service.create_refresh_token(token=token, refresh_token=token)

    # Then
    assert sut.token
    assert sut.refresh_token
