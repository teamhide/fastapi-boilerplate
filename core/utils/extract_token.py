from typing import Union, NoReturn

from jwt.exceptions import DecodeError, ExpiredSignatureError

from core.exception import CustomException
from core.utils.token_helper import TokenHelper


def extract_payload_from_token(token: str) -> Union[dict, NoReturn]:
    try:
        return TokenHelper().decode(token=token)
    except DecodeError:
        raise CustomException(error='decode error', code=400)
    except ExpiredSignatureError:
        raise CustomException(error='expired token', code=400)
