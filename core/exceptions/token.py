from core.exceptions import CustomException
from core.exceptions.error_code import ErrorCode


class DecodeTokenException(CustomException):
    code = 400
    error_code = ErrorCode.Token.DecodeToken
    message = "token decode error"


class ExpiredTokenException(CustomException):
    code = 400
    error_code = ErrorCode.Token.ExpiredToken
    message = "expired token"
