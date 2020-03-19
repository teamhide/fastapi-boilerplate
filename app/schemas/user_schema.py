from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    nickname: str


class GetUserListResponseSchema(UserSchema):
    pass


class CreateUserRequestSchema(BaseModel):
    email: str
    password1: str
    password2: str
    nickname: str


class CreateUserResponseSchema(UserSchema):
    pass
