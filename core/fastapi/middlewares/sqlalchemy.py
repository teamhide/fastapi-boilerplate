from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from core.db.session import set_session_context, reset_session_context, session


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
            raise e
        finally:
            await session.remove()
            reset_session_context(context=context)

        return response
