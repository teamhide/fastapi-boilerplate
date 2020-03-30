from .user_schema import *


class ExceptionResponseSchema(BaseException):
    error: str
