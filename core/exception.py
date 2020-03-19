class CustomException(Exception):
    def __init__(self, code: int, **kwargs):
        self.code = code
        self.kwargs = kwargs
