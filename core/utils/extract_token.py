from typing import Union, NoReturn

from core.exception import CustomException
from core.utils import TokenHelper


def extract_payload(authorization: str) -> Union[str, NoReturn]:
    try:
        token = authorization.split('Bearer')[1]
    except IndexError:
        raise CustomException(error='invalid header', code=400)

    return TokenHelper().decode(token=token)


def extract_user_id(authorization: str) -> Union[int, NoReturn]:
    try:
        token = authorization.split()[1]
    except AttributeError:
        raise CustomException(error='authorization header is empty', code=400)
    except IndexError:
        raise CustomException(error='invalid header', code=400)

    payload = TokenHelper().decode(token=token)

    try:
        return payload['user_id']
    except KeyError:
        raise CustomException(error='invalid payload', code=400)
