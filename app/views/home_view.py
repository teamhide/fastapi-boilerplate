from fastapi import APIRouter

home_router = APIRouter()


@home_router.get('/')
def home():
    return {'status': True}
