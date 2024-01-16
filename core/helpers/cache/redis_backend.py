import pickle
from typing import Any

import ujson

from core.helpers.cache.base import BaseBackend
from core.helpers.redis import redis_client


class RedisBackend(BaseBackend):
    async def get(self, *, key: str) -> Any:
        result = await redis_client.get(key)
        if not result:
            return

        return ujson.loads(result)

    async def set(self, *, response: Any, key: str, ttl: int = 60) -> None:
        if isinstance(response, dict):
            response = ujson.dumps(response)
        else:
            response = pickle.dumps(response)

        await redis_client.set(name=key, value=response, ex=ttl)

    async def delete_startswith(self, *, value: str) -> None:
        async for key in redis_client.scan_iter(f"{value}*"):
            await redis_client.delete(key)
