import asyncio
from functools import wraps

from .celery_worker import celery_app


def async_task(self, *args, **opts):
    """
    A decorator to transform synchronous task functions into asynchronous Celery tasks.

    This decorator wraps the function within an asynchronous loop, enabling it to be
    scheduled and run by Celery as an asynchronous task.

    Args:
        *args: Variable length argument list for task decorator options.
        **opts: Arbitrary keyword arguments for task decorator options.

    Returns:
        function: A Celery task that wraps the original function.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                future = asyncio.ensure_future(f(*args, **kwargs))
                return future
            else:
                return loop.run_until_complete(f(*args, **kwargs))

        celery_task = celery_app.task(wrapper, *args, **opts)
        return celery_task

    return decorator
