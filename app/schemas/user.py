from pydantic import BaseModel


class GetUserListResponseSchema(BaseModel):
    id: int
    email: str
    nickname: str

    class Config:
        orm_mode = True


class CreateUserRequestSchema(BaseModel):
    email: str
    password1: str
    password2: str
    nickname: str


class CreateUserResponseSchema(BaseModel):
    id: int
    email: str
    nickname: str

    class Config:
        orm_mode = True
