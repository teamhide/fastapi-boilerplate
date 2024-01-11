class CustomException(Exception):
    code = 400
    error_code = "BAD_GATEWAY"
    message = "BAD GATEWAY"

    def __init__(self, message=None):
        if message:
            self.message = message
