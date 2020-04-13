from .user_schema import *


class ExceptionResponseSchema(BaseModel):
    error: str
