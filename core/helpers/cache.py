import inspect
import pickle
from functools import wraps
from typing import Any, Callable

import ujson

from core.helpers.redis import redis


class Cacheable:
    def __init__(self, prefix: str, ttl: int = 60):
        self.prefix = prefix
        self.ttl = ttl

    def __call__(self, function: Callable):
        @wraps(function)
        async def decorator(*args, **kwargs) -> Any:
            try:
                key = await self._make_key(function=function)
                cached_response = await self._from_cache(key=key)
                if cached_response:
                    return cached_response

                response = await function(*args, **kwargs)
                await self._to_cache(response=response, key=key)
                return response
            except Exception as e:
                raise e

        return decorator

    async def _make_key(self, function: Callable) -> str:
        path = f"{inspect.getmodule(function).__name__}.{function.__name__}"
        args = ""

        for arg in inspect.signature(function).parameters.values():
            args += arg.name

        if args:
            return f"{path}.{args}"

        return path

    async def _from_cache(self, key: str) -> Any:
        result = await redis.get(key)
        if not result:
            return

        try:
            return ujson.loads(result.decode("utf8"))
        except UnicodeDecodeError:
            return pickle.loads(result)

    async def _to_cache(self, response: Any, key: str) -> None:
        if isinstance(response, dict):
            response = ujson.dumps(response)
        elif isinstance(response, object):
            response = pickle.dumps(response)

        await redis.set(name=key, value=response, ex=self.ttl)
