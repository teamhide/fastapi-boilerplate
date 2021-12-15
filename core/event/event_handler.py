from contextvars import ContextVar, Token
from typing import Type, Dict, Union

from pydantic import BaseModel

from core.event.base_event import BaseEvent
from core.event.exceptions import (
    InvalidEventTypeException,
    InvalidParameterTypeException,
)


class EventHandler:
    def __init__(self):
        self.events: Dict[Type[BaseEvent], Union[BaseModel, None]] = {}

    async def store(
        self, event: Type[BaseEvent], parameter: BaseModel = None,
    ) -> None:
        if not issubclass(event, BaseEvent):
            raise InvalidEventTypeException

        if parameter and not isinstance(parameter, BaseModel):
            raise InvalidParameterTypeException

        self.events[event] = parameter

    async def publish(self) -> None:
        event: Type[BaseEvent]
        for event, parameter in self.events.items():
            await event().run(parameter=parameter)

        self.events.clear()


event_context = ContextVar("event_context")


def get_event_handler() -> EventHandler:
    import os

    if "PYTEST_CURRENT_TEST" in os.environ:
        return EventHandler()

    return event_context.get()


def set_event_handler(handler: EventHandler) -> Token:
    return event_context.set(handler)


def reset_event_handler(token: Token) -> None:
    event_context.reset(token)
