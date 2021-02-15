from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from core.db import session

session_context = ContextVar("session_context")


def get_request_id():
    return session_context.get()


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        session.registry.scopefunc = get_request_id

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint,
    ):
        request_id = str(uuid4())
        token = session_context.set(request_id)

        try:
            response = await call_next(request)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.remove()
            session_context.reset(token)

        return response
