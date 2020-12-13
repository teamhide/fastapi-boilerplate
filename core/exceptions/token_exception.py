from core.exceptions import CustomException


class DecodeTokenException(CustomException):
    code = 400
    error_code = 10000
    message = "token decode error"


class ExpiredTokenException(CustomException):
    code = 400
    error_code = 10001
    message = "expired token"
