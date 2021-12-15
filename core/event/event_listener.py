from core.event.event_handler import get_event_handler


class EventListener:
    def __call__(self, func):
        async def _inner(*args, **kwargs):
            event_handler = get_event_handler()

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                raise e from None

            await event_handler.publish()
            return result

        return _inner
