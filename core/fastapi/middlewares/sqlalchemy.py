from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from core.db import session, set_session_context, reset_session_context

session_context = ContextVar("session_context")


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint,
    ):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            response = await call_next(request)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.remove()
            reset_session_context(context=context)

        return response
