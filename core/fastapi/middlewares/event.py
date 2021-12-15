from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from core.event.event_handler import (
    set_event_handler,
    reset_event_handler,
    EventHandler,
)


class EventMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint,
    ):
        token = set_event_handler(handler=EventHandler())

        try:
            response = await call_next(request)
        except Exception as e:
            raise e from None
        finally:
            reset_event_handler(token=token)

        return response
