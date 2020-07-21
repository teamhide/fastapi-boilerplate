from typing import Union, NoReturn

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import DecodeError, ExpiredSignatureError

from core.config import get_config
from core.exceptions import DecodeTokenException, ExpiredTokenException


def extract_token(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Union[dict, NoReturn]:
    config = get_config()
    try:
        return jwt.decode(
            authorization.credentials,
            config.JWT_SECRET_KEY,
            config.JWT_ALGORITHM,
        )
    except DecodeError:
        raise DecodeTokenException
    except ExpiredSignatureError:
        raise ExpiredTokenException
