from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.views import home_router
from app.views.v1 import user_router
from core.config import get_config
from core.db import session
from core.exceptions import CustomException


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(home_router)
    app.include_router(user_router, prefix="/api/v1/users", tags=["User"])


def init_listeners(app: FastAPI) -> None:
    # Exception handler
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )

    # Middleware for SQLAlchemy session
    @app.middleware("http")
    async def remove_session(request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            raise e from None
        finally:
            session.remove()

        return response


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        docs_url=None if get_config().ENV == "production" else "/docs",
        redoc_url=None if get_config().ENV == "production" else "/redoc",
    )
    init_routers(app=app)
    init_cors(app=app)
    init_listeners(app=app)
    return app


app = create_app()
