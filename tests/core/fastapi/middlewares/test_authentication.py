from http.client import HTTPConnection
from unittest.mock import Mock, patch

import pytest
from jwt.exceptions import PyJWTError

from core.fastapi.middlewares import authentication
from core.fastapi.middlewares.authentication import AuthBackend, CurrentUser

auth_backend = AuthBackend()


@pytest.mark.asyncio
@patch.object(authentication, "jwt")
async def test_auth_backend_empty_header(jwt_mock):
    # Given
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {}
    jwt_mock.decode.return_value = {"user_id": 1}

    # When
    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    # Then
    assert authenticated is False
    assert user.id is None


@pytest.mark.asyncio
@patch.object(authentication, "jwt")
async def test_auth_backend_invalid_header(jwt_mock):
    # Given
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "Bearer1234"}
    jwt_mock.decode.return_value = {"user_id": 1}

    # When
    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    # Then
    assert authenticated is False
    assert user.id is None


@pytest.mark.asyncio
@patch.object(authentication, "jwt")
async def test_auth_backend_not_startswith_bearer(jwt_mock):
    # Given
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "hide 1234"}
    jwt_mock.decode.return_value = {"user_id": 1}

    # When
    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    # Then
    assert authenticated is False
    assert user.id is None


@pytest.mark.asyncio
@patch.object(authentication, "jwt")
async def test_auth_backend_empty_credentials(jwt_mock):
    # Given
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "Bearer "}
    jwt_mock.decode.return_value = {"user_id": 1}

    # When
    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    # Then
    assert authenticated is False
    assert user.id is None


@pytest.mark.asyncio
@patch.object(authentication, "jwt")
async def test_auth_backend_invalid_token(jwt_mock):
    # Given
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "Bearer"}
    jwt_mock.decode.side_effect = PyJWTError

    # When
    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    # Then
    assert authenticated is False
    assert user.id is None


@pytest.mark.asyncio
@patch.object(authentication, "jwt")
async def test_auth_backend(jwt_mock):
    # Given
    conn_mock = Mock(spec=HTTPConnection)
    conn_mock.headers = {"Authorization": "bearer credentials"}
    jwt_mock.decode.return_value = {"user_id": 1}

    # When
    authenticated, user = await auth_backend.authenticate(conn=conn_mock)

    # Then
    assert authenticated is True
    assert user == CurrentUser(id=1)
