from datetime import datetime, timedelta
from typing import Union, NoReturn

import jwt

from core.config import get_config
from core.exception import CustomException


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
            raise CustomException(error='invalid token', code=401)
        except jwt.exceptions.ExpiredSignatureError:
            raise CustomException(error='token expired', code=401)

    def decode_expired_token(self, token: str) -> Union[dict, NoReturn]:
        try:
            return jwt.decode(
                token,
                self.config.JWT_SECRET_KEY,
                self.config.JWT_ALGORITHM,
                options={'verify_exp': False}
            )
        except jwt.exceptions.DecodeError:
            raise CustomException(error='invalid token', code=401)
