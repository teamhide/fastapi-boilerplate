from datetime import datetime, timedelta
from typing import Union, NoReturn

import jwt

from core.config import get_config
from core.exceptions import DecodeTokenException, ExpiredTokenException


class TokenHelper:
    def __init__(self):
        self.config = get_config()

    def encode(self, payload: dict, expire_period: int = 3600) -> str:
        token = jwt.encode(
            payload={
                **payload,
                'exp': datetime.utcnow() + timedelta(seconds=expire_period),
            },
            key=self.config.JWT_SECRET_KEY,
            algorithm=self.config.JWT_ALGORITHM,
        ).decode('utf8')
        return token

    def decode(self, token: str) -> Union[dict, NoReturn]:
        try:
            return jwt.decode(
                token,
                self.config.JWT_SECRET_KEY,
                self.config.JWT_ALGORITHM,
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    def decode_expired_token(self, token: str) -> Union[dict, NoReturn]:
        try:
            return jwt.decode(
                token,
                self.config.JWT_SECRET_KEY,
                self.config.JWT_ALGORITHM,
                options={'verify_exp': False}
            )
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
