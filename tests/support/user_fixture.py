from app.user.domain.entity.user import User
from app.user.domain.vo.location import Location


def make_user(
    id: int | None = None,
    password: str = "password",
    email: str = "h@id.e",
    nickname: str = "hide",
    is_admin: bool = False,
    lat: float = 37.123,
    lng: float = 127.123,
):
    return User(
        id=id,
        password=password,
        email=email,
        nickname=nickname,
        is_admin=is_admin,
        location=Location(lat=lat, lng=lng),
    )
