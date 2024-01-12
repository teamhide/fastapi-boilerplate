from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    email: str
    password1: str
    password2: str
    nickname: str
    lat: float
    lng: float
