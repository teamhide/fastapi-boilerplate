class ErrorCode:
    class Token:
        DecodeToken = 10000
        ExpiredToken = 10001

    class User:
        PasswordDoesNotMatch = 20000
        DuplicateEmailOrNickname = 20001
