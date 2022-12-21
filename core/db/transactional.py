from functools import wraps
from typing import TypeVar, ParamSpec, Callable, Awaitable, Coroutine, Any

from core.db import session

T = TypeVar("T")
P = ParamSpec("P")


class Transactional:
    def __call__(
        self,
        func: Callable[P, Awaitable[T]],
    ) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(func)
        async def _transactional(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                result = await func(*args, **kwargs)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

            return result

        return _transactional
