from functools import wraps
from typing import Any, Callable, Type

from core.helpers.cache.base import BaseKeyMaker, BaseBackend


class Cacheable:
    default_key_maker: Type[BaseKeyMaker] = None
    default_backend: Type[BaseBackend] = None

    def __init__(
        self,
        prefix: str,
        ttl: int = 60,
        key_maker: Type[BaseKeyMaker] = None,
        backend: Type[BaseBackend] = None,
    ):
        self.prefix = prefix
        self.ttl = ttl
        if not key_maker and not self.default_key_maker:
            from core.helpers.cache.custom_key_maker import CustomKeyMaker

            self.key_maker = CustomKeyMaker()
        elif self.default_key_maker:
            self.key_maker = self.default_key_maker()
        else:
            self.key_maker = key_maker()

        if not backend and not self.default_backend:
            from core.helpers.cache.redis_backend import RedisBackend

            self.backend = RedisBackend()
        elif self.default_backend:
            self.backend = self.default_backend()
        else:
            self.backend = backend()

    def __call__(self, function: Callable):
        @wraps(function)
        async def decorator(*args, **kwargs) -> Any:
            try:
                key = await self.key_maker.make(function=function)
                cached_response = await self.backend.get(key=key)
                if cached_response:
                    return cached_response

                response = await function(*args, **kwargs)
                await self.backend.save(response=response, key=key, ttl=self.ttl)
                return response
            except Exception as e:
                raise e

        return decorator

    @classmethod
    def init_backend(cls, backend: Type[BaseBackend]) -> None:
        cls.default_backend = backend

    @classmethod
    def init_key_maker(cls, key_maker: Type[BaseKeyMaker]) -> None:
        cls.default_key_maker = key_maker
