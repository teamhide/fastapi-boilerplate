from fastapi import APIRouter

home_router = APIRouter()


@home_router.get("/", dependencies=)
def home():
    return {"status": True}
